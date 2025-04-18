import streamlit as st
import streamlit.components.v1 as components
import base64
import leafmap.maplibregl as leafmap
import altair as alt
import ibis
from ibis import _
import ibis.selectors as s
import os
import pandas as pd 
import geopandas as gpd
from shapely import wkb  
import sqlalchemy
import pathlib
from typing import Optional
from functools import reduce

from variables import *
from utils import *

## Create the table from remote parquet only if it doesn't already exist on disk
con = ibis.duckdb.connect("duck.db", extensions=["spatial"])
current_tables = con.list_tables()

if "mydata" not in set(current_tables):
    tbl = con.read_parquet(ca_parquet)
    con.create_table("mydata", tbl)

ca = con.table("mydata")

st.set_page_config(layout="wide", page_title="CA Protected Areas Explorer", page_icon=":globe:")
# session state for syncing app 
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = False

for col,val in style_options.items():
    for name in val['stops']:
        key = val['property']+str(name[0])
        if key not in st.session_state:
            st.session_state[key] = True
            
#customizing style with CSS 
st.markdown(app_formatting,unsafe_allow_html=True)

st.markdown("<h2>CA 30x30 Planning & Assessment Prototype</h2>", unsafe_allow_html=True)

st.markdown('<p class="medium-font"> In October 2020, Governor Newsom issued <a href="https://www.gov.ca.gov/wp-content/uploads/2020/10/10.07.2020-EO-N-82-20-.pdf" target="_blank">Executive Order N-82-20</a>, which establishes a state goal of conserving 30% of California’s lands and coastal waters by 2030 – known as <a href="https://www.californianature.ca.gov/" target="_blank">CA 30x30</a>. </p>',
unsafe_allow_html=True)

st.markdown('<p class = "medium-font"> This is an interactive cloud-native geospatial tool for exploring and visualizing California\'s protected lands. </p>', unsafe_allow_html = True)

st.divider()

m = leafmap.Map(style="positron")
#############

chatbot_container = st.container()
with chatbot_container:
    llm_left_col, llm_right_col = st.columns([5,1], vertical_alignment = "bottom")
    with llm_left_col:
        with st.popover("💬 Example Queries"):
            '''
            Mapping queries:        
            - Show me all 30x30 conserved lands managed by The Nature Conservancy.
            - Show me amphibian biodiversity hotspots that aren't currently conserved.
            - Show me protected areas with at least 80% overlap with regions of high endemic species richness.
            '''
            
            '''
            Exploratory data queries:
            - What is a GAP code?
            - What percentage of 30x30 conserved land has been impacted by wildfire?
            - What is the total acreage of areas designated as easements?
            - Which county has the most 30x30 conserved land?
            '''
            
            st.info('If the map appears blank, queried data may be too small to see at the default zoom level. Check the table below the map, as query results will also be displayed there.', icon="ℹ️")
    
    with llm_right_col:
        llm_choice = st.selectbox("Select LLM:", llm_options, key = "llm", help = "Select which model to use.")   
        llm = llm_options[llm_choice]
           
##### Chatbot stuff 
from pydantic import BaseModel, Field
class SQLResponse(BaseModel):
    """Defines the structure for SQL response."""
    sql_query: str = Field(description="The SQL query generated by the assistant.")
    explanation: str = Field(description="A detailed explanation of how the SQL query answers the input question.")

with open('app/system_prompt.txt', 'r') as file:
    template = file.read()

from langchain_openai import ChatOpenAI
managers = ca.sql("SELECT DISTINCT manager FROM mydata;").execute()
names = ca.sql("SELECT name FROM mydata GROUP BY name HAVING SUM(acres) >10000;").execute()
ecoregions = ca.sql("SELECT DISTINCT ecoregion FROM mydata;").execute()

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
]).partial(dialect="duckdb", table_info = ca.schema(), managers = managers, names = names, ecoregions = ecoregions)

chatbot_toggles = {key: False for key in keys}
structured_llm = llm.with_structured_output(SQLResponse)
few_shot_structured_llm = prompt | structured_llm

def run_sql(query,color_choice):
    """
    Filter data based on an LLM-generated SQL query and return matching IDs.

    Args:
        query (str): The natural language query to filter the data.
        color_choice (str): The column used for plotting.
    """
    output = few_shot_structured_llm.invoke(query)
    sql_query = output.sql_query
    explanation =output.explanation
    if not sql_query: # if the chatbot can't generate a SQL query.
        st.success(explanation)
        return pd.DataFrame({'id' : []})
        
    result = ca.sql(sql_query).execute()
    if result.empty :
        explanation = "This query did not return any results. Please try again with a different query."
        st.warning(explanation, icon="⚠️")
        st.caption("SQL Query:")
        st.code(sql_query,language = "sql") 
        if 'geom' in result.columns:
            return result.drop('geom',axis = 1)
        else: 
            return result
    
    elif ("id" and "geom" in result.columns): 
        style = get_pmtiles_style_llm(style_options[color_choice], result["id"].tolist())
        legend, position, bg_color, fontsize = get_legend(style_options,color_choice)

        m.add_legend(legend_dict = legend, position = position, bg_color = bg_color, fontsize = fontsize)
        m.add_pmtiles(ca_pmtiles, style=style, opacity=alpha, tooltip=True, fit_bounds=True)
        m.fit_bounds(result.total_bounds.tolist())    
        result = result.drop('geom',axis = 1) #printing to streamlit so I need to drop geom
    else:   
        st.write(result)  # if we aren't mapping, just print out the data  

    with st.popover("Explanation"):
        st.write(explanation)
        st.caption("SQL Query:")
        st.code(sql_query,language = "sql") 
        
    return result

#############

filters = {}

with st.sidebar:
    with st.popover("ℹ️ Help"):
        '''
        - ❌ Safari/iOS not yet supported.  
        - 📊 Use this sidebar to color-code the map by different attributes **(Group by)**, toggle on data layers and view summary charts **(Data Layers)**, or filter data **(Filters)**.
        - 💬 For a more tailored experience, query our dataset of protected areas and their precomputed mean values for each of the displayed layers, using the experimental chatbot. The language model tries to answer natural language questions by drawing only from curated datasets (listed below).
        '''
    st.divider()
    color_choice = st.radio("Group by:", style_options, key = "color", help = "Select a category to change map colors and chart groupings.")   
    colorby_vals = get_color_vals(style_options, color_choice) #get options for selected color_by column 
    alpha = 0.8
    st.divider()

##### Chatbot 
with chatbot_container:
    with llm_left_col:
        example_query = "👋 Input query here"
        prompt = st.chat_input(example_query, key="chain", max_chars=300)

# new container for output so it doesn't mess with the alignment of llm options 
with st.container():
    if prompt: 
        st.chat_message("user").write(prompt)
        try:
            with st.chat_message("assistant"):
                with st.spinner("Invoking query..."):

                    out = run_sql(prompt,color_choice)
                    if ("id" in out.columns) and (not out.empty):
                        ids = out['id'].tolist()
                        cols = out.columns.tolist()
                        chatbot_toggles = {
                                key: (True if key in cols else value) 
                                for key, value in chatbot_toggles.items()
                            }
                        for key, value in chatbot_toggles.items():
                            st.session_state[key] = value  # Update session state
                    else:
                        ids = []
        except Exception as e:
            error_message = f"ERROR: An unexpected error has occured with the following query:\n\n*{prompt}*\n\n which raised the following error:\n\n{type(e)}: {e}\n"
            st.warning("Please try again with a different query", icon="⚠️")
            st.write(error_message)
            st.stop()

#### Data layers 
with st.sidebar:  
    st.markdown('<p class = "medium-font-sidebar"> Data Layers:</p>', help = "Select data layers to visualize on the map. Summary charts will update based on the displayed layers.", unsafe_allow_html= True)
    
    #display toggles to turn on data layers            
    for section, slider_key, items in layer_config:
        with st.expander(section):
            st.slider("transparency", 0.0, 1.0, 0.1 if slider_key != "calfire" else 0.15, key=slider_key)
            for item in items:
                if len(item) == 4:
                    _, label, toggle_key, default = item
                    st.toggle(label, key=toggle_key, value=default)
                else:
                    _, label, toggle_key = item
                    st.toggle(label, key=toggle_key)
    st.divider()
    
#### Filters
    st.markdown('<p class = "medium-font-sidebar"> Filters:</p>', help = "Apply filters to adjust what data is shown on the map.", unsafe_allow_html= True)

    for label in style_options: # get selected filters (based on the buttons selected)
        with st.expander(label):  
            if label in ["GAP Code","30x30 Status"]: # gap code 1 and 2 are on by default
                opts = get_buttons(style_options, label)
            else: # other buttons are not on by default.
                opts = get_buttons(style_options, label) 
            filters.update(opts)
            
        selected = {k: v for k, v in filters.items() if v}
        if selected: 
            filter_cols = list(selected.keys())
            filter_vals = list(selected.values())
        else: 
            filter_cols = []
            filter_vals = []

    st.divider()
    
    # adding github logo 
    st.markdown(f"<div class='spacer'>{github_html}</div>", unsafe_allow_html=True)
    st.markdown(":left_speech_bubble: [Get in touch or report an issue](https://github.com/boettiger-lab/CBN-taskforce/issues)")


# Display CA 30x30 Data
if 'out' not in locals():
    style = get_pmtiles_style(style_options[color_choice], alpha, filter_cols, filter_vals)
    legend, position, bg_color, fontsize = get_legend(style_options, color_choice)
    m.add_legend(legend_dict = legend, position = position, bg_color = bg_color, fontsize = fontsize)
    m.add_pmtiles(ca_pmtiles, style=style, name="CA", tooltip=True, fit_bounds=True)
    
column = select_column[color_choice]
colors = color_table(select_colors, color_choice, column)

# get summary tables used for charts + printed table 
# df - charts; df_tab - printed table (omits colors) 
if 'out' not in locals():
    df, df_tab, df_percent, df_bar_30x30 = get_summary_table(ca, column, select_colors, color_choice, filter_cols, filter_vals,colorby_vals)
    total_percent = (100*df_percent.percent_CA.sum()).round(2)
else:
    df = get_summary_table_sql(ca, column, colors, ids)
    total_percent = (100*df.percent_CA.sum()).round(2)

# check if any layer toggle is active
any_chart_toggled = any(
    st.session_state.get(toggle_key, False)
    for _, _, items in layer_config
    for _, _, toggle_key, *_ in items
)

# check if using stacked bar chart 
show_stacked = (column not in ["status", "gap_code"]) and ('df_bar_30x30' in locals())

if 'out' in locals():
    show_chatbot_chart = out.columns.any() in keys
else:
    show_chatbot_chart = False
# main display 
main = st.container()
with main:
    map_col, stats_col = st.columns([2,1])

    with map_col:
        m.to_streamlit(height=650) # adding map
        with st.expander("🔍 View/download data"): # adding data table  
            if 'out' not in locals():
                st.dataframe(df_tab, use_container_width = True)  
            else:
                st.dataframe(out, use_container_width = True)

    with stats_col:
        with st.container():
            # donut chart 
            st.markdown(f"{total_percent}% CA Protected", help = "Total percentage of 30x30 conserved lands, updates based on displayed data")
            st.altair_chart(area_chart(df, column), use_container_width=True)
            
            # display the pill selection if we will use any barcharts

            if any_chart_toggled or show_stacked or show_chatbot_chart:
                option_map = {
                    'percent': "%",
                    'acres': "Acres",
                }
                chart_choice = st.pills(
                    label="Bar chart metrics",
                    options=option_map.keys(),
                    format_func=lambda option: option_map[option],
                    selection_mode="single",
                    label_visibility="collapsed",
                    default="percent",
                )
            if chart_choice:    
                if show_stacked:
                    y = 'percent_group' if chart_choice == 'percent' else 'acres'
                    if color_choice == 'Resilient & Connected Network': # line break, this title is long 
                         color_choice = 'Resilient &\n Connected Network'
                    chart = stacked_bar(df = df_bar_30x30, x = column, y = y, metric = chart_choice, title = color_choice + '\nby 30x30 Status', colors = colors)
                    st.altair_chart(chart, use_container_width=True)  

                # data layer summary charts   
                for _, _, items in layer_config:
                    for suffix, label, toggle_key, *_ in items:
                        if st.session_state.get(toggle_key, False):
                            y_col = f"{chart_choice}_{suffix}"
                            st.altair_chart(bar_chart(df, column, y_col, label, metric=chart_choice), use_container_width=True)
            else:
                st.warning("Please select a metric to display bar chart.")

st.caption("***The label 'established' is inferred from the California Protected Areas Database, which may introduce artifacts. For details on our methodology, please refer to our <a href='https://github.com/boettiger-lab/CBN-taskforce' target='_blank'>our source code</a>.", unsafe_allow_html=True)

st.caption("***Under California’s 30x30 framework, only GAP codes 1 and 2 are counted toward the conservation goal.") 

st.divider()

with open('app/footer.md', 'r') as file:
    footer = file.read()
st.markdown(footer)


