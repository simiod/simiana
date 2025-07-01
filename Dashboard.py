import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

creds_path = "simi-takeover.json"
sheet_name = "IA Practice"

# === Auto-refresh every 5 minutes (300 seconds) ===
st_autorefresh(interval=300_000, key="auto_refresh")

# === Load data from Google Sheets ===
@st.cache_data(ttl=300)  # cache for 5 minutes to match auto-refresh
def load_data(sheet):
    # Use credentials to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["simiana"]  
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    
    
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(sheet)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # Ensure 'Value' is numeric, change the name of
    df["Utilization %"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(subset=["Serialization", "Utilization %"], inplace=True)
    return df

# === Streamlit layout ===
st.title(":wrench: Induct Data Monitor :rocket:")
st.caption("Auto-refreshes every 5 minutes. You can also trigger a manual refresh below.")

# === Manual Refresh Button ===
if st.button("🔄 Manual Refresh"):
    st.cache_data.clear()
    st.rerun()

# === Create toggle button for value marker annotations ===
text_markers = None
toggle_markers= st.toggle("Display Values", value=True, key='B1', help="Turn **on/off** utilization % value markers for a neater display", disabled=False, label_visibility="visible")
if toggle_markers:         
    text_markers = "Utilization %"
    markers = True

# === Load and display data ===
induct_106_min_data = load_data("Induct 106 Min")
induct_106_hour_data = load_data("Induct 106 Hour")
induct_106_day_data = load_data("Induct 106 Day")
# === Load and display data ===
induct_105_min_data = load_data("Induct 105 Min")
induct_105_hour_data = load_data("Induct 105 Hour")
induct_105_day_data = load_data("Induct 105 Day")
tabs_1, tabs_2 = st.tabs(['Induct 105','Induct 106'])

# === Create Induct 105 ===
with tabs_1:
    custom_colors_categorical = {'Combi_util': 'hotpink', 'Tote_util': 'orange', 'Tray_util': 'lightblue'}

    fig_1 = px.line(induct_105_min_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers, title="Induct 105 Minute analysis")
    fig_1.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_1, use_container_width=True, key='A1' )

    fig_2 = px.line(induct_105_hour_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers,, title="Induct 105 Hourly analysis")
    fig_2.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_2, use_container_width=True, key='A2')

    fig_3 = px.line(induct_105_day_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers, title="Induct 105 Daily analysis")
    fig_3.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_3, use_container_width=True, key='A3')

# === Create Induct 106 ===
with tabs_2:

    fig_1 = px.line(induct_106_min_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers, title="Induct 106 Minute analysis")
    fig_1.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center            
        )

    )

    st.plotly_chart(fig_1, use_container_width=True, key='1' )

    fig_2 = px.line(induct_106_hour_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers, title="Induct 106 Hourly analysis")
    fig_2.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_2, use_container_width=True, key= '2')

    fig_3 = px.line(induct_106_day_data, x="Serialization", y="Utilization %", color="Category", color_discrete_map=custom_colors_categorical, markers= toggle_markers, text= text_markers, title="Induct 106 Daily analysis")
    fig_3.update_layout(
        legend=dict(
            orientation="h",  # Horizontal legend
            y=-0.2,  # Move legend below the graph
            x=0.5,  # Center the legend horizontally
            xanchor="center"  # Align legend to center
        )
    )
    st.plotly_chart(fig_3, use_container_width=True, key='3')






























