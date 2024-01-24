import streamlit as st
from utils import spacer
from scipy.optimize import fsolve
import re
import inspect

def format_scientific_latex(number, precision=3):
    """
    Format a number into scientific notation with LaTeX formatting.

    Args:
    number (float): The number to format.
    precision (int): The number of decimal places.

    Returns:
    str: Formatted string in scientific notation.
    """
    # Format to scientific notation with specified precision
    formatted_number = f"{number:.{precision}e}"

    # Split at 'e' and reconstruct with LaTeX-friendly format
    number_parts = formatted_number.split('e')
    return f"{number_parts[0]} \\times 10^{{{number_parts[1]}}}"


# regex patterns for extracting values from RPA response
patterns = {
    'isp': r"Specific impulse \(vac\):\s+([\d.]+)\s+s",
    'cf': r"Thrust coefficient:\s+([\d.]+)\s+",
    'thrust_vac': r"Chamber thrust \(vac\):\s+([\d.]+)\s+kN",
    'thrust_opt': r"Chamber thrust \(opt\):\s+([\d.]+)\s+kN",
    'isp_opt': r"Specific impulse \(opt\):\s+([\d.]+)\s+s",
    'ox_flow_rate': r"Oxidizer mass flow rate:\s+([\d.]+)\s+kg/s",
    'fuel_flow_rate': r"Fuel mass flow rate:\s+([\d.]+)\s+kg/s",
    'dc': r"Dc =\s+([\d.]+)\s+mm",
    'dt': r"Dt =\s+([\d.]+)\s+mm",
    'de': r"De =\s+([\d.]+)\s+mm",
    'lc': r"Lc =\s+([\d.]+)\s+mm",
    'le': r"Le =\s+([\d.]+)\s+mm"
}

# extract RPA values with regex patterns
def extract_values(rpa_response):
    values = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, rpa_response)
        if match:
            values[key] = float(match.group(1))
        else:
            st.error(f"Could not find the value for {key.replace('_', ' ').title()}.")
            return None
    return values

# validate user-submitted RPA output
def validate_rpa_output(output):
    validation_results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            validation_results[key] = True
        else:
            validation_results[key] = False
    return validation_results


#===========================================================#
#===================== MAIN APP ============================#
#===========================================================#

def main():

    # intro
    st.image('./assets/Logo_masinski_fakultet.jpg', width=100)
    st.markdown("### Raketni motori")
    st.markdown("# Seminarski rad")
    spacer()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Student: Ivan Karaman, 1186/23")
    with col2:
        st.markdown("##### Profesor: dr Nikola Davidović")
    st.markdown('***')
    
    # problem statement
    st.markdown("### Zadatak")
    st.write('Na osnovu definisanih ulaznih parametara potrebno je da se odrede performanse idealnog raketnog motora na tečno gorivo: specifični impuls, karakteristična brzina, koeficijent potiska, kao i preliminarna geometrija komore i mlaznika. Proračun uraditi za odnos mešanja koji odgovaraja maksimalnom specifičnom impulsu pomoću programa RPA, a zatim ručno izračunati iste vrednosti koristeći vrednosti karakteristične brzine i osobina produkata sagorevanja iz programa.')
    
    st.markdown('***')
    
    #===================== RPA =====================#
    # TODO - call RPA scripts/API to load output

    # title with tooltip
    tooltip_message = "U budućim verzijama programa, planira se direktna integracija sa API-jem ili skriptom programa RPA."
    st.title("1. Korišćenje programa RPA", help=tooltip_message)
    st.markdown("""
Ova Python aplikacija koristi podatka iz programa [RPA Rocket Propulsion Analysis](https://www.rocket-propulsion.com/index.htm) za računanje performansi raketnog motora.
""")
    st.header("1.1. Ulazni podaci")
    st.markdown("""
1. Podaci u sidebar-u levo **"Zadati ulazni podaci"** ubačeni su u RPA grafički, a koriste se i za analitičko rešenje (naredna sekcija 2.). Mogu se izmeniti po potrebi, ali izmena neće uticati na izlaz iz RPA zbog nedovršene integracije za RPA API.
2. **Ulazni podaci iz RPA** u sidebar-u dobijeni iz izlaza RPA, ali se mogu izmeniti po potrebi za testiranje analitičkog rešenja (npr. ako se želi izračunati drugačiji odnos mešanja goriva i oksidatora)
3. Kombinacija gorivo/oksidator data je u dropdown meniju ispod. Za sad postoji samo jedna opcija, ali se planira integracija sa API-jem ili skriptom programa RPA u budućim verzijama ovog Python programa kako bi korisnici mogli direktno interagovati sa RPA odavde)
""")

    if st.button("Screenshot-ovi iz RPA"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image('./assets/engine_definition.png', width=200)
        with col2:
            st.image('./assets/engine_definition.png', width=200)
        with col3:
            st.image('./assets/propellant_specification.png', width=200)
    
    # RADIO options    
    
    propellant_options = ["Hidrazin / Tečni kiseonik"]
    selected_propellant = st.selectbox("Gorivo/Oksidator", propellant_options)
        
    if st.button("🖼️ Screenshot izbora goriva/oksidatora"):
        st.image('./assets/propellant_specification.png')

    st.markdown("#### Opcija 1: Iskopirati ")


    # download .cfg
    st.download_button('💾 Preuzmi RPA konfiguraciju (.cfg)', './rpa/hail_hydra2.cfg', 'hail_hydra2.cfg', 'text/plain')

    st.markdown('***')  
    #==========================================================#
    #===================== 2. OUTPUT DATA =====================#
    #==========================================================#
    
    st.header("1.2. Performanse idealnog raketnog motora")
    st.markdown("""
U ovoj sekciji aplikacije prikazani su izlazni podaci iz programa RPA. Izvlačenje numeričkih podataka iz RPA izlaza (u tekstualnom ili HTML formatu) je automatizovo, ali zbog nedovršene integracije sami izlazi su uneti manualno.
""")
    spacer()
    
    st.subheader("1.2.1. Izlaz is RPA (Engine Design)")
    
    #===================== regex output =====================#
    
    # RPA output        
    rpa_response_default = """Thrust and mass flow rates
------------------------------------------
   Chamber thrust (vac):   22.53665     kN
 Specific impulse (vac):  320.80146      s
   Chamber thrust (opt):   20.58303     kN
 Specific impulse (opt):  292.99241      s
   Total mass flow rate:    7.16362   kg/s
Oxidizer mass flow rate:    3.28718   kg/s
    Fuel mass flow rate:    3.87644   kg/s

Geometry of thrust chamber with parabolic nozzle
------------------------------------------
    Dc =   80.32  mm       b =   30.00 deg
    R2 =   80.33  mm      R1 =   23.28  mm
    L* = 1000.00  mm
    Lc =  177.26  mm    Lcyl =  106.81  mm
    Dt =   31.04  mm
    Rn =    5.93  mm      Tn =   22.42 deg
    Le =   98.33  mm      Te =    8.00 deg
    De =   82.12  mm
 Ae/At =    7.00    
 Le/Dt =    3.17    
Le/c15  =  102.33 % (relative to length of cone nozzle with Te=15 deg)

  Mass =    9.99  kg

  Divergence efficiency:    0.99157       
        Drag efficiency:    0.96223       
     Thrust coefficient:    1.66234  (vac)
"""
    if 'rpa_response' not in st.session_state:
        st.session_state['rpa_response'] = rpa_response_default
    
    if st.button("📋 Kopiraj RPA izlaz"):
        rpa_output = st.text_area("Paste RPA output here", height=300)
        if st.button("Validiraj RPA izlaz"):
            if rpa_output:
                validation_results = validate_rpa_output(rpa_output)
                if all(validation_results.values()):
                    st.success("RPA izlaz je uspešno validiran.")
                    st.session_state['rpa_response'] = rpa_output
                else:
                    st.error("RPA izlaz nije validan. Proverite sledeće vrednosti:")
                    for key, valid in validation_results.items():
                        if not valid:
                            st.write(f"Vrednost za {key} nije pronađena ili je u pogrešnom formatu.")
            else:
                st.error("Morate uneti RPA izlaz.")
    
    # display RPA output
    rpa_response = st.session_state['rpa_response']
    st.code(rpa_response)

    # regex pattern for extracting values from RPA response
    values = extract_values(rpa_response)

    st.write("Ovaj program izvlaci vrednosti iz RPA izlaza koristeci REGEX pattern za svaku vrednost. Vrednosti se mogu naci u sidebar-u levo i izmeniti po potrebi.")
    st.markdown("##### Podaci izvučeni REGEX-om:")
    
    if values:
        isp_rpa = values['isp']
        cf_rpa = values['cf']
        thrust_vac_rpa = values['thrust_vac']
        thrust_opt_rpa = values['thrust_opt']
        isp_opt_rpa = values['isp_opt']
        ox_flow_rate_rpa = values['ox_flow_rate']
        fuel_flow_rate_rpa = values['fuel_flow_rate']
        dc_rpa = values['dc'] # chamber diameter
        dt_rpa = values['dt'] # throat diameter
        de_rpa = values['de'] # exit diameter
        lc_rpa = values['lc'] # chamber length
        le_rpa = values['le'] # nozzle exit length
        
        # quick calculations for final data
        Cstar_rpa = (thrust_vac_rpa * 1000) / ((ox_flow_rate_rpa + fuel_flow_rate_rpa) * cf_rpa)
        of_rpa = ox_flow_rate_rpa / fuel_flow_rate_rpa
        
        # raw code display
        st.code(f'''
        # performanse
        Isp (vakuum) = {isp_rpa} s
        Cf (vakuum) = {cf_rpa}
        Potisak komore (vakuum) = {thrust_vac_rpa} kN
        Potisak komore (optimalni) = {thrust_opt_rpa} kN
        Specifični impuls (optimalno) = {isp_opt_rpa} s
        Protok mase oksidatora = {ox_flow_rate_rpa} kg/s
        Protok mase goriva = {fuel_flow_rate_rpa} kg/s
        # izracunate vrednosti
        Cstar (vakuum) = {Cstar_rpa:.0f} m/s # optimalni C* dat u sledecoj sekciji
        OF = {of_rpa:.3f}
        # geometrija komore
        Dc = {dc_rpa} mm # precnik komore
        Dt = {dt_rpa} mm # precnik grla mlaznika
        De = {de_rpa} mm # precnik izlaza mlaznika
        Lc = {lc_rpa} mm # duzina komore
        Le = {le_rpa} mm # duzina izlaza mlaznika
        ''')

        with st.expander("Provera raw REGEX teksta (opciono)"):
            st.code(inspect.getsource(extract_values))
            st.text(f"Isp (vac) = {isp_rpa} s")
            st.text(f"Cf (vac) = {cf_rpa}")
            st.text(f"Chamber Thrust (vac) = {thrust_vac_rpa} kN")
            st.text(f"Specific Impulse (opt) = {isp_opt_rpa} s")
            st.text(f"Oxidizer Mass Flow Rate = {ox_flow_rate_rpa} kg/s")
            st.text(f"Fuel Mass Flow Rate = {fuel_flow_rate_rpa} kg/s")
            st.write(f"OF = {of_rpa:.3f}") 
            st.success(f"Cstar (vac) = {Cstar_rpa:.0f} m/s")
            st.text(f"Dc = {dc_rpa} mm")
            st.text(f"Dt = {dt_rpa} mm")
            st.text(f"De = {de_rpa} mm")
            st.text(f"Lc = {lc_rpa} mm")
            st.text(f"Le = {le_rpa} mm")

        st.markdown('***')
    
    #===================== sidebar =====================#
    with st.sidebar:
        # Inputs for the variables
        st.title("Zadati ulazni podaci")
        
        Pa_atm = st.number_input('Atmosferski pritisak `Pa` [atm]', value=1)
        Pa = Pa_atm * 101325
        st.text(f'P = {Pa} = {Pa:.1e} Pa')
        P_bar = st.number_input('Pritisak u komori `P` [bar]', value=180)
        P = P_bar * 100000
        st.text(f'P = {P} Pa = {P:.1e} Pa')  # Display chamber pressure in Pascals with both formats

        F = st.number_input('Sila potiska `F` [kN]', value = 22)
        epsilon_i = st.number_input('Stepen sirenja mlaznika `epsilon_i`', value=7.0)
        d_dkdr = st.number_input('Precnik komore / grla mlaznika `d_dkdr`', value=3.0)
        Lstar = st.number_input('Karakteristicna duzina `Lstar` [m]', value=1.0, step=1.0)
        
        st.markdown('***') # ------------
        
        tooltip_sidebar = "vrednosti izvučene REGEX analizom RPA izlaza"
        st.title("Ulazni podaci iz RPA", help=tooltip_sidebar)
        
        mg = st.number_input('Maseni protok goriva `mg` [Kg/s]', value=fuel_flow_rate_rpa, step=1.0) 
        OF = st.number_input('Odnos mesanja oksidator/gorivo `OF`', value=of_rpa, step=1.0)
        mox = st.number_input('Maseni protok oksidatora `mox` [Kg/s]', value=ox_flow_rate_rpa, step=1.0)
        # propellant.components.ratio.value = 5.9
        Cstar = st.number_input('Karakteristicna brzina `Cstar` [m/s]', value=Cstar_rpa, step=100.0)
        R = st.number_input('Gasna konstanta `R` [J/Kg·K]', value=433.5, step=1.0, help="hidrazin/tečni kiseonik u komori, 'nozzle inlet' u RPA")
        kappa = st.number_input('Odnos specificnih toplota pri konstantnom pritisku i zapremini `kappa`', value=1.1716, format='%.4f', step=0.01, help="kappa u komori, 'nozzle inlet' u RPA")
    
    #===================== 1.2.2 PERFORMANCE =====================#
    st.subheader("1.2.2. Analiza performansi")
    
    st.markdown("Ovde su prikazane specifikacije goriva korišćenog u raketnom motoru.")
    html_file_path = './rpa/1_propellant_specification.html'
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    st.markdown(html_content, unsafe_allow_html=True)

    spacer()

    if st.button('⚠️ Prikaži ceo HTML', key='full_html', help='⚠️ Pažnja! velika HTML tabela, zauzima mnogo mesta na ekranu'):
        html_file_path = './rpa/hydra2.html'
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        st.markdown(html_content, unsafe_allow_html=True)

    # thermal
    st.markdown("#### a) Termička Analiza")
    st.markdown("Prikaz termičkih svojstava motora, uključujući temperature i toplotne tokove.")
    if st.button('Prikaži RPA Podatke - Termička Analiza', key='thermal'):
        html_file_path = './rpa/2_thermodynamic_properties.html'
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        st.markdown(html_content, unsafe_allow_html=True)

    spacer()

    # fractions combustion
    st.markdown("#### b) Sastavi Sagorevanja")
    st.markdown("Detalji o sastavima proizvoda sagorevanja i njihovim frakcijama.")
    if st.button('Prikaži RPA Podatke - Sastavi Sagorevanja', key='combustion'):
        html_file_path = './rpa/3_fractions_combustion.html'
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        st.markdown(html_content, unsafe_allow_html=True)

    spacer()

    # performance
    st.markdown("#### c) Performanse")
    st.markdown("Analiza performansi motora, uključujući specifični impuls i koeficijent potiska.")
    if st.button('Prikaži RPA Podatke - Performanse', key='performance'):
        html_file_path = './rpa/4_performance.html'
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        st.markdown(html_content, unsafe_allow_html=True)
    
    st.markdown('***')
    
    #===================== 1.2.3 GEOMETRY =====================#
    st.subheader("1.2.3. Geometrija mlaznika")
    st.image('./assets/geometry.png')
    
    #======================================================#
    #===================== ANALYTICAL =====================#
    #======================================================#
    st.markdown('***')
    
    st.title('Analitičko rešenje')
    st.markdown('**zadate vrednosti**')
    st.code('''1. Oksidator/gorivo: tečni kiseonik / hidrazin
2. Pritisak u komori: 𝑝 = 180 𝑏𝑎𝑟
3. Atmosferski pritisak: 𝑝𝑎 = 1 𝑎𝑡𝑚
4. Sila potiska: 𝐹 = 22 𝑑𝑎𝑁
5. Stepen širenja: 𝜀 = 7
6. Odnost prečnika komore i grla mlaznika Dk/dkr = 3
7. Karakteristična dužina L* = 1m''')
#    Protok mase oksidatora = {ox_flow_rate_rpa} kg/s
#         Protok mase goriva = {fuel_flow_rate_rpa

    # 1. Akr ==============================
    st.code('1. Kriticni presek i precnik mlaznika:')
    dkr = dt_rpa/1000 # throat area in meters
    dkr_sci = format_scientific_latex(dkr)
    
    col1, col2 = st.columns([3,4])
    with col1:
        st.markdown(f'$ d_{{kr}} = {dkr:.4f} \\, \\text{{m}} $')
        st.markdown(f'> $ d_{{kr}} = {dkr_sci} \\, \\text{{m}} $')
    with col2:
        st.text('vrednost iz RPA izlaza')
    
    spacer('2em')
    
    Akr = dkr**2 * 3.14159 / 4
    st.markdown('$ A_{kr} = d_{kr}^2 \cdot \\frac{\\pi}{4}$')
    st.markdown(f'$ A_{{kr}} = {dkr:.5f}^2 \cdot \\frac{{\\pi}}{{4}} = {Akr:.5f} \\, m^2 $')
    Akr_sci = format_scientific_latex(Akr)
    st.markdown(f'> $ A_{{kr}} = {Akr_sci} \\, m^2 $')
    
    spacer()

    # mass flow rates ==============================
    # mox = OF * mg
    st.code('2. Maseni protoci:')
    
    P_sci = format_scientific_latex(P)
    st.markdown(f'$ C_{{star}} = {Cstar:.2f} \\, \\text{{m/s}} $')
   
    spacer('1em') 
    m_dot = P * Akr / Cstar # total mass flow rate
    st.markdown(f'$\dot{{m}} = \\frac{{P \cdot A_{{kr}}}} {{ C_{{star}} }} $')
    st.markdown(f'$\dot{{m}} = \\frac{{{P_sci} \cdot \\, {Akr:.5f}}} {{ {Cstar:.2f} }} = {m_dot:.3f} \\, \\text{{kg/s}} $')

    spacer('1em')
    mg = m_dot / (1 + OF) # fuel mass flow rate
    mox = m_dot - mg # oxidizer mass flow rate
    st.markdown(f'$ m_{{g}} = \dot{{m}} \cdot \\frac{{1}}{{OF + 1}} = {m_dot:.3f} \cdot \\frac{{1}}{{{OF:.3f} + 1}} = {mg:.3f} \\, \\text{{kg/s}} $')
    st.markdown(f'$ m_{{ox}} = \dot{{m}} - m_{{g}} = {m_dot:.3f} - {mg:.3f} = {mox:.3f} \\, \\text{{kg/s}} $')
    
    spacer()

    # Vkom ==============================
    Vkom = Lstar * Akr
    st.code('3. Zapremina komore:')
    st.markdown('$V_{kom} = L_{kar} \cdot A_{kr}$')
    st.markdown(f'$ V_{{kom}} = {Lstar:.3f} \, \cdot \, {Akr_sci} = {Vkom:.5f} \\, m^3 $')
    Vkom_sci = format_scientific_latex(Vkom)
    st.markdown(f'> $ V_{{kom}} = {Vkom_sci} \\, m^3 $')
    
    spacer()

    # 4. Chamber Diameter and Length ==============================
    # TODO numbers???
    dk = dkr * d_dkdr
    st.code('4. Precnik i duzina komore')
    st.markdown('$d_{k} = d_{kr} \cdot \\frac{D_k}{d_{kr}}$')
    st.markdown(f'$ d_{{k}} = {dkr:.3f} \, \cdot \, {d_dkdr:.3f} = {dk:.3f} \\, \\text{{m}} $')
    
    # lk - chamber length ==============================
    lk = Vkom / (dk**2 * 3.14159 / 4)
    st.markdown('$l_{k} = \\frac{V_{kom}}{\\frac{d_{k}^2 \cdot \\pi}{4}}$')
    # st.markdown(f'$ l_{{k}} = \\frac{{{Vkom:.3f}}}{{\\frac{{{dk:.3f}}^2 \cdot \\pi}}{{4}}}} = {lk:.3f} \\, \\text{{m}} $')
    st.markdown(f'$ l_{{k}} = \\frac{{ {Vkom:.5f} }}{{ \\frac{{ {dk:.3f}^2 \cdot \\pi }}{{ 4 }} }} = {lk:.3f} \\, \\text{{m}} $')
    lk_sci = format_scientific_latex(lk)
    st.markdown(f'> $ l_{{k}} = {lk_sci} \\, \\text{{m}} $')
    spacer()

    # 5. Nozzle Exit Area and Diameter
    st.code('5. Izlazni presek i precnik mlaznika')
    Ai = epsilon_i * Akr
    di = (Ai * 4 / 3.14159)**0.5
    st.markdown('$A_{i} = \\epsilon_i \cdot A_{kr}$')
    st.markdown(f'$ A_{{i}} = {epsilon_i:.3f} \\cdot {Akr:.5f} = {Ai:.5f} \\, \\text{{m}}^{{2}} $')
    st.markdown('$d_{i} = \\sqrt{\\frac{A_{i} \cdot 4}{\\pi}}$')
    st.markdown(f'$ d_{{i}} = \\sqrt{{\\frac{{{Ai:.3f} \\cdot 4}}{{\\pi}}}} = {di:.3f} \\, \\text{{m}} $')
    di_sci = format_scientific_latex(di)
    st.markdown(f'> $ d_{{i}} = {di_sci} \\, \\text{{m}} $')
    
    # -----------------fsolve---------------------#
    # mach
    st.markdown('***') 
    st.code('6. Odredjivanje Mahovog broja na izlazu mlaznika')

    st.markdown(f'$\epsilon_{{i}} = {epsilon_i:.2f}$', help='zadati stepen sirenja mlaznika, izmeniti u sidebar-u')
    st.markdown(r'''
        $ \epsilon_{i} = \frac{
        \left(1 + \frac{\kappa - 1}{2} \cdot M_{iter}^2\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
        }{
        M_{iter} \left(\frac{\kappa + 1}{2}\right)^{\frac{\kappa + 1}{2(\kappa - 1)}}
        } $
    ''')
    
    col1, col2 = st.columns([1,3])
    with col1:
        Mi_guess = st.number_input("M iterativni izbor", value=2.8, step=0.1)
    with col2:
        spacer('2em')
        st.markdown(f"$ M_{{iter}} = {Mi_guess:.3f}$")

    # fsolve
    def equation(Mi, kappa, epsilon_i):
        epsilon_i_opt_numerator = (1 + (kappa - 1) / 2 * Mi**2)**((kappa + 1) / (2 * (kappa - 1)))
        epsilon_i_opt_denominator = Mi * ((kappa + 1) / 2)**((kappa + 1) / (2 * (kappa - 1)))
        return epsilon_i_opt_numerator / epsilon_i_opt_denominator - epsilon_i

    Mi_solution = fsolve(equation, Mi_guess, args=(kappa, epsilon_i))
    
    st.code(f"""from scipy.optimize import fsolve
def equation(Mi, kappa, epsilon_i):
    epsilon_i_opt_numerator = (1 + (kappa - 1) / 2 * Mi**2)**((kappa + 1) / (2 * (kappa - 1)))
    epsilon_i_opt_denominator = Mi * ((kappa + 1) / 2)**((kappa + 1) / (2 * (kappa - 1)))
    return epsilon_i_opt_numerator / epsilon_i_opt_denominator - epsilon_i
Mi_guess = {Mi_guess:.1f}
Mi_solution = fsolve(equation, Mi_guess, args=(kappa, epsilon_i))
Mi_solution = {Mi_solution[0]:.4f}
""")
    col1, col2 = st.columns([1,3])
    with col1:
        M_i = st.number_input("M_i ručna izmena", value=Mi_solution[0], step=1.00)
    with col2:
        spacer('2em')
        st.markdown(fr"$M_i = {M_i:.3f}$")

    # 7. Static Pressure at Nozzle Exit
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
    pi_sci = format_scientific_latex(pi)
    st.markdown(f'> $ p_{{i}} = {pi_sci} \\, \\text{{Pa}} $')
    
    spacer()

    # Optimalni stepen sirenja mlaznika
    Mi_opt = (((P/Pa)**((kappa - 1)/kappa) - 1) * (2/(kappa - 1)))**0.5

    st.code('8. Optimalni stepen sirenja mlaznika (do atmosferskog P od 1 bar)')
    st.markdown(r'''
    $$ M_{i \text{ opt}} = \sqrt{\left[\left(\frac{P}{P_a}\right)^{\frac{\kappa - 1}{\kappa}} - 1\right] \cdot \frac{2}{\kappa - 1}} $$
    ''')
    st.markdown(f'$ M_{{i opt}} = \\sqrt{{\\left[\\left(\\frac{{{P:.2e}}}{{{Pa:.2e}}}\\right)^{{\\frac{{{kappa} - 1}}{{{kappa}}}}} - 1\\right] \\cdot \\frac{{2}}{{{kappa} - 1}}}} = {Mi_opt:.3f} $')
    st.markdown(f'> $ M_{{i opt}} = {Mi_opt:.3f} $')
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
    st.markdown(f'> $ \epsilon_{{i opt}} = {e_i_opt:.3f} $')

    spacer()

    # Calculate optimal nozzle exit area
    Aiopt = e_i_opt * Akr
    st.markdown(r'''
    $$ A_{i_{opt}} = \epsilon_{i opt} \cdot A_{kr} $$
    ''')
    st.markdown(f'''
        $ A_{{i_{{opt}}}} = {e_i_opt:.3f} \cdot {Akr:.3f} = {Aiopt:.5f} \\, \\text{{m}}^2 $
    ''')
    Aiopt_sci = format_scientific_latex(Aiopt)
    st.markdown(f'> $ A_{{i{{opt}}}} = {Aiopt_sci} \\, \\text{{m}}^2 $')
    spacer()

    # Calculate optimal nozzle exit diameter
    st.code('izlazni precnik')
    diopt = (Aiopt * 4 / 3.14159)**0.5
    st.markdown(r'''
    $$ d_{i_{opt}} = \sqrt{A_{i_{opt}} \cdot \frac{4}{\pi}} $$
    ''')
    st.markdown(f'''
        $ d_{{i_{{opt}}}} = \sqrt{{ {Aiopt:.4f} \\cdot \\frac{{4}}{{\\pi}} }} = {diopt:.3f} \\, \\text{{m}}^2 $
    ''')
    diopt_sci = format_scientific_latex(diopt)
    st.markdown(f'> $ d_{{iopt}} = {diopt_sci} \\, \\text{{m}} $')
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
    T_sci = format_scientific_latex(T)
    st.markdown(f'> $ T = {T_sci} \\, \\text{{K}} $')
    st.success(f'T = {T:.3f} K')
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
    Vi_sci = format_scientific_latex(Vi)
    st.markdown(f'> $ V_{{i}} = {Vi_sci} \\, \\text{{m/s}} $')
    spacer()

    Vi_opt = (2*kappa/(kappa-1) * R * T * (1 - 1/((P/Pa)**((kappa-1)/kappa))))**0.5
    st.markdown(r'''
        $$ V_{iopt} = \sqrt{ \frac{2 \kappa}{\kappa - 1} \cdot R \cdot T \cdot \left[ 1 - \frac{1}{\left(\frac{P}{p_a}\right)^{\frac{\kappa - 1}{\kappa}}} \right] } $$
    ''')
    st.markdown(f'''
        $ V_{{iopt}} = \sqrt{{ \\frac{{2 \cdot {kappa}}}{{ {kappa} - 1 }} \cdot {R} \cdot {T:.3f} \cdot \\left[ 1 - \\frac{{1}}{{\\left(\\frac{{ {P} }}{{ {Pa:.3f} }}\\right)^{{\\frac{{ {kappa} - 1 }}{{ {kappa} }}}}}} \\right] }}  = {Vi_opt:.3f} \\, \\text{{m/s}} $
    ''')
    Vi_opt_sci = format_scientific_latex(Vi_opt)
    st.markdown(f'> $ V_{{iopt}} = {Vi_opt_sci} \\, \\text{{m/s}} $')
    
    # ===================== thrust ===================== #
    # Thrust at given expansion ratio
    st.code('11. Zadata sila potiska')
    F = F * 1000 # kN to N    
    st.markdown(f'$ F = {F:.2f} \\, \\text{{N}} $')
    F_sci = format_scientific_latex(F)
    st.markdown(f'> $ F = {F_sci} \\, \\text{{N}} $')
    spacer()
    
    # F = (mox + mg) * Vi + Ai * (pi - Pa)
    # st.markdown(f'''
    #     $ F = ({mox:.3f} + {mg:.3f}) \cdot {Vi:.3f} + {Ai:.3f} \cdot ({pi:.3f} - {Pa:.3f}) = {F:.3f} \\, \\text{{N}} $
    # ''')

    # Thrust at optimal expansion ratio
    Fopt = (mox + mg) * Vi_opt
    st.markdown(r'''
        $$ F_{opt} = (m_{ox} + m_{g}) \cdot V_{iopt} $$
    ''')
    st.markdown(f'''
        $ F_{{opt}} = ({mox:.3f} + {mg:.3f}) \cdot {Vi_opt:.3f} = {Fopt:.3f} \\, \\text{{N}} $
    ''')
    Fopt_sci = format_scientific_latex(Fopt)
    st.markdown(f'> $ F_{{opt}} = {Fopt_sci} \\, \\text{{N}} $')
    spacer()

    # Thrust Coefficient ============================================
    st.code('12. Koeficijent potiska')
    
    Cf = F / (P * Akr)
    st.markdown(r'''
        $$ C_f = \frac{F}{P \cdot A_{kr}} $$
    ''')
    # st.markdown(f'''
    #     $ C_f = \\frac{{ {F:.0f} }}{{ {P:.0f} \\cdot {Akr:.5f} }} = {Cf:.3f} $
    # ''')
    # scientific notation Cf variant
    P_sci = format_scientific_latex(P)
    st.markdown(f'''
        $ C_f = \\frac{{ {F_sci} }}{{ {P_sci} \\cdot {Akr_sci} }} = {Cf:.3f} $
    ''')
    st.markdown(f'> $ C_f = {Cf:.3f} $')
    spacer()

    # Specific Impulse at Given Expansion Ratio =======================
    st.code('13. Specifični impuls pri zadanom stepenu sirenja')
    Isp = F / (mox + mg)
    Isp_sec = Isp / 9.80665
    st.markdown(r'''
        $$ I_{sp} = \frac{F}{(m_{ox} + m_{g})} $$
    ''')
    st.markdown(f'''
        $ I_{{sp}} = \\frac{{ {F:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp:.2f} \\, \\text{{Ns/Kg}} = {Isp_sec:.2f} \\, \\text{{s}}$
    ''')
    st.markdown(f'> $ I_{{sp}} = {Isp:.2f} \\, \\text{{Ns/Kg}} $')
    spacer()

    # Specific Impulse at Optimal Expansion Ratio
    st.code('Specifični impuls pri optimalnom stepenu sirenja:')
    Isp_opt = Fopt / (mox + mg)
    Isp_opt_sec = Isp_opt / 9.80665
    st.markdown(r'''
        $$ I_{sp_{opt}} = \frac{F_{opt}}{(m_{ox} + m_{g})} $$
    ''')
    st.markdown(f'''
        $ I_{{sp_{{opt}}}} = \\frac{{ {Fopt:.3f} }}{{ ({mox:.3f} + {mg:.3f}) }} = {Isp_opt:.3f} \\, \\text{{Ns/kg}}  = {Isp_opt_sec:.2f} \\, \\text{{s}}$
    ''', help='Isp/g = value in seconds')
    st.markdown(f'> $ I_{{sp_{{opt}}}} = {Isp_opt:.2f} \\, \\text{{Ns/Kg}} $')
    spacer()
    
    # ===================== COMPARISON TABLE ===================== #
    st.subheader("Poređenje rezultata")
    
    st.code(kappa)

    g = 9.80665
    

    st.markdown(f"""
    | Parameter                          | RPA Value                     | Analytical Value     | Difference             | % Difference          |
    |------------------------------------|-------------------------------|----------------------|------------------------|-----------------------|
    | **Performanse**                    |                               |                      |                        |                       |
    | Isp — Specifični impuls (Vac)      | `{isp_rpa*g:.2f} Ns/Kg` | `{Isp:.2f} Ns/Kg`    | `{(isp_rpa*g - Isp):.2f} Ns/Kg` | `{((isp_rpa*g - Isp) / Isp * 100):.2f}%` |
    | Cf – Koeficijent potiska (Vac)     | `{cf_rpa}`                    | `{Cf:.4f}`           | `{(cf_rpa - Cf):.4f}` | `{((cf_rpa - Cf) / Cf * 100):.2f}%` |
    | F - Potisak komore (Vac)           | `{thrust_vac_rpa} kN`         | `{F/1000:.3f} kN`    | `{(thrust_vac_rpa - F/1000):.2f} kN` | `{((thrust_vac_rpa - F/1000) / (F/1000) * 100):.2f}%` |
    | Fopt - Potisak komore (Opt)        | `{thrust_opt_rpa} kN`         | `{Fopt/1000:.3f} kN` | `{(thrust_vac_rpa - Fopt/1000):.2f} kN` | `{((thrust_opt_rpa - Fopt/1000) / (Fopt/1000) * 100):.2f}%` |
    | Isp_opt - Specifični impuls (Opt)  | `{isp_opt_rpa*g:.2f} Ns/Kg` | `{Isp_opt:.2f} Ns/Kg` | `{(isp_opt_rpa*g - Isp_opt):.2f} Ns/Kg` | `{((isp_opt_rpa*g - Isp_opt) / Isp_opt * 100):.2f}%` |
    | OF - Odnos oksidator/gorivo (OF)   | `{of_rpa:.3f}`                | `{OF:.3f}`           | `{(of_rpa - OF):.3f}`   | `{((of_rpa - OF) / OF * 100):.2f}%`   |
    | **Geometrija komore**              |                               |                      |                            |                       |
    | Dc - Prečnik komore                | `{dc_rpa} mm`                 | `{dk*1000:.3f} mm`   | `{(dc_rpa-dk*1000):.3f}` | `{((dc_rpa - dk*1000) / (dk*1000) * 100):.2f}%` |
    | Dt - Prečnik grla mlaznika         | `{dt_rpa} mm`                 | `{dkr*1000:.3f} mm`  | `{(dt_rpa-dkr*1000):.3f}`| `{((dt_rpa - dkr*1000) / (dkr*1000) * 100):.2f}%`|
    | De - Izlazni prečnik (presek)      | `{de_rpa} mm`                 | `{diopt*1000:.3f} mm`   | `{(de_rpa-di*1000):.3f}` | `{((de_rpa - di*1000) / (di*1000) * 100):.2f}%` |
    | Lc - Dužina komore                 | `{lc_rpa} mm`                 | `{lk*1000:.3f} mm`   | `{(lc_rpa-lk*1000):.3f}` | `{((lc_rpa - lk*1000) / (lk*1000) * 100):.2f}%` |
    | Le - Dužina izlaza mlaznika        | `{le_rpa} mm`                 | Placeholder          | Placeholder              | Placeholder            |
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

