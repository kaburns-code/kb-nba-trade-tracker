import streamlit as st
from utils.claude_client import stream_response
 
SYSTEM = """You are an expert NBA salary cap analyst and trade reporter. For each rumor:
- Be specific about real dollar amounts (use basketball-reference.com data)
- Apply NBA trade rules correctly: receiving team can take back up to 125% + $100k of outgoing salary
- Note years remaining on contracts (important for trade value)
- Note player options, team options, and no-trade clauses when relevant
- Clearly state if a trade WORKS or DOESN'T WORK under the salary cap rules
- Use ✅ for salary-legal trades, ⚠️ for close calls, ❌ for salary-illegal as proposed"""
 
PROMPT = """Search for the latest NBA trade rumors for the 2026 offseason from ESPN, The Athletic, 
Bleacher Report, and other reputable sources.
 
For each rumor, provide this structured analysis:
 
### 🔥 [Team A] ↔ [Team B]: [Key Players]
 
**What's being discussed:** [1-2 sentence summary of the rumor]
 
**Salary breakdown:**
- [Player A] (Team A): $XX.XM — X years remaining [any options]
- [Player B] (Team B): $XX.XM — X years remaining [any options]
- [Additional players/picks if applicable]
 
**Cap math:** [Does this trade work under NBA salary matching rules? Show the math.]
 
**Trade legality:** ✅/⚠️/❌ [Works / Close / Doesn't work as reported]
 
**Why it makes sense / Why it doesn't:** [2-3 sentences on fit and motivation]
 
---
 
Find at least 5 specific rumors with real player names and dollar amounts. 
Pull salary data from basketball-reference.com."""
 
 
def render():
    st.markdown('<p class="section-label">Active Rumors + Salary Cap Analysis</p>', unsafe_allow_html=True)
 
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Current trade discussions with salary matching analysis under NBA trade rules.")
    with col2:
        refresh = st.button("🔄 Refresh Rumors", use_container_width=True)
 
    # Custom rumor input
    with st.expander("➕ Analyze a specific rumored trade"):
        st.write("Enter a trade you've heard about and we'll analyze the salary math.")
        custom_col1, custom_col2 = st.columns(2)
        with custom_col1:
            team1 = st.text_input("Team 1", placeholder="e.g. Boston Celtics")
            players_out = st.text_area("Players going OUT from Team 1", placeholder="e.g. Jaylen Brown", height=80)
        with custom_col2:
            team2 = st.text_input("Team 2", placeholder="e.g. New Orleans Pelicans")
            players_in = st.text_area("Players coming IN to Team 1", placeholder="e.g. Dejounte Murray, Trey Murphy", height=80)
 
        if st.button("⚡ Analyze This Trade", use_container_width=True):
            if team1 and team2 and players_out and players_in:
                custom_prompt = f"""Analyze this specific proposed NBA trade using current salary data from basketball-reference.com:
 
**{team1} receives:** {players_in}
**{team2} receives:** {players_out}
 
Provide:
1. Current salary for each player (search basketball-reference.com)
2. Years remaining and any player/team options
3. Full salary matching math under NBA trade rules (125% + $100k rule)
4. Whether this trade is legal as proposed
5. What adjustments (add a player, pick, TPE) would make it work if it doesn't
6. Cap impact on both teams going forward
7. Trade value assessment — who wins this trade?"""
 
                placeholder = st.empty()
                stream_response(custom_prompt, placeholder, system=SYSTEM)
            else:
                st.warning("Fill in both teams and the players involved.")
 
    st.divider()
 
    cache_key = "rumors_cache"
 
    if cache_key not in st.session_state or refresh:
        placeholder = st.empty()
        with st.spinner("Scanning trade rumors and salary data..."):
            result = stream_response(PROMPT, placeholder, system=SYSTEM)
        st.session_state[cache_key] = result
    else:
        st.markdown(st.session_state[cache_key])
        st.caption("↑ Cached — click Refresh Rumors for latest.")
