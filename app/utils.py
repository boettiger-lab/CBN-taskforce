import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import leafmap.foliumap as leafmap
import altair as alt
import ibis
from ibis import _
import ibis.selectors as s
import os
from shapely import wkb  
from functools import reduce
from itertools import chain
from variables import *
from pandas.api.types import CategoricalDtype
from math import pi

######################## UI FUNCTIONS 
def get_buttons(style_options, style_choice):
    """
    Creates Streamlit checkboxes based on style options and returns the selected filters.
    """
    column = style_options[style_choice]['property']
    opts = [style[0] for style in style_options[style_choice]['stops']]

    buttons = {}
    for name in opts:
        key = column + str(name)
        buttons[name] = st.checkbox(f"{name}", key=key, on_change = sync_checkboxes, args = (key,))

    filter_choice = [key for key, value in buttons.items() if value]
    
    return {column: filter_choice}

def sync_checkboxes(source):
    """
    Synchronizes checkbox selections in Streamlit based on 30x30 status and GAP codes. 
    """
    # gap 1 and gap 2 on -> 30x30 Conservation Area on
    if source in ["gap_codeGAP 1", "gap_codeGAP 2"]:
        st.session_state['status30x30 Conservation Area'] = st.session_state["gap_codeGAP 1"] and st.session_state['gap_codeGAP 2']

    # 30x30-conserved on -> gap 1 and gap 2 on
    elif source == "status30x30 Conservation Area":
        st.session_state['gap_codeGAP 1'] = st.session_state['status30x30 Conservation Area']
        st.session_state['gap_codeGAP 2'] = st.session_state['status30x30 Conservation Area']

    # other-conserved on <-> gap 3 on
    elif source == "gap_codeGAP 3":
        st.session_state["statusOther Conservation Area"] = st.session_state['gap_codeGAP 3']
    elif source == "statusOther Conservation Area":
        if "gap_codeGAP 3" in st.session_state and st.session_state["statusOther Conservation Area"] != st.session_state['gap_codeGAP 3']:
            st.session_state['gap_codeGAP 3'] = st.session_state["statusOther Conservation Area"]

    # unknown on <-> gap 4 on
    elif source == "gap_codeGAP 4":
        st.session_state['statusPublic or Unknown Conservation Area'] = st.session_state['gap_codeGAP 4']

    elif source == "statusPublic or Unknown Conservation Area":
        if "gap_codeGAP 4" in st.session_state and st.session_state['statusPublic or Unknown Conservation Area'] != st.session_state['gap_codeGAP 4']:
            st.session_state['gap_codeGAP 4'] = st.session_state['statusPublic or Unknown Conservation Area']

    # non-conserved on <-> gap 0 
    elif source == "gapNon-Conservation Area":
        st.session_state['statusNon-Conservation Area'] = st.session_state['gapNon-Conservation Area']

    elif source == "statusNon-Conservation Area":
        if "gapNon-Conservation Area" in st.session_state and st.session_state['statusNon-Conservation Area'] != st.session_state['gapNon-Conservation Area']:
            st.session_state['gapNon-Conservation Area'] = st.session_state['statusNon-Conservation Area']


def color_table(select_colors, color_choice, column):
    """
    Converts selected color mapping into a DataFrame.
    """
    # return ibis.memtable(select_colors[color_choice], columns=[column, "color"]).to_pandas()
    return ibis.memtable(select_colors[color_choice], columns=[column, "color"])

def get_color_vals(style_options, style_choice):
    """
    Extracts available color values for a selected style option.
    """
    column = style_options[style_choice]['property']
    return {column: [style[0] for style in style_options[style_choice]['stops']]}


######################## SUMMARY & DATA FUNCTIONS 
def get_summary(ca, combined_filter, column, main_group, feature_col, colors = None, feature = False):
    """
    Computes summary statistics for the filtered dataset.
    """    
    # precompute total_feature values across full table
    total_features = {
        key: (getattr(_, key) * _.acres).sum().name(f"total_feature_{key}")
        for key in keys
    }
    
    totals = ca.aggregate(**total_features).execute().iloc[0].to_dict()

    # base columns
    base_aggs = {
        "percent_CA": (_.acres.sum() / ca_area_acres),
        "acres": _.acres.sum(),
        }

    # add percent + acres aggregates
    dynamic_aggs = {}
    for key in keys:
        suffix = key.replace("pct_", "").replace("-", "_")
        dynamic_aggs.update({
            f"pct_network_{suffix}": (getattr(_, key) * _.acres).sum() / _.acres.sum(),
            f"acres_{suffix}": (getattr(_, key) * _.acres).sum(),
            f"pct_feature_{suffix}": (getattr(_, key) * _.acres).sum() / totals[key],
        })

    # join all aggregates
    all_aggs = {**base_aggs, **dynamic_aggs}
    # group and aggregate
    df = (ca.filter(combined_filter)
          .group_by(*column)
          .aggregate(**all_aggs)
          .mutate(percent_CA=_.percent_CA.round(5), acres=_.acres.round(0))
        )

     # Compute total acres by group and percent of group
    group_totals = (ca.filter(combined_filter)
                  .group_by(main_group)
                  .aggregate(total_acres=_.acres.sum())
                )
    
    df = (df.inner_join(group_totals, main_group)
          .mutate(percent_group=( _.acres / _.total_acres))
         )

    # if colors is not None and not colors.empty:
    if colors is not None:
        df = df.inner_join(colors, column[-1])
    return df.cast({col: "string" for col in column}).execute()

def get_summary_table(ca, column, select_colors, color_choice, filter_cols, filter_vals, colorby_vals, feature_col = None):
    """
    Generates summary tables for visualization and reporting.
    """
    colors = color_table(select_colors, color_choice, column)

    #if a filter is selected, add to list of filters 
    filters = [getattr(_, col).isin(vals) for col, vals in zip(filter_cols, filter_vals) if vals]
    #show color_by column in table by adding it as a filter (if it's not already a filter)
    if column not in filter_cols:
        filter_cols.append(column)
        filters.append(getattr(_, column).isin(colorby_vals[column]))

    #combining all the filters into ibis filter expression 
    combined_filter = reduce(lambda x, y: x & y, filters)

    #df used for printed table
    df_tab = get_summary(ca, combined_filter, filter_cols, column, feature_col, colors=None)

    df_feature = None if feature_col is None else get_summary(ca, combined_filter, [column], column, feature_col, colors, feature = True)
    df_network = None if df_feature is not None else get_summary(ca, combined_filter, [column], column, feature_col, colors)        
    # df for stacked 30x30 status bar chart 
    df_bar_30x30 = None if column in ["status", "gap_code"] else get_summary(ca, combined_filter | (_.status.isin(['Non-Conservation Area'])), [column, 'status'], column, feature_col, color_table(select_colors, "30x30 Status", 'status'))
    return df_network, df_feature, df_tab, df_bar_30x30 


def get_summary_table_sql(ca, column, colors, ids, feature_col = None):
    """
    Generates a summary table using specific IDs as filters.
    """
    combined_filter = _.id.isin(ids)
    df_network = get_summary(ca, combined_filter, [column], column, feature_col, colors)
    df_feature = get_summary(ca, combined_filter, [column], column, feature_col, colors, feature = True)
    return df_network, df_feature

def extract_columns(sql_query):
    # Find all substrings inside double quotes
    columns = list(dict.fromkeys(re.findall(r'"(.*?)"', sql_query)))
    return columns


######################## MAP STYLING FUNCTIONS 

def get_county_bounds(county):
    return county_bounds[county]
    
from itertools import chain

def get_pmtiles_style(paint, alpha=1, filter_cols=None, filter_vals=None, ids=None):
    """
    Generates a MapLibre GL style for PMTiles with either filters or a list of IDs.

    """
    if ids:
        filter_expr = ["in", ["get", "id"], ["literal", ids]]
    else:
        # we don't want to overwhelm streamlit so if they didn't filter anything, don't provide filter arg 
        filter_length = sum([len(x) for x in filter_vals])
        if filter_length == 75: # this means all the filters are checked
            filter_expr = None
        else: 
            filters = [
                ["match", ["get", col], val, True, False]
                for col, val in zip(filter_cols, filter_vals)
            ]
            filter_expr = ["all", *filters]
            
            
    config = {
        "id": "ca30x30",
        "source": "ca",
        "source-layer": source_layer_name,
        "type": "fill",
        "paint": {
            "fill-color": paint,
            "fill-opacity": alpha
        }
    }
    
    if filter_expr:
        config["filter"] = filter_expr
    
    return {
        "version": 8,
        "sources": {
            "ca": {
                "type": "vector",
                "url": f"pmtiles://{ca_pmtiles}"
            }
        },
        "layers": [config]
    }



def get_legend(style_options, color_choice, leafmap_backend, df = None, column = None):
    """
    Generates a legend dictionary with color mapping and formatting adjustments.
    """
    legend = {cat: color for cat, color in style_options[color_choice]['stops']}
    if df is not None:
        if ~df.empty:
            categories = df[column].to_list() #if we filter out categories, don't show them on the legend 
            legend = {cat: color for cat, color in legend.items() if str(cat) in categories}
    position, fontsize, bg_color = 'bottomleft', 15, 'white'

    if leafmap_backend == 'MapLibre':
        position = 'bottom-left'


    # shorten legend for ecoregions 
    if color_choice == "Ecoregion":
        legend = {key.replace("Northern California", "NorCal"): value for key, value in legend.items()} 
        legend = {key.replace("Southern California", "SoCal"): value for key, value in legend.items()} 
        legend = {key.replace("Southeastern", "SE."): value for key, value in legend.items()} 
        legend = {key.replace("and", "&"): value for key, value in legend.items()} 
        legend = {key.replace("California", "CA"): value for key, value in legend.items()} 
        legend = {key.replace("Northwestern", "NW."): value for key, value in legend.items()} 
        bg_color = 'rgba(255, 255, 255, 0.6)'
        fontsize = 12
    return legend, position, bg_color, fontsize


### tooltip for pmtiles
from leafmap.foliumap import PMTilesMapLibreTooltip
from branca.element import Template

class CustomTooltip(PMTilesMapLibreTooltip):
    _template = Template("""
    {% macro script(this, kwargs) -%}
    var maplibre = {{ this._parent.get_name() }}.getMaplibreMap();
    const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false });

    maplibre.on('mousemove', function(e) {
        const features = maplibre.queryRenderedFeatures(e.point);
        const filtered = features.filter(f => f.properties && f.properties.id);

        if (filtered.length) {
            const props = filtered[0].properties;
            const html = `
              <div><strong>ID:</strong> ${props.id || 'N/A'}</div>
              <div><strong>Name:</strong> ${props.name || 'N/A'}</div>
              <div><strong>Manager:</strong> ${props.manager || 'N/A'}</div>
              <div><strong>County:</strong> ${props.county || 'N/A'}</div>
              <div><strong>Status:</strong> ${props.status || 'N/A'}</div>
              <div><strong>GAP Code:</strong> ${props.gap_code || 'N/A'}</div>
              <div><strong>Habitat Type:</strong> ${props.habitat_type || 'N/A'}</div>
              <div><strong>Climate Zone:</strong> ${props.climate_zone || 'N/A'}</div>
              <div><strong>Land Tenure:</strong> ${props.land_tenure || 'N/A'}</div>
              <div><strong>Ecoregion:</strong> ${props.ecoregion || 'N/A'}</div>
              <div><strong>Acres:</strong> ${
  props.acres ? (parseFloat(props.acres).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })) : 'N/A'
}</div>
            `;
            popup.setLngLat(e.lngLat).setHTML(html).addTo(maplibre);
            if (popup._container) {
                popup._container.style.zIndex = 9999;
            }
        } else {
            popup.remove();
        }
    });
    {% endmacro %}
    """)


######################## CHART FUNCTIONS 
def area_chart(df, column, color_choice):
    """
    Generates an Altair pie chart representing the percentage of protected areas.
    """
    sort, _, _, _,_,_,_= get_chart_settings(column,color_choice)
    df = df.copy()
    df[column] = df[column].apply(lambda x: get_label_transform(column, x))
    
    unique_labels = sorted(df[column].unique())
    if sort == 'x':
        labels_sorted = unique_labels
    elif sort == '-x':
        labels_sorted = unique_labels[::-1]
    else:
        labels_sorted = sort 

    cat_dtype = CategoricalDtype(categories=labels_sorted, ordered=True)
    df["order_index"] = df[column].astype(cat_dtype).cat.codes  
    
    pie = (
        alt.Chart(df)
        .mark_arc(innerRadius=50, outerRadius=120, stroke="black", strokeWidth=0.1)
        .encode(
            alt.Theta("percent_CA:Q", scale=alt.Scale(type="linear", rangeMax=pi/2, rangeMin=-pi/2)),
            alt.Order("order_index:O"),
            alt.Color(
                f'{column}:N',
                scale=alt.Scale(domain=df[column].tolist(), range=df["color"].tolist()),
                legend=None),
            tooltip=[
                alt.Tooltip(column, type="nominal"),
                alt.Tooltip("percent_CA", type="quantitative", format=",.1%"),
                alt.Tooltip("acres", type="quantitative", format=",.0f"),
            ]
        )
        .properties(title=[f"Percent of California", f"by {color_choice}"], height=300)
        .configure_title(fontSize=16, align="center", anchor="middle", offset=15)
    )
    return pie



def bar_chart(df, x, y, title, metric = "percent", percent_type = None):
    """Creates a simple bar chart."""
    return create_bar_chart(df, x, y, title, metric, percent_type)

def stacked_bar(df, x, y, metric, title, colors, color = "status"):
    """Creates a stacked bar chart."""
    return create_bar_chart(df, x, y, title, metric, color=color, stacked=True, colors=colors)

def get_chart_settings(x, feature_name, y=None, stacked=None, metric=None, percent_type=None):
    """
    Returns sorting, axis settings, and y-axis title mappings for chart rendering.
    """
    y_title = {
        'percent': "Percent",
        'acres': "Acres"
    }.get(metric)

    x_title = next(k for k, v in select_column.items() if v == x)
    angle = 270 if x in {
        "manager_type", "ecoregion", "status", "habitat_type",
         "access_type", "climate_zone", "land_tenure"
    } else 0

    chart_title, subtitle = '', ''
    y = y or ''



    if percent_type == "Network":
        chart_title = f"{feature_name} Within Each {x_title}"
        y_title = f"% of Area with {feature_name}"
        subtitle = f"Acres of {feature_name} in each {x_title},\ndivided by total acres of each {x_title}"

    elif percent_type == "Feature":
        chart_title = f"Distribution of\n{feature_name} by {x_title}"
        y_title = f"% of Total {feature_name}"
        subtitle = f"Acres of {feature_name} in each {x_title},\ndivided by total acres of {feature_name}"

    if stacked:
        chart_title = f"{x_title}\nby 30x30 Status"
    
    elif metric == "acres" and not stacked:
        chart_title = f"Acres of {feature_name.rstrip()}\nWithin Each {x_title}"

    
    height = (
        350 if stacked else
        620 if "freshwater" in y else
        720 if "increased" in y and percent_type == "Feature" else
        700 if "increased" in y else
        550 if x in ["ecoregion", "habitat_type"] else
        450 if x == "manager_type" else
        550 if x == "access_type" else
        600 if percent_type else
        540
    )

    return sort_options.get(x, "x"), angle, height, y_title, x_title, chart_title, subtitle


def get_label_transform(x, label=None):
    transform = label_transforms.get(x, (f"datum.{x}", None))
    func = transform[1]
    if label is not None:
        return func(label) if callable(func) else label
    return transform[0]
    
def get_hex(df, color, order):
    """
    Returns a list of hex color codes and categories sorted based on `sort_order`.
    """
    return (df.drop_duplicates(subset=color, keep="first")
                .set_index(color)
                .reindex(order)
                .dropna()
                .reset_index()).T.values.tolist()

@st.fragment
def create_bar_chart(
    df, x, y, feature_name, metric,
    percent_type=None, color=None, stacked=False, colors=None
):
    """
    Generalized function to create a bar chart, supporting both standard and stacked bars.
    """
    # get settings and formatting 
    sort, angle, height, y_title, x_title, chart_title, subtitle = get_chart_settings(
        x, feature_name, y, stacked, metric, percent_type
    )
    label_transform = get_label_transform(x)
    y_format = "~s" if metric == "acres" else ",.2%"
    tooltip_y = alt.Tooltip(y, type="quantitative", format=y_format)

    # base chart
    base_chart = (
        alt.Chart(df)
        .mark_bar(stroke="black", strokeWidth=0.1)
        .transform_calculate(xlabel=label_transform)
        .encode(
            x=alt.X("xlabel:N", sort=sort, axis=alt.Axis(labelAngle=angle, title=x_title, labelLimit=200)),
            y=alt.Y(y, axis=alt.Axis(title=y_title, offset=-5, format=y_format)),
            tooltip=[alt.Tooltip(x, type="nominal"), tooltip_y]
        )
        .properties(height=height)
    )

    # stacked chart
    if stacked:
        order = [
            "30x30 Conservation Area",
            "Other Conservation Area",
            "Public or Unknown Conservation Area",
            "Non-Conservation Area"
        ]
        sort_order, color_hex = get_hex(df[[color, "color"]], color, order)

        df["stack_order"] = df[color].apply(lambda val: sort_order.index(val) if val in sort_order else len(sort_order))
        y_axis_scale = alt.Y(
            y,
            axis=alt.Axis(title=y_title, offset=-5, format=y_format),
            scale=alt.Scale(domain=[0, 1]) if metric == "percent" else alt.Undefined
        )

        stacked_chart = base_chart.encode(
            x=alt.X("xlabel:N", sort=sort, title=None, axis=alt.Axis(labels=False)),
            y=y_axis_scale,
            color=alt.Color(color, sort=sort_order, scale=alt.Scale(domain=sort_order, range=color_hex)),
            order=alt.Order("stack_order:Q", sort="ascending"),
            tooltip=[
                alt.Tooltip(x, type="nominal"),
                alt.Tooltip(color, type="nominal"),
                alt.Tooltip("percent_group", type="quantitative", format=",.2%"),
                alt.Tooltip("acres", type="quantitative", format=",.0f"),
            ]
        )

        # prepare label layer
        colors = colors.to_pandas()
        colors["xlabel"] = [get_label_transform(x, str(lab)) for lab in colors[x]]
        symbol_layer = (
            alt.Chart(colors)
            .mark_point(filled=True, shape="circle", size=100, tooltip=False, yOffset=5)
            .encode(
                x=alt.X("xlabel:N", sort=sort, axis=alt.Axis(labelAngle=angle, title=None, labelLimit=200)),
                color=alt.Color("color:N", scale=None)
            )
            .properties(height=1)
        )

        final_chart = alt.vconcat(stacked_chart, symbol_layer, spacing=8).resolve_scale(x="shared")

    # non-stacked chart
    else:
        final_chart = base_chart.encode(
            color=alt.Color("color").scale(None)
        )

    # final formatting 
    final_chart = final_chart.properties(
        title={
            "text": chart_title.split("\n") if "\n" in chart_title else chart_title,
            "subtitle": subtitle.split("\n") if "\n" in subtitle else subtitle,
        }
    ).configure_legend(
        symbolStrokeWidth=0.1,
        direction="horizontal",
        orient="top",
        columns=2,
        title=None,
        labelOffset=2,
        offset=5,
        symbolType="square",
        labelFontSize=13,
    ).configure_title(
        fontSize=16,
        align="center",
        anchor="middle",
        offset=10,
        subtitleColor="gray"
    )
    return final_chart


import minio
import datetime
minio_key = os.getenv("MINIO_KEY")
if minio_key is None:
    minio_key = st.secrets["MINIO_KEY"]

minio_secret = os.getenv("MINIO_SECRET")
if minio_secret is None:
    minio_secret = st.secrets["MINIO_SECRET"]


def minio_logger(consent, query, sql_query, llm_explanation, llm_choice, filename="query_log.csv", bucket="shared-ca30x30-app",
                 key=minio_key, secret=minio_secret,
                 endpoint="minio.carlboettiger.info"):
    mc = minio.Minio(endpoint, key, secret)
    mc.fget_object(bucket, filename, filename)
    log = pd.read_csv(filename)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    if consent:
        df = pd.DataFrame({"timestamp": [timestamp], "user_query": [query], "llm_sql": [sql_query], "llm_explanation": [llm_explanation], "llm_choice":[llm_choice]})

    # if user opted out, do not store query
    else:  
        df = pd.DataFrame({"timestamp": [timestamp], "user_query": ['USER OPTED OUT'], "llm_sql": [''], "llm_explanation": [''], "llm_choice":['']})
    
    pd.concat([log,df]).to_csv(filename, index=False, header=True)
    mc.fput_object(bucket, filename, filename, content_type="text/csv")
