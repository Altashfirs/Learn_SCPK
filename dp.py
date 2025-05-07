import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn import datasets

iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['Target'] = iris.target

st.write("Dataset Iris")
st.write(df)

st.write("Informasi Dataset")
st.write(df.info())

st.write("Missing Values")
st.write(df.isnull().sum())

st.write("Statistik Deskriptif")
st.write(df.describe())

st.write("Visualisasi Data")
fig, ax = plt.subplots(figsize=(10,5))

for species in df['Target'].unique():
    subset = df["Target"] == species
    ax.plot(subset.index, subset['petal length (cm)'], marker='.', label=species)

st.pyplot(fig)