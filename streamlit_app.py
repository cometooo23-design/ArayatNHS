"""
Arayat National High School — Performance Dashboard
Streamlit entry point — no sidebar required.

Run locally:
    pip install streamlit
    streamlit run streamlit_app.py

Architecture:
  - data.json is the single source of truth (commit this to GitHub).
  - On load, Streamlit injects data.json into the dashboard via sessionStorage.
  - The dashboard saves all edits to localStorage for instant in-browser persistence.
  - The floating 💾 Export JSON button in the dashboard downloads data.json so you
    can commit it to GitHub (or drop it in the project folder to update the server).
  - For Streamlit Cloud: use the "📂 Load JSON" button inside the dashboard to paste
    in updated data — no sidebar needed.
"""

import json
import streamlit as st
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ANHS Dashboard",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Remove all Streamlit chrome for a clean full-screen dashboard experience
st.markdown("""
<style>
  #MainMenu, header[data-testid="stHeader"], footer,
  .stDeployButton, [data-testid="collapsedControl"] { display: none !important; }
  .block-container { padding: 0 !important; max-width: 100% !important; }
  section[data-testid="stSidebar"] { display: none !important; }
  iframe { border: none; display: block; }
</style>
""", unsafe_allow_html=True)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
HTML_FILE = BASE_DIR / "dashboard.html"

# ── Load data ─────────────────────────────────────────────────────────────────
def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {}

def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

# ── Session state ─────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = load_data()

# Handle save coming from the hidden textarea (JS → st.text_area → Python)
if "pending_save" in st.session_state and st.session_state.pending_save:
    try:
        incoming = json.loads(st.session_state.pending_save)
        save_data(incoming)
        st.session_state.data = incoming
        st.session_state.pending_save = ""
        st.toast("✅ data.json updated on server!", icon="💾")
    except Exception as e:
        st.warning(f"Save error: {e}")

# ── Build HTML with injected data + save bridge ───────────────────────────────
def build_html(data: dict) -> str:
    if not HTML_FILE.exists():
        return "<h1 style='font-family:sans-serif;padding:40px'>dashboard.html not found — place it next to streamlit_app.py</h1>"

    raw = HTML_FILE.read_text(encoding="utf-8")
    data_js = json.dumps(data, ensure_ascii=False)

    # Inject server data into sessionStorage (overrides stale localStorage)
    head_inject = f"""
<script>
// ── Server-side data injection (Streamlit → dashboard) ──────────────────
(function(){{
  try{{
    sessionStorage.setItem('anhs_injected', JSON.stringify({data_js}));
  }}catch(e){{}}
}})();
</script>"""

    # Patch loadPersistedData to prefer injected server data
    new_load_fn = """function loadPersistedData(){
  try{
    var injRaw=typeof sessionStorage!=="undefined"?sessionStorage.getItem("anhs_injected"):null;
    var raw=injRaw||localStorage.getItem("anhs_data");
    if(!raw)return;var s=JSON.parse(raw);
    if(s.YEARS){YEARS.length=0;s.YEARS.forEach(y=>YEARS.push(y));}
    if(s.enrollment)Object.assign(enrollment,s.enrollment);
    if(s.promoRates)Object.assign(promoRates,s.promoRates);
    if(s.dropouts){dropouts.length=0;s.dropouts.forEach(d=>dropouts.push(d));}
    if(s.lwd)Object.assign(lwd,s.lwd);
    if(s.teachers)s.teachers.forEach((st,i)=>{if(teachers[i])Object.assign(teachers[i],st);});
    if(s.seats)s.seats.forEach((ss,i)=>{if(seats[i])Object.assign(seats[i],ss);});
    if(s.insightsData)Object.assign(insightsData,s.insightsData);
    if(s.transitions){transitions.length=0;s.transitions.forEach(t=>transitions.push(t));}
    YEARS.forEach(yr=>{if(!PAL[yr])PAL[yr]={m:"#37474F",f:"#90A4AE"};});
  }catch(e){console.warn(e);}
}"""

    import re
    patched = raw.replace("</head>", head_inject + "\n</head>", 1)
    patched = re.sub(
        r'function loadPersistedData\(\)\{.*?\}(?=\nfunction showToast)',
        new_load_fn.strip(),
        patched,
        flags=re.DOTALL
    )
    return patched

# ── Render ────────────────────────────────────────────────────────────────────
data         = st.session_state.data
html_content = build_html(data)

st.components.v1.html(html_content, height=980, scrolling=True)
