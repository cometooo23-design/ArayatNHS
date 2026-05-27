# Arayat National High School — Performance Dashboard

A fully interactive school performance dashboard — works standalone in any browser, and deploys to Streamlit with zero configuration.

## 🚀 Quick Start

### Option A — Open directly (no install, works offline)
```
Double-click dashboard.html
```
All data persists automatically in your browser's localStorage.

### Option B — Run with Streamlit (recommended for sharing / GitHub)
```bash
pip install streamlit
streamlit run streamlit_app.py
```
Opens at http://localhost:8501 — **no sidebar, full-screen dashboard**.

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `dashboard.html` | Full dashboard — standalone, works offline |
| `data.json` | **All school data lives here** — commit this to GitHub |
| `streamlit_app.py` | Streamlit wrapper (no sidebar needed) |
| `requirements.txt` | `pip install -r requirements.txt` |
| `README.md` | This file |

---

## ✏️ How to Add or Edit Data

### Adding a new school year
1. Click **✏️ Edit** in the dashboard header
2. Click **＋ New Year** — enter e.g. `2026-2027`
3. The new year gets a **distinct color** and appears in all charts immediately
4. Fill in all the data fields and click **💾 Save Changes**
5. Click **💾 Export JSON** (header button) → downloads updated `data.json`
6. Replace `data.json` in your project folder

### Editing existing year data
1. Click **✏️ Edit** → select the year from the dropdown
2. Update any values → **💾 Save Changes**
3. All charts update instantly — enrollment, promotion rates, teachers, facilities, insights

### What auto-updates when you save
- All enrollment charts and KPIs
- Promotion rate charts and tables
- **JHS→SHS transition rate** — recalculated automatically from G10/G11 enrollment
- Gender ratio, dropout history, teacher counts, seat capacity
- Insights & Recommendations panel

---

## 📊 Year Comparison

Use the **School Year** dropdown (top-right header):

| Selection | What you see |
|-----------|-------------|
| Single year | All charts show that year's data; KPIs reflect that year |
| **2+ years checked** | Bar charts stack/group by year; line charts highlight selected years; tables show all selected years side-by-side |
| **All** | Full historical view across every year |

Check multiple years by clicking them in the dropdown — charts update immediately.

---

## 🌐 Deploy to Streamlit Cloud (free)

1. Push this folder to a **public or private GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, file `streamlit_app.py`
4. Click **Deploy** — done!

### Updating data on Streamlit Cloud
Since the server filesystem resets on Streamlit Cloud, edit `data.json` directly in GitHub:
1. Make edits via the dashboard locally → **💾 Export JSON**
2. Commit and push the new `data.json` to GitHub
3. Streamlit Cloud auto-redeploys

---

## 🔧 Technical Notes

- **No sidebar** — the Streamlit app hides all Streamlit chrome for a clean full-screen experience
- **Data priority**: `data.json` (server) → `localStorage` (browser) — server always wins on fresh load
- **New years get auto-colors** — 8 distinct color pairs, never repeating
- **Transition rates auto-calculate** — saving G10 enrollment recalculates the JHS→SHS rate for the next year
- The dashboard is a single self-contained HTML file — no external dependencies beyond Chart.js (CDN)
