# urls for main layer 
ca_parquet = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30cbn_newlyprotected.parquet'
ca_pmtiles = 'https://minio.carlboettiger.info/public-ca30x30/ca30x30cbn_newlyprotected.pmtiles'
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
source_layer_name = re.sub(r'\W+', '', os.path.splitext(os.path.basename(ca_pmtiles))[0]) #stripping hyphens to get layer name 

#vector data 
url_ACE_rarerank_statewide = get_url('ACE_biodiversity/ACE_rarerank_statewide','ACE_rarerank_statewide.pmtiles')
url_ACE_rarerank_ecoregion = get_url('ACE_biodiversity/ACE_rarerank_ecoregion','ACE_rarerank_ecoregion.pmtiles')
url_ACE_biorank_statewide = get_url('ACE_biodiversity/ACE_biorank_statewide','ACE_biorank_statewide.pmtiles')
url_ACE_biorank_ecoregion = get_url('ACE_biodiversity/ACE_biorank_ecoregion','ACE_biorank_ecoregion.pmtiles')

url_ACE_amph_richness = get_url('ACE_biodiversity/ACE_amphibian_richness','ACE_amphibian_richness.pmtiles')
url_ACE_reptile_richness = get_url('ACE_biodiversity/ACE_reptile_richness','ACE_reptile_richness.pmtiles')
url_ACE_bird_richness = get_url('ACE_biodiversity/ACE_bird_richness','ACE_bird_richness.pmtiles')
url_ACE_mammal_richness = get_url('ACE_biodiversity/ACE_mammal_richness','ACE_mammal_richness.pmtiles')
url_ACE_rare_amph_richness = get_url('ACE_biodiversity/ACE_rare_amphibian_richness','ACE_rare_amphibian_richness.pmtiles')
url_ACE_rare_reptile_richness = get_url('ACE_biodiversity/ACE_rare_reptile_richness','ACE_rare_reptile_richness.pmtiles')
url_ACE_rare_bird_richness = get_url('ACE_biodiversity/ACE_rare_bird_richness','ACE_rare_bird_richness.pmtiles')
url_ACE_rare_mammal_richness = get_url('ACE_biodiversity/ACE_rare_mammal_richness','ACE_rare_mammal_richness.pmtiles')
url_ACE_end_amph_richness = get_url('ACE_biodiversity/ACE_endemic_amphibian_richness','ACE_endemic_amphibian_richness.pmtiles')
url_ACE_end_reptile_richness = get_url('ACE_biodiversity/ACE_endemic_reptile_richness','ACE_endemic_reptile_richness.pmtiles')
url_ACE_end_bird_richness = get_url('ACE_biodiversity/ACE_endemic_bird_richness','ACE_endemic_bird_richness.pmtiles')
url_ACE_end_mammal_richness = get_url('ACE_biodiversity/ACE_endemic_mammal_richness','ACE_endemic_mammal_richness.pmtiles')

url_wetlands = get_url('Freshwater_resources/Wetlands','CA_wetlands.pmtiles')
url_fire = get_url('Climate_risks/Historical_fire_perimeters','calfire_2023.pmtiles')
url_farmland = get_url('NBS_agriculture/Farmland_all/Farmland','Farmland_2018.pmtiles')
url_grazing = get_url('NBS_agriculture/Farmland_all/Lands_suitable_grazing','Grazing_land_2018.pmtiles')
url_DAC = get_url('Progress_data_new_protection/DAC','DAC_2022.pmtiles')
url_low_income = get_url('Progress_data_new_protection/Low_income_communities','low_income_CalEnviroScreen4.pmtiles')

# raster data
url_climate_zones = get_url('Climate_zones', 'climate_zones_10_processed_COG.tif')
url_habitat = get_url('Habitat', 'CWHR13_2022_processed_COG.tif')
url_plant_richness = get_url('Biodiversity_unique/Plant_richness', 'species_D_80percentile_processed_COG.tif')
url_endemic_plant_richness = get_url('Biodiversity_unique/Rarityweighted_endemic_plant_richness', 'endemicspecies_E_80percentile_processed_COG.tif')
url_resilient_conn_network = get_url('Connectivity_resilience/Resilient_connected_network_allcategories', 
                                 'rcn_wIntactBioCat_caOnly_2020-10-27_processed_COG.tif')

# column names for all data layers 
keys = [
    "update_newly_protected", "update_increased_management", "update_data_improvement",
    "ACE_amphibian_richness", "ACE_reptile_richness", "ACE_bird_richness",
    "ACE_mammal_richness", "ACE_rare_amphibian_richness", "ACE_rare_reptile_richness",
    "ACE_rare_bird_richness", "ACE_rare_mammal_richness", "ACE_endemic_amphibian_richness",
    "ACE_endemic_reptile_richness", "ACE_endemic_bird_richness", "ACE_endemic_mammal_richness",
    "plant_richness", "rarityweighted_endemic_plant_richness", "wetlands", "farmland", "grazing",
    "DAC", "low_income", "fire"]

chatbot_toggles = {key: False for key in keys}

# data layers dict 
layer_config = [
    #[(section, 'a_amph', [(col_name, full name, key, chatbot toggle key, citation)])]
    ('📈 Data Updates', 'a_new', [
        ('update_newly_protected', 'Newly Protected', keys[0], chatbot_toggles[keys[0]],None),
        ('update_increased_management', 'Increased Management', keys[1], chatbot_toggles[keys[1]],None),
        ('update_data_improvement', 'Data Improvement', keys[2], chatbot_toggles[keys[2]], None),
    ]),
    ('🐸 Amphibian', 'a_amph', [
        ('amphibian_richness', 'Amphibian Richness', keys[3], chatbot_toggles[keys[3]], 'Ref #5'),
        ('rare_amphibian_richness', 'Rare Amphibian Richness', keys[4], chatbot_toggles[keys[4]], 'Ref #5'),
        ('endemic_amphibian_richness', 'Endemic Amphibian Richness', keys[5], chatbot_toggles[keys[5]], 'Ref #5'),
    ]),
    ('🐍 Reptile', 'a_rept', [
        ('reptile_richness', 'Reptile Richness', keys[6], chatbot_toggles[keys[6]], 'Ref #5'),
        ('rare_reptile_richness', 'Rare Reptile Richness', keys[7], chatbot_toggles[keys[7]], 'Ref #5'),
        ('endemic_reptile_richness', 'Endemic Reptile Richness', keys[8], chatbot_toggles[keys[8]], 'Ref #5'),
    ]),
    ('🦜 Bird', 'a_bird', [
        ('bird_richness', 'Bird Richness', keys[9], chatbot_toggles[keys[9]], 'Ref #5'),
        ('rare_bird_richness', 'Rare Bird Richness', keys[10], chatbot_toggles[keys[10]], 'Ref #5'),
        ('endemic_bird_richness', 'Endemic Bird Richness', keys[11], chatbot_toggles[keys[11]], 'Ref #5'),
    ]),
    ('🦌 Mammal', 'a_mammal', [
        ('mammal_richness', 'Mammal Richness', keys[12], chatbot_toggles[keys[12]], 'Ref #5'),
        ('rare_mammal_richness', 'Rare Mammal Richness', keys[13], chatbot_toggles[keys[13]], 'Ref #5'),
        ('endemic_mammal_richness', 'Endemic Mammal Richness', keys[14], chatbot_toggles[keys[14]], 'Ref #5'),
    ]),
    ('🌿 Plant', 'a_plant', [
        ('plant_richness', 'Plant Richness', keys[15], chatbot_toggles[keys[15]], 'Ref #6'),
        ('rarityweighted_endemic_plant_richness', 'Rarity-Weighted\nEndemic Plant Richness', keys[16], chatbot_toggles[keys[16]], 'Ref #6'),
    ]),
    ('💧 Freshwater Resources', 'freshwater', [
        ('wetlands', 'Wetlands', keys[17], chatbot_toggles[keys[17]], 'Ref #7'),
    ]),
    ('🚜 Agriculture', 'agriculture', [
        ('farmland', 'Farmland', keys[18], chatbot_toggles[keys[18]], 'Ref #8'),
        ('grazing', 'Lands Suitable for Grazing', keys[19], chatbot_toggles[keys[19]], 'Ref #8'),
    ]),
    ('👤 People', 'SVI', [
        ('DAC', 'Disadvantaged Communities', keys[20], chatbot_toggles[keys[20]], 'Ref #9'),
        ('low_income', 'Low-Income Communities', keys[21], chatbot_toggles[keys[21]], 'Ref #10'),
    ]),
    ('🔥 Climate Risks', 'calfire', [
        ('fire', 'Historical Fire Perimeters', keys[22], chatbot_toggles[keys[22]], 'Ref #11'),
    ])
]

# colors for plotting 
private_access_color = "#DE881E" # orange 
public_access_color = "#3388ff" # blue
tribal_color = "#BF40BF" # purple
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
    <span class='medium-font-sidebar'>
        <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' class='bi bi-github ' 
            style='height:1em;width:1em;fill:currentColor;vertical-align:-0.125em;margin-right:4px;'  
            aria-hidden='true' role='img'>
            <path d='{github_logo}'></path>
        </svg>
        <span>Source Code:</span>
        <a href='https://github.com/boettiger-lab/ca-30x30' target='_blank'>https://github.com/boettiger-lab/CBN-taskforce</a>
    </span>
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
    </style>
    """

# Maplibre styles. (should these be functions?)
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
        ['Tribal', tribal_color],
        ['Private', private_color],
        ['HOA', hoa_color],
    ],
    'default': white
}

easement = {
    'property': 'easement',
    'type': 'categorical',
    'stops': [
        ['True', private_access_color],
        ['False', public_access_color],
    ],
    'default': white
}

year = {
    'property': 'established',
    'type': 'categorical',
    'stops': [
        ['pre-2024', year2023_color],
        ['2024', year2024_color],
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
        ['Restricted Access', tribal_color],
    ],
    'default': white
}

gap = {
    'property': 'gap_code',
    'type': 'categorical',
    'stops': [
        [1, "#26633d"],
        [2, "#879647"],
        [3, "#bdcf72"],
        [4, "#6d6e6d"]
    ],
    'default': white
}

status = {
    'property': 'status',
    'type': 'categorical',
    'stops': [
        ['30x30-conserved', "#56711f"],
        ['other-conserved', "#b6ce7a"],
        ['unknown', "#e5efdb"],
        ['non-conserved', "#e1e1e1"]
        # ['non-conserved', white]

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
    ],
    'default': white
}

climate_zone = {
    'property': 'climate_zone',
    'type': 'categorical',
    'stops': [
        [1.0, "#2ca02c"],
        [2.0, "#98df8a"],
        [3.0, "#9467bd"],
        [4.0, "#17becf"],
        [5.0, "#d62728"],
        [6.0, "#ff9896"],
        [7.0, "#dbdb8d"],
        [8.0, "#bcbd22"],
        [9.0, "#c5b0d5"],
        [10.0, "#e377c2"],
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
    ],
    'default': white
}

habitat_type = {
    'property': 'habitat_type',
    'type': 'categorical',
    'stops': [
        ['Agriculture', "#2ca02c"],
        ['Conifer Forest', "#98df8a"],
        ['Conifer Woodland', "#9467bd"],
        ['Desert Shrub', "#bcbd22"],
        ['Desert Woodland', "#d62728"],
        ['Hardwood Forest', "#ff9896"],
        ['Hardwood Woodland', "#8c564b"],
        ['Herbaceous', "#f7b6d2"],
        ['Barren/Other', "#c7c7c7"],
        ['Shrub', "#aec7e8"],
        ['Wetland', "#9edae5"],
        ['Water', "#17becf"],
        ['Urban', "#ffbb78"],
    ],
    'default': white
}

networks = {
    'property': 'resilient_connected_network',
    'type': 'categorical',
    'stops': [
        [110, "#54a0f7"],
        [103, "#72b3fd"],
        [1010, "#6b9ad3"],
        [1100, "#a2b0d5"],
        [1110, "#bfd1ff"],
        [10000, "#a87001"],
        [10010, "#d09514"],
        [20000, "#ffa807"],
        [20010, "#fed087"],
        [30000, "#88cc6a"],
        [30010, "#257202"],
        [40000, "#e377c2"],
        [0, "#ffffff"],
    ],
    'default': white
}

update_type_style = {
        "version": 8,
        "sources": {"ca": {"type": "vector", "url": f"pmtiles://{ca_pmtiles}"}},
        "layers": [
            {
                "id": "ca30x30",
                "source": "ca",
                "source-layer": source_layer_name,
                "type": "fill",
                "paint": {
                    "fill-color": [
                        "interpolate", ["linear"], ["get", "update_newly_protected"],
                        0, white,
                        1, purple
                    ]
                }
            }
        ]
    }

 



style_options = {
    "30x30 Status": status,
    "GAP Code": gap,
    "Ecoregion": ecoregion,
    "Climate Zone": climate_zone,
    "Habitat Type": habitat_type,
    "Resilient & Connected Network": networks,
    "Manager Type": manager,
    "Easement": easement,
    # "Year": year,
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
    "Easement": "easement",
    # "Year": "established",
    "Access Type": "access_type",
}

select_colors = {
    "30x30 Status": status["stops"],
    "GAP Code": gap["stops"],
    # "Year": year["stops"],
    "Ecoregion": ecoregion["stops"],
    "Climate Zone": climate_zone["stops"],
    "Habitat Type": habitat_type["stops"],
    "Manager Type": manager["stops"],
    "Easement": easement["stops"],
    "Access Type": access["stops"],
    "Resilient & Connected Network": networks["stops"],

}

from langchain_openai import ChatOpenAI
import streamlit as st
# from langchain_openai.chat_models.base import BaseChatOpenAI

## dockerized streamlit app wants to read from os.getenv(), otherwise use st.secrets
import os
api_key = os.getenv("NRP_API_KEY")
if api_key is None:
    api_key = st.secrets["NRP_API_KEY"]

llm_options = {
    # "llama-3.3-quantized": ChatOpenAI(model = "cirrus", api_key=st.secrets['CIRRUS_LLM_API_KEY'], base_url = "https://llm.cirrus.carlboettiger.info/v1",  temperature=0),
    "llama3.3": ChatOpenAI(model = "llama3-sdsc", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "gemma3": ChatOpenAI(model = "gemma3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    # "DeepSeek-R1-Distill-Qwen-32B": BaseChatOpenAI(model = "DeepSeek-R1-Distill-Qwen-32B", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    "watt": ChatOpenAI(model = "watt", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
    # "phi3": ChatOpenAI(model = "phi3", api_key=api_key, base_url = "https://llm.nrp-nautilus.io/",  temperature=0),
}


