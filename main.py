import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("F:\PythonProject\pythonProject\StreamlitApp\quarterly_canada_population.csv")

st.title("Canada Dataset Preview")
st.divider()
st.markdown("Source table can be found [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")
with st.expander("Click to view dataframe"):
  st.dataframe(df)

st.divider()

with st.form("population-form"):
    col1, col2, col3 = st.columns(3,border=True)

    with col1 :
        st.write("choose the start date")
        start_q = st.selectbox("Quarter", options=['Q1','Q2','Q3','Q4'], index=2, key='start_q')
        start_y = st.slider("Year", min_value=1991, max_value=2025, value=1992,step=1, key='start_y')

    with col2 :
        st.write("choose the end date")
        end_q = st.selectbox("Quarter", options=['Q1','Q2','Q3','Q4'], index=2, key='end_q')
        end_y = st.slider("Year", min_value=1991, max_value=2025, value=1992,step=1, key='end_y')

    with col3 :
        st.write("choose location")
        loc = st.selectbox("location", options=df.columns[1:], index=0, key="loc")

    st.form_submit_button("calculate", type="primary")

start_date = f"{start_q} {start_y}"
end_date = f"{end_q} {end_y}"

def format_date_for_comparison(date):
    if date[1] == 2:
        return float(date[2:]) + 0.25
    elif date[1] == 3:
        return float(date[2:]) + 0.50
    elif date[1] == 4:
        return float(date[2:]) + 0.75
    else:
        return float(date[2:])

def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

def display_dashboard(start_date, end_date, target):
    tab1, tab2 = st.tabs(["Population change", "Compare"])

    with tab1:
        st.subheader(f"Population change from {start_date} to {end_date}")

        col1, col2 = st.columns(2)

        with col1:
            initial = df.loc[df['Quarter'] == start_date, target].item()
            final = df.loc[df['Quarter'] == end_date, target].item()

            percentage_diff = round((final - initial) / initial * 100, 2)
            delta = f"{percentage_diff}%"
            st.metric(start_date, value=initial)
            st.metric(end_date, value=final, delta=delta)

        with col2:
            start_idx = df.loc[df['Quarter'] == start_date].index.item()
            end_idx = df.loc[df['Quarter'] == end_date].index.item()
            filtered_df = df.iloc[start_idx: end_idx+1]

            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)

    with tab2:
        st.subheader('Compare with other locations')
        all_targets = st.multiselect("Choose other locations", options=filtered_df.columns[1:], default=[target])

        fig, ax = plt.subplots()
        for each in all_targets:
            ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([filtered_df['Quarter'].iloc[0], filtered_df['Quarter'].iloc[-1]])
        fig.autofmt_xdate()
        st.pyplot(fig)

if start_date not in df['Quarter'].tolist() or end_date not in df['Quarter'].tolist():
    st.error("No data available. Check your quarter and year selection")
elif end_before_start(start_date, end_date):
    st.error("Dates don't work. Start date must come before end date.")
else:
    display_dashboard(start_date, end_date, loc)
