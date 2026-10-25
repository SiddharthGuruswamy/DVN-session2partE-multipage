import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(
    page_title="Mapping Demo",
    page_icon="🌍",
)

st.title("Mapping Demo")
st.write(
    "Explore the tutorial's San Francisco Bay Area "
    "transport data. Toggle layers in the sidebar."
)

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "streamlit/example-data/master/hello/v1/"
)


@st.cache_data
def load_data(filename):
    return pd.read_json(BASE_URL + filename)


try:
    bikes = load_data("bike_rental_stats.json")
    stops = load_data("bart_stop_stats.json")
    paths = load_data("bart_path_stats.json")
except Exception as error:
    st.error(f"Could not load the map data: {error}")
    st.stop()

layers = {
    "Bike rentals": pdk.Layer(
        "HexagonLayer",
        data=bikes,
        get_position=["lon", "lat"],
        radius=200,
        elevation_scale=4,
        elevation_range=[0, 1000],
        extruded=True,
        pickable=True,
    ),
    "BART station exits": pdk.Layer(
        "ScatterplotLayer",
        data=stops,
        get_position=["lon", "lat"],
        get_color=[200, 30, 0, 160],
        get_radius="exits",
        radius_scale=0.05,
        pickable=True,
    ),
    "BART station names": pdk.Layer(
        "TextLayer",
        data=stops,
        get_position=["lon", "lat"],
        get_text="name",
        get_color=[30, 30, 30, 220],
        get_size=13,
        get_alignment_baseline="'bottom'",
    ),
    "Outbound flow": pdk.Layer(
        "ArcLayer",
        data=paths,
        get_source_position=["lon", "lat"],
        get_target_position=["lon2", "lat2"],
        get_source_color=[200, 30, 0, 160],
        get_target_color=[200, 30, 0, 160],
        get_width="outbound",
        width_scale=0.0001,
        width_min_pixels=3,
        width_max_pixels=30,
        auto_highlight=True,
        pickable=True,
    ),
}

st.sidebar.subheader("Map layers")

selected_layers = [
    layer
    for name, layer in layers.items()
    if st.sidebar.checkbox(name, value=True)
]

if selected_layers:
    deck = pdk.Deck(
        map_style=(
            "https://basemaps.cartocdn.com/"
            "gl/positron-gl-style/style.json"
        ),
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=selected_layers,
    )
    st.pydeck_chart(deck)
else:
    st.info("Select at least one map layer.")

st.caption("Source: Streamlit tutorial example datasets.")
