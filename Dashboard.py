import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_autorefresh import st_autorefresh
import time
from googleapiclient.errors import HttpError
import google.auth.exceptions
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import datetime

st.set_page_config(layout="wide")


#=== Timestamp variables ==
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]
credentials = Credentials.from_service_account_info(
    st.secrets["simiana"], scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)
file_id = "1-tD1JEvzrNbQ3cEnLKm0EkJEy-t6g1eeHobuVN5D2E0"


creds_path = "simi-takeover.json"
sheet_name = "IA Practice"

# === Auto-refresh every 5 minutes (300 seconds) ===
st_autorefresh(interval=300_000, key="auto_refresh")



# === Load data from Google Sheets ===
@st.cache_data(ttl=120)  # cache for 2 min for fresh data
def load_all_induct_data_batch(sheet_name, worksheet_names, max_retries=5):
    # Use credentials to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Directly access Streamlit secrets and parse them as JSON
    credentials_dict = st.secrets["simiana"]  
    
    # Authenticate using the credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)

    
    sh = client.open(sheet_name)
    
    ranges = []
    for ws_name in worksheet_names:
        ws = sh.worksheet(ws_name)
        last_row = ws.row_count
        last_col_letter = chr(64 + ws.col_count)
        ranges.append(f"'{ws_name}'!A1:{last_col_letter}{last_row}")

    attempt = 0
    while attempt < max_retries:
        try:
            batch_data = sh.values_batch_get(ranges)
            break  # success, exit loop
        except (HttpError, google.auth.exceptions.TransportError) as e:
            wait_time = 2 ** attempt  # exponential backoff: 1,2,4,8,16s
            st.warning(f"API rate limit hit or network error, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            attempt += 1
    else:
        st.error("Failed to load data from Google Sheets after multiple retries.")
        return {ws_name: pd.DataFrame() for ws_name in worksheet_names}
    
    data_dict = {}
    for ws_name, values in zip(worksheet_names, batch_data["valueRanges"]):
        rows = values.get("values", [])
        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0])
            df["Utilization %"] = pd.to_numeric(df["Value"], errors="coerce")
            df.dropna(subset=["Serialization", "Utilization %"], inplace=True)
            data_dict[ws_name] = df
        else:
            data_dict[ws_name] = pd.DataFrame()

    return data_dict
    
# === Define worksheet names ===
worksheet_names = [
    f"Induct {induct} {period}"
    for induct in range(101, 109)
    for period in ["Min", "Hour", "Day"]
]

SHEET_NAME = "IA Practice" 

# Load all data at once (this returns a dictionary of DataFrames)
all_data = load_all_induct_data_batch(SHEET_NAME, worksheet_names)

@st.cache_data(ttl=120)
def get_sheet_last_modified_time(file_id):
    try:
        file = drive_service.files().get(fileId=file_id, fields='modifiedTime').execute()
        return file.get('modifiedTime')
    except Exception as e:
        st.error(f"Error fetching last modified time: {e}")
        return None
    
# === Streamlit layout ===
st.title(":package: LCY3 AFE Induct Data Monitor :package:")
st.caption("Auto-refreshes every 5 minutes. Data is cached every 2 minutes.")

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

last_modified_iso = get_sheet_last_modified_time(file_id)
if last_modified_iso:
    last_modified_dt = datetime.datetime.fromisoformat(last_modified_iso.replace("Z", "+00:00"))
    st.caption(f"📅 Data last updated on: {last_modified_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
else:
    st.caption("📅 Last update time not available.")

# Make sure all the tabs span the width of the page and arent squashed
st.markdown("""
    <style>
    div[data-baseweb="tab-list"] {
        flex-wrap: wrap; /* Allows wrapping if too many tabs */
        justify-content: space-evenly; /* Evenly spread across width */
    }
    </style>
""", unsafe_allow_html=True)


# === Tabs for each induct ===
tabs = st.tabs([f"Induct {i}" for i in range(101, 109)])

# === Formatting the formatting ===
custom_colors_categorical = {'Combi_util': 'hotpink', 'Tote_util': 'orange', 'Tray_util': 'lightblue'}

# === Plot the data for each induct and timeframe ===
for idx, induct_num in enumerate(range(101, 109)):
    with tabs[idx]:
        st.subheader(f"📊 Induct {induct_num}")
        for period, title in [("Min", "Minute"), ("Hour", "Hourly"), ("Day", "Daily")]:
            df = all_data.get(f"Induct {induct_num} {period}", pd.DataFrame())
            if df.empty:
                st.info(f"No data found for Induct {induct_num} {period}")
                continue

            fig = px.line(
                df,
                x="Serialization",
                y="Utilization %",
                color="Category",
                color_discrete_map=custom_colors_categorical,
                markers=toggle_markers,
                text=text_markers,
                title=f"Induct {induct_num} {title} analysis"
            )
            fig.update_layout(legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"))
            st.plotly_chart(fig, use_container_width=True)


































