import streamlit as st
import requests

# --- 1. SETUP & CONFIG ---
API_KEY = "701fe347-07c1-48a5-ab52-834e2cdf6f07
"  # <--- PASTE YOUR KEY FROM CRICKETDATA.ORG HERE
BASE_URL = "https://api.cricapi.com/v1"

st.set_page_config(page_title="WillowMind AI", page_icon="🏏", layout="wide")

# Custom Styling to make it look like an App
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN (API FUNCTIONS) ---
def fetch_data(endpoint, params=""):
    url = f"{BASE_URL}/{endpoint}?apikey={API_KEY}{params}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

# --- 3. THE INTERFACE ---
st.title("🏏 WillowMind: Professional Cricket AI")

# Create two tabs: One for Search, one for Live Scores
tab1, tab2 = st.tabs(["🔍 Search Stats", "🔴 Live Matches"])

with tab1:
    st.header("Search Player Archives")
    query = st.text_input("Enter Player Name:", placeholder="e.g. MS Dhoni")
    
    if query:
        with st.spinner('Accessing database...'):
            # Step A: Search for Player ID
            search = fetch_data("players", f"&offset=0&search={query}")
            
            if search and search.get("data"):
                player = search["data"][0]
                pid = player["id"]
                
                # Step B: Get Full Details using ID
                details = fetch_data("players_info", f"&id={pid}")
                info = details.get("data", {})
                
                # Step C: Show the Results
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(info.get('playerImg', 'https://via.placeholder.com/150'), width=200)
                with col2:
                    st.subheader(info.get('name'))
                    st.write(f"**Country:** {info.get('country')}")
                    st.write(f"**Role:** {info.get('role')}")
                    st.write(f"**Style:** {info.get('battingStyle')} / {info.get('bowlingStyle')}")
                
                # Show Stats Table
                if info.get('stats'):
                    st.write("---")
                    st.write("### Career Stats")
                    st.table(info['stats'])
            else:
                st.error("No player found. Try the full name.")

with tab2:
    st.header("Live Scoreboard")
    if st.button("Refresh Scores"):
        live = fetch_data("currentMatches", "&offset=0")
        if live and live.get("data"):
            for match in live["data"]:
                with st.expander(f"{match['name']} - {match['status']}"):
                    st.write(f"**Venue:** {match['venue']}")
                    if match.get('score'):
                        for s in match['score']:
                            st.info(f"{s['inning']}: {s['r']}/{s['w']} ({s['o']} overs)")
        else:
            st.write("No live matches at the moment.")

st.sidebar.markdown("### About WillowMind")
st.sidebar.info("This AI app is connected directly to the CricketData API for real-time 2026 updates.")
