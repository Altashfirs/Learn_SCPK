import streamlit as st
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

udara_luar = ctrl.Antecedent(np.arange(0, 11, 1), 'udara_luar')
udara_dalam = ctrl.Antecedent(np.arange(0, 11, 1), 'udara_dalam')
kelembapan = ctrl.Antecedent(np.arange(0, 11, 1), 'kelembapan')

kipas_angin = ctrl.Consequent(np.arange(0, 26, 1), 'kipas_angin')
pendingin_udara = ctrl.Consequent(np.arange(0, 26, 1), 'pendingin_udara')
pemanas = ctrl.Consequent(np.arange(0, 26, 1), 'pemanas')

udara_luar['Dingin'] = fuzz.trimf(udara_luar.universe, [0, 0, 5])
udara_luar['Sejuk'] = fuzz.trapmf(udara_luar.universe, [0, 4, 6, 10])
udara_luar['Hangat'] = fuzz.trimf(udara_luar.universe, [5, 10, 10])

udara_dalam['Sejuk'] = fuzz.trimf(udara_dalam.universe, [0, 0, 5])
udara_dalam['Nyaman'] = fuzz.trapmf(udara_dalam.universe, [0, 3, 7, 10])
udara_dalam['Hangat'] = fuzz.trimf(udara_dalam.universe, [5, 10, 10])

kelembapan['Kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 5])
kelembapan['Sedang'] = fuzz.trapmf(kelembapan.universe, [0, 4, 6, 10])
kelembapan['Lembab'] = fuzz.trimf(kelembapan.universe, [5, 10, 10])

kipas_angin['Lambat'] = fuzz.trimf(kipas_angin.universe, [0, 0, 12])
kipas_angin['Sedang'] = fuzz.trimf(kipas_angin.universe, [0, 12, 25])
kipas_angin['Cepat'] = fuzz.trimf(kipas_angin.universe, [12, 25, 25])

pendingin_udara['Sedikit'] = fuzz.trimf(pendingin_udara.universe, [0, 0, 12])
pendingin_udara['Sedang'] = fuzz.trimf(pendingin_udara.universe, [0, 12, 25])
pendingin_udara['Banyak'] = fuzz.trimf(pendingin_udara.universe, [12, 25, 25])

pemanas['Rendah'] = fuzz.trimf(pemanas.universe, [0, 0, 12])
pemanas['Sedang'] = fuzz.trimf(pemanas.universe, [0, 12, 25])
pemanas['Tinggi'] = fuzz.trimf(pemanas.universe, [12, 25, 25])

rules = [
    ctrl.Rule(udara_luar['Dingin'] & udara_dalam['Sejuk'] & kelembapan['Kering'], kipas_angin['Lambat']),
    ctrl.Rule(udara_luar['Dingin'] & udara_dalam['Sejuk'] & kelembapan['Kering'], pendingin_udara['Sedikit']),
    ctrl.Rule(udara_luar['Dingin'] & udara_dalam['Sejuk'] & kelembapan['Kering'], pemanas['Tinggi']),
    
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], kipas_angin['Sedang']),
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], pendingin_udara['Sedang']),
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], pemanas['Rendah']),
    
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Hangat'] & kelembapan['Lembab'], kipas_angin['Cepat']),
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Hangat'] & kelembapan['Lembab'], pendingin_udara['Sedikit']),
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Hangat'] & kelembapan['Lembab'], pemanas['Rendah']),
    
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Sejuk'] & kelembapan['Sedang'], kipas_angin['Lambat']),
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Sejuk'] & kelembapan['Sedang'], pendingin_udara['Banyak']),
    ctrl.Rule(udara_luar['Sejuk'] & udara_dalam['Sejuk'] & kelembapan['Sedang'], pemanas['Sedang']),
    
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], kipas_angin['Cepat']),
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], pendingin_udara['Sedang']),
    ctrl.Rule(udara_luar['Hangat'] & udara_dalam['Nyaman'] & kelembapan['Sedang'], pemanas['Rendah']),
]

kipas_angin_ctrl = ctrl.ControlSystem(rules)
kipas_angin_sim = ctrl.ControlSystemSimulation(kipas_angin_ctrl)

pendingin_udara_ctrl = ctrl.ControlSystem(rules)
pendingin_udara_sim = ctrl.ControlSystemSimulation(pendingin_udara_ctrl)

pemanas_ctrl = ctrl.ControlSystem(rules)
pemanas_sim = ctrl.ControlSystemSimulation(pemanas_ctrl)

st.set_page_config(page_title="Tugas 4")
st.markdown("## Tugas 4 - SPK dengan Metode Fuzzy")

st.markdown("#### Input Nilai")

udara_luar_value = st.slider("Udara Luar (0 - 10)", 0.0, 10.0, 5.0, 0.5)
udara_dalam_value = st.slider("Udara Dalam (0 - 10)", 0.0, 10.0, 5.0, 0.5)
kelembapan_value = st.slider("Kelembapan (0 - 10)", 0.0, 10.0, 5.0, 0.5)

kipas_angin_sim.input['udara_luar'] = udara_luar_value
kipas_angin_sim.input['udara_dalam'] = udara_dalam_value
kipas_angin_sim.input['kelembapan'] = kelembapan_value

pendingin_udara_sim.input['udara_luar'] = udara_luar_value
pendingin_udara_sim.input['udara_dalam'] = udara_dalam_value
pendingin_udara_sim.input['kelembapan'] = kelembapan_value

pemanas_sim.input['udara_luar'] = udara_luar_value
pemanas_sim.input['udara_dalam'] = udara_dalam_value
pemanas_sim.input['kelembapan'] = kelembapan_value

kipas_angin_sim.compute()
pendingin_udara_sim.compute()
pemanas_sim.compute()

st.markdown("#### Hasil")
st.write(f"Suhu Udara Luar: {udara_luar_value}")
st.write(f"Suhu Udara Dalam: {udara_dalam_value}")
st.write(f"Kelembapan: {kelembapan_value}")
st.write(f"Kipas Angin: {kipas_angin_sim.output['kipas_angin']:.2f}")
st.write(f"Pendingin Udara: {pendingin_udara_sim.output['pendingin_udara']:.2f}")
st.write(f"Pemanas: {pemanas_sim.output['pemanas']:.2f}")

def plot_fuzzy_sets(variable, title, input_value):
    st.write(f"#### {title}")
    fig, ax = plt.subplots()
    variable.view(ax=ax)
    plt.axvline(x=input_value, color='black', linestyle='--', label=f'Hasil: {input_value}')
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    st.pyplot(plt.gcf())

with st.expander("Grafik Fungsi Keanggotaan"):
    st.markdown("# Fungsi keanggotaan Input")
    
    luarTabs, dalamTabs, kelembapanTabs = st.tabs(["Suhu Udara Luar", "Suhu Udara Dalam", "Kelembapan"])
    
    with luarTabs:
        plot_fuzzy_sets(udara_luar, "Fungsi Keanggotaan Udara Luar", udara_luar_value)

    with dalamTabs:
        plot_fuzzy_sets(udara_dalam, "Fungsi Keanggotaan Udara Dalam", udara_dalam_value)
        
    with kelembapanTabs:
        plot_fuzzy_sets(kelembapan, "Fungsi Keanggotaan Kelembapan", kelembapan_value)
    
    st.markdown("# Fungsi keanggotaan Output")
    kipasTabs, pendinginTabs, pemanasTabs = st.tabs(["Kipas Angin", "Pendingin Udara", "Pemanas"])
    
    with kipasTabs:
        plot_fuzzy_sets(kipas_angin, "Fungsi Keanggotaan Kipas Angin", kipas_angin_sim.output['kipas_angin'])
    
    with pendinginTabs:
        plot_fuzzy_sets(pendingin_udara, "Fungsi Keanggotaan Pendingin Udara", pendingin_udara_sim.output['pendingin_udara'])
    
    with pemanasTabs:
        plot_fuzzy_sets(pemanas, "Fungsi Keanggotaan Pemanas", pemanas_sim.output['pemanas'])
