import streamlit as st
from utils.claude_client import fetch_json

SYSTEM = """You are an NBA salary cap expert. Return ONLY valid JSON, no markdown, no explanation.
Use real salary data from basketball-reference.com. Never fabricate numbers."""

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
    st.markdown("### 🔍 Trade Finder")
    st.caption("Find salary-compatible trade partners across the league")

    mode = st.radio("Search by:", ["Player", "Team"], horizontal=True)

    if mode == "Player":
        col1, col2 = st.columns([2, 1])
        with col1:
            player_name = st.text_input("Player name", placeholder="e.g. Jaylen Brown")
        with col2:
            flexibility = st.selectbox("Salary range", ["Tight (±10%)", "Standard (±25%)", "Wide (±40%)"])

        if st.button("🔍 Find Matches", use_container_width=True, disabled=not player_name):
            flex_map = {"Tight (±10%)": "10%", "Standard (±25%)": "25%", "Wide (±40%)": "40%"}
            pct = flex_map[flexibility]

            prompt = f"""Search basketball-reference.com for {player_name}'s current salary and contract.
Then find 6 NBA players from different teams with salaries within {pct} of {player_name}'s salary.

Return ONLY this JSON:
{{
  "target": {{
    "name": "{player_name}",
    "team": "Current Team",
    "salary": "$32.5M",
    "years_left": 3,
    "options": "Player option 2027 / None",
    "age": 27
  }},
  "matches": [
    {{
      "name": "Player Name",
      "team": "Team Name",
      "salary": "$30M",
      "years_left": 2,
      "options": "None",
      "age": 28,
      "salary_difference": "+$2.5M",
      "trade_works": true,
      "fit_note": "Why this swap makes sense for both teams",
      "complication": "Any NTC, injury history, or cap issue"
    }}
  ],
  "package_deals": [
    {{
      "description": "Player A + Player B",
      "teams_involved": ["Team X", "Team Y"],
      "combined_salary": "$33M",
      "note": "Why this package works"
    }}
  ]
}}"""

            with st.spinner(f"Finding matches for {player_name}..."):
                data = fetch_json(prompt, system=SYSTEM)

            if not data:
                return

            target = data.get("target", {})
            matches = data.get("matches", [])
            packages = data.get("package_deals", [])

            # Target player card
            st.markdown("#### Target Player")
            st.markdown(f"""
<div style="background:white; border:2px solid #3b82f6; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem; display:inline-block; min-width:220px;">
  <div style="font-size:1.1rem; font-weight:700; color:#111827;">{target.get('name','')}</div>
  <div style="font-size:0.85rem; color:#6b7280; margin:2px 0;">{target.get('team','')} · Age {target.get('age','')}</div>
  <div style="font-size:1rem; font-weight:700; color:#3b82f6; margin-top:6px;">{target.get('salary','')}</div>
  <div style="font-size:0.78rem; color:#9ca3af;">{target.get('years_left','?')} yrs remaining · {target.get('options','No options')}</div>
</div>
""", unsafe_allow_html=True)

            # Matches grid
            st.markdown("#### Salary Matches")
            cols = st.columns(3)
            for i, m in enumerate(matches):
                with cols[i % 3]:
                    works = m.get("trade_works", True)
                    border = "#16a34a" if works else "#dc2626"
                    badge = "✅ Works" if works else "❌ Cap issue"
                    badge_bg = "#dcfce7" if works else "#fee2e2"
                    badge_color = "#166534" if works else "#991b1b"

                    st.markdown(f"""
<div style="background:white; border:1px solid #e5e7eb; border-top:3px solid {border}; border-radius:10px; padding:0.9rem; margin-bottom:0.75rem; height:100%;">
  <div style="font-weight:600; font-size:0.95rem; color:#111827;">{m.get('name','')}</div>
  <div style="font-size:0.78rem; color:#6b7280;">{m.get('team','')} · Age {m.get('age','')}</div>
  <div style="font-size:0.9rem; font-weight:600; color:#3b82f6; margin:5px 0;">{m.get('salary','')}</div>
  <div style="font-size:0.75rem; color:#9ca3af;">{m.get('years_left','?')} yrs · {m.get('options','No options')}</div>
  <div style="margin-top:8px;">
    <span style="background:{badge_bg}; color:{badge_color}; font-size:0.72rem; font-weight:600; padding:2px 8px; border-radius:20px;">{badge}</span>
    <span style="font-size:0.75rem; color:#6b7280; margin-left:6px;">{m.get('salary_difference','')}</span>
  </div>
  <div style="font-size:0.78rem; color:#4b5563; margin-top:6px; line-height:1.4;">{m.get('fit_note','')}</div>
  {'<div style="font-size:0.72rem; color:#d97706; margin-top:4px;">⚠️ ' + m.get('complication','') + '</div>' if m.get('complication') else ''}
</div>
""", unsafe_allow_html=True)

            # Package deals
            if packages:
                st.markdown("#### 📦 Multi-Player Packages")
                for pkg in packages:
                    st.markdown(f"""
<div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:0.9rem; margin-bottom:0.5rem;">
  <div style="font-weight:600; color:#0369a1;">{pkg.get('description','')}</div>
  <div style="font-size:0.82rem; color:#0369a1; margin-top:2px;">Combined: {pkg.get('combined_salary','')} · {', '.join(pkg.get('teams_involved',[]))}</div>
  <div style="font-size:0.8rem; color:#4b5563; margin-top:4px;">{pkg.get('note','')}</div>
</div>
""", unsafe_allow_html=True)

    else:  # Team mode
        col1, col2 = st.columns([2, 1])
        with col1:
            team_name = st.selectbox("Select team", NBA_TEAMS)
        with col2:
            focus = st.selectbox("Focus on", [
                "All tradeable players",
                "Max contracts only",
                "Expiring contracts",
                "Young players (U25)"
            ])

        if st.button("🔍 Analyze Trade Options", use_container_width=True):
            focus_map = {
                "All tradeable players": "all players on tradeable contracts",
                "Max contracts only": "max or near-max salary players",
                "Expiring contracts": "players in the final year of their contract",
                "Young players (U25)": "players under 25 years old"
            }

            prompt = f"""Search basketball-reference.com for the {team_name}'s current roster and salaries.
Focus on {focus_map[focus]}.

Return ONLY this JSON:
{{
  "team": "{team_name}",
  "total_payroll": "$180M",
  "luxury_tax_position": "Over by $12M",
  "cap_snapshot": "1-2 sentence summary of cap situation",
  "tradeable_players": [
    {{
      "name": "Player Name",
      "salary": "$32M",
      "years_left": 2,
      "options": "Player option 2027",
      "age": 28,
      "trade_value": "High / Medium / Low",
      "best_match_teams": ["Team A", "Team B"],
      "best_match_players": ["Player X ($30M)", "Player Y ($28M + Player Z $4M)"],
      "cap_impact_if_traded": "Saves $32M, drops below luxury tax",
      "note": "Key context about trading this player"
    }}
  ]
}}"""

            with st.spinner(f"Analyzing {team_name} trade options..."):
                data = fetch_json(prompt, system=SYSTEM)

            if not data:
                return

            # Team cap snapshot
            cap_cols = st.columns(3)
            cap_cols[0].metric("Total Payroll", data.get("total_payroll", "—"))
            cap_cols[1].metric("Luxury Tax", data.get("luxury_tax_position", "—"))
            cap_cols[2].metric("Team", data.get("team", "—"))

            if data.get("cap_snapshot"):
                st.info(data["cap_snapshot"])

            st.divider()

            players = data.get("tradeable_players", [])
            for p in players:
                tv = p.get("trade_value", "Medium")
                tv_color = "#16a34a" if tv == "High" else "#d97706" if tv == "Medium" else "#dc2626"

                with st.expander(f"**{p.get('name','')}** · {p.get('salary','')} · {p.get('years_left','?')} yrs"):
                    pc1, pc2, pc3, pc4 = st.columns(4)
                    pc1.metric("Salary", p.get("salary", "—"))
                    pc2.metric("Years Left", p.get("years_left", "—"))
                    pc3.metric("Age", p.get("age", "—"))
                    pc4.markdown(f"**Trade Value**")
                    pc4.markdown(f"<span style='color:{tv_color}; font-weight:700;'>{tv}</span>", unsafe_allow_html=True)

                    if p.get("options"):
                        st.caption(f"📋 {p['options']}")

                    mc1, mc2 = st.columns(2)
                    with mc1:
                        st.markdown("**Best Match Teams**")
                        for t in p.get("best_match_teams", []):
                            st.markdown(f"- {t}")
                    with mc2:
                        st.markdown("**Salary Match Players**")
                        for m in p.get("best_match_players", []):
                            st.markdown(f"- {m}")

                    if p.get("cap_impact_if_traded"):
                        st.success(f"💰 {p['cap_impact_if_traded']}")
                    if p.get("note"):
                        st.caption(p["note"])

    st.divider()
    with st.expander("📋 NBA Trade Rules Reference"):
        st.markdown("""
| Outgoing Salary | Max You Can Receive Back |
|---|---|
| Under $7.5M | Up to $7.5M + $100k |
| $7.5M — $29.9M | Up to 125% + $100k |
| $30M+ | Up to 125% |

**Key Terms:** TPE (Traded Player Exception) · PO (Player Option) · TO (Team Option) · ETO (Early Termination) · NTC (No-Trade Clause)

**Luxury Tax Line (2025-26):** ~$170M · **Second Apron:** ~$189M (hard cap if triggered)
        """)
