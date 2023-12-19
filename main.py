import streamlit as st
from utils import spacer, variables_two_columns


# 1. Oksidator/gorivo: tečni kiseonik / hidrazin
# 2. Pritisak u komori: 𝑝 = 180 𝑏𝑎𝑟
# 3. Atmosferski pritisak: 𝑝𝑎 = 1 𝑎𝑡𝑚
# 4. Sila potiska: 𝐹 = 2200 𝑑𝑎𝑁
# 5. Stepen širenja: 𝜀 = 7
# 6. Odnost prečnika komore i grla mlaznika Dk/dkr=3
# 7. Karakteristična dužina L*=1m

def main():

  # Title for the section
  st.header("🚀 Tečni kiseonik / hidrazin")
  st.write('Na osnovu definisanih ulaznih parametara potrebno je da se odrede performanse idealnog raketnog motora na tečno gorivo: specifični impuls, karakteristična brzina, koeficijent potiska, kao i preliminarna geometrija komore i mlaznika. Proračun uraditi za odnos mešanja koji odgovaraja maksimalnom specifičnom impulsu pomoću programa RPA, a zatim ručno izračunati iste vrednosti koristeći vrednosti karakteristične brzine i osobina produkata sagorevanja iz programa.')

  # Inputs for the variables
  mg = st.number_input('Maseni protok goriva (mg)', value=1.0)
  OF = st.number_input('Odnos mesanja oksidator/gorivo (OF)', value=5.0)
  st.markdown('***')
  P = st.number_input('(2) Pritisak u komori (P)', value=180.0 * (10**5))
  Pa = st.number_input('(3) Atmosferski pritisak (Pa)', value=101325.0)
  F = st.number_input('(4) Sila potiska', value = 2200)
  epsilon_i = st.number_input('(5) Stepen sirenja mlaznika (epsilon_i)', value=7.0)
  d_dkdr = st.number_input('(6) Odnos precnika komore i grla mlaznika (d_dkdr)', value=3)
  Lkar = st.number_input('(7) Karakteristicna duzina (Lkar)', value=1.0)
  st.markdown('***')
  st.subheader('vrednosti is RPA')
  col1, col2, col3 = st.columns(3)
  with col1:
    Cstar = st.number_input('Karakteristicna brzina (Cstar)', value=2000.0)
  with col2:
    R = st.number_input('Gasna konstanta (R)', value=546.0)
  with col3:
    kappa = st.number_input('Odnos specificnih toplota pri konstantnom pritisku i zapremini (kappa)', value=1.2)

  # =============================
  st.title('Calculations')
  # 1. Maseni protok oksidatora
  mox = OF * mg
  st.write('1. Maseni protok oksidatora:')
  st.markdown('$m_{ox} = OF \cdot mg$')
  st.markdown(f'$ m_{{ox}} = {OF:.3f} \cdot {mg:.3f} = {mox:.3f} \\, \\text{{kg/s}} $', unsafe_allow_html=True)
  spacer()

  # 2. Kriticni presek i precnik mlaznika
  Akr = Cstar * (mg + mox) / P
  dkr = (Akr * 4 / 3.14159)**0.5
  st.write('2. Kriticni presek i precnik mlaznika:')
  st.markdown('$A_{kr} = \\frac{C_{star} \cdot (mg + m_{ox})}{P}$')
  st.markdown(f'$ A_{{kr}} = \\frac{{ {Cstar:.3f} \, \cdot \, ({mg:.3f} + {mox:.3f}) }}{{ {P:.3f} }} = {Akr:.3f} \\, m^2 $')
  st.markdown('$d_{kr} = \\sqrt{A_{kr} \cdot \\frac{4}{\\pi}}$')
  st.markdown(f'$ d_{{kr}} = \\sqrt{{{Akr:.3f} \cdot \\frac{{4}}{{\\pi}}}} = {dkr:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)
  spacer()

  # 3. Zapremina komore
  Vkom = Lkar * Akr
  st.write('3. Zapremina komore:')
  st.markdown('$V_{kom} = L_{kar} \cdot A_{kr}$')
  st.markdown(f'$ V_{{kom}} = {Lkar:.3f} \, \cdot \, {Akr:.3f} = {Vkom:.3f} \\, m^3 $')
  spacer()

  # 4. Chamber Diameter and Length
  dk = dkr * d_dkdr
  lk = Vkom / (dk**2 * 3.14159 / 4)
  st.write('4. Precnik i duzina komore:')
  st.markdown('$d_{k} = d_{kr} \cdot \\frac{D_k}{d_{kr}}$')
  st.markdown(f'$ d_{{k}} = {dkr:.3f} \, \cdot \, {d_dkdr:.3f} = {dk:.3f} \\, \\text{{m}} $')
  st.markdown('$l_{k} = \\frac{V_{kom}}{\\frac{d_{k}^2 \cdot \\pi}{4}}$')
  # st.markdown(f'$ l_{{k}} = \\frac{{{Vkom:.3f}}}{{\\frac{{{dk:.3f}}^2 \cdot \\pi}}{{4}}}} = {lk:.3f} \\, \\text{{m}} $')
  st.markdown(f'$ l_{{k}} = \\frac{{ {Vkom:.3f} }}{{ \\frac{{ {dk:.3f}^2 \cdot \\pi }}{{ 4 }} }} = {lk:.3f} \\, \\text{{m}} $')

  spacer()

  # 5. Nozzle Exit Area and Diameter
  Ai = epsilon_i * Akr
  di = (Ai * 4 / 3.14159)**0.5
  st.write('5. Izlazni presek i precnik mlaznika:')
  st.markdown('$A_{i} = \\epsilon_i \cdot A_{kr}$')
  st.markdown(f'$ A_{{i}} = {epsilon_i:.3f} \, \cdot \, {Akr:.3f} = {Ai:.3f} \\, \\text{{m^2}} $')
  st.markdown('$d_{i} = \\sqrt{\\frac{A_{i} \cdot 4}{\\pi}}$')

  st.markdown(f'$ d_{{i}} = \\sqrt{{\\frac{{{Ai:.3f} \\cdot 4}}{{\\pi}}}} = {di:.3f} \\, \\text{{m}} $')
  # st.markdown(f'$ d_{{i}} = \\sqrt{{{{\\frac{{ {Ai:.3f} \\cdot 4 }}{{ \\pi }}}}}} = {di:.3f} \\, \\text{{m}} $')

  # 6. Determining Mach number at nozzle exit
  st.header("TODO M_iter")

  # 7. Staticki pritisak na izlazu iz mlaznika
  M_i = 2.9
  pi = P / ((1 + (kappa - 1) / 2 * M_i**2)**(kappa / (kappa - 1)))
  st.write('7. Statički pritisak na izlazu iz mlaznika:')
  st.markdown(r'''
      $ p_i = \frac{P}{
      \left(1 + \frac{\kappa - 1}{2} \cdot M_i^2\right)^{\frac{\kappa}{\kappa - 1}}
      } $
  ''')
  st.markdown(f'$ p_i = {pi:.2e} \\, \\text{{Pa}} $')
  spacer()



if __name__ == "__main__":
  main()
