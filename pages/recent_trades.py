import streamlit as st
from utils.claude_client import stream_response
 
ESPN_URL = "https://www.espn.com/nba/story/_/id/48957844/nba-trade-tracker-details-every-deal-2026-offseason-draft-free-agency"
 
SYSTEM = """You are an NBA trade analyst. When presenting trades:
- List them most recent first
- Use clear markdown formatting with headers for each trade
- Include: date, teams, players exchanged, pick compensation, and salary context
- Flag salary implications with 💰
- Flag pick implications with 🏆
- Keep each trade entry concise but complete
- Use real data only — do not fabricate trades"""
 
PROMPT = f"""Search ESPN's NBA trade tracker at {ESPN_URL} and list every trade from the 2026 NBA offseason, 
ordered most recent first. 
 
For each trade include:
- **Date** of the trade
- **Teams involved**
- **Players/picks exchanged** (who went where)
- **Salary context**: approximate salaries of players involved
- **Years remaining** on key contracts
 
Use markdown headers (###) for each trade. After all trades, add a brief "📊 Cap Impact Summary" 
section noting which teams gained/shed the most salary this offseason."""
 
 
def render():
    st.markdown('<p class="section-label">2026 Offseason — Most Recent First</p>', unsafe_allow_html=True)
 
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Live trade data fetched directly from ESPN's official trade tracker.")
    with col2:
        refresh = st.button("🔄 Refresh Trades", use_container_width=True)
 
    st.divider()
 
    cache_key = "trades_cache"
 
    if cache_key not in st.session_state or refresh:
        placeholder = st.empty()
        with st.spinner("Fetching latest trades from ESPN..."):
            result = stream_response(PROMPT, placeholder, system=SYSTEM)
        st.session_state[cache_key] = result
    else:
        st.markdown(st.session_state[cache_key])
        st.caption("↑ Cached result — click Refresh Trades to fetch latest.")
