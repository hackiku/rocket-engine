import streamlit as st


def mass_flow_rates_rpa():

    method = st.radio(
    "Izaberite metod za izračunavanje masenog protoka:",
    ('Izračunajte pomoću C* vrednosti', 'Koristi RPA masene protoke')
    )

    if method == 'Koristi RPA masene protoke':
        # Use RPA mass flow values (mg, mox)
        mox = ox_flow_rate_rpa
        mg = fuel_flow_rate_rpa
    else:
        # Calculate using C* value
        dkr = dt_rpa # throat diameter from RPA regex
        Akr = (dkr**2 * 3.14159) / 4  # Assuming dkr is the throat diameter
        mox = P * Akr / Cstar  # Oxidizer mass flow rate
        mg = mox / OF  # Fuel mass flow rate
        # Akr ==============================
        st.code('1. Maseni protoci iz RPA:')
        mg = P * Akr / Cstar
        st.code('1. Maseni protoci:')
        st.markdown(f'$m_{{g}} = {mg:.3f} \\, \\text{{kg/s}} $')
        st.markdown('$m_{ox} = OF \cdot m_{g}$')
        st.markdown(f'$ m_{{ox}} = {OF:.3f} \cdot {mg:.3f} = {mox:.3f} \\, \\text{{kg/s}} $', unsafe_allow_html=True)
        spacer()

        Akr = Cstar * (mg + mox) / P
        dkr = (Akr * 4 / 3.14159)**0.5
        st.code('2. Kriticni presek i precnik mlaznika:')
        st.markdown('$ A_{kr} = \\frac{C_{star} \cdot (mg + m_{ox})}{P}$')
        st.markdown(f'$ A_{{kr}} = \\frac{{ {Cstar:.3f} \, \cdot \, ({mg:.3f} + {mox:.3f}) }}{{ {P:.3f} }} = {Akr:.6f} \\, m^2 $')    
        # scientific notation Akr
        Akr_sci = format_scientific_latex(Akr)
        st.markdown(f'> $ A_{{kr}} = {Akr_sci} \\, m^2 $')
