import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# !JANGAN DIUBAH UBAH
# -------------------------------
data = {
    "Company": [
        *["McDonald"] * 10,
        *["Burger King"] * 10,
        *["KFC"] * 10,
        *["Subway"] * 10,
        *["Wendy's"] * 10,
    ],
    "Item": [
        # McDonald
        "Hamburger", "Cheeseburger", "Double Cheeseburger", "McDouble", "Quarter Pounder with Cheese",
        "Big Mac", "McChicken", "Filet-O-Fish", "McNuggets (6pc)", "McRib",
        
        # Burger King
        "Whopper", "Whopper Jr.", "Big King", "Chicken Fries", "Bacon King",
        "Double Stacker", "Fish Sandwich", "Spicy Nuggets", "Crispy Chicken Sandwich", "Onion Rings",
        
        # KFC
        "Original Recipe Chicken", "Popcorn Chicken", "Zinger Burger", "Twister Wrap", "BBQ Chicken Sandwich",
        "Chicken Wings", "Hot & Spicy Chicken", "Nashville Hot Chicken", "Chicken Tenders", "Grilled Chicken",
        
        # Subway
        "Turkey Breast Sandwich", "Tuna Sub", "Chicken Teriyaki Sub", "Veggie Delight", "Italian B.M.T",
        "Meatball Marinara", "Roast Beef Sub", "Steak & Cheese", "Subway Melt", "Spicy Italian",
        
        # Wendy's
        "Baconator", "Spicy Chicken Sandwich", "Jr. Cheeseburger", "Asiago Ranch Chicken", "Daves Single",
        "Son of Baconator", "Pretzel Bacon Pub Cheeseburger", "Crispy Chicken Nuggets", "Homestyle Chicken Sandwich", "BBQ Cheeseburger"
    ],
    "Calories": [
        # McDonald
        250, 300, 440, 390, 510,
        540, 400, 380, 250, 520, 
        
        # Burger King
        657, 410, 540, 290, 1150,
        600, 380, 340, 750, 350,
        
        # KFC
        320, 380, 420, 450, 470,
        360, 500, 550, 400, 370,
        
        # Subway
        280, 480, 360, 230, 450,
        550, 450, 500, 400, 460,
        
        # Wendy's
        950, 500, 370, 720, 590,
        850, 780, 400, 600, 650
    ],
    "Proteins": [
        # McDonald
        12, 15, 25, 22, 29,
        27, 23, 20, 13, 30,
        
        # Burger King
        28, 22, 31, 15, 60,
        32, 22, 18, 45, 16,
        
        # KFC
        35, 22, 33, 30, 25,
        28, 31, 35, 26, 24,
        
        # Subway
        18, 20, 25, 10, 22,
        28, 26, 30, 22, 25,
        
        # Wendy's
        57, 32, 20, 40, 33,
        45, 50, 22, 38, 42
    ]
}

df = pd.DataFrame(data)
# -------------------------------
st.write("# Fast Food Nutrition Explorer")
search_makanan = st.text_input("Cari nama makanan")

tabel, visualisasi = st.tabs(["Tabel", "Visualisasi"])

with tabel:
    minCal, maxCal = st.slider("Pilih Rentang Kalori", min(df["Calories"]), max(df["Calories"]), (min(df["Calories"]), max(df["Calories"])))
    filtered_df = df.query(f"Calories >= {minCal} & Calories <= {maxCal}")
    filtered_df = df[(df["Calories"] >= minCal) & (df["Calories"] <= maxCal)]
    
    if search_makanan:
        filtered_df = filtered_df[filtered_df["Item"].str.contains(search_makanan, case=False)]
        
    st.dataframe(filtered_df)
    with st.expander("Statistik Data"):
        st.write(df.describe())
        
with visualisasi:
    company = df["Company"].unique()
    perusahaan = st.selectbox("Pilih Perusahaan", company)
    filtered_df = df[df["Company"] == perusahaan]
    
    if search_makanan:
        filtered_df = filtered_df[filtered_df["Item"].str.contains(search_makanan, case=False)]
        
    st.write("## Calories vs Protein")
    filtered_calories = filtered_df["Calories"]
    filtered_proteins = filtered_df["Proteins"]
    plt.figure(figsize=(6, 5))
    plt.scatter(filtered_calories, filtered_proteins, color='blue', label=perusahaan)
    plt.xlabel('Calories')
    plt.ylabel('Proteins')
    plt.legend()
    st.pyplot(plt)