import anthropic
import streamlit as st
import json
import re
 
 
def get_client() -> anthropic.Anthropic:
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ No ANTHROPIC_API_KEY found. Add it to Streamlit secrets.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)
 
 
def fetch_json(prompt: str, system: str = "") -> dict | list | None:
    """Call Claude with web search, expect a JSON response back."""
    client = get_client()
    kwargs = dict(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
 
    with st.spinner("Fetching live data..."):
        response = client.messages.create(**kwargs)
 
    raw = "".join(b.text for b in response.content if hasattr(b, "text"))
 
    # Strip markdown code fences if present
    clean = re.sub(r"```json|```", "", raw).strip()
 
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\}|\[.*\])", clean, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        st.error("Could not parse structured data. Raw response below:")
        st.code(raw)
        return None
