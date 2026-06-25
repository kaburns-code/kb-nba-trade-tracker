import streamlit as st
from utils.claude_client import fetch_json

SYSTEM = """You are an NBA salary cap analyst. Return ONLY valid JSON, no markdown, no explanation.
Use real salary data from basketball-reference.com. Never fabricate numbers."""

PROMPT = """Search for the latest NBA trade rumors for the 2026 offseason from ESPN, The Athletic, and Bleacher Report.
Also check basketball-reference.com for salary data.

Return this exact JSON structure:
{
  "rumors": [
    {
      "teams": ["Team A", "Team B"],
      "headline": "Short punchy headline",
      "source": "ESPN / The Athletic / etc",
      "reported_date": "June 2026",
      "players_discussed": [
        {
          "name": "Player Name",
          "team": "Current Team",
          "salary": "$32.5M",
          "years_left": 3,
          "options": "Player option 2027",
          "going_to": "Other Team"
        }
      ],
      "salary_out": "$32.5M",
      "salary_in": "$28M + $6M",
      "salary_total_in": "$34M",
      "trade_legal": true,
      "legality_note": "Works — receiving team takes back $34M on $32.5M out (104%), under 125% threshold",
      "why_it_makes_sense": "2-3 sentences on fit and motivation for both teams",
      "obstacle": "Main reason this might not happen"
    }
  ]
}

Find at least 5 rumors with real player names and real salary figures. Return ONLY the JSON."""


def render():
    st.markdown("### 🔥 Trade Rumors & Salary Analysis")
    st.caption("Active rumors with cap math — sourced from ESPN, The Athletic, Bleacher Report")

    col1, col2 = st.columns([4, 1])
    with col2:
        refresh = st.button("🔄 Refresh", use_container_width=True)

    # Custom trade analyzer
    with st.expander("⚡ Analyze your own rumored trade"):
        c1, c2 = st.columns(2)
        with c1:
            team1 = st.text_input("Team sending", placeholder="e.g. Boston Celtics")
            players_out = st.text_area("Players going out", placeholder="e.g. Jaylen Brown", height=80)
        with c2:
            team2 = st.text_input("Team receiving", placeholder="e.g. New Orleans Pelicans")
            players_in = st.text_area("Players coming back", placeholder="e.g. Dejounte Murray, Trey Murphy", height=80)

        if st.button("⚡ Analyze This Trade", use_container_width=True):
            if team1 and team2 and players_out and players_in:
                custom_prompt = f"""Search basketball-reference.com and analyze this NBA trade. Return ONLY JSON:
{{
  "trade": {{
    "team_a": "{team1}",
    "team_b": "{team2}",
    "players_out": [
      {{"name": "player", "salary": "$XM", "years_left": 2, "options": "none"}}
    ],
    "players_in": [
      {{"name": "player", "salary": "$XM", "years_left": 2, "options": "none"}}
    ],
    "total_salary_out": "$XM",
    "total_salary_in": "$XM",
    "trade_legal": true,
    "legality_explanation": "Full math explanation",
    "verdict": "WORKS / CLOSE / DOESN'T WORK",
    "fix_if_broken": "What would make it work",
    "who_wins": "Team A / Team B / Even",
    "why": "Explanation of trade value"
  }}
}}

Players out from {team1}: {players_out}
Players in to {team1}: {players_in}
Use real current salaries from basketball-reference.com."""

                with st.spinner("Analyzing trade..."):
                    result = fetch_json(custom_prompt)

                if result and "trade" in result:
                    t = result["trade"]
                    verdict = t.get("verdict", "")
                    color = "#16a34a" if "WORKS" in verdict else "#d97706" if "CLOSE" in verdict else "#dc2626"

                    st.markdown(f"""
<div style="background:white; border:1px solid #e5e7eb; border-radius:12px; padding:1.25rem; margin-top:1rem;">
  <div style="font-size:1.1rem; font-weight:700; color:{color}; margin-bottom:0.75rem;">{verdict}</div>
  <div style="font-size:0.85rem; color:#4b5563; margin-bottom:0.5rem;">{t.get('legality_explanation','')}</div>
</div>
""", unsafe_allow_html=True)

                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Salary Out", t.get("total_salary_out", "—"))
                    col_b.metric("Salary In", t.get("total_salary_in", "—"))
                    col_c.metric("Who Wins", t.get("who_wins", "—"))

                    if t.get("fix_if_broken"):
                        st.info(f"💡 **Fix:** {t['fix_if_broken']}")
                    if t.get("why"):
                        st.markdown(f"**Trade Value:** {t['why']}")

    st.divider()

    if "rumors_data" not in st.session_state or refresh:
        data = fetch_json(PROMPT, system=SYSTEM)
        if data:
            st.session_state["rumors_data"] = data
        else:
            return

    data = st.session_state.get("rumors_data")
    if not data:
        return

    rumors = data.get("rumors", [])

    for rumor in rumors:
        teams = " ↔ ".join(rumor.get("teams", []))
        legal = rumor.get("trade_legal", True)
        border_color = "#16a34a" if legal else "#dc2626"
        verdict_color = "#f59e0b"

        with st.container():
            # Header row
            hc1, hc2, hc3 = st.columns([3, 1, 1])
            with hc1:
                st.markdown(f"**{teams}**")
                st.caption(f"📰 {rumor.get('source','')} · {rumor.get('reported_date','')}")
            with hc2:
                if legal:
                    st.success("✅ Legal")
                else:
                    st.error("❌ Illegal")
            with hc3:
                st.markdown(f"**Out:** {rumor.get('salary_out','—')}")
                st.markdown(f"**In:** {rumor.get('salary_total_in','—')}")

            st.markdown(f"*{rumor.get('headline','')}*")

            # Players grid
            players = rumor.get("players_discussed", [])
            if players:
                cols = st.columns(min(len(players), 3))
                for i, p in enumerate(players):
                    with cols[i % 3]:
                        st.markdown(f"""
<div style="background:#f9fafb; border:1px solid #e5e7eb; border-left:3px solid {border_color}; border-radius:8px; padding:0.75rem; margin-bottom:0.5rem;">
  <div style="font-weight:600; font-size:0.9rem;">{p.get('name','')}</div>
  <div style="font-size:0.75rem; color:#6b7280;">{p.get('team','')} → {p.get('going_to','')}</div>
  <div style="font-size:0.85rem; font-weight:600; color:#3b82f6; margin-top:3px;">{p.get('salary','')}</div>
  <div style="font-size:0.72rem; color:#9ca3af;">{p.get('years_left','?')} yrs · {p.get('options','') or 'No options'}</div>
</div>
""", unsafe_allow_html=True)

            # Cap math + analysis
            note_cols = st.columns(2)
            with note_cols[0]:
                if rumor.get("legality_note"):
                    st.markdown("**⚖️ Cap Math**")
                    st.caption(rumor["legality_note"])
            with note_cols[1]:
                if rumor.get("why_it_makes_sense"):
                    st.markdown("**🤔 Why It Makes Sense**")
                    st.caption(rumor["why_it_makes_sense"])

            if rumor.get("obstacle"):
                st.warning(f"🚧 **Obstacle:** {rumor['obstacle']}")

            st.divider()
