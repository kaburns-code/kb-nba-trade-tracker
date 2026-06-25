import streamlit as st
from utils.claude_client import stream_response
 
SYSTEM = """You are an NBA salary cap and trade expert. Use real salary data from basketball-reference.com. 
Apply NBA trade rules accurately. Be specific with dollar amounts and contract details.
Never fabricate player salaries — search for real current figures."""
 
NBA_TEAMS = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
    "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
    "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
    "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
    "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards"
]
 
 
def render():
    st.markdown('<p class="section-label">Salary-Compatible Trade Partner Finder</p>', unsafe_allow_html=True)
    st.write("Search by player or team to find salary-matching trade candidates across the league.")
 
    mode = st.radio("Search by:", ["Player", "Team"], horizontal=True)
 
    if mode == "Player":
        col1, col2 = st.columns([2, 1])
        with col1:
            player_name = st.text_input("Player name", placeholder="e.g. Jaylen Brown, Zion Williamson")
        with col2:
            flexibility = st.selectbox("Salary flexibility", ["Exact match (±10%)", "Flexible (±25%)", "Wide (±40%)"])
 
        include_picks = st.checkbox("Include pick sweeteners in analysis", value=True)
 
        if st.button("🔍 Find Trade Matches", use_container_width=True, disabled=not player_name if mode == "Player" else False):
            flex_map = {"Exact match (±10%)": "within 10%", "Flexible (±25%)": "within 25%", "Wide (±40%)": "within 40%"}
            flex_str = flex_map[flexibility]
 
            prompt = f"""Search basketball-reference.com for the current salary and contract details for {player_name}.
 
Then find 6-8 NBA players from different teams with salaries {flex_str} of {player_name}'s salary who would be trade-eligible matches.
 
For each match provide:
 
### [Player Name] — [Team]
- **Salary:** $XX.XM (20XX-XX season)
- **Contract:** X years remaining [note any player option, team option, or ETO]
- **Trade math:** [Show that salaries match under NBA rules]
- **Why this works:** [1-2 sentences on basketball fit and why both teams might want this]
- **Complication:** [Any no-trade clause, injury history, or cap issue to flag]
 
After the player matches, add a section:
 
### 🏀 Package Deals
Suggest 2-3 multi-player packages (smaller contracts + picks) that would also match {player_name}'s salary.
 
{"Also note what first-round picks from each team are currently available/unprotected." if include_picks else ""}
 
Use real 2025-26 salary data only."""
 
            placeholder = st.empty()
            with st.spinner(f"Finding salary matches for {player_name}..."):
                stream_response(prompt, placeholder, system=SYSTEM)
 
    else:  # Team mode
        col1, col2 = st.columns([2, 1])
        with col1:
            team_name = st.selectbox("Select team", NBA_TEAMS)
        with col2:
            focus = st.selectbox("Focus on", ["All tradeable players", "Max contracts only", "Expiring contracts", "Young players (U25)"])
 
        target_team = st.selectbox("Find matches with (optional)", ["Any team"] + [t for t in NBA_TEAMS if t != team_name])
 
        if st.button("🔍 Analyze Team's Trade Options", use_container_width=True):
            focus_map = {
                "All tradeable players": "all players on tradeable contracts",
                "Max contracts only": "max or near-max salary players",
                "Expiring contracts": "players in the final year of their contract (expiring)",
                "Young players (U25)": "players under 25 years old"
            }
            target_str = f"focusing on potential trades with the {target_team}" if target_team != "Any team" else "across all 29 other teams"
 
            prompt = f"""Search basketball-reference.com for the {team_name}'s current roster and salary data.
 
Identify their {focus_map[focus]} and analyze their trade options {target_str}.
 
First, give a quick **Cap Snapshot** for the {team_name}:
- Total payroll
- Luxury tax position
- Key contract details (top 5 salaries)
- Available trade exceptions if any
 
Then for each key tradeable player, show:
 
### [Player Name] — ${'{'}salary{'}'} — X yrs remaining
**Could get back:** List 3-4 specific players from other teams with matching salaries
**Best realistic fit:** [Your top recommendation with reasoning]
**Cap impact of trading them:** [What it does to the team's cap situation]
 
{"Specifically focus on trade possibilities with the " + target_team + " and show detailed salary matching between the two teams." if target_team != "Any team" else ""}
 
End with a **Trade Priority Ranking** — which player should the {team_name} move first and why."""
 
            placeholder = st.empty()
            with st.spinner(f"Analyzing {team_name} trade options..."):
                stream_response(prompt, placeholder, system=SYSTEM)
 
    st.divider()
 
    # Quick reference cap rules
    with st.expander("📋 NBA Trade Rules Reference"):
        st.markdown("""
**Salary Matching Rules (2025-26 season)**
 
| Outgoing Salary | Teams can receive back |
|---|---|
| Under $7.5M | Up to $7.5M + $100k |
| $7.5M — $29.9M | Up to 125% + $100k |
| $30M+ | Up to 125% |
 
**Key Terms**
- **TPE (Traded Player Exception):** Allows a team to absorb a salary without matching
- **Player Option (PO):** Player can opt out after the season
- **Team Option (TO):** Team can waive the player after the season  
- **ETO (Early Termination Option):** Player can end contract 1 year early
- **NTC (No-Trade Clause):** Player must consent to any trade
- **Luxury Tax Line (2025-26):** ~$170M — teams over this pay a penalty per dollar
 
**Hard Cap:** Teams using certain cap exceptions cannot exceed the "second apron" (~$189M in 2025-26).
        """)
