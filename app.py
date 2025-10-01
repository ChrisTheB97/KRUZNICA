import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile, os

st.set_page_config(page_title="Body na kružnici", layout="centered")

# Sidebar – nastavenia a autor
st.sidebar.header("Nastavenia")
sekcia = st.sidebar.radio("Sekcia", ["Generátor", "O projekte"])
autor = st.sidebar.text_input("Autor", value="Tvoje meno")
kontakt = st.sidebar.text_input("Kontakt", value="email@example.com")

# Vstupy
x_stred = st.sidebar.number_input("Stred X", value=0.0, format="%.2f")
y_stred = st.sidebar.number_input("Stred Y", value=0.0, format="%.2f")
polomer = st.sidebar.number_input("Polomer", min_value=0.1, value=5.0, format="%.2f")
pocet_bodov = st.sidebar.slider("Počet bodov", 3, 500, 10)
farba = st.sidebar.color_picker("Farba bodov", "#ff0000")
jednotka = st.sidebar.text_input("Jednotka osí", value="m")

if sekcia == "Generátor":
    st.title("Generátor bodov na kružnici")

    uhly = np.linspace(0, 2*np.pi, pocet_bodov, endpoint=False)
    x = x_stred + polomer * np.cos(uhly)
    y = y_stred + polomer * np.sin(uhly)

    # Kružnica + body
    fig, ax = plt.subplots(figsize=(6,6))
    theta = np.linspace(0, 2*np.pi, 400)
    ax.plot(x_stred + polomer*np.cos(theta), y_stred + polomer*np.sin(theta), linewidth=1)
    ax.scatter(x, y, c=farba, s=35)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(f"X [{jednotka}]")
    ax.set_ylabel(f"Y [{jednotka}]")
    ax.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig)

    # Export do PDF
    if st.button("Exportovať do PDF"):
        tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig.savefig(tmp_img.name, dpi=200, bbox_inches="tight")

        pdf = FPDF()
        pdf.add_page()

        # ✅ pridáme font s podporou diakritiky
        pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)

        pdf.cell(0, 10, "Generovanie bodov na kružnici", ln=True, align="C")
        pdf.ln(5)
        pdf.cell(0, 8, f"Autor: {autor}", ln=True)
        pdf.cell(0, 8, f"Kontakt: {kontakt}", ln=True)
        pdf.cell(0, 8, f"Stred: ({x_stred:.2f}, {y_stred:.2f}) {jednotka}", ln=True)
        pdf.cell(0, 8, f"Polomer: {polomer:.2f} {jednotka}", ln=True)
        pdf.cell(0, 8, f"Počet bodov: {pocet_bodov}", ln=True)
        pdf.ln(5)
        pdf.image(tmp_img.name, w=170)

        out_path = "vystup.pdf"
        pdf.output(out_path)

        with open(out_path, "rb") as f:
            st.download_button("📥 Stiahnuť PDF", f, file_name="vystup.pdf", mime="application/pdf")

        os.unlink(tmp_img.name)
        st.success("PDF bolo vygenerované a je pripravené na stiahnutie ✅")

else:
    st.title("O projekte")
    st.write("""
**Názov úlohy:** Body na kružnici – webová aplikácia  
**Použité technológie:** Python, Streamlit, Matplotlib, FPDF2  

**Popis:**  
Používateľ zadáva stred, polomer, počet bodov a farbu.  
Aplikácia vykreslí body na kružnici s číselnými osami (vrátane jednotiek)  
a umožní export do PDF s parametrami úlohy, menom a kontaktom autora.
""")
    st.write(f"**Autor:** {autor}  \n**Kontakt:** {kontakt}")
