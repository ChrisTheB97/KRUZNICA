import math
from io import BytesIO
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Body na kružnici", page_icon="⚪", layout="centered")

st.title("Body na kružnici")
st.caption("Zadaj stred, polomer, počet bodov, farbu → vykreslenie, tabuľka, CSV, PDF.")

st.sidebar.header("Vstupné parametre")
c1, c2 = st.sidebar.columns(2)
x0 = c1.number_input("x₀", value=0.0, step=0.5, format="%.3f")
y0 = c2.number_input("y₀", value=0.0, step=0.5, format="%.3f")
r = st.sidebar.number_input("Polomer r", min_value=0.0, value=5.0, step=0.5, format="%.3f")
N = st.sidebar.number_input("Počet bodov N", min_value=1, max_value=2000, value=12, step=1)
units = st.sidebar.text_input("Jednotka osí", value=DEFAULT_UNITS)
dot_color = st.sidebar.color_picker("Farba bodov", value="#1f77b4")
dot_size = st.sidebar.slider("Veľkosť bodov", min_value=20, max_value=200, value=80)
show_circle = st.sidebar.checkbox("Zobraziť obrys kružnice", value=True)
connect_points = st.sidebar.checkbox("Prepojiť body polyčiarou", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("Údaje do PDF")
name_pdf = st.sidebar.text_input("Tvoje meno", value=STUDENT_NAME)
contact_pdf = st.sidebar.text_input("Kontakt", value=STUDENT_CONTACT)

theta = np.linspace(0, 2 * math.pi, int(N), endpoint=False)
x = x0 + r * np.cos(theta)
y = y0 + r * np.sin(theta)

df = pd.DataFrame({"i (od 1)": np.arange(1, N + 1), "x": x, "y": y, "uhol_deg": np.degrees(theta)})

fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
if show_circle and r > 0:
    ax.add_artist(plt.Circle((x0, y0), r, fill=False, linewidth=1.5))
ax.scatter(x, y, s=dot_size, c=dot_color, zorder=3)
if connect_points and N > 1:
    ax.plot(np.append(x, x[0]), np.append(y, y[0]), linewidth=1.0)
ax.set_xlabel(f"x [{units}]"); ax.set_ylabel(f"y [{units}]")
ax.grid(True, linestyle="--", alpha=0.5)
ax.set_aspect("equal", adjustable="box")
all_x = np.append(x, [x0 - r, x0 + r]); all_y = np.append(y, [y0 - r, y0 + r])
pad = max(1.0, r*0.1)
ax.set_xlim(all_x.min() - pad, all_x.max() + pad); ax.set_ylim(all_y.min() - pad, all_y.max() + pad)
st.pyplot(fig, use_container_width=True)

st.subheader("Súradnice bodov")
st.dataframe(df.style.format({"x": "{:.6f}", "y": "{:.6f}", "uhol_deg": "{:.2f}"}), use_container_width=True)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Stiahnuť CSV", data=csv, file_name="body_kruznica.csv", mime="text/csv")

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

def build_pdf(fig_obj) -> bytes:
    buf_img = BytesIO(); fig_obj.savefig(buf_img, format="png", dpi=300, bbox_inches="tight"); buf_img.seek(0)
    img = ImageReader(buf_img)
    pdf = BytesIO(); c = canvas.Canvas(pdf, pagesize=A4); W, H = A4
    c.setFont("Helvetica-Bold", 16); c.drawString(20*mm, H-20*mm, "Body na kružnici – výstup")
    c.setFont("Helvetica", 11); c.drawString(20*mm, H-28*mm, f"Dátum a čas: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    yline = H-40*mm
    lines = [f"Stred: x₀ = {x0:.3f} {units}, y₀ = {y0:.3f} {units}",
             f"Polomer r = {r:.3f} {units}", f"Počet bodov N = {N}",
             f"Farba bodov = {dot_color}", f"Jednotky osí = [{units}]",
             f"Študent: {name_pdf}", f"Kontakt: {contact_pdf}",
             f"Škola/Kurz: {SCHOOL} / {COURSE}"]
    for line in lines: c.drawString(20*mm, yline, line); yline -= 6*mm
    img_w, img_h = img.getSize(); max_w, max_h = (W-40*mm), (yline-20*mm); scale = min(max_w/img_w, max_h/img_h)
    c.drawImage(img, (W-img_w*scale)/2, yline-img_h*scale, width=img_w*scale, height=img_h*scale)
    c.showPage(); c.save(); pdf.seek(0); return pdf.getvalue()

pdf_bytes = build_pdf(fig)
st.download_button("Stiahnuť PDF", data=pdf_bytes, file_name="kruznica_vystup.pdf", mime="application/pdf")

st.info("Info o autorovi nájdeš v menu ☰ → Pages → „Info o projekte“.")
