import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

st.set_page_config(
    page_title="Fieldnotes | Research Desk",
    page_icon="⌕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #f4f4ed;
        --muted: #aeb9b3;
        --line: rgba(235, 242, 232, 0.16);
        --accent: #d9f36a;
        --panel: rgba(11, 23, 22, 0.84);
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] {
        background:
            linear-gradient(90deg, rgba(7, 17, 17, 0.95) 0%, rgba(7, 17, 17, 0.78) 48%, rgba(7, 17, 17, 0.55) 100%),
            linear-gradient(0deg, rgba(7, 17, 17, 0.82), rgba(7, 17, 17, 0.18)),
            url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=2400&q=85") center / cover fixed;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
    .block-container { max-width: 1180px; padding-top: 3rem; padding-bottom: 4rem; }

    h1, h2, h3, [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0 !important;
        color: var(--ink) !important;
    }
    h1 { font-size: clamp(2.5rem, 5vw, 4.2rem) !important; line-height: 1.02 !important; }
    h2 { font-size: 1.45rem !important; }
    p, label, [data-testid="stMarkdownContainer"] { color: var(--ink); }
    .eyebrow {
        color: var(--accent);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .lede { max-width: 640px; color: #cad2cb; font-size: 1.04rem; line-height: 1.65; }
    div[data-testid="stForm"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 1.2rem 1.3rem 0.8rem;
        backdrop-filter: blur(14px);
    }
    div[data-testid="stTextInput"] input {
        min-height: 3.1rem;
        background: rgba(255, 255, 255, 0.08);
        color: var(--ink);
        border-color: rgba(235, 242, 232, 0.22);
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }
    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
        min-height: 2.8rem;
        border: 0;
        border-radius: 5px;
        background: var(--accent);
        color: #172018;
        font-weight: 700;
    }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background: #e8ff8a;
        color: #172018;
        border: 0;
    }
    [data-testid="stTabs"] button { color: #d3dbd4; }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--accent);
        border-bottom-color: var(--accent);
    }
    [data-testid="stAlert"] { background: rgba(11, 23, 22, 0.9); }
    [data-testid="stDownloadButton"] button {
        border-radius: 5px;
        border-color: var(--line);
        color: var(--ink);
        background: rgba(255, 255, 255, 0.07);
    }
    hr { border-color: var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)


configured_keys = {
    "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
    "TRAVILY_API_KEY": bool(os.getenv("TRAVILY_API_KEY")),
}

st.markdown('<div class="eyebrow">Research, gathered and reviewed</div>', unsafe_allow_html=True)
st.title("Make a topic\nmake sense.")
st.markdown(
    '<p class="lede">Search current sources, read the strongest material, then turn the findings into a reviewed report.</p>',
    unsafe_allow_html=True,
)

missing_keys = [key for key, configured in configured_keys.items() if not configured]

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. How are cities adapting to extreme heat?",
        key="topic",
    )
    submitted = st.form_submit_button("Run research")

if submitted:
    if not topic.strip():
        st.warning("Enter a research topic to start.")
    elif missing_keys:
        st.warning("Configure the Google AI and Tavily credentials in your `.env` file to run research.")
    else:
        try:
            from pipeline import run_research_pipeline

            with st.spinner("Searching, reading sources, and preparing the review…"):
                result = run_research_pipeline(topic.strip())
            st.session_state.research_result = result
            st.session_state.research_topic = topic.strip()
        except Exception as error:
            st.error(f"The research run could not be completed: {error}")

result = st.session_state.get("research_result")
if result:
    st.divider()
    st.markdown(f'<div class="eyebrow">Latest report · {st.session_state.research_topic}</div>', unsafe_allow_html=True)
    report = str(result.get("report", "No report was returned."))
    download_name = "research-report.md"
    st.download_button("Download report", report, file_name=download_name, mime="text/markdown")

    report_tab, sources_tab, notes_tab, review_tab = st.tabs(
        ["Report", "Search results", "Source notes", "Critic review"]
    )
    with report_tab:
        st.markdown(report)
    with sources_tab:
        st.markdown(str(result.get("search_results", "No search results were returned.")))
    with notes_tab:
        st.markdown(str(result.get("scraped_content", "No source notes were returned.")))
    with review_tab:
        st.markdown(str(result.get("feedback", "No critic review was returned.")))