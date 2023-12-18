import streamlit as st
from utils import spacer, variables_two_columns

def main():
  v_ne_poh = aircraft_specs["Performance"]["Never Exceed Speed"]["value"]

  col1, col2, col3 = st.columns([4, 1, 2])
  with col1:
    percentage_of_vne = st.slider("Percentage of Vne (%)", min_value=0, max_value=100, value=70, step=1)
  with col2:
    unit = st.radio("", ['Km/h', 'm/s'])
  with col3:
    if unit == 'Km/h':
      v_ne = st.number_input("Never Exceed Speed (Km/h)", value=v_ne_poh, min_value=0.00, step=10.00)
      v_krst.value = percentage_of_vne / 100.0 * (v_ne / 3.6)  # Convert to m/s
    else:
      v_ne = st.number_input("Never Exceed Speed (m/s)", value=v_ne_poh / 3.6, min_value=0.00, step=1.00)
      v_krst.value = percentage_of_vne / 100.0 * v_ne  # Already in m/s

  st.latex(f"v_{{\\text{{krst}}}} = \\frac{{\\text{{Vne}} \\times {percentage_of_vne}\\%}}{{100}} = \\frac{{{v_ne:.3f} \\times {percentage_of_vne}}}{{100}}")
  st.latex(f"v_{{\\text{{krst}}}} = {v_krst.value*3.6:.2f} \\, \\text{{Km/h}} = {v_krst.value:.2f} \\, \\text{{m/s}}")

  spacer()


if __name__ == "__main__":
  main()