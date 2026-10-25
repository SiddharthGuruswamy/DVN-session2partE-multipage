import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DataFrame Demo",
    page_icon="📊",
)

st.title("DataFrame Demo")
st.write(
    "Compare gross agricultural production for "
    "countries in the tutorial dataset."
)


@st.cache_data
def load_data():
    url = (
        "https://streamlit-demo-data.s3-us-west-2."
        "amazonaws.com/agri.csv.gz"
    )
    return pd.read_csv(url).set_index("Region")


try:
    df = load_data()
except Exception as error:
    st.error(f"Could not load agricultural data: {error}")
    st.stop()

defaults = [
    country
    for country in ["China", "United States of America"]
    if country in df.index
]

countries = st.multiselect(
    "Choose countries",
    options=df.index.tolist(),
    default=defaults,
)

if not countries:
    st.info("Choose at least one country.")
    st.stop()

selected = df.loc[countries].copy() / 1_000_000.0

st.subheader("Gross agricultural production ($ billions)")
st.dataframe(selected.sort_index())

long_data = (
    selected.T
    .rename_axis("Year")
    .reset_index()
    .melt(
        id_vars="Year",
        var_name="Country",
        value_name="Production",
    )
)

long_data["Year"] = pd.to_datetime(
    long_data["Year"].astype(str),
    format="%Y",
)

chart = alt.Chart(long_data).mark_area(
    opacity=0.3
).encode(
    x=alt.X("Year:T", title="Year"),
    y=alt.Y(
        "Production:Q",
        title="Gross agricultural production ($ billions)",
        stack=None,
    ),
    color=alt.Color("Country:N", title="Country"),
    tooltip=[
        "Country:N",
        alt.Tooltip("Year:T", format="%Y"),
        alt.Tooltip("Production:Q", format=",.2f"),
    ],
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

st.caption(
    "Source: UN Data, distributed through the "
    "Streamlit tutorial dataset."
)
