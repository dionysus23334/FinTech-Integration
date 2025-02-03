
import streamlit as st
import pandas as pd
import time
import numpy as np

# Assuming your data is in a pandas DataFrame
# Example: DataFrame with custom data
data = pd.DataFrame({
    # 'x': np.arange(100),
    'y': np.random.randn(100).cumsum()  # Just an example of random data
})

st.write(data)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

# Initially show the first row (or any initial data)
last_rows = data.iloc[:1, :]
chart = st.line_chart(last_rows)

for i in range(1, len(data) + 1):
    # Get the next set of rows (instead of generating random data)
    new_rows = data.iloc[:i, :]
    
    status_text.text(f"{i}% Complete")
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
