import streamlit as st

from __main__ import STUDENT_NAME, STUDENT_CONTACT, SCHOOL, COURSE  # berieme údaje z app.py

st.set_page_config(page_title="Info o projekte", page_icon="ℹ️", layout="centered")

st.title("Info o projekte")
st.write("""
Webová aplikácia vizualizuje **body na kružnici** podľa zadaného stredu, polomeru,
počtu bodov a farby. Zobrazuje graf s číselnými hodnotami na osiach a umožňuje
export do **PDF** aj **CSV**.
""")

st.subheader("Autor")
st.markdown(f"- **Meno:** {STUDENT_NAME}\n- **Kontakt:** {STUDENT_CONTACT}\n- **Škola / Predmet:** {SCHOOL} – {COURSE}")

st.subheader("Použité technológie")
st.markdown("""
- **Streamlit** (web UI)
- **NumPy** (výpočty)
- **Matplotlib** (graf)
- **Pandas** (tabuľka/CSV)
- **ReportLab** (PDF)
""")

st.subheader("Matematika")
st.markdown("""
Pre `i = 0 … N-1`, `θ_i = 2π·i/N`  
`x_i = x₀ + r·cos(θ_i)`, `y_i = y₀ + r·sin(θ_i)`
""")
