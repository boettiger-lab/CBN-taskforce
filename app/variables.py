# urls for main layer 
ca_parquet = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30_cbn_v3.parquet'
ca_pmtiles = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30_cbn_v3.pmtiles'
low_res_pmtiles = 'https://minio.carlboettiger.info/public-ca30x30/pmtiles_v3_options/ca30x30_cbn_v3_zg.pmtiles'

# computed by taking the sum of all the acres in this file:
# https://minio.carlboettiger.info/public-ca30x30/CBN-data/Progress_data_new_protection/Land_Status_Zone_Ecoregion_Counties/all_regions_reGAP_county_eco.parquet
ca_area_acres = 101523750.68856516 
chart_choice = "percent" # 

# this should go in utils, but I need it to build urls
# so keeping it here to avoid circular import 
import os
def get_url(folder, file, base_folder = 'CBN'):
    """
    Get url for minio hosted data
    """
    minio = 'https://minio.carlboettiger.info/'
    bucket = 'public-ca30x30'
    if base_folder is None:
        path = os.path.join(bucket,folder,file)
    else:
        path = os.path.join(bucket,base_folder,folder,file)
    url = minio+path
    return url

# column names for all data layers 
keys = [
    "pct_top_amphibian_richness",
    "pct_top_reptile_richness", 
    "pct_top_bird_richness", 
    "pct_top_mammal_richness", 
    "pct_top_plant_richness", 
    "pct_wetlands",
    "pct_top_freshwater_richness",
    "pct_farmland",
    "pct_grazing_lands",
    "pct_disadvantaged_community", 
    "pct_low_income_community", 
]

chatbot_toggles = {key: False for key in keys}

# data layers dict 
layer_config = [
    #[(section, 'a_amph', [(col_name, full name, key, chatbot toggle key, citation)])]
    ('🐻 Vertebrates', 'a_amph', [
        ('pct_top_amphibian_richness', 'Amphibian Richness', keys[0], chatbot_toggles[keys[0]], 'Areas with the top 20% of amphibian richness (Reference #5)'),
        ('pct_top_reptile_richness', 'Reptile Richness', keys[1], chatbot_toggles[keys[1]], 'Areas with the top 20% of reptile richness (Reference #5)'),
        ('pct_top_bird_richness', 'Bird Richness', keys[2], chatbot_toggles[keys[2]], 'Areas with the top 20% of bird richness (Reference #5)'),
        ('pct_top_mammal_richness', 'Mammal Richness', keys[3], chatbot_toggles[keys[3]], 'Areas with the top 20% of mammal richness (Reference #5)'),
    ]),
    ('🌿 Plants', 'a_plant', [
        ('pct_top_plant_richness', 'Plant Richness', keys[4], chatbot_toggles[keys[4]], 'Areas with the top 20% of plant richness (Reference #6)'),
    ]),
    ('💧 Freshwater Resources', 'freshwater', [
        ('pct_wetlands', 'Wetlands', keys[5], chatbot_toggles[keys[5]], 'Areas that are freshwater emergent, freshwater forested/shrub, or estuarine and marine wetlands (Reference #7)'),
        ('pct_top_freshwater_richness', 'Freshwater Species Richness', keys[6], chatbot_toggles[keys[6]], 'Areas with the top 20% of freshwater species richness (Reference #8)'),
    ]),
    ('🚜 Agriculture', 'agriculture', [
        ('pct_farmland', 'Farmland', keys[7], chatbot_toggles[keys[7]], 'Farmlands with prime, unique, or of statewide or local importance (Reference #9)'),
        ('pct_grazing_lands', 'Lands Suitable for Grazing', keys[8], chatbot_toggles[keys[8]], 'Lands suitable for grazing (Reference #9)'),
    ]),
    ('👤 People', 'SVI', [
        ('pct_disadvantaged_community', 'Disadvantaged Communities', keys[9], chatbot_toggles[keys[9]], 'Areas in disadvantaged communities (Reference #10)'),
        ('pct_low_income_community', 'Low-Income Communities', keys[10], chatbot_toggles[keys[10]], 'Areas in low-income communities (Reference #11)'),
    ]),
]

# colors for plotting 
white =  "#FFFFFF" 

# github logo 
github_logo = 'M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z'

github_html = f"""
    <span style='font-size:15px;'>
        <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' class='bi bi-github ' 
            style='height:1em;width:1em;fill:currentColor;vertical-align:-0.125em;margin-right:4px;'  
            aria-hidden='true' role='img'>
            <path d='{github_logo}'></path>
        </svg>
        <span>Source Code:</span>
        <a href='https://github.com/boettiger-lab/CBN-taskforce' target='_blank'>https://github.com/boettiger-lab/CBN-taskforce</a>
    </span>
"""

question_icon = """
<svg xmlns='http://www.w3.org/2000/svg' height='1em' viewBox='0 0 24 24' width='1em' 
     style='fill:currentColor;vertical-align:-0.125em;'>
  <path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 
           10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm1.07-7.75l-.9.92C12.45 
           12.9 12 13.5 12 15h-2v-.5c0-.8.45-1.5 1.17-2.08l1.24-1.26c.37-.36.59-.86.59-1.41 
           0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 
           1.79 4 4c0 .88-.36 1.68-.93 2.25z'/>
</svg>
"""

## customize formatting
app_formatting =  """
    <style>
        /* Customizing font size for radio text */
        div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-size: 18px !important;
        }
        /* Reduce margin below the header */
        h2 {
            margin-top: 0rem !important; 
            margin-bottom: 0rem !important; /* Reduce space below headers */
        }
        /* Customizing font size for medium-font class */
        .medium-font {
            font-size: 18px !important; 
            margin-top: 0rem !important;
            margin-bottom: 0.25rem !important; /* Reduce space below */
        }
        .medium-font-sidebar {
            font-size: 17px !important;
            margin-bottom: 0.75rem !important; /* Reduce space below */
        }
        /* Customizing layout and divider */
        hr {
            margin-top: 0rem !important;  /* Adjust to reduce top margin */
            margin-bottom: 0.5rem !important; /* Adjust to reduce bottom margin */
        }
        .stAppHeader {
            background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
            visibility: visible;  /* Ensure the header is visible */
        }
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        /* Reduce whitespace for the overall expander container */
        .st-expander {
            margin-top: 0rem;  /* Space above the expander */
            margin-bottom: 0rem; /* Space below the expander */
        }
        /* Adjust padding for the content inside the expander */
        .st-expander-content {
            padding: 0rem 0rem;  /* Reduce padding inside */
        }
        /* Optional: Adjust the expander header if needed */
        .st-expander-header {
            margin-top: 0rem;
            margin-bottom: 0rem;
        }
        .spacer { margin-bottom: 30px; } /* padding in sidebar */
        [data-testid="stSidebar"] > div:first-child { /* reduce whitespace at the top of the sidebar */
            padding-top: 0rem !important; 
        }
        .caption-shift-up {
            font-size: 13px !important;
            margin-top: -9rem !important;
            margin-bottom: 0rem !important;
            text-align: right !important;
            font-style: italic !important;
            color: gray; /* optional: caption-like color */

        }
        .caption {
            font-size: 13px !important;
            margin-top: -2rem !important;
            margin-bottom: 0rem !important;
            text-align: right !important;
            font-style: italic !important;
            color: gray; /* optional: caption-like color */
        }
        .st-key-county div[data-baseweb="select"] > div:first-child {
            background-color: #f0f2f5 !important;
            border-color: #caccd0 !important;
            font-size: 14px !important;
            height: 3.5em !important;
            padding-top: 0.3rem !important;
            padding-bottom: 0.3rem !important;
            padding-left: 0.2rem !important;
            padding-right: 0.25rem !important;
            color: #000000 !important;
        }
    </style>
    """

manager = {
    'property': 'manager_type',
    'type': 'categorical',
    'stops': [
        ['Federal', "#529642"],
        ['State', "#A1B03D"],
        ['Non Profit', "#D77031"],
        ['Special District', "#0096FF"],
        ['Unknown', "#bbbbbb"],
        ['County', "#DE3163"],
        ['City', "#ADD8E6"],
        ['Joint', "#DAB0AE"],
        ['Tribal', "#00008B"],
        ['Private', "#7A3F1A"],
        ['HOA', "#A89BBC"],
        ['None', white],
    ],
    'default': white
}

land_tenure = {
    'property': 'land_tenure',
    'type': 'categorical',
    'stops': [
        ['Easement', '#DE881E'],
        ['Non-Easement', "#5B9BE0"],
        ['None', white],

    ],
    'default': white
}
access = {
    'property': 'access_type',
    'type': 'categorical',
    'stops': [
        ['Open Access', '#009E73'],
        ['Restricted Access', '#E69F00'],
        ['No Public Access', '#D55E00'],
        ['Unknown Access', "#bbbbbb"],
        ['None', white],
    ],
    'default': white
}

gap = {
    'property': 'gap_code',
    'type': 'categorical',
    'stops': [
        ['GAP 1', "#26633d"],
        ['GAP 2', "#879647"],
        ['GAP 3', "#bdcf72"],
        ['GAP 4', "#6d6e6d"],
        ['None', white],

    ],
    'default': white
}

status = {
    'property': 'status',
    'type': 'categorical',
    'stops': [
        ['30x30 Conservation Area', "#56711f"],
        ['Other Conservation Area', "#b6ce7a"],
        ['Public or Unknown Conservation Area', "#e5efdb"],
        ['Non-Conservation Area', "#e1e1e1"]
    ],
}

ecoregion = {
    'property': 'ecoregion',
    'type': 'categorical',
    'stops': [
        ['Southeastern Great Basin', "#2ca02c"],
        ['Mojave Desert', "#98df8a"],
        ['Sonoran Desert', "#9467bd"],
        ['Sierra Nevada', "#17becf"],
        ['Southern California Mountains and Valleys', "#d62728"],
        ['Mono', "#ff9896"],
        ['Central California Coast', "#9edae5"],
        ['Klamath Mountains', "#f7b6d2"],
        ['Northern California Coast', "#c7c7c7"],
        ['Northern California Coast Ranges', "#aec7e8"],
        ['Northwestern Basin and Range', "#8c564b"],
        ['Colorado Desert', "#e377c2"],
        ['Central Valley Coast Ranges', "#7f7f7f"],
        ['Southern California Coast', "#c5b0d5"],
        ['Sierra Nevada Foothills', "#1f77b4"],
        ['Southern Cascades', "#ff7f0e"],
        ['Modoc Plateau', "#c49c94"],
        ['Great Valley (South)', "#bcbd22"],
        ['Northern California Interior Coast Ranges', "#ffbb78"],
        ['Great Valley (North)', "#dbdb8d"],
        ['None', white],
    ],
    'default': white
}

climate_zone = {
    'property': 'climate_zone',
    'type': 'categorical',
    'stops': [
        ['Zone 1', "#2ca02c"],
        ['Zone 2', "#98df8a"],
        ['Zone 3', "#9467bd"],
        ['Zone 4', "#17becf"],
        ['Zone 5', "#d62728"],
        ['Zone 6', "#ff9896"],
        ['Zone 7', "#dbdb8d"],
        ['Zone 8', "#bcbd22"],
        ['Zone 9', "#c5b0d5"],
        ['Zone 10', "#e377c2"],
        ['None', white],

    ],
    'default': white
}

ecoregion = {
    'property': 'ecoregion',
    'type': 'categorical',
    'stops': [
        ['Southeastern Great Basin', "#2ca02c"],
        ['Mojave Desert', "#98df8a"],
        ['Sonoran Desert', "#9467bd"],
        ['Sierra Nevada', "#17becf"],
        ['Southern California Mountains and Valleys', "#d62728"],
        ['Mono', "#ff9896"],
        ['Central California Coast', "#9edae5"],
        ['Klamath Mountains', "#f7b6d2"],
        ['Northern California Coast', "#c7c7c7"],
        ['Northern California Coast Ranges', "#aec7e8"],
        ['Northwestern Basin and Range', "#8c564b"],
        ['Colorado Desert', "#e377c2"],
        ['Central Valley Coast Ranges', "#7f7f7f"],
        ['Southern California Coast', "#c5b0d5"],
        ['Sierra Nevada Foothills', "#1f77b4"],
        ['Southern Cascades', "#ff7f0e"],
        ['Modoc Plateau', "#c49c94"],
        ['Great Valley (North)', "#dbdb8d"],
        ['Northern California Interior Coast Ranges', "#ffbb78"],
        ['Great Valley (South)', "#bcbd22"],
        ['None', white],
    ],
    'default': white
}

habitat_type = {
    'property': 'habitat_type',
    'type': 'categorical',
    'stops': [
        ['Agriculture', "#CCCCCC"],
        ['Barren/Other', white],
        ['Conifer Forest', "#267300"],
        ['Conifer Woodland', "#ABCD66"],
        ['Desert Shrub', "#FFEBBE"],
        ['Desert Woodland', "#D7C29E"],
        ['Hardwood Forest', "#002673"],
        ['Hardwood Woodland', "#6699CD"],
        ['Grassland', "#A87000"],
        ['Shrub', "#F5CA7A"],
        ['Urban', "#686868"],
        ['Water', "#BEFFE8"],
        ['Wetland', "#00A884"],
        ['None', white],
    ],
    'default': white
}


style_options = {
    "30x30 Status": status,
    "GAP Code": gap,
    "Ecoregion": ecoregion,
    "Habitat Type": habitat_type,
    "Climate Zone": climate_zone,
    "Manager Type": manager,
    "Land Tenure Type": land_tenure,
    "Access Type": access,
}

select_column = {
    "30x30 Status":  "status",
    "GAP Code": "gap_code",
    "Ecoregion":  "ecoregion",
    "Habitat Type":  "habitat_type",
    "Climate Zone":  "climate_zone",
    "Manager Type": "manager_type",
    "Land Tenure Type": "land_tenure",
    "Access Type": "access_type",
}

select_colors = {
    "30x30 Status": status["stops"],
    "GAP Code": gap["stops"],
    "Ecoregion": ecoregion["stops"],
    "Habitat Type": habitat_type["stops"],
    "Climate Zone": climate_zone["stops"],
    "Manager Type": manager["stops"],
    "Land Tenure Type": land_tenure["stops"],
    "Access Type": access["stops"],

}

error_messages = {
    "bad_request": lambda llm, e, tb_str: f"""
**Error – LLM Unavailable** 

*The LLM you selected `{llm}` is no longer available. Please select a different model.*

**Error Details:**
`{type(e)}: {e}`

""",

    "internal_server_error": lambda llm, e, tb_str: f"""
**Error – LLM Temporarily Unavailable**

The LLM you selected `{llm}` is currently down due to maintenance or provider outages. It may remain offline for several hours.

**Please select a different model or try again later.**

**Error Details:**
`{type(e)}: {e}`

""",

    "unexpected_llm_error": lambda prompt, e, tb_str: f"""
🐞 **BUG: Unexpected Error in Application**

An error occurred while processing your query:

> "{prompt}"

**Error Details:**
`{type(e)}: {e}`

Traceback:

```{tb_str}```
---

🚨 **Help Us Improve!**

Please help us fix this issue by reporting it on GitHub:
[📄 Report this issue](https://github.com/boettiger-lab/CBN-taskforce/issues)

Include the query you ran and any other relevant details. Thanks!
""",

    "unexpected_error": lambda e, tb_str: f"""
🐞 **BUG: Unexpected Error in Application**


**Error Details:**
`{type(e)}: {e}`

Traceback:

```{tb_str}```

---

🚨 **Help Us Improve!**

Please help us fix this issue by reporting it on GitHub:
[📄 Report this issue](https://github.com/boettiger-lab/CBN-taskforce/issues)

Include the steps you took to get this message and any other details that might help us debug. Thanks!
"""
}

help_message = '''
- ❌ Safari/iOS not fully supported. For Safari/iOS users, change the **Leafmap module** from MapLibre to Folium in **(Map Settings)** below. 
- 📊 Use this sidebar to color-code the map by different attributes **(Group by)**, filter data **(Filters)**, toggle on data layers and view summary charts **(Data Layers)**, and customize mapping in **(Map Settings)**.
- 🐢 If the map is lagging and slow to load, toggle on **Low Resolution** in **(Map Settings)**.
- 💬 For a more tailored experience, query our dataset of protected areas and their precomputed metrics for each of the displayed layers, using the experimental chatbot. The language model tries to answer natural language questions by drawing only from curated datasets (listed below).
'''

example_queries = """
Mapping queries:
- Show me amphibian biodiversity hotspots not covered by the 30x30 network.
- Show me GAP 3 lands with mean bird richness in the top 10%.
- Show me easements with 60% or more overlap with high plant biodiversity regions.
- Show me protected areas that are open to the public in disadvantaged communities. 
- Show me all 30x30 conservation areas managed by The Nature Conservancy.

Exploratory data queries:
- What is a GAP code?
- What is the habitat composition of the 30x30 network?
- Which county has the highest percentage of 30x30 conservation areas?
- Summarize the habitat types in the Mojave preserve.
- What ecoregion has the highest bird species richness?

"""

chatbot_limitations = """
**Chatbot Limitations:**
- The chatbot is independent from **Filters**, which do not modify the chatbot's input or output.
- The chatbot has no memory and won't remember previous questions or responses.
- The chatbot can’t directly generate charts or change map colors, it only updates them by adjusting  **Data Layers** or **Group by** based on your query. To update these, ask about a grouping variable (e.g., `ecoregion`) or data layer (e.g., `wetlands`). 
"""

chatbot_info = """
If the map appears blank, queried data may be too small to see at the default zoom level. Check the table below the map, as query results will also be displayed there.
"""
label_transforms = {
    "access_type": ("replace(datum.access_type, ' Access', '')", lambda lbl: lbl.replace(" Access", "")),
    "ecoregion": (
        "replace(replace(replace(replace(replace("
        "replace(datum.ecoregion, 'Northern California', 'NorCal'),"
        "'Southern California', 'SoCal'),"
        "'Southeastern', 'SE.'),"
        "'Northwestern', 'NW.'),"
        "'and', '&'),"
        "'California', 'CA')",
        lambda lbl: (lbl.replace("Northern California", "NorCal")
                     .replace("Southern California", "SoCal")
                     .replace("Southeastern", "SE.")
                     .replace("Northwestern", "NW.")
                     .replace("and", "&")
                     .replace("California", "CA"))
    ),
}

sort_options = {
    "established": "-x",
    "access_type": [
        "Open",
        "Restricted",
        "No Public",
        "Unknown",
        "None",
    ],
    "land_tenure": [
        "Easement",
        "Non-Easement",
        "None",
    ],
    "manager_type": [
        "Federal",
        "Tribal",
        "State",
        "Special District",
        "County",
        "City",
        "HOA",
        "Joint",
        "Non Profit",
        "Private",
        "Unknown",
        "None",
    ],
    "status": [
        "30x30 Conservation Area",
        "Other Conservation Area",
        "Public or Unknown Conservation Area",
        "Non-Conservation Area"
    ],
    "ecoregion": [
        "SE. Great Basin",
        "Mojave Desert",
        "Sonoran Desert",
        "Sierra Nevada",
        "SoCal Mountains & Valleys",
        "Mono",
        "Central CA Coast",
        "Klamath Mountains",
        "NorCal Coast",
        "NorCal Coast Ranges",
        "NW. Basin & Range",
        "Colorado Desert",
        "Central Valley Coast Ranges",
        "SoCal Coast",
        "Sierra Nevada Foothills",
        "Southern Cascades",
        "Modoc Plateau",
        "Great Valley (North)",
        "NorCal Interior Coast Ranges",
        "Great Valley (South)"
        "None",

    ],
    "climate_zone": [
        "Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5",
        "Zone 6", "Zone 7", "Zone 8", "Zone 9", "Zone 10", "None"
    ],
}

counties = ['Alameda','Alpine','Amador','Butte',
            'Calaveras','Colusa','Contra Costa',
            'Del Norte','El Dorado','Fresno',
            'Glenn','Humboldt','Imperial',
            'Inyo','Kern','Kings','Lake',
            'Lassen','Los Angeles','Madera',
            'Marin','Mariposa','Mendocino',
            'Merced','Modoc','Mono','Monterey',
            'Napa','Nevada','Orange','Placer',
            'Plumas','Riverside','Sacramento',
            'San Benito','San Bernardino',
            'San Diego','San Francisco',
            'San Joaquin','San Luis Obispo',
            'San Mateo','Santa Barbara',
            'Santa Clara','Santa Cruz',
            'Shasta','Sierra','Siskiyou',
            'Solano','Sonoma','Stanislaus',
            'Sutter','Tehama','Trinity',
            'Tulare','Tuolumne','Ventura',
            'Yolo','Yuba']
counties = [c + ' County' for c in counties]

county_bounds = {
    'Alameda': [-122.42384326, 37.15395019, -121.41909054, 38.20581216],
    'Alpine': [-120.12258426, 38.27799315, -119.49223011, 38.98342773],  # padded
    'Amador': [-121.07730731, 37.91749178, -120.02237157, 38.50911291],
    'Butte': [-122.06925623, 39.29575927, -121.07659059, 40.15172491],
    'Calaveras': [-121.04563506, 37.78291105, -119.96784279, 38.55989257],  # padded
    'Colusa': [-122.835104, 38.62390909, -121.74535019, 39.7146368],
    'Contra Costa': [-122.49136196, 37.41848003, -121.48427173, 38.40451269],
    'Del Norte': [-124.34222097, 41.33080831, -123.46781185, 42.05093718],
    'El Dorado': [-121.19871594, 38.2024066, -119.82715698, 39.3675152],
    'Fresno': [-120.91924675, 35.90667589, -118.36128145, 37.58611123],
    'Glenn': [-122.98825654, 39.08298316, -121.80664646, 40.10062595],
    'Humboldt': [-124.42174856, 40.00139253, -123.40574433, 41.46572559],
    'Imperial': [-116.10627333, 32.61840233, -114.46278797, 33.43383607],
    'Inyo': [-118.79005686, 35.78658302, -115.64806204, 37.46492214],
    'Kern': [-120.19415436, 34.78853746, -117.61634054, 35.79830877],
    'Kings': [-120.36511242, 35.73861179, -119.42437670, 36.53883302],  # padded
    'Lake': [-123.14417624, 38.61765293, -122.28982221, 39.63152361],
    'Lassen': [-121.38200128, 39.65762659, -119.94560445, 41.23462163],  # padded
    'Los Angeles': [-118.99473688, 32.74821787, -117.59626902, 34.87326884],  # padded
    'Madera': [-120.59535559, 36.71290957, -118.97313702, 37.82824405],  # padded
    'Marin': [-123.0745472, 37.51434498, -122.30271529, 38.62116119],
    'Mariposa': [-120.44543630, 37.13302862, -119.25916114, 37.95278231],  # padded
    'Mendocino': [-124.07304087, 38.70798088, -122.76767857, 40.05203171],  # padded
    'Merced': [-121.29761545, 36.69041903, -120.00247704, 37.68351397],  # padded
    'Modoc': [-121.50733566, 41.13389108, -119.94860791, 42.04770261],  # padded
    'Mono': [-119.70129170, 37.41265974, -117.78305435, 38.76421963],  # padded
    'Monterey': [-122.03121233, 35.73903942, -120.16394627, 36.96976420],  # padded
    'Napa': [-122.69680992, 38.10486635, -122.01139053, 38.91431964],  # padded
    'Nevada': [-121.32983631, 38.70521113, -119.9531695, 39.82697761],
    'Orange': [-118.16591131, 33.08695359, -117.36276683, 34.24763009],
    'Placer': [-121.53447175, 38.66121391, -119.95248410, 39.36647773],  # padded
    'Plumas': [-121.54814672, 39.54728718, -120.04904721, 40.49953710],  # padded
    'Riverside': [-117.72631999, 33.37595837, -114.38492273, 34.13010291],  # padded
    'Sacramento': [-121.91280525, 37.96826995, -120.97708001, 38.78635417],  # padded
    'San Benito': [-121.69390644, 36.14676935, -120.54665891, 37.03889695],  # padded
    'San Bernardino': [-117.85270608, 33.82100430, -114.08077973, 35.85925465],  # padded
    'San Diego': [-117.64618783, 32.48428490, -116.03103175, 33.55539079],  # padded
    'San Francisco': [-123.15831309, 37.39318221, -122.23148009, 38.22820082],
    'San Joaquin': [-121.63486555, 37.43190337, -120.86703421, 38.35012427],  # padded
    'San Luis Obispo': [-121.39814635, 34.84751703, -119.42262333, 35.84522760],  # padded
    'San Mateo': [-122.57582244, 36.8066465, -122.03170059, 38.25830103],
    'Santa Barbara': [-120.72308089, 33.41314654, -118.97754553, 35.16466474],  # padded
    'Santa Clara': [-122.25265825, 36.59311358, -121.15829193, 38.03463353],
    'Santa Cruz': [-122.36756095, 36.54559289, -121.53152181, 37.58548653],
    'Shasta': [-123.11905637, 40.23542875, -121.26956590, 41.23540519],  # padded
    'Sierra': [-121.10816357, 39.09131235, -119.95115691, 39.84189314],
    'Siskiyou': [-123.76921666, 40.94216151, -121.39597247, 42.05950135],  # padded
    'Solano': [-122.45704233, 37.73190147, -121.54328788, 38.48131072],
    'Sonoma': [-123.58409675, 38.01945545, -122.29969676, 38.90265626],  # padded
    'Stanislaus': [-121.53508015, 37.08465560, -120.33777967, 38.12751340],  # padded
    'Sutter': [-121.99803192, 38.43464395, -121.36457683, 39.20570925],
    'Tehama': [-123.11606980, 39.74740002, -121.29202780, 40.49616085],  # padded
    'Trinity': [-123.67375901, 39.92696451, -122.39579472, 41.41855813],  # padded
    'Tulare': [-119.57337697, 35.78670323, -117.98078853, 36.75315532],
    'Tuolumne': [-120.70310289, 37.58351397, -119.14950790, 38.48587454],  # padded
    'Ventura': [-119.62884548, 33.16442311, -118.58248588, 34.95117361],  # padded
    'Yolo': [-122.47292975, 38.26334133, -121.45117107, 38.97599413],  # padded
    'Yuba': [-121.63634257, 38.91834060, -121.00962750, 39.63941541]
}



basemaps = ['CartoDB.DarkMatter', 'CartoDB.DarkMatterNoLabels', 
            'CartoDB.DarkMatterOnlyLabels','CartoDB.Positron', 
            'CartoDB.PositronNoLabels', 'CartoDB.PositronOnlyLabels',
            'CartoDB.Voyager', 'CartoDB.VoyagerLabelsUnder', 'CartoDB.VoyagerNoLabels',
            'CartoDB.VoyagerOnlyLabels', 'CyclOSM', 'Esri.NatGeoWorldMap',
            'Esri.WorldGrayCanvas', 'Esri.WorldPhysical', 'Esri.WorldShadedRelief',
            'Esri.WorldStreetMap', 'Gaode.Normal', 'Gaode.Satellite',
            'NASAGIBS.ASTER_GDEM_Greyscale_Shaded_Relief', 'NASAGIBS.BlueMarble', 
            'NASAGIBS.ModisTerraBands367CR','NASAGIBS.ModisTerraTrueColorCR',
            'NLCD 2021 CONUS Land Cover', 'OPNVKarte',
            'OpenStreetMap', 'OpenTopoMap', 'SafeCast',
            'TopPlusOpen.Color', 'TopPlusOpen.Grey', 'UN.ClearMap',
            'USGS Hydrography', 'USGS.USImagery', 'USGS.USImageryTopo',
            'USGS.USTopo']


#maplibregl tooltip 
tooltip_cols = ['id','name','manager','county','status','gap_code',
                'habitat_type','climate_zone','land_tenure','ecoregion','acres']
tooltip_template = "<br>".join([f"{col}: {{{{ {col} }}}}" for col in tooltip_cols])

from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_openai.chat_models.base import BaseChatOpenAI

## dockerized streamlit app wants to read from os.getenv(), otherwise use st.secrets
import os
api_key = os.getenv("NRP_API_KEY")
if api_key is None:
    api_key = st.secrets["NRP_API_KEY"]

openrouter_api = os.getenv("OPENROUTER_API_KEY")
if openrouter_api is None:
    openrouter_api = st.secrets["OPENROUTER_API_KEY"]

llm_options = {
    "mistral-small-3.2-24b-instruct": ChatOpenAI(model = "mistralai/mistral-small-3.2-24b-instruct:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "devstral-small-2505": ChatOpenAI(model = "mistralai/devstral-small-2505:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "gpt-oss-20b": ChatOpenAI(model = "openai/gpt-oss-20b:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "deepseek-r1t2-chimera": ChatOpenAI(model = "tngtech/deepseek-r1t2-chimera:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "kimi-dev-72b": ChatOpenAI(model = "moonshotai/kimi-dev-72b:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "hunyuan-a13b-instruct": ChatOpenAI(model = "tencent/hunyuan-a13b-instruct:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    # "deepseek-chat-v3-0324": ChatOpenAI(model = "deepseek/deepseek-chat-v3-0324:free", api_key=openrouter_api, base_url = "https://openrouter.ai/api/v1",  temperature=0),
    "olmo": ChatOpenAI(model = "olmo", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "llama3": ChatOpenAI(model = "llama3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    # "deepseek-r1": BaseChatOpenAI(model = "deepseek-r1", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "qwen3": ChatOpenAI(model = "qwen3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "gemma3": ChatOpenAI(model = "gemma3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),

}