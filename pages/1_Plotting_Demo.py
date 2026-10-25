import time

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Plotting Demo",
    page_icon="📈",
)

st.title("Plotting Demo")
st.write(
    "An animated random walk demonstrates how a chart "
    "updates as new data arrives."
)
st.caption("Generated demonstration data, not real observations.")

rng = np.random.default_rng(42)

data = pd.DataFrame(
    rng.normal(size=(1, 3)),
    columns=["Series A", "Series B", "Series C"],
)

chart_area = st.empty()
progress = st.sidebar.progress(0)
status = st.sidebar.empty()

for step in range(1, 101):
    increments = rng.normal(size=(5, 3))
    new_values = (
        data.iloc[-1].to_numpy()
        + increments.cumsum(axis=0)
    )

    new_rows = pd.DataFrame(
        new_values,
        columns=data.columns,
    )

    data = pd.concat(
        [data, new_rows],
        ignore_index=True,
    )

    chart_area.line_chart(data)
    progress.progress(step)
    status.text(f"{step}% complete")
    time.sleep(0.03)

progress.empty()
status.text("Animation complete.")

st.button("Run animation again")
