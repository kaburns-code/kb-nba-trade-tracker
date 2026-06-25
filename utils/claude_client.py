import anthropic
import streamlit as st
from typing import Generator
 
 
def get_client() -> anthropic.Anthropic:
    """Initialize Anthropic client from Streamlit secrets or env."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ No ANTHROPIC_API_KEY found. Add it to `.streamlit/secrets.toml` or as an environment variable.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)
 
 
def stream_response(prompt: str, placeholder, system: str = "") -> str:
    """
    Stream a Claude response with web search into a Streamlit placeholder.
    Returns the full text when done.
    """
    client = get_client()
    full_text = ""
 
    kwargs = dict(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
 
    with client.messages.stream(**kwargs) as stream:
        for text in stream.text_stream:
            full_text += text
            placeholder.markdown(full_text + "▌")
 
    placeholder.markdown(full_text)
    return full_text
 
 
def simple_query(prompt: str, system: str = "") -> str:
    """Non-streaming query, returns full response text."""
    client = get_client()
    kwargs = dict(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )
    if system:
        kwargs["system"] = system
 
    response = client.messages.create(**kwargs)
    return "".join(b.text for b in response.content if hasattr(b, "text"))
