import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Streamlit! 👋")
st.sidebar.success("Choose a demo from the sidebar.")

st.markdown("""
This multipage app follows the official Streamlit tutorial.

Use the sidebar to explore:

- **Plotting Demo:** an animated chart of generated data.
- **Mapping Demo:** geographic data shown as selectable map layers.
- **DataFrame Demo:** agricultural production data for selected countries.

Each page has its own Python file inside the `pages/` folder.
""")

st.caption(
    "Source: Streamlit documentation, Create a multipage app."
)
