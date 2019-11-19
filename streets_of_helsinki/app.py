import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache(allow_output_mutation=True)
def load_data():
    url = (
        "https://kartta.hel.fi/ws/geoserver/avoindata/wfs?"
        "version=1.0.0&"
        "request=GetFeature&"
        "typeName=avoindata:YLRE_Katualue_alue"
    )
    data = gpd.read_file(url)
    data = data.loc[~(data["luokka"] == "Kaavoittamaton")]
    data = data.assign(category=data["kadun_nimi"].apply(get_category))

    return data


@st.cache
def get_category(k):
    for cat in [
        "kuja",
        "katu",
        "tie",
        "polku",
        "kaari",
        "ranta",
        "rinne",
        "väylä",
        "mäki",
        "kaarre",
        "raitti",
        "laituri",
        "laita",
        "linja",
        "tori",
        "aukio",
        "pää",
        "penger",
        "portti",
        "silta",
        "kierto",
    ]:
        if k.lower().endswith(cat):
            return cat


st.set_page_config(
    page_title="Streets of Helsinki",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="auto",
)

data = load_data()
for filter in ["suurpiiri", "kaupunginosa", "osa_alue"]:
    selected = st.sidebar.selectbox(
        filter.replace("_", "-").capitalize(),
        [None] + list(sorted(data[filter].unique())),
    )
    if selected == None:
        break
    data = data.loc[data[filter] == selected]

all_categories = (
    data.groupby("category")
    .apply(lambda group: group["kadun_nimi"].nunique())
    .rename("count")
    .sort_values(ascending=False)
    .to_frame()
)

top_categories = (
    pd.concat(
        [all_categories.reset_index(), pd.Series(plt.cm.tab10.colors, name="colors")],
        axis=1,
    )
    .set_index("category")
    .dropna()
)

inds_other_categories = ~data["category"].isin(top_categories.index)
data.loc[inds_other_categories, "category"] = "muu"
top_categories.loc["muu"] = (
    data.loc[inds_other_categories, "kadun_nimi"].nunique(),
    (0.8, 0.8, 0.8),
)

fig, ax = plt.subplots(figsize=(20, 20))
ax2 = plt.axes([1, 0.3, 0.1, 0.4])
for num, (name, (count, color)) in enumerate(top_categories.iterrows()):
    data.loc[data["category"] == name, "geometry"].plot(ax=ax, color=color)
    ax2.barh(num, count, color=color)
    ax2.text(0, num, f"{name.capitalize()}", ha="right", va="center", fontsize=12)
    ax2.text(count, num, f"{count:.0f}", ha="left", va="center", fontsize=12)
    ax2.set_ylim([11, -1])
ax.axis("scaled")
ax.axis("off")
ax2.axis("off")
fig.tight_layout()
print(ax)
st.pyplot(fig)
