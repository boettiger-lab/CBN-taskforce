# urls for main layer 
ca_parquet = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30cbn_newlyprotected_v1.parquet'
ca_pmtiles = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30cbn_newlyprotected_v1.pmtiles'
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
    "pct_newly_protected", "pct_increased_management", "pct_data_improvement",
    "pct_top_amphibian_richness", "pct_rare_amphibian_richness",
    "pct_endemic_amphibian_richness",
    "pct_top_reptile_richness", "pct_rare_reptile_richness","pct_endemic_reptile_richness",
    "pct_top_bird_richness", "pct_rare_bird_richness","pct_endemic_bird_richness",
    "pct_top_mammal_richness", "pct_rare_mammal_richness","pct_endemic_mammal_richness",
    "pct_top_plant_richness", "pct_rarityweighted_endemic_plant_richness", "pct_wetlands",
    "pct_top_freshwater_richness",
    "pct_farmland", "pct_grazing_lands","pct_disadvantaged_community", "pct_low_income", "pct_fire"]

chatbot_toggles = {key: False for key in keys}

# data layers dict 
layer_config = [
    #[(section, 'a_amph', [(col_name, full name, key, chatbot toggle key, citation)])]
    ('🐸 Amphibian', 'a_amph', [
        ('pct_top_amphibian_richness', 'Amphibian Richness', keys[3], chatbot_toggles[keys[3]], 'Areas with the top 20% of amphibian richness (Reference #5)'),
        ('pct_rare_amphibian_richness', 'Rare Amphibian Richness', keys[4], chatbot_toggles[keys[4]], 'Areas with rare amphibian richness (Reference #5)'),
        ('pct_endemic_amphibian_richness', 'Endemic Amphibian Richness', keys[5], chatbot_toggles[keys[5]], 'Areas with endemic amphibian richness (Reference #5)'),
    ]),
    ('🐍 Reptile', 'a_rept', [
        ('pct_top_reptile_richness', 'Reptile Richness', keys[6], chatbot_toggles[keys[6]], 'Areas with the top 20% of reptile richness (Reference #5)'),
        ('pct_rare_reptile_richness', 'Rare Reptile Richness', keys[7], chatbot_toggles[keys[7]], 'Areas with rare reptile richness (Reference #5)'),
        ('pct_endemic_reptile_richness', 'Endemic Reptile Richness', keys[8], chatbot_toggles[keys[8]], 'Areas with endemic reptile richness (Reference #5)'),
    ]),
    ('🦜 Bird', 'a_bird', [
        ('pct_top_bird_richness', 'Bird Richness', keys[9], chatbot_toggles[keys[9]], 'Areas with the top 20% of bird richness (Reference #5)'),
        ('pct_rare_bird_richness', 'Rare Bird Richness', keys[10], chatbot_toggles[keys[10]], 'Areas with rare bird richness (Reference #5)'),
        ('pct_endemic_bird_richness', 'Endemic Bird Richness', keys[11], chatbot_toggles[keys[11]], 'Areas with endemic bird richness (Reference #5)'),
    ]),
    ('🦌 Mammal', 'a_mammal', [
        ('pct_top_mammal_richness', 'Mammal Richness', keys[12], chatbot_toggles[keys[12]], 'Areas with the top 20% of mammal richness (Reference #5)'),
        ('pct_rare_mammal_richness', 'Rare Mammal Richness', keys[13], chatbot_toggles[keys[13]], 'Areas with rare mammal richness (Reference #5)'),
        ('pct_endemic_mammal_richness', 'Endemic Mammal Richness', keys[14], chatbot_toggles[keys[14]], 'Areas with endemic mammal richness (Reference #5)'),
    ]),
    ('🌿 Plant', 'a_plant', [
        ('pct_top_plant_richness', 'Plant Richness', keys[15], chatbot_toggles[keys[15]], 'Areas with the top 20% of plant richness (Reference #6)'),
        ('pct_rarityweighted_endemic_plant_richness', 'Rarity-Weighted Endemic\n Plant Richness', keys[16], chatbot_toggles[keys[16]], 'Areas with the top 20% of rarity-weighted endemic plant richness (Reference #6)'),
    ]),
    ('💧 Freshwater Resources', 'freshwater', [
        ('pct_wetlands', 'Wetlands', keys[17], chatbot_toggles[keys[17]], 'Areas that are freshwater emergent, freshwater forested/shrub, or estuarine and marine wetlands (Reference #7)'),
        ('pct_top_freshwater_richness', 'Freshwater Species Richness', keys[18], chatbot_toggles[keys[18]], 'Areas with the top 20% of freshwater species richness (Reference #8)'),
    ]),
    ('🚜 Agriculture', 'agriculture', [
        ('pct_farmland', 'Farmland', keys[19], chatbot_toggles[keys[19]], 'Farmlands with prime, unique, or of statewide or local importance (Reference #9)'),
        ('pct_grazing_lands', 'Lands Suitable for Grazing', keys[20], chatbot_toggles[keys[20]], 'Lands suitable for grazing (Reference #9)'),
    ]),
    ('👤 People', 'SVI', [
        ('pct_disadvantaged_community', 'Disadvantaged Communities', keys[21], chatbot_toggles[keys[21]], 'Areas in disadvantaged communities (Reference #10)'),
        ('pct_low_income', 'Low-Income Communities', keys[22], chatbot_toggles[keys[22]], 'Areas in low-income communities (Reference #11)'),
    ]),
    ('🔥 Climate Risks', 'calfire', [
        ('pct_fire', 'Wildfires', keys[23], chatbot_toggles[keys[23]], 'Areas burned in the last 10 years (Reference #12)'),
    ]),
    ('📈 Data Updates', 'a_new', [
        ('pct_newly_protected', 'Newly Protected Land', keys[0], chatbot_toggles[keys[0]],'Lands that were privately-owned and unprotected and moved into conservation ownership and management'),
        ('pct_increased_management', 'Land with Increased Management', keys[1], chatbot_toggles[keys[1]],'Lands that were newly counted towards 30x30 due to increased management or durability of protection and/or retirement of extractive uses (previously GAP 3 or 4)'),
        ('pct_data_improvement', 'Land with Data Improvement', keys[2], chatbot_toggles[keys[2]],'Lands that are newly counted towards 30x30 due to additional GAP information but for which no on the ground conservation actions, policies, or management changes took place')
    ])
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
    ],
    'default': white
}

networks = {
    'property': 'resilient_connected_network',
    'type': 'categorical',
    'stops': [
        ['Resilient biodiverse', "#257202"],
        ['Additional resilient secured', "#1667f6"],
        ['Biodiverse well-connected landscape', "#6b9ad3"],
        ['Resilient well-connected landscape', "#a2b0d5"],
        ['Resilient biodiverse well-connected landscape', "#bfd1ff"],
        ['Climate migration route within well-connected landscape', "#9acb73"],
        ['Linkage', "#d09514"],
        ['Linkage and climate migration route', "#7d7121"],
        ['Coastal migration space', "#e377c2"],
        ['None', "#ffffff"],
    ],
    'default': white
}


style_options = {
    "30x30 Status": status,
    "GAP Code": gap,
    "Ecoregion": ecoregion,
    "Climate Zone": climate_zone,
    "Habitat Type": habitat_type,
    "Resilient & Connected Network": networks,
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
    "Resilient & Connected Network": "resilient_connected_network",
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
    "Resilient & Connected Network": networks["stops"],

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
- 📊 Use this sidebar to color-code the map by different attributes **(Group by)**, toggle on data layers and view summary charts **(Data Layers)**, or filter data **(Filters)**.
- 💬 For a more tailored experience, query our dataset of protected areas and their precomputed mean values for each of the displayed layers, using the experimental chatbot. The language model tries to answer natural language questions by drawing only from curated datasets (listed below).
'''

example_queries = """
Mapping queries:
- Show me protected areas with any recent additions.
- Show me amphibian biodiversity hotspots that aren't currently conserved.
- Show me protected areas in disadvantaged communities.
- Show me 30x30 conservation areas where at least 80% of the land overlaps with regions of high endemic species richness.
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

from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_openai.chat_models.base import BaseChatOpenAI

## dockerized streamlit app wants to read from os.getenv(), otherwise use st.secrets
import os
api_key = os.getenv("NRP_API_KEY")
if api_key is None:
    api_key = st.secrets["NRP_API_KEY"]

llm_options = {
    "gemma3": ChatOpenAI(model = "gemma3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "llama3": ChatOpenAI(model = "llama3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "deepseek-r1": BaseChatOpenAI(model = "deepseek-r1", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "olmo": ChatOpenAI(model = "olmo", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "qwen3": ChatOpenAI(model = "qwen3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
}

