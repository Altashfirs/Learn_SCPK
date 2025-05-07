import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("community.csv")

st.write("## Aplikasi Eksplorasi Dataset Community")
st.write("Menyajikan dataset iris secara interaktif")

number_show = st.sidebar.number_input(
    "Jumlah data yang ingin ditampilkan",
    0,
    len(df),
    100
)

st.write("### Dataset Community")
st.dataframe(df.head(number_show))

with st.expander("Informasi Detail"):
    st.write("Dimensi Dataset: ", df.shape)
    st.write("Dimensi Statistik:")
    st.write(df.describe())
    st.write("Missing Values:")
    st.write(df.isnull().sum())
    
st.write("### Visualisasi Data")
age, height = st.tabs(["Age", "height"])

with height:
    st.write("#### Line Plot - Height per Index")
    plt.figure(figsize=(12, 6))
    for continent in df['Continent'].unique():
        continent_data = df[df['Continent'] == continent]
        plt.plot(continent_data.index, continent_data['Height'], label=continent, marker="o")

    # Adding labels and title
    plt.xlabel("")
    plt.ylabel("")
    plt.legend()
    plt.grid()

    # Display the plot in Streamlit
    st.pyplot(plt)
    
with age:
    st.write("#### Line Plot - Age per Index")
    
    # Remove Antarctica from the DataFrame
    df_ant = df[df['Continent'] != 'Antarctica']

    # Get unique continents
    continents = df_ant['Continent'].unique()

    # Create a figure with subplots
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(7, 6), sharex=True)

    # Flatten the axes array for easy iteration
    axes = axes.flatten()
    
    colors = ['red','green','blue','cyan','purple', 'orange']

    # Loop through each continent and plot the data
    for ax, continent, color in zip(axes, continents, colors):
        continent_data = df_ant[df_ant['Continent'] == continent]
        ax.plot(continent_data.index, continent_data['Age'], marker='o', label=continent, color=color)
        ax.legend()
        
    # Atur ticks sumbu x dan y
        ax.set_xticks([0, 200, 400])
        ax.set_yticks([20, 40])
        
        ax.set_xlabel(' ')
        ax.legend(loc='upper left')

    # Adjust layout
    plt.tight_layout()
    
    st.pyplot(fig)
