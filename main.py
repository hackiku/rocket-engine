import streamlit as st
from utils import spacer, variables_two_columns

def main():

  # Title for the section
  st.write("Proracun performansi i geometrije")

  # Inputs for the variables
  mg = st.number_input('Maseni protok goriva (mg)', value=1.0)
  OF = st.number_input('Odnos mesanja oksidator/gorivo (OF)', value=5.0)
  P = st.number_input('Pritisak u komori (P)', value=100.0 * (10**5))
  Lkar = st.number_input('Karakteristicna duzina (Lkar)', value=1.0)
  Cstar = st.number_input('Karakteristicna brzina (Cstar)', value=2000.0)
  epsilon_i = st.number_input('Stepen sirenja mlaznika (epsilon_i)', value=6.0)
  d_dkdr = st.number_input('Odnos precnika komore i grla mlaznika (d_dkdr)', value=2.5)
  R = st.number_input('Gasna konstanta (R)', value=546.0)
  kappa = st.number_input('Odnos specificnih toplota pri konstantnom pritisku i zapremini (kappa)', value=1.2)
  Pa = st.number_input('Atmosferski pritisak (Pa)', value=101325.0)


  # Maseni protok oksidatora
  mox = OF * mg
  st.write('Maseni protok oksidatora:')
  st.markdown('$m_{ox} = OF \cdot mg$')
  st.markdown(f'$ m_{{ox}} = {OF:.3f} \cdot {mg:.3f} = {mox:.3f} \\, \\text{{kg/s}} $', unsafe_allow_html=True)
  spacer()

  # Kriticni presek i precnik mlaznika
  st.write('Kriticni presek i precnik mlaznika:')
  Akr = Cstar * (mg + mox) / P
  dkr = (Akr * 4 / 3.14159)**0.5
  st.markdown('$A_{kr} = C_{star} \cdot (mg + m_{ox}) / P$')
  st.markdown(f'$ A_{{kr}} = {Cstar:.3f} \cdot ({mg:.3f} + {mox:.3f}) / {P:.3f} = {Akr:.3f} \\, \\text{{m^2}} $', unsafe_allow_html=True)
  st.markdown('$d_{kr} = \\sqrt{A_{kr} \\cdot \\frac{4}{\\pi}}$')
  st.markdown(f'$ d_{{kr}} = \\sqrt{{ {Akr:.3f} \\cdot \\frac{{4}}{{\\pi}}}} = {dkr:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)
  spacer()

  # Zapremina komore
  Vkom = Lkar * Akr
  st.subheader('Zapremina komore:')
  st.markdown('$V_{kom} = L_{kar} \cdot A_{kr}$')
  st.markdown(f'$ V_{{kom}} = {Lkar:.3f} \cdot {Akr:.3f} = {Vkom:.3f} \\, \\text{{m^3}} $', unsafe_allow_html=True)
  spacer()

  # Precnik i duzina komore
  dk = dkr * d_dkdr
  lk = Vkom / (dk**2 * 3.14159 / 4)
  st.write('Precnik i duzina komore:')
  st.markdown('$d_{k} = d_{kr} \cdot d/d_{kdr}$')
  st.markdown(f'$ d_{{k}} = {dkr:.3f} \cdot {d_dkdr:.3f} = {dk:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)
  st.markdown('$l_{k} = V_{kom} / (\\frac{d_{k}^2 \cdot \\pi}{4})$')
  # st.markdown(f'$ l_{{k}} = {Vkom:.3f} / (\\frac{{{dk:.3f}}^2 \cdot \\pi}{4}) = {lk:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)
  spacer()

  # Izlazni presek i precnik mlaznika
  Ai = epsilon_i * Akr
  di = (Ai * 4 / 3.14159)**0.5
  st.write('Izlazni presek i precnik mlaznika:')
  st.markdown('$A_{i} = \\epsilon_i \cdot A_{kr}$')
  st.markdown(f'$ A_{{i}} = {epsilon_i:.3f} \cdot {Akr:.3f} = {Ai:.3f} \\, \\text{{m^2}} $', unsafe_allow_html=True)
  st.markdown('$d_{i} = \\sqrt{\\frac{A_{i} \cdot 4}{\\pi}}$')
  # st.markdown(f'$ d_{{i}} = \\sqrt{{\\frac{{{Ai:.3f}} \cdot 4}}{{\\pi}}} = {di:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)

  spacer()

if __name__ == "__main__":
  main()
