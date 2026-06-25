import streamlit as st
from utils.claude_client import fetch_json
 
ESPN_URL = "https://www.espn.com/nba/story/_/id/48957844/nba-trade-tracker-details-every-deal-2026-offseason-draft-free-agency"
 
SYSTEM = """You are an NBA trade analyst. Return ONLY valid JSON, no markdown, no explanation.
Use real data only — do not fabricate trades."""
 
PROMPT = f"""Search ESPN's NBA trade tracker at {ESPN_URL} and return the trades as JSON.
 
Return this exact structure:
{{
  "last_updated": "approximate date you fetched this",
  "total_trades": 10,
  "trades": [
    {{
      "date": "June 25, 2026",
      "teams": ["Team A", "Team B"],
      "headline": "One sentence summary of the trade",
      "players_exchanged": [
        {{"name": "Player Name", "from": "Team A", "to": "Team B", "salary": "$24.5M", "years_left": 2}},
        {{"name": "Player Name", "from": "Team B", "to": "Team A", "salary": "$18M", "years_left": 1}}
      ],
      "picks": ["Team A sends 2027 1st to Team B"],
      "salary_note": "Team A takes on $6.5M more in this deal",
      "cap_legal": true
    }}
  ]
}}
 
Return the most recent trades first. Return ONLY the JSON object, nothing else."""
 
 
def salary_color(salary_str: str) -> str:
    try:
        val = float(salary_str.replace("$", "").replace("M", "").replace(",", ""))
        if val >= 35:
            return "#dc2626"
        elif val >= 20:
            return "#d97706"
        else:
            return "#16a34a"
    except Exception:
        return "#6b7280"
 
 
def render():
    st.markdown("### 🔄 Recent Trades")
    st.caption("Live from ESPN's official 2026 offseason trade tracker")
 
    col1, col2 = st.columns([4, 1])
    with col2:
        refresh = st.button("🔄 Refresh", use_container_width=True)
 
    if "trades_data" not in st.session_state or refresh:
        data = fetch_json(PROMPT, system=SYSTEM)
        if data:
            st.session_state["trades_data"] = data
        else:
            return
 
    data = st.session_state.get("trades_data")
    if not data:
        return
 
    trades = data.get("trades", [])
    last_updated = data.get("last_updated", "")
 
    # Summary bar
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Trades", data.get("total_trades", len(trades)))
    m2.metric("Most Recent", trades[0]["date"] if trades else "—")
    m3.metric("Data As Of", last_updated)
 
    st.divider()
 
    for trade in trades:
        teams = " ↔ ".join(trade.get("teams", []))
        headline = trade.get("headline", "")
        date = trade.get("date", "")
        players = trade.get("players_exchanged", [])
        picks = trade.get("picks", [])
        salary_note = trade.get("salary_note", "")
        cap_legal = trade.get("cap_legal", True)
 
        with st.container():
            # Trade header
            col_date, col_legal = st.columns([3, 1])
            with col_date:
                st.markdown(f"**{teams}**")
                st.caption(f"📅 {date}")
            with col_legal:
                if cap_legal:
                    st.success("✅ Cap Legal")
                else:
                    st.error("❌ Cap Issue")
 
            st.markdown(f"*{headline}*")
 
            # Players grid
            if players:
                num_cols = min(len(players), 3)
                cols = st.columns(num_cols)
                for i, player in enumerate(players):
                    with cols[i % num_cols]:
                        sal = player.get("salary", "N/A")
                        yrs = player.get("years_left", "?")
                        frm = player.get("from", "")
                        to = player.get("to", "")
                        color = salary_color(sal)
                        st.markdown(f"""
<div style="background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:0.75rem; margin-bottom:0.5rem;">
  <div style="font-weight:600; font-size:0.95rem; color:#111827;">{player.get('name','')}</div>
  <div style="font-size:0.78rem; color:#6b7280; margin:2px 0;">{frm} → {to}</div>
  <div style="font-size:0.88rem; font-weight:600; color:{color}; margin-top:4px;">{sal}</div>
  <div style="font-size:0.75rem; color:#9ca3af;">{yrs} yr{'s' if yrs != 1 else ''} remaining</div>
</div>
""", unsafe_allow_html=True)
 
            # Picks and salary note
            detail_cols = st.columns(2)
            with detail_cols[0]:
                if picks:
                    st.markdown("**🏆 Picks**")
                    for p in picks:
                        st.markdown(f"- {p}")
            with detail_cols[1]:
                if salary_note:
                    st.markdown("**💰 Salary Note**")
                    st.markdown(salary_note)
 
            st.divider()
 
