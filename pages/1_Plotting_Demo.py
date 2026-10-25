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
    "can receive new rows while the app runs."
)
st.caption("Generated demonstration data, not real observations.")

rng = np.random.default_rng(42)
data = pd.DataFrame(
    rng.normal(size=(1, 3)),
    columns=["Series A", "Series B", "Series C"],
)

chart = st.line_chart(data)
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
        index=range(len(data), len(data) + 5),
    )

    data = pd.concat([data, new_rows])
    chart.add_rows(new_rows)

    progress.progress(step)
    status.text(f"{step}% complete")
    time.sleep(0.03)

progress.empty()
status.text("Animation complete.")

st.button("Run animation again")
