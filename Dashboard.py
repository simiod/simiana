import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(layout="wide")

creds_path = "simi-takeover.json"
sheet_name = "IA Practice"

# === Load data from Google Sheets ===
@st.cache_data(ttl=300)  # cache for 5 minutes to match auto-refresh
def load_data(sheet):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["simiana"] 
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # Ensure 'Value' is numeric
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(subset=["Serialization", "Value"], inplace=True)
    return df

# === Streamlit layout ===
st.title(":wrench: Induct Data Monitor :rocket:")
st.caption("Auto-refreshes every 5 minutes. You can also trigger a manual refresh below.")

# === Load and display data ===
induct_106_min_data = load_data("Induct 106 Min")
induct_106_hour_data = load_data("Induct 106 Hour")
induct_106_day_data = load_data("Induct 106 Day")
# === Load and display data ===
induct_105_min_data = load_data("Induct 105 Min")
induct_105_hour_data = load_data("Induct 105 Hour")
induct_105_day_data = load_data("Induct 105 Day")
tabs_1, tabs_2 = st.tabs(['Induct 105','Induct 106'])
with tabs_1:
#    st.dataframe(induct_106_min_data)
     # Show numbers at each point and use color to differentiate (optional: based on category or series name)
    #fig_1 = px.line(induct_106_min_data, x="Serialization", y="Value", markers=True, title="Minute View",
                    #text="Value")  # shows value on hover and on the chart
#    fig_2 = px.line(df_hour_plc_1, x="Serialization", y="Value", markers=True, title="Hourly View",
#                    text="Value")
#    fig_3 = px.line(df_day_plc_1, x="Serialization", y="Value", markers=True, title="Daily View",
#                    text="Value")
    # Optionally adjust appearance of the text
#    fig_1.update_traces(textposition="top center", line=dict(color="royalblue"))
#    fig_2.update_traces(textposition="top center", line=dict(color="seagreen"))
#    fig_3.update_traces(textposition="top center", line=dict(color="indianred"))
    # Display in Streamlit
    #st.plotly_chart(fig_1, use_container_width=True, key='1')
#    st.plotly_chart(fig_2, use_container_width=True, key='2')
#    st.plotly_chart(fig_3, use_container_width=True, key='3')
# Create figure
    fig_1 = px.line(induct_105_min_data, x="Serialization", y="Value", color="Category", title="Induct 105 Minute analysis")
    fig_1.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_1, use_container_width=True, key='A1' )

    fig_2 = px.line(induct_105_min_data, x="Serialization", y="Value", color="Category", title="Induct 105 Hourly analysis")
    fig_2.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_2, use_container_width=True, key='A2')

    fig_3 = px.line(induct_105_day_data, x="Serialization", y="Value", color="Category", title="Induct 105 Daily analysis")
    fig_3.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_3, use_container_width=True, key='A3')
with tabs_2:
#    st.dataframe(induct_106_min_data)
     # Show numbers at each point and use color to differentiate (optional: based on category or series name)
    #fig_1 = px.line(induct_106_min_data, x="Serialization", y="Value", markers=True, title="Minute View",
                    #text="Value")  # shows value on hover and on the chart
#    fig_2 = px.line(df_hour_plc_1, x="Serialization", y="Value", markers=True, title="Hourly View",
#                    text="Value")
#    fig_3 = px.line(df_day_plc_1, x="Serialization", y="Value", markers=True, title="Daily View",
#                    text="Value")
    # Optionally adjust appearance of the text
#    fig_1.update_traces(textposition="top center", line=dict(color="royalblue"))
#    fig_2.update_traces(textposition="top center", line=dict(color="seagreen"))
#    fig_3.update_traces(textposition="top center", line=dict(color="indianred"))
    # Display in Streamlit
    #st.plotly_chart(fig_1, use_container_width=True, key='1')
#    st.plotly_chart(fig_2, use_container_width=True, key='2')
#    st.plotly_chart(fig_3, use_container_width=True, key='3')
# Create figure
    fig_1 = px.line(induct_106_min_data, x="Serialization", y="Value", color="Category", title="Induct 106 Minute analysis")
    fig_1.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_1, use_container_width=True, key='1' )

    fig_2 = px.line(induct_106_min_data, x="Serialization", y="Value", color="Category", title="Induct 106 Hourly analysis")
    fig_2.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_2, use_container_width=True, key= '2')

    fig_3 = px.line(induct_106_day_data, x="Serialization", y="Value", color="Category", title="Induct 106 Daily analysis")
    fig_3.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_3, use_container_width=True, key='3')






























