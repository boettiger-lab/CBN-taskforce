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
    'Alameda': [-122.37384326, 37.45395019, -121.46909054, 37.90581216],
    'Alpine': [-120.07258426, 38.32799315, -119.54223011, 38.93342773],
    'Amador': [-121.02730731, 38.21749178, -120.07237157, 38.70911291],
    'Butte': [-122.06925623, 39.29575927, -121.07659059, 40.15172491],
    'Calaveras': [-120.99563506, 37.83291105, -120.01784279, 38.50989257],
    'Colusa': [-122.78510400, 38.92390909, -121.79535019, 39.41463680],
    'Contra Costa': [-122.44136196, 37.71848003, -121.53427173, 38.10451269],
    'Del Norte': [-124.29222097, 41.38080831, -123.51781185, 42.00093718],
    'El Dorado': [-121.14871594, 38.50240660, -119.87715698, 39.06751520],
    'Fresno': [-120.91924675, 35.90667589, -118.36128145, 37.58611123],
    'Glenn': [-122.93825654, 39.38298316, -121.85664646, 39.80062595],
    'Humboldt': [-124.42174856, 40.00139253, -123.40574433, 41.46572559],
    'Imperial': [-116.10627333, 32.61840233, -114.46278797, 33.43383607],
    'Inyo': [-118.79005686, 35.78658302, -115.64806204, 37.46492214],
    'Kern': [-120.19415436, 34.78853746, -117.61634054, 35.79830877],
    'Kings': [-120.31511242, 35.78861179, -119.47437670, 36.48883302],
    'Lake': [-123.09417624, 38.66765293, -122.33982221, 39.58152361],
    'Lassen': [-121.33200128, 39.70762659, -119.99560445, 41.18462163],
    'Los Angeles': [-118.94473688, 32.79821787, -117.64626902, 34.82326884],
    'Madera': [-120.54535559, 36.76290957, -119.02313702, 37.77824405],
    'Marin': [-123.02454720, 37.81434498, -122.35271529, 38.32116119],
    'Mariposa': [-120.39543630, 37.18302862, -119.30916114, 37.90278231],
    'Mendocino': [-124.02304087, 38.75798088, -122.81767857, 40.00203171],
    'Merced': [-121.24761545, 36.74041903, -120.05247704, 37.63351397],
    'Modoc': [-121.45733566, 41.18389108, -119.99860791, 41.99770261],
    'Mono': [-119.65129170, 37.46265974, -117.83305435, 38.71421963],
    'Monterey': [-121.98121233, 35.78903942, -120.21394627, 36.91976420],
    'Napa': [-122.64680992, 38.15486635, -122.06139053, 38.86431964],
    'Nevada': [-121.27983631, 39.00521113, -120.00316950, 39.52697761],
    'Orange': [-118.11591131, 33.38695359, -117.41276683, 33.94763009],
    'Placer': [-121.48447175, 38.71121391, -120.00248410, 39.31647773],
    'Plumas': [-121.49814672, 39.59728718, -120.09904721, 40.44953710],
    'Riverside': [-117.67631999, 33.42595837, -114.43492273, 34.08010291],
    'Sacramento': [-121.86280525, 38.01826995, -121.02708001, 38.73635417],
    'San Benito': [-121.64390644, 36.19676935, -120.59665891, 36.98889695],
    'San Bernardino': [-117.80270608, 33.87100430, -114.13077973, 35.80925465],
    'San Diego': [-117.59618783, 32.53428490, -116.08103175, 33.50539079],
    'San Francisco': [-123.10831309, 37.69318221, -122.28148009, 37.92820082],
    'San Joaquin': [-121.58486555, 37.48190337, -120.91703421, 38.30012427],
    'San Luis Obispo': [-121.34814635, 34.89751703, -119.47262333, 35.79522760],
    'San Mateo': [-122.52582244, 37.10664650, -122.08170059, 37.70830103],
    'Santa Barbara': [-120.67308089, 33.46314654, -119.02754553, 35.11466474],
    'Santa Clara': [-122.20265825, 36.89311358, -121.20829193, 37.48463353],
    'Santa Cruz': [-122.31756095, 36.84559289, -121.58152181, 37.28548653],
    'Shasta': [-123.06905637, 40.28542875, -121.31956590, 41.18540519],
    'Sierra': [-121.05816357, 39.39131235, -120.00115691, 39.77689314],
    'Siskiyou': [-123.71921666, 40.99216151, -121.44597247, 42.00950135],
    'Solano': [-122.40704233, 38.03190147, -121.59328788, 38.54031072],
    'Sonoma': [-123.53409675, 38.06945545, -122.34969676, 38.85265626],
    'Stanislaus': [-121.48508015, 37.13465560, -120.38777967, 38.07751340],
    'Sutter': [-121.94803192, 38.73464395, -121.41457683, 39.30570925],
    'Tehama': [-123.06606980, 39.79740002, -121.34202780, 40.44616085],
    'Trinity': [-123.62375901, 39.97696451, -122.44579472, 41.36855813],
    'Tulare': [-119.57337697, 35.78670323, -117.98078853, 36.75315532],
    'Tuolumne': [-120.65310289, 37.63351397, -119.19950790, 38.43587454],
    'Ventura': [-119.57884548, 33.21442311, -118.63248588, 34.90117361],
    'Yolo': [-122.42292975, 38.31334133, -121.50117107, 38.92599413],
    'Yuba': [-121.63634257, 38.91834060, -121.00962750, 39.63941541]
}



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

