import streamlit as st
 
st.set_page_config(
    page_title="KB Trade Tracker",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
 
.hero {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b3e 60%, #0a0a1a 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
}
.hero h1 {
    color: white;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 0.25rem;
}
.hero p {
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
}
.hero-badges {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.team-dot {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    color: white;
    border: 1.5px solid rgba(255,255,255,0.15);
}
.source-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 5px;
    font-size: 11px;
    font-weight: 700;
    margin: 0 3px;
}
.espn { background: #cc0000; color: white; }
.bbref { background: #1a3a5c; color: white; }
 
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #eee;
}
.trade-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
}
.rumor-card {
    border-left-color: #f59e0b !important;
}
.trade-date {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-bottom: 0.4rem;
}
.trade-teams {
    font-weight: 600;
    font-size: 1rem;
    color: #111827;
    margin-bottom: 0.25rem;
}
.trade-detail {
    font-size: 0.85rem;
    color: #4b5563;
    line-height: 1.6;
}
.salary-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 0.75rem;
    font-size: 0.82rem;
}
.match-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.75rem;
    margin-bottom: 0.5rem;
}
.match-player { font-weight: 600; color: #111827; }
.match-team { font-size: 0.8rem; color: #6b7280; }
.match-sal { color: #3b82f6; font-weight: 600; font-size: 0.85rem; margin-top: 3px; }
.match-yrs { font-size: 0.75rem; color: #9ca3af; }
.ok { color: #16a34a; font-weight: 600; }
.warn { color: #d97706; font-weight: 600; }
.bad { color: #dc2626; font-weight: 600; }
</style>
""", unsafe_allow_html=True)
 
# --- Hero Section ---
st.markdown("""
<div class="hero">
  <div class="hero-badges">
    <span class="team-dot" style="background:#006BB6">NYK</span>
    <span class="team-dot" style="background:#007A33">BOS</span>
    <span class="team-dot" style="background:#C8102E">MIA</span>
    <span class="team-dot" style="background:#1D1160">LAL</span>
    <span class="team-dot" style="background:#CE1141">HOU</span>
    <span class="team-dot" style="background:#E03A3E">CLE</span>
    <span class="team-dot" style="background:#5A2D81">SAC</span>
    <span class="team-dot" style="background:#002B5C">MEM</span>
    <span class="team-dot" style="background:#00538C">DAL</span>
    <span class="team-dot" style="background:#1a1a1a">BKN</span>
  </div>
  <h1>🏀 KB Trade Tracker</h1>
  <p>
    Live trade data via
    <span class="source-badge espn">ESPN</span>
    and
    <span class="source-badge bbref">Basketball-Reference</span>
  </p>
</div>
""", unsafe_allow_html=True)
 
# --- Navigation ---
tab1, tab2, tab3 = st.tabs(["🔄 Recent Trades", "🔥 Trade Rumors & Salary Analysis", "🔍 Trade Finder"])
 
with tab1:
    from pages import recent_trades
    recent_trades.render()
 
with tab2:
    from pages import rumors
    rumors.render()
 
with tab3:
    from pages import trade_finder
    trade_finder.render()
