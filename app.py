import streamlit as st
import eda
import predict

# Set up the page configuration
st.set_page_config(page_title="Earthquake App", layout="wide")

# Sidebar for navigation
with st.sidebar:
    st.write("# Page Navigation")

    # Toggle for selecting the page
    page = st.selectbox("Pilih Halaman", ("EDA", "Prediksi"))

    # Display selected page
    st.write(f"Halaman yang dituju: {page}")

    st.write("## About")
    st.markdown('''
    Page ini berisikan hasil analisis data terhadap gempa bumi dan prediksi kekuatan gempa berdasarkan atribut yang dimiliki.
    ''')

# Main content based on the selected page
if page == 'EDA':
    eda.run_eda()  # Assuming run_eda is a function in the eda module
else:
    predict.run_prediction()  # Assuming run_prediction is a function in the predict module

