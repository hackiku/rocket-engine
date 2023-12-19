import streamlit as st
from utils import spacer
# from transcendental_epsilon_mi_opt import *

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

  with st.sidebar:
  # Inputs for the variables
    st.title("Ulazni podaci")
    mg = st.number_input('Maseni protok goriva (mg)', value=1.0)
    OF = st.number_input('Odnos mesanja oksidator/gorivo (OF)', value=5.0)
    st.markdown('***')
    P = st.number_input('(2) Pritisak u komori (P)', value=100.0 * (10**5))
    Pa = st.number_input('(3) Atmosferski pritisak (Pa)', value=101325)
    F = st.number_input('(4) Sila potiska', value = 2200)
    epsilon_i = st.number_input('(5) Stepen sirenja mlaznika (epsilon_i)', value=6.0)
    d_dkdr = st.number_input('(6) Odnos precnika komore i grla mlaznika (d_dkdr)', value=3)
    Lkar = st.number_input('(7) Karakteristicna duzina (Lkar)', value=1.0)
    st.subheader('vrednosti is RPA')  
    Cstar = st.number_input('Karakteristicna brzina (Cstar)', value=2000.0)
    R = st.number_input('Gasna konstanta (R)', value=546.0)
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
  st.write('5. Izlazni presek i precnik mlaznika:')
  Ai = epsilon_i * Akr
  di = (Ai * 4 / 3.14159)**0.5
  st.markdown('$A_{i} = \\epsilon_i \cdot A_{kr}$')
  st.markdown(f'$ A_{{i}} = {epsilon_i:.3f} \\cdot {Akr:.3f} = {Ai:.5f} \\, \\text{{m}}^{{2}} $')
  st.markdown('$d_{i} = \\sqrt{\\frac{A_{i} \cdot 4}{\\pi}}$')
  st.markdown(f'$ d_{{i}} = \\sqrt{{\\frac{{{Ai:.3f} \\cdot 4}}{{\\pi}}}} = {di:.3f} \\, \\text{{m}} $')

  # 6. Determining Mach number at nozzle exit
  st.write('Odredjivanje Mahovog broja na izlazu mlaznika')
  st.subheader("TODO M_iter")
  
  st.markdown(r'''
      $ \epsilon_{i opt} = \frac{
      \left(1 + \frac{\kappa - 1}{2} \cdot M_{iter}^2\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
      }{
      M_{iter} \left(\frac{\kappa + 1}{2}\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
      } $
  ''')

  # 7. Staticki pritisak na izlazu iz mlaznika
  M_i = st.number_input("M_i value", value=2.917)
  
  pi = P / ((1 + (kappa - 1) / 2 * M_i**2)**(kappa / (kappa - 1)))
  st.write('7. Statički pritisak na izlazu iz mlaznika:')
  st.markdown(r'''
      $ p_i = \frac{P}{
      \left(1 + \frac{\kappa - 1}{2} \cdot M_i^2\right)^{\frac{\kappa}{\kappa - 1}}
      } $
  ''')
  st.markdown(f'''
    $ p_i = \\frac{{{P:.2e}}}{{\\left(1 + \\frac{{{kappa} - 1}}{{2}} \cdot {M_i:.2f}^2\\right)^{{\\frac{{{kappa}}}{{{kappa} - 1}}}}}} = {pi:.3f} \\, \\text{{Pa}} $
  ''')

  spacer()

  # Optimalni stepen sirenja mlaznika
  Mi_opt = (((P/Pa)**((kappa - 1)/kappa) - 1) * (2/(kappa - 1)))**0.5

  st.write('8. Optimalni stepen sirenja mlaznika (do atmosferskog pritiska od 1bar) i njemu odgovarajuci izlazni precnik:')
  st.markdown(r'''
  $$ M_{i \text{ opt}} = \sqrt{\left[\left(\frac{P}{P_a}\right)^{\frac{\kappa - 1}{\kappa}} - 1\right] \cdot \frac{2}{\kappa - 1}} $$
  ''')
  st.markdown(f'$ M_{{i opt}} = \\sqrt{{\\left[\\left(\\frac{{{P:.2e}}}{{{Pa:.2e}}}\\right)^{{\\frac{{{kappa} - 1}}{{{kappa}}}}} - 1\\right] \\cdot \\frac{{2}}{{{kappa} - 1}}}} = {Mi_opt:.3f} $')

  spacer()

  # 9. Calculate the optimal expansion ratio (e_i opt)
  e_i_opt = (1 + (kappa - 1)/2 * Mi_opt**2)**((kappa + 1)/(2 * (kappa - 1))) / Mi_opt / ((kappa + 1)/2)**((kappa + 1)/(2 * (kappa - 1)))
  st.write('9. Optimalni ekspanzioni odnos:')
  st.markdown(r'''
      $ \epsilon_{i opt} = \frac{
      \left(1 + \frac{\kappa - 1}{2} \cdot M_{i opt}^2\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
      }{
      M_{i opt} \left(\frac{\kappa + 1}{2}\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
      } $
  ''')
  st.markdown(f'''
      $ \epsilon_{{i opt}} = \\frac{{
      \\left(1 + \\frac{{{kappa} - 1}}{{2}} \cdot {Mi_opt:.3f}^2\\right)^{{\\frac{{{kappa} + 1}}{{2({kappa} - 1)}}}}
      }}{{
      {Mi_opt:.3f} \cdot \\left(\\frac{{{kappa} + 1}}{{2}}\\right)^{{\\frac{{{kappa} + 1}}{{2({kappa} - 1)}}}}
      }} = {e_i_opt:.3f} $
  ''')

  spacer()

  # Calculate optimal nozzle exit area
  Aiopt = e_i_opt * Akr
  st.write('Optimal Nozzle Exit Area:')
  st.markdown(r'''
      $$ A_{opt} = \epsilon_{i opt} \cdot A_{kr} $$
  ''')
  st.markdown(f'''
      $ A_{{opt}} = {e_i_opt:.3f} \cdot {Akr:.3f} = {Aiopt:.3f} \\, \\text{{m}}^2 $
  ''')
  spacer()

  # Calculate optimal nozzle exit diameter
  diopt = (Aiopt * 4 / 3.14159)**0.5
  st.write('Optimal Nozzle Exit Diameter:')
  st.markdown(r'''
      $$ d_{iopt} = \sqrt{A_{iopt} \cdot \frac{4}{\pi}} $$
  ''')
  st.markdown(f'''
      $ d_{{iopt}} = \sqrt{{ {Aiopt:.3f} \\cdot \\frac{{4}}{{\\pi}} }} = {diopt:.3f} \\, \\text{{m}}^2 $
  ''')
  spacer()

  # Calculation of the temperature function Gamma(kappa)
  st.write('Totalna temperatura u komori:')
  st.markdown(r'''
      $$ \Gamma(\kappa) = \sqrt{\kappa} \left( \frac{2}{\kappa + 1} \right)^{\frac{\kappa + 1}{2(\kappa - 1)}} $$
  ''')
  Gamma_kappa = (kappa**0.5) * ((2 / (kappa + 1))**((kappa + 1)/(2 * (kappa - 1))))
  st.markdown(f'''
      $ \Gamma(\kappa) = \sqrt{{ {kappa} }} \\left( \\frac{{2}}{{ {kappa} + 1 }} \\right)^{{\\frac{{ {kappa} + 1 }}{{2( {kappa} - 1)}}}} = {Gamma_kappa:.3f} $
  ''')

  # Calculation of the total temperature in the chamber T
  T = (Cstar * Gamma_kappa)**2 / R
  st.markdown(r'''
      $$ T = \frac{(C_{star} \cdot \Gamma(k))^2}{R} $$
  ''')
  st.markdown(f'''
      $ T = \\frac{{({Cstar:.3f} \\cdot {Gamma_kappa:.3f})^2}}{{{R:.3f}}} = {T:.3f} \\, \\text{{K}} $
  ''')
  
  spacer()

  # brzina isticanja pri zadanom i optimalnom stepenu sirenja
  st.write("Brzina isticanja pri zadanom i optimalnom stepenu sirenja")
  Vi = (2*kappa/(kappa-1) * R * T * (1 - 1/((P/pi)**((kappa-1)/kappa))))**0.5
  st.markdown(r'''
      $$ V_i = \sqrt{ \frac{2 \kappa}{\kappa - 1} \cdot R \cdot T \cdot \left[ 1 - \frac{1}{\left(\frac{P}{p_i}\right)^{\frac{\kappa - 1}{\kappa}}} \right] } $$
  ''')
  st.markdown(f'''
      $ V_i = \sqrt{{ \\frac{{2 \cdot {kappa}}}{{ {kappa} - 1 }} \cdot {R} \cdot {T:.3f} \cdot \\left[ 1 - \\frac{{1}}{{\\left(\\frac{{ {P} }}{{ {pi:.3f} }}\\right)^{{\\frac{{ {kappa} - 1 }}{{ {kappa} }}}}}} \\right] }}  = {Vi:.3f} \\, \\text{{m/s}} $
  ''')

  Vi_opt = (2*kappa/(kappa-1) * R * T * (1 - 1/((P/Pa)**((kappa-1)/kappa))))**0.5
  st.markdown(r'''
      $$ V_{iopt} = \sqrt{ \frac{2 \kappa}{\kappa - 1} \cdot R \cdot T \cdot \left[ 1 - \frac{1}{\left(\frac{P}{p_i}\right)^{\frac{\kappa - 1}{\kappa}}} \right] } $$
  ''')
  st.markdown(f'''
      $ V_{{iopt}} = \sqrt{{ \\frac{{2 \cdot {kappa}}}{{ {kappa} - 1 }} \cdot {R} \cdot {T:.3f} \cdot \\left[ 1 - \\frac{{1}}{{\\left(\\frac{{ {P} }}{{ {Pa:.3f} }}\\right)^{{\\frac{{ {kappa} - 1 }}{{ {kappa} }}}}}} \\right] }}  = {Vi_opt:.3f} \\, \\text{{m/s}} $
  ''')

  # Thrust at given expansion ratio
  st.write('Potisak pri zadanom stepenu sirenja:')
  F = (mox + mg) * Vi + Ai * (pi - Pa)
  st.markdown(r'''
      $$ F = (m_{ox} + m_{g}) \cdot V_{i} + A_{i} \cdot (p_{i} - p_{a}) $$
  ''')
  st.markdown(f'''
      $ F = ({mox:.3f} + {mg:.3f}) \cdot {Vi:.3f} + {Ai:.3f} \cdot ({pi:.3f} - {Pa:.3f}) = {F:.3f} \\, \\text{{N}} $
  ''')
  spacer()

  # Thrust at optimal expansion ratio
  st.write('Potisak pri optimalnom stepenu sirenja:')
  Fopt = (mox + mg) * Vi_opt
  st.markdown(r'''
      $$ F_{opt} = (m_{ox} + m_{g}) \cdot V_{iopt} $$
  ''')
  st.markdown(f'''
      $ F_{{opt}} = ({mox:.3f} + {mg:.3f}) \cdot {Vi_opt:.3f} = {Fopt:.3f} \\, \\text{{N}} $
  ''')
  spacer()

  # Thrust Coefficient
  st.write('Koeficijent potiska:')
  Cf = F / (P * Akr)
  st.markdown(r'''
      $$ C_f = \frac{F}{P \cdot A_{kr}} $$
  ''')
  st.markdown(f'''
      $ C_f = \\frac{{ {F:.3f} }}{{ {P:.3f} \\cdot {Akr:.5f} }} = {Cf:.3f} $
  ''')
  spacer()

  # Specific Impulse at Given Expansion Ratio
  st.write('Specifični impuls pri zadanom stepenu sirenja:')
  Isp = F / (mox + mg)
  st.markdown(r'''
      $$ I_{sp} = \frac{F}{(m_{ox} + m_{g})} $$
  ''')
  st.markdown(f'''
      $ I_{{sp}} = \\frac{{ {F:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp:.3f} \\, \\text{{s}} $
  ''')
  spacer()

  # Specific Impulse at Optimal Expansion Ratio
  st.write('Specifični impuls pri optimalnom stepenu sirenja:')
  Isp_opt = Fopt / (mox + mg)
  st.markdown(r'''
      $$ I_{sp_{opt}} = \frac{F_{opt}}{(m_{ox} + m_{g})} $$
  ''')
  st.markdown(f'''
      $ I_{{sp_{{opt}}}} = \\frac{{ {Fopt:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp_opt:.3f} \\, \\text{{s}} $
  ''')
  spacer()

if __name__ == "__main__":
  main()
