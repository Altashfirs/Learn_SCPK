import streamlit as st
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

# Define fuzzy variables
rasa = ctrl.Antecedent(np.arange(0, 11, 1), 'rasa') # Input
pelayanan = ctrl.Antecedent(np.arange(0, 11, 1), 'pelayanan') # Input
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip') # Output

# Define fuzzy membership functions with triangular and triangular shapes
rasa['Tidak Enak'] = fuzz.trimf(rasa.universe, [0, 0, 5])
rasa['Biasa'] = fuzz.trapmf(rasa.universe, [0, 4, 6, 10])
rasa['Enak'] = fuzz.trimf(rasa.universe, [5, 10, 10])

pelayanan['Buruk'] = fuzz.trimf(pelayanan.universe, [0, 0, 5])
pelayanan['Biasa'] = fuzz.trapmf(pelayanan.universe, [0, 3, 7, 10])
pelayanan['Baik'] = fuzz.trimf(pelayanan.universe, [5, 10, 10])

tip ['Sedikit'] = fuzz.trimf(tip.universe, [0, 0, 12])
tip ['Sedang'] = fuzz.trimf(tip.universe, [0, 12, 25])
tip ['Banyak'] = fuzz.trimf(tip.universe, [12, 25, 25])

# Define fuzzy rules
rules = [
    ctrl.Rule(rasa['Tidak Enak'] | pelayanan['Buruk'], tip['Sedikit']),
    ctrl.Rule(pelayanan['Biasa'], tip['Sedang']),
    ctrl.Rule(rasa['Enak'] & pelayanan['Baik'], tip['Banyak'])
]

# Create control system with rules
tipping_ctrl = ctrl.ControlSystem(rules)
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

st.title("Sistem Pendukung Keputusan (SPK) - Metode Fuzzy")
st.write("## Fuzzy Logic Tipping System")

st.write("#### Input Data")

# Get user input for rasa and pelayanan
rasa_value = st.slider("Rasa (0 - 10)", 0.0, 10.0, 5.0, 0.5)
pelayanan_value = st.slider("Pelayanan (0 - 10)", 0.0, 10.0, 5.0, 0.5)

# Set input values in the control system
tipping.input['rasa'] = rasa_value
tipping.input['pelayanan'] = pelayanan_value

# Compute the output
tipping.compute()

# Display the output
st.write("#### Output Data")
st.write(f"Rasa: {rasa_value}")
st.write(f"Pelayanan: {pelayanan_value}")
st.write(f"Tip: {tipping.output['tip']:.2f}")

def plot_fuzzy_sets(variable, title):
    st.write(f"#### {title}")
    fig, ax = plt.subplots()
    variable.view(ax=ax)
    st.pyplot(plt.gcf())
    
plot_fuzzy_sets(rasa, "Fuzzy Sets for Rasa")
plot_fuzzy_sets(pelayanan, "Fuzzy Sets for Pelayanan")
plot_fuzzy_sets(tip, "Fuzzy Sets for Tip")