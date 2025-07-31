# urls for main layer 
ca_parquet = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30_cbn_v3.parquet'
ca_pmtiles = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30_cbn_v3.pmtiles'
# 

# computed by taking the sum of all the acres in this file:
# https://minio.carlboettiger.info/public-ca30x30/CBN-data/Progress_data_new_protection/Land_Status_Zone_Ecoregion_Counties/all_regions_reGAP_county_eco.parquet
ca_area_acres = 101523750.68856516 
style_choice = "GAP Status Code"
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

import re
source_layer_name = re.sub(r'\W+', '', os.path.splitext(os.path.basename(ca_pmtiles))[0])
#stripping hyphens to get layer name 

# column names for all data layers 
keys = [
    "pct_top_amphibian_richness",
    "pct_top_reptile_richness", 
    "pct_top_bird_richness", 
    "pct_top_mammal_richness", 
    # "mean_amphibian_richness",
    # "mean_reptile_richness", 
    # "mean_bird_richness", 
    # "mean_mammal_richness", 
    "pct_top_plant_richness", 
    # "mean_plant_richness", 
    "pct_wetlands",
    "pct_top_freshwater_richness",
    # "mean_freshwater_richness",
    "pct_farmland",
    "pct_grazing_lands",
    "pct_disadvantaged_community", 
    "pct_low_income_community", 
    "pct_fire"]

chatbot_toggles = {key: False for key in keys}

# data layers dict 
layer_config = [
    #[(section, 'a_amph', [(col_name, full name, key, chatbot toggle key, citation)])]
    ('🐸 Amphibian', 'a_amph', [
        ('pct_top_amphibian_richness', 'Amphibian Richness', keys[0], chatbot_toggles[keys[0]], 'Areas with the top 20% of amphibian richness (Reference #5)'),
        # ('mean_amphibian_richness', 'Mean Amphibian Richness', keys[1], chatbot_toggles[keys[1]], 'Average amphibian richness calculated over each area (Reference #5)'),
    ]),
    ('🐍 Reptile', 'a_rept', [
        ('pct_top_reptile_richness', 'Reptile Richness', keys[1], chatbot_toggles[keys[1]], 'Areas with the top 20% of reptile richness (Reference #5)'),
        # ('mean_reptile_richness', 'Mean Reptile Richness', keys[3], chatbot_toggles[keys[3]], 'Average reptile richness calculated over each area (Reference #5)'),

    ]),
    ('🦜 Bird', 'a_bird', [
        ('pct_top_bird_richness', 'Bird Richness', keys[2], chatbot_toggles[keys[2]], 'Areas with the top 20% of bird richness (Reference #5)'),
        # ('mean_bird_richness', 'Mean Bird Richness', keys[5], chatbot_toggles[keys[5]], 'Average bird richness calculated over each area (Reference #5)'),

    ]),
    ('🦌 Mammal', 'a_mammal', [
        ('pct_top_mammal_richness', 'Mammal Richness', keys[3], chatbot_toggles[keys[3]], 'Areas with the top 20% of mammal richness (Reference #5)'),
        # ('mean_mammal_richness', 'Mean Mammal Richness', keys[7], chatbot_toggles[keys[7]], 'Average mammal richness calculated over each area (Reference #5)'),
    ]),
    ('🌿 Plant', 'a_plant', [
        ('pct_top_plant_richness', 'Plant Richness', keys[4], chatbot_toggles[keys[4]], 'Areas with the top 20% of plant richness (Reference #6)'),
        # ('mean_plant_richness', 'Mean Plant Richness', keys[9], chatbot_toggles[keys[9]], 'Average plant richness calculated over each area (Reference #6)'),

    ]),
    ('💧 Freshwater Resources', 'freshwater', [
        ('pct_wetlands', 'Wetlands', keys[5], chatbot_toggles[keys[5]], 'Areas that are freshwater emergent, freshwater forested/shrub, or estuarine and marine wetlands (Reference #7)'),
        ('pct_top_freshwater_richness', 'Freshwater Species Richness', keys[6], chatbot_toggles[keys[6]], 'Areas with the top 20% of freshwater species richness (Reference #8)'),
        # ('mean_freshwater_richness', 'Mean Freshwater Species Richness', keys[12], chatbot_toggles[keys[12]], 'Average freshwater species richness calculated over each area (Reference #8)'),
    ]),
    ('🚜 Agriculture', 'agriculture', [
        ('pct_farmland', 'Farmland', keys[7], chatbot_toggles[keys[7]], 'Farmlands with prime, unique, or of statewide or local importance (Reference #9)'),
        ('pct_grazing_lands', 'Lands Suitable for Grazing', keys[8], chatbot_toggles[keys[8]], 'Lands suitable for grazing (Reference #9)'),
    ]),
    ('👤 People', 'SVI', [
        ('pct_disadvantaged_community', 'Disadvantaged Communities', keys[9], chatbot_toggles[keys[9]], 'Areas in disadvantaged communities (Reference #10)'),
        ('pct_low_income_community', 'Low-Income Communities', keys[10], chatbot_toggles[keys[10]], 'Areas in low-income communities (Reference #11)'),
    ]),
    ('🔥 Climate Risks', 'calfire', [
        ('pct_fire', 'Wildfires', keys[11], chatbot_toggles[keys[11]], 'Areas burned in the last 10 years (Reference #12)'),
    ]),
]

# colors for plotting 
private_access_color = "#DE881E" # orange 
public_access_color = "#3388ff" # blue
purple = "#BF40BF" # purple
mixed_color = "#005a00" # green
year2023_color = "#26542C" # green
year2024_color = "#F3AB3D" # orange 
federal_color = "#529642" # green
state_color = "#A1B03D" # light green
local_color = "#365591" # blue
special_color = "#0096FF" # blue
private_color = "#7A3F1A" # brown
joint_color = "#DAB0AE" # light pink
county_color = "#DE3163" # magenta
city_color = "#ADD8E6" #light blue
hoa_color = "#A89BBC" # purple
nonprofit_color =  "#D77031" #orange
purple =  "#00008B" #purple
cyan = "#1bc7c3" #cyan
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
    </style>
    """

manager = {
    'property': 'manager_type',
    'type': 'categorical',
    'stops': [
        ['Federal', federal_color],
        ['State', state_color],
        ['Non Profit', nonprofit_color],
        ['Special District', special_color],
        ['Unknown', "#bbbbbb"],
        ['County', county_color],
        ['City', city_color],
        ['Joint', joint_color],
        ['Tribal', purple],
        ['Private', private_color],
        ['HOA', hoa_color],
        ['None', white],
    ],
    'default': white
}

land_tenure = {
    'property': 'land_tenure',
    'type': 'categorical',
    'stops': [
        ['Easement', private_access_color],
        ['Non-Easement', public_access_color],
        ['None', white],

    ],
    'default': white
}
access = {
    'property': 'access_type',
    'type': 'categorical',
    'stops': [
        ['Open Access', public_access_color],
        ['No Public Access', private_access_color],
        ['Unknown Access', "#bbbbbb"],
        ['Restricted Access', purple],
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
        ['Great Valley (South)', "#bcbd22"],
        ['Northern California Interior Coast Ranges', "#ffbb78"],
        ['Great Valley (North)', "#dbdb8d"],
        ['None', white],
    ],
    'default': white
}

habitat_type = {
    'property': 'habitat_type',
    'type': 'categorical',
    'stops': [
        ['Agriculture', "#CCCCCC"],
        ['Barren/Other', "#FFFFFF"],
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
    "Climate Zone": climate_zone,
    "Habitat Type": habitat_type,
    "Manager Type": manager,
    "Land Tenure Type": land_tenure,
    "Access Type": access,
}

select_column = {
    "30x30 Status":  "status",
    "GAP Code": "gap_code",
    "Ecoregion":  "ecoregion",
    "Climate Zone":  "climate_zone",
    "Habitat Type":  "habitat_type",
    "Manager Type": "manager_type",
    "Land Tenure Type": "land_tenure",
    "Access Type": "access_type",
}

select_colors = {
    "30x30 Status": status["stops"],
    "GAP Code": gap["stops"],
    "Ecoregion": ecoregion["stops"],
    "Climate Zone": climate_zone["stops"],
    "Habitat Type": habitat_type["stops"],
    "Manager Type": manager["stops"],
    "Land Tenure Type": land_tenure["stops"],
    "Access Type": access["stops"],

}

error_messages = {
    "bad_request": lambda llm: f"""
**Error Code 400 – LLM Unavailable** 

*The LLM you selected `{llm}` is no longer available. Please select a different model.*
""",
    
    "internal_server_error": lambda llm: f"""
**Error Code 500 – LLM Temporarily Unavailable**

The LLM you selected `{llm}` is currently down due to maintenance or provider outages. It may remain offline for several hours.

**Please select a different model or try again later.**
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
- 📊 Use this sidebar to color-code the map by different attributes **(Group by)**, filter data **(Filters)**, or toggle on data layers and view summary charts **(Data Layers)**.
- 💬 For a more tailored experience, query our dataset of protected areas and their precomputed metrics for each of the displayed layers, using the experimental chatbot. The language model tries to answer natural language questions by drawing only from curated datasets (listed below).
'''

example_queries = """
Mapping queries:
- Show me amphibian biodiversity hotspots that aren't currently conserved.
- Show me protected areas in disadvantaged communities.
- Show me all 30x30 conservation areas managed by The Nature Conservancy.

Exploratory data queries:
- What is a GAP code?
- What percentage of 30x30 conserved land has been impacted by wildfire?
- How many acres are newly protected easements?
- Which county has the highest percentage of wetlands?
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

counties = ['All',
            'Alameda','Alpine','Amador','Butte',
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

county_bounds = {
    'Alameda': [-122.37384325785614, 37.45395019087806, -121.46909053649193, 37.90581215615551],
    'Alpine': [-120.07258425884774, 38.327993145831655, -119.54223011041208, 38.93342773013462],
    'Amador': [-121.02730731480422, 38.217491780743636, -120.07237156968037, 38.70911291117487],
    'Butte': [-122.06925623406984, 39.295759266788785, -121.07659058901427, 40.151724905958844],
    'Calaveras': [-120.99563505712699, 37.832911048889336, -120.01784279081615, 38.50989256828466],
    'Colusa': [-122.7851039963557, 38.92390908599703, -121.79535019214951, 39.41463679832666],
    'Contra Costa': [-122.44136195698891, 37.71848003161996, -121.53427173214118, 38.10451269178112],
    'Del Norte': [-124.29222096554467, 41.380808308174196, -123.51781185269014, 42.00093718008948],
    'El Dorado': [-121.14871593526819, 38.50240659596396, -119.87715698072778, 39.06751520300653],
    'Fresno': [-120.91924675434643, 35.906675889793114, -118.36128145056477, 37.58611123324542],
    'Glenn': [-122.9382565375967, 39.382983163760805, -121.85664645766673, 39.80062595168279],
    'Humboldt': [-124.42174856047471, 40.00139252700087, -123.40574432966143, 41.46572559085193],
    'Imperial': [-116.10627332812045, 32.618402326401856, -114.46278796859593, 33.43383606750038],
    'Inyo': [-118.7900568626879, 35.78658301549606, -115.64806204409115, 37.464922140000915],
    'Kern': [-120.19415436469426, 34.78853746313057, -117.61634054187135, 35.7983087685926],
    'Kings': [-120.31511241500048, 35.78861179496948, -119.47437670425381, 36.48883301918508],
    'Lake': [-123.09417624448064, 38.66765292825958, -122.33982220613575, 39.58152361426639],
    'Lassen': [-121.33200127890402, 39.70762659323746, -119.99560445053615, 41.18462162566647],
    'Los Angeles': [-118.94473687665884, 32.79821786822939, -117.64626902157303, 34.823268840850936],
    'Madera': [-120.5453555935079, 36.76290956666377, -119.02313701874256, 37.77824405308708],
    'Marin': [-123.02454720223808, 37.81434498425288, -122.35271528742317, 38.32116119123995],
    'Mariposa': [-120.39543629671475, 37.18302861670762, -119.3091611358611, 37.902782310170124],
    'Mendocino': [-124.02304086840115, 38.75798088034271, -122.8176785694875, 40.00203170873202],
    'Merced': [-121.24761545052745, 36.74041902700379, -120.05247703565685, 37.63351397040037],
    'Modoc': [-121.45733565901256, 41.183891080265816, -119.99860790992162, 41.99770261425136],
    'Mono': [-119.65129169554416, 37.46265974380474, -117.8330543487398, 38.71421962752979],
    'Monterey': [-121.98121232673658, 35.7890394151396, -120.2139462682171, 36.919764203214925],
    'Napa': [-122.64680992261836, 38.15486634651152, -122.06139053020189, 38.864319635366094],
    'Nevada': [-121.27983631175151, 39.00521112712352, -120.00316950265977, 39.5269776072248],
    'Orange': [-118.11591130948763, 33.3869535933095, -117.41276683318105, 33.94763009369535],
    'Placer': [-121.48447174569603, 38.71121391174871, -120.0024840996466, 39.316477729088426],
    'Plumas': [-121.49814672171111, 39.59728718352163, -120.09904721387224, 40.44953709582471],
    'Riverside': [-117.67631998709106, 33.42595836771541, -114.43492272617631, 34.08010291317722],
    'Sacramento': [-121.8628052495484, 38.01826994810689, -121.02708000920751, 38.7363541729806],
    'San Benito': [-121.64390643788927, 36.19676935270105, -120.59665891295839, 36.98889694533727],
    'San Bernardino': [-117.80270607757481, 33.87100430334213, -114.1307797292214, 35.80925464587483],
    'San Diego': [-117.59618782585494, 32.534284897747774, -116.08103174786864, 33.50539078723194],
    'San Francisco': [-123.10831309140733, 37.69318220804253, -122.28148008634933, 37.92820081871259],
    'San Joaquin': [-121.58486554707626, 37.481903374861155, -120.91703421015885, 38.300124270425094],
    'San Luis Obispo': [-121.3481463468677, 34.897517026385394, -119.47262333499197, 35.79522759709139],
    'San Mateo': [-122.5258224417463, 37.10664649951801, -122.08170058501933, 37.70830102997501],
    'Santa Barbara': [-120.67308089356803, 33.46314653916473, -119.02754553140863, 35.114664743543855],
    'Santa Clara': [-122.20265824664642, 36.89311357700511, -121.20829193496792, 37.48463352900927],
    'Santa Cruz': [-122.31756094951439, 36.8455928887126, -121.58152180864509, 37.285486526818595],
    'Shasta': [-123.0690563724846, 40.28542875156154, -121.31956589577165, 41.1854051911446],
    'Sierra': [-121.05816357318655, 39.391312349649645, -120.00115690935537, 39.776893139510406],
    'Siskiyou': [-123.71921666125596, 40.992161506975485, -121.44597246960173, 42.0095013546309],
    'Solano': [-122.40704233020435, 38.031901469642186, -121.59328788355768, 38.54031071585052],
    'Sonoma': [-123.53409674915936, 38.06945545436569, -122.34969676191652, 38.85265625600535],
    'Stanislaus': [-121.48508014594434, 37.13465559553392, -120.3877796675966, 38.077513404644776],
    'Sutter': [-121.94803192250085, 38.73464395327457, -121.41457682661877, 39.30570924614072],
    'Tehama': [-123.06606979920167, 39.797400024908534, -121.34202780109031, 40.4461608526014],
    'Trinity': [-123.6237590070662, 39.976964508183706, -122.44579471602161, 41.36855812773586],
    'Tulare': [-119.57337696768919, 35.786703233263246, -117.98078852804592, 36.75315531553344],
    'Tuolumne': [-120.6531028934154, 37.63351397040037, -119.1995078951056, 38.435874537731834],
    'Ventura': [-119.57884547615261, 33.214423112310726, -118.63248587968316, 34.901173610510234],
    'Yolo': [-122.42292975313535, 38.313341330770385, -121.5011710694855, 38.925994128593054],
    'Yuba': [-121.63634256943894, 38.918340603636125, -121.00962749771216, 39.639415414392985]
}

filter_expr_all = [
    'all',
    ['match', ['get', 'status'],
        [
            '30x30 Conservation Area',
            'Other Conservation Area',
            'Public or Unknown Conservation Area',
            'Non-Conservation Area'
        ],
        True, False
    ],
    ['match', ['get', 'gap_code'],
        [
            'GAP 1', 'GAP 2', 'GAP 3', 'GAP 4', 'None'
        ],
        True, False
    ],
    ['match', ['get', 'ecoregion'],
        [
            'Southeastern Great Basin',
            'Mojave Desert',
            'Sonoran Desert',
            'Sierra Nevada',
            'Southern California Mountains and Valleys',
            'Mono',
            'Central California Coast',
            'Klamath Mountains',
            'Northern California Coast',
            'Northern California Coast Ranges',
            'Northwestern Basin and Range',
            'Colorado Desert',
            'Central Valley Coast Ranges',
            'Southern California Coast',
            'Sierra Nevada Foothills',
            'Southern Cascades',
            'Modoc Plateau',
            'Great Valley (South)',
            'Northern California Interior Coast Ranges',
            'Great Valley (North)',
            'None'
        ],
        True, False
    ],
    ['match', ['get', 'climate_zone'],
        [
            'Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5',
            'Zone 6', 'Zone 7', 'Zone 8', 'Zone 9', 'Zone 10', 'None'
        ],
        True, False
    ],
    ['match', ['get', 'habitat_type'],
        [
            'Agriculture', 'Barren/Other', 'Conifer Forest', 'Conifer Woodland',
            'Desert Shrub', 'Desert Woodland', 'Hardwood Forest', 'Hardwood Woodland',
            'Grassland', 'Shrub', 'Urban', 'Water', 'Wetland', 'None'
        ],
        True, False
    ],
    ['match', ['get', 'manager_type'],
        [
            'Federal', 'State', 'Non Profit', 'Special District', 'Unknown',
            'County', 'City', 'Joint', 'Tribal', 'Private', 'HOA', 'None'
        ],
        True, False
    ],
    ['match', ['get', 'land_tenure'],
        ['Easement', 'Non-Easement', 'None'],
        True, False
    ],
    ['match', ['get', 'access_type'],
        ['Open Access', 'No Public Access', 'Unknown Access', 'Restricted Access', 'None'],
        True, False
    ]
]



from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_openai.chat_models.base import BaseChatOpenAI

## dockerized streamlit app wants to read from os.getenv(), otherwise use st.secrets
import os
api_key = os.getenv("NRP_API_KEY")
if api_key is None:
    api_key = st.secrets["NRP_API_KEY"]

llm_options = {
    "llama3-sdsc": ChatOpenAI(model = "llama3-sdsc", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "olmo": ChatOpenAI(model = "olmo", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "llama3": ChatOpenAI(model = "llama3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "deepseek-r1": BaseChatOpenAI(model = "deepseek-r1", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "qwen3": ChatOpenAI(model = "qwen3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "gemma3": ChatOpenAI(model = "gemma3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),

}

