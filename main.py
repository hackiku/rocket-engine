import streamlit as st
from utils import spacer
from scipy.optimize import fsolve
import re

# regex pattern for extracting values from RPA response
def extract_values(rpa_response):
    patterns = {
        'isp': r"Specific impulse \(vac\):\s+([\d.]+)\s+s",
        'cf': r"Thrust coefficient:\s+([\d.]+)\s+",
        'thrust_vac': r"Chamber thrust \(vac\):\s+([\d.]+)\s+kN",
        'isp_opt': r"Specific impulse \(opt\):\s+([\d.]+)\s+s",
        'ox_flow_rate': r"Oxidizer mass flow rate:\s+([\d.]+)\s+kg/s",
        'fuel_flow_rate': r"Fuel mass flow rate:\s+([\d.]+)\s+kg/s"
    }

    values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, rpa_response)
        if match:
            values[key] = float(match.group(1))
        else:
            st.error(f"Could not find the value for {key.replace('_', ' ').title()}.")
            return None

    return values



def main():

    # intro
    st.image('./assets/Logo_masinski_fakultet.jpg', width=100)
    st.title("Raketni motori: seminarski rad")
    st.subheader("Ivan Karaman, 1186/23")
    spacer()
    st.write('Na osnovu definisanih ulaznih parametara potrebno je da se odrede performanse idealnog raketnog motora na tečno gorivo: specifični impuls, karakteristična brzina, koeficijent potiska, kao i preliminarna geometrija komore i mlaznika. Proračun uraditi za odnos mešanja koji odgovaraja maksimalnom specifičnom impulsu pomoću programa RPA, a zatim ručno izračunati iste vrednosti koristeći vrednosti karakteristične brzine i osobina produkata sagorevanja iz programa.')
    
    st.markdown('***')
    
    # propellant selector
    # TODO - call RPA scripts/API to load output
    
    propellant_options = ["Hidrazin / Tečni kiseonik"]
    selected_fuel = st.selectbox("Izabrati kombinaciju Gorivo/Oksidator", propellant_options)
    
    st.code('''# 1. Oksidator/gorivo: tečni kiseonik / hidrazin
# 2. Pritisak u komori: 𝑝 = 180 𝑏𝑎𝑟
# 3. Atmosferski pritisak: 𝑝𝑎 = 1 𝑎𝑡𝑚
# 4. Sila potiska: 𝐹 = 2200 𝑑𝑎𝑁
# 5. Stepen širenja: 𝜀 = 7
# 6. Odnost prečnika komore i grla mlaznika Dk/dkr=3
# 7. Karakteristična dužina L*=1m''')
  
    # RPA output        
    rpa_response = """Thrust and mass flow rates
------------------------------------------
   Chamber thrust (vac):   22.53030     kN
 Specific impulse (vac):  321.23033      s
   Chamber thrust (opt):   20.47012     kN
 Specific impulse (opt):  291.85683      s
   Total mass flow rate:    7.15204   kg/s
Oxidizer mass flow rate:    4.14013   kg/s
    Fuel mass flow rate:    3.01191   kg/s

Geometry of thrust chamber with truncated ideal contour (TIC) nozzle
(designed using method of characteristics)
------------------------------------------
    Dc =   80.02  mm       b =   30.00 deg
    R2 =   14.67  mm      R1 =    0.36  mm
    L* = 1000.00  mm
    Lc =  169.87  mm    Lcyl =  123.29  mm
    Dt =   30.88  mm
    Rn =   11.80  mm      Tn =   21.08 deg (max)
    Le =  100.66  mm      Te =    6.17 deg
    De =   81.71  mm
 Ae/At =    7.00    
 Le/Dt =    3.26    
Le/c15  =  105.28 % (relative to length of cone nozzle with Te=15 deg)

  Mass =    9.91  kg

                  Tw/T0:    0.20000       
  Divergence efficiency:    1.00000       
        Drag efficiency:    0.97848       
     Thrust coefficient:    1.67237  (vac)
"""
    # display RPA output
    st.code(rpa_response)
    
    # st.balloons()
    
    # regex pattern for extracting values from RPA response
    values = extract_values(rpa_response)

    if values:
        isp = values['isp']
        cf = values['cf']
        thrust_vac = values['thrust_vac']
        isp_opt = values['isp_opt']
        ox_flow_rate = values['ox_flow_rate']
        fuel_flow_rate = values['fuel_flow_rate']
        
        # Now you can use these variables in your code
        st.text(f"Isp (vac) = {isp} s")
        st.text(f"Cf (vac) = {cf}")
        st.text(f"Chamber Thrust (vac) = {thrust_vac} kN")
        st.text(f"Specific Impulse (opt) = {isp_opt} s")
        st.text(f"Oxidizer Mass Flow Rate = {ox_flow_rate} kg/s")
        st.text(f"Fuel Mass Flow Rate = {fuel_flow_rate} kg/s")
    
    Cstar_rpa = (thrust_vac * 1000) / ((ox_flow_rate + fuel_flow_rate) * cf)
    st.success(f"Cstar (vac) = {Cstar_rpa:.0f} m/s")
    of_rpa = ox_flow_rate / fuel_flow_rate
    st.write(f"OF = {of_rpa:.3f}")
    
    st.subheader("Ulazni podaci iz RPA")
    col1, col2 = st.columns(2)
    with col1:
        st.code('vrednosti iz RPA')
        mg = st.number_input('Maseni protok goriva (mg)', value=fuel_flow_rate, step=1.0) 
        OF = st.number_input('Odnos mesanja oksidator/gorivo (OF)', value=of_rpa, step=1.0)
        mox = st.number_input('Maseni protok oksidatora (mox)', value=ox_flow_rate, step=1.0)
        # propellant.components.ratio.value = 5.9
    with col2:
        st.code('vrednosti iz RPA')
        Cstar = st.number_input('Karakteristicna brzina (Cstar)', value=Cstar_rpa, step=100.0)
        R = st.number_input('Gasna konstanta (R)', value=380.4, step=1.0)
        kappa = st.number_input('Odnos specificnih toplota pri konstantnom pritisku i zapremini (kappa)', value=1.2022)

    st.markdown('***')
        
    with st.sidebar:
        # Inputs for the variables
        st.title("Ulazni podaci (analitika)")
        
        Pa_atm = st.number_input('2️⃣ Atmosferski pritisak (atm)', value=1)
        Pa = Pa_atm * 101325
        st.text(f'P = {Pa} = {Pa:.1e} Pa')
        P_bar = st.number_input('3️⃣ Pritisak u komori (bar)', value=180)
        P = P_bar * 100000
        st.text(f'P = {P} Pa = {P:.1e} Pa')  # Display chamber pressure in Pascals with both formats

        F = st.number_input('(4) Sila potiska kN', value = 22)
        epsilon_i = st.number_input('(5) Stepen sirenja mlaznika (epsilon_i)', value=7.0)
        d_dkdr = st.number_input('(6) Odnos precnika komore i grla mlaznika (d_dkdr)', value=3.0)
        Lstar = st.number_input('(7) Karakteristicna duzina (Lstar)', value=1.0, step=1.0)
        # st.markdown('***')
    
    
    #--------------calculations-------------------------#
    st.title('Analitičko rešenje')

    # mox
    # mox = OF * mg
    mox = 4.14013
    st.code('1. Maseni protok oksidatora:')
    st.markdown('$m_{ox} = OF \cdot mg$')
    st.markdown(f'$ m_{{ox}} = {OF:.0f} \cdot {mg:.3f} = {mox:.3f} \\, \\text{{kg/s}} $', unsafe_allow_html=True)
    spacer()

    # Akr
    Akr = Cstar * (mg + mox) / P
    dkr = (Akr * 4 / 3.14159)**0.5
    st.code('2. Kriticni presek i precnik mlaznika:')
    st.markdown('$A_{kr} = \\frac{C_{star} \cdot (mg + m_{ox})}{P}$')
    st.markdown(f'$ A_{{kr}} = \\frac{{ {Cstar:.3f} \, \cdot \, ({mg:.3f} + {mox:.3f}) }}{{ {P:.3f} }} = {Akr:.3f} \\, m^2 $')
    spacer('2em')
    st.markdown('$d_{kr} = \\sqrt{A_{kr} \cdot \\frac{4}{\\pi}}$')
    st.markdown(f'$ d_{{kr}} = \\sqrt{{{Akr:.3f} \cdot \\frac{{4}}{{\\pi}}}} = {dkr:.3f} \\, \\text{{m}} $', unsafe_allow_html=True)
    spacer()

    # Vkom
    Vkom = Lstar * Akr
    st.code('3. Zapremina komore:')
    st.markdown('$V_{kom} = L_{kar} \cdot A_{kr}$')
    st.markdown(f'$ V_{{kom}} = {Lstar:.3f} \, \cdot \, {Akr:.3f} = {Vkom:.3f} \\, m^3 $')
    spacer()

    # 4. Chamber Diameter and Length
    d_dkdr = 80.02 / 30.88
    dk = dkr * d_dkdr
    lk = Vkom / (dk**2 * 3.14159 / 4)
    st.code('4. Precnik i duzina komore')
    st.markdown('$d_{k} = d_{kr} \cdot \\frac{D_k}{d_{kr}}$')
    st.markdown(f'$ d_{{k}} = {dkr:.3f} \, \cdot \, {d_dkdr:.3f} = {dk:.3f} \\, \\text{{m}} $')
    st.markdown('$l_{k} = \\frac{V_{kom}}{\\frac{d_{k}^2 \cdot \\pi}{4}}$')
    # st.markdown(f'$ l_{{k}} = \\frac{{{Vkom:.3f}}}{{\\frac{{{dk:.3f}}^2 \cdot \\pi}}{{4}}}} = {lk:.3f} \\, \\text{{m}} $')
    st.markdown(f'$ l_{{k}} = \\frac{{ {Vkom:.3f} }}{{ \\frac{{ {dk:.3f}^2 \cdot \\pi }}{{ 4 }} }} = {lk:.3f} \\, \\text{{m}} $')

    spacer()

    # 5. Nozzle Exit Area and Diameter
    st.code('5. Izlazni presek i precnik mlaznika')
    Ai = epsilon_i * Akr
    di = (Ai * 4 / 3.14159)**0.5
    st.markdown('$A_{i} = \\epsilon_i \cdot A_{kr}$')
    st.markdown(f'$ A_{{i}} = {epsilon_i:.3f} \\cdot {Akr:.3f} = {Ai:.5f} \\, \\text{{m}}^{{2}} $')
    st.markdown('$d_{i} = \\sqrt{\\frac{A_{i} \cdot 4}{\\pi}}$')
    st.markdown(f'$ d_{{i}} = \\sqrt{{\\frac{{{Ai:.3f} \\cdot 4}}{{\\pi}}}} = {di:.3f} \\, \\text{{m}} $')

    # -----------------fsolve---------------------#
    # mach
    st.markdown('***') 
    st.code('Odredjivanje Mahovog broja na izlazu mlaznika')

    st.markdown(r'''
        $ \epsilon_{i opt} = \frac{
        \left(1 + \frac{\kappa - 1}{2} \cdot M_{iter}^2\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
        }{
        M_{iter} \left(\frac{\kappa + 1}{2}\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
        } $
    ''')
    
    # fsolve
    def equation(Mi, kappa, epsilon_i):
        epsilon_i_opt_numerator = (1 + (kappa - 1) / 2 * Mi**2)**((kappa + 1) / (2 * (kappa - 1)))
        epsilon_i_opt_denominator = Mi * ((kappa + 1) / 2)**((kappa + 1) / (2 * (kappa - 1)))
        return epsilon_i_opt_numerator / epsilon_i_opt_denominator - epsilon_i

    Mi_guess = 28

    Mi_solution = fsolve(equation, Mi_guess, args=(kappa, epsilon_i))

    # Output the result - Mi value
    st.code(f"The solution for Mi is: {Mi_solution[0]}")
    M_i = st.number_input("M_i value", value=Mi_solution[0], step=1.00)

    pi = P / ((1 + (kappa - 1) / 2 * M_i**2)**(kappa / (kappa - 1)))
    st.code('7. Statički pritisak na izlazu iz mlaznika:')
    st.markdown(r'''
        $ p_i = \frac{P}{
        \left(1 + \frac{\kappa - 1}{2} \cdot M_i^2\right)^{\frac{\kappa}{\kappa - 1}}
        } $
    ''')
    st.markdown(f'''
    $ p_i = \\frac{{{P:.2e}}}{{\\left(1 + \\frac{{{kappa} - 1}}{{2}} \cdot {M_i:.3f}^2\\right)^{{\\frac{{{kappa}}}{{{kappa} - 1}}}}}} = {pi:.3f} \\, \\text{{Pa}} $
    ''')

    spacer()

    # Optimalni stepen sirenja mlaznika
    Mi_opt = (((P/Pa)**((kappa - 1)/kappa) - 1) * (2/(kappa - 1)))**0.5

    st.code('8. Optimalni stepen sirenja mlaznika (do atmosferskog P od 1 bar)')
    st.markdown(r'''
    $$ M_{i \text{ opt}} = \sqrt{\left[\left(\frac{P}{P_a}\right)^{\frac{\kappa - 1}{\kappa}} - 1\right] \cdot \frac{2}{\kappa - 1}} $$
    ''')
    st.markdown(f'$ M_{{i opt}} = \\sqrt{{\\left[\\left(\\frac{{{P:.2e}}}{{{Pa:.2e}}}\\right)^{{\\frac{{{kappa} - 1}}{{{kappa}}}}} - 1\\right] \\cdot \\frac{{2}}{{{kappa} - 1}}}} = {Mi_opt:.3f} $')

    spacer()

    # 9. Calculate the optimal expansion ratio (e_i opt)
    e_i_opt = (1 + (kappa - 1)/2 * Mi_opt**2)**((kappa + 1)/(2 * (kappa - 1))) / Mi_opt / ((kappa + 1)/2)**((kappa + 1)/(2 * (kappa - 1)))
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
    st.markdown(r'''
    $$ A_{opt} = \epsilon_{i opt} \cdot A_{kr} $$
    ''')
    st.markdown(f'''
        $ A_{{opt}} = {e_i_opt:.3f} \cdot {Akr:.3f} = {Aiopt:.3f} \\, \\text{{m}}^2 $
    ''')
    spacer()

    # Calculate optimal nozzle exit diameter
    st.code('izlazni precnik')
    diopt = (Aiopt * 4 / 3.14159)**0.5
    st.markdown(r'''
    $$ d_{iopt} = \sqrt{A_{iopt} \cdot \frac{4}{\pi}} $$
    ''')
    st.markdown(f'''
        $ d_{{iopt}} = \sqrt{{ {Aiopt:.3f} \\cdot \\frac{{4}}{{\\pi}} }} = {diopt:.3f} \\, \\text{{m}}^2 $
    ''')
    spacer()

    # Calculation of the temperature function Gamma(kappa)
    st.code('9. Totalna temperatura u komori')
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
    st.code("10. Brzina isticanja pri zadanom i optimalnom stepenu sirenja")
    Vi = (2*kappa/(kappa-1) * R * T * (1 - 1/((P/pi)**((kappa-1)/kappa))))**0.5
    st.markdown(r'''
        $$ V_i = \sqrt{ \frac{2 \kappa}{\kappa - 1} \cdot R \cdot T \cdot \left[ 1 - \frac{1}{\left(\frac{P}{p_i}\right)^{\frac{\kappa - 1}{\kappa}}} \right] } $$
    ''')
    st.markdown(f'''
        $ V_i = \sqrt{{ \\frac{{2 \cdot {kappa}}}{{ {kappa} - 1 }} \cdot {R} \cdot {T:.3f} \cdot \\left[ 1 - \\frac{{1}}{{\\left(\\frac{{ {P} }}{{ {pi:.3f} }}\\right)^{{\\frac{{ {kappa} - 1 }}{{ {kappa} }}}}}} \\right] }}  = {Vi:.3f} \\, \\text{{m/s}} $
    ''')

    Vi_opt = (2*kappa/(kappa-1) * R * T * (1 - 1/((P/Pa)**((kappa-1)/kappa))))**0.5
    st.markdown(r'''
        $$ V_{iopt} = \sqrt{ \frac{2 \kappa}{\kappa - 1} \cdot R \cdot T \cdot \left[ 1 - \frac{1}{\left(\frac{P}{p_a}\right)^{\frac{\kappa - 1}{\kappa}}} \right] } $$
    ''')
    st.markdown(f'''
        $ V_{{iopt}} = \sqrt{{ \\frac{{2 \cdot {kappa}}}{{ {kappa} - 1 }} \cdot {R} \cdot {T:.3f} \cdot \\left[ 1 - \\frac{{1}}{{\\left(\\frac{{ {P} }}{{ {Pa:.3f} }}\\right)^{{\\frac{{ {kappa} - 1 }}{{ {kappa} }}}}}} \\right] }}  = {Vi_opt:.3f} \\, \\text{{m/s}} $
    ''')

    # Thrust at given expansion ratio
    st.code('11. Potisak pri zadanom stepenu sirenja')
    F = (mox + mg) * Vi + Ai * (pi - Pa)
    st.markdown(r'''
        $$ F = (m_{ox} + m_{g}) \cdot V_{i} + A_{i} \cdot (p_{i} - p_{a}) $$
    ''')
    st.markdown(f'''
        $ F = ({mox:.3f} + {mg:.3f}) \cdot {Vi:.3f} + {Ai:.3f} \cdot ({pi:.3f} - {Pa:.3f}) = {F:.3f} \\, \\text{{N}} $
    ''')
    spacer()

    # Thrust at optimal expansion ratio
    Fopt = (mox + mg) * Vi_opt
    st.markdown(r'''
        $$ F_{opt} = (m_{ox} + m_{g}) \cdot V_{iopt} $$
    ''')
    st.markdown(f'''
        $ F_{{opt}} = ({mox:.3f} + {mg:.3f}) \cdot {Vi_opt:.3f} = {Fopt:.3f} \\, \\text{{N}} $
    ''')
    spacer()

    # Thrust Coefficient
    st.code('12. Koeficijent potiska')
    Cf = F / (P * Akr)
    st.markdown(r'''
        $$ C_f = \frac{F}{P \cdot A_{kr}} $$
    ''')
    st.markdown(f'''
        $ C_f = \\frac{{ {F:.3f} }}{{ {P:.3f} \\cdot {Akr:.5f} }} = {Cf:.3f} $
    ''')
    spacer()

    # Specific Impulse at Given Expansion Ratio
    st.write('13. Specifični impuls pri zadanom stepenu sirenja')
    Isp = F / (mox + mg)
    st.markdown(r'''
        $$ I_{sp} = \frac{F}{(m_{ox} + m_{g})} $$
    ''')
    st.markdown(f'''
        $ I_{{sp}} = \\frac{{ {F:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp:.3f} \\, \\text{{Ns/Kg}} $
    ''')
    spacer()

    # Specific Impulse at Optimal Expansion Ratio
    st.write('Specifični impuls pri optimalnom stepenu sirenja:')
    Isp_opt = Fopt / (mox + mg)
    st.markdown(r'''
        $$ I_{sp_{opt}} = \frac{F_{opt}}{(m_{ox} + m_{g})} $$
    ''')
    st.markdown(f'''
        $ I_{{sp_{{opt}}}} = \\frac{{ {Fopt:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp_opt:.3f} \\, \\text{{Ns/kg}} $
    ''')
    spacer()

    st.markdown(f"""| Parameter                      | Raw RPA regex    | RPA Value         | Calculated Value   |
|--------------------------------|------------------|-------------------|--------------------|
| Specific Impulse (Vac)         | `321.23033 s`    | `{isp} s`         | `{Isp/9.80665} Ns/Kg`       |
| Thrust Coefficient (Vac)       | `1.67237`        | `{cf}`            | `{Cf}`          |
| Chamber Thrust (Vac)           | `22.53030 kN`    | `{thrust_vac} kN` | `{F} kN`|
| Specific Impulse (Opt)         | `291.85683 s`    | `{isp_opt} s`     | `{Isp_opt/9.80665} s`   |
| Oxidizer/Fuel Ratio (OF)       | `{of_rpa:.3f}`   | `{OF}`            | `{OF}`          |

""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
