import streamlit as st
import joblib
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim

def run_prediction():
    st.title("Masukkan Data Gempa")

    # Form Input
    time = st.text_input("Tanggal (YYYY-MM-DD)", placeholder="2025-08-09")
    latitude = st.number_input("Latitude", format="%.6f", value=None, placeholder="-8.650000")
    longitude = st.number_input("Longitude", format="%.6f", value=None, placeholder="115.220000")
    depth = st.number_input("Kedalaman (km)", format="%.2f", value=None, placeholder="10.2")
    magType = st.selectbox("Tipe Magnitudo", ["mb", "ml", "ms", "mw", "me", "mi", "mb_lg", "mwb", "mwc"], index=0)
    nst = st.number_input("Jumlah Stasiun (nst)", format="%d", value=None, placeholder="40")
    gap = st.number_input("Gap", format="%.2f", value=None, placeholder="65")
    dmin = st.number_input("Dmin", format="%.2f", value=None, placeholder="0.35")
    rms = st.number_input("RMS", format="%.2f", value=None, placeholder="0.82")
    horizontalError = st.number_input("Horizontal Error", format="%.2f", value=None, placeholder="0.7")
    depthError = st.number_input("Depth Error", format="%.2f", value=None, placeholder="0.5")
    magError = st.number_input("Magnitude Error", format="%.2f", value=None, placeholder="0.05")
    magNst = st.number_input("Magnitude Nst", format="%d", value=None, placeholder="40")
    status = st.text_input("Status", value="reviewed")
    locationSource = st.text_input("Sumber Lokasi", value="us")
    magSource = st.text_input("Sumber Magnitudo", value="us")
    date = st.text_input("Waktu (HH:MM:SS)", placeholder="14:23:00")
    eq_type = st.text_input("Tipe Kejadian", value="earthquake")
    location = st.text_input("Lokasi (opsional)", placeholder="Kosongkan untuk auto dari koordinat")
    net = st.text_input("Net", value="us")
    eq_id = st.text_input("ID", placeholder="us1234567")

    # Saat tombol diklik
    if st.button("Prediksi Magnitudo"):
        model = joblib.load("model_best_tunning.pkl")

        # Auto isi lokasi jika kosong
        if location.strip() == "":
            try:
                geolocator = Nominatim(user_agent="geoapi")
                loc = geolocator.reverse(f"{latitude}, {longitude}")
                location = loc.address if loc else "Tidak diketahui"
            except:
                location = "Tidak diketahui"

        # Buat dataframe input
        input_data = pd.DataFrame([{
            "time": time,
            "latitude": latitude,
            "longitude": longitude,
            "depth": depth,
            "magType": magType,
            "nst": nst,
            "gap": gap,
            "dmin": dmin,
            "rms": rms,
            "horizontalError": horizontalError,
            "depthError": depthError,
            "magError": magError,
            "magNst": magNst,
            "status": status,
            "locationSource": locationSource,
            "magSource": magSource,
            "date": date,
            "type": eq_type,
            "location": location,
            "net": net,
            "id": eq_id
        }])

        # Prediksi
        prediction = model.predict(input_data)[0]

        # Simpan ke session_state
        st.session_state["last_prediction"] = {
            "data": input_data,
            "prediction": prediction,
            "latitude": latitude,
            "longitude": longitude
        }

        # Simpan ke history
        if "predictions" not in st.session_state:
            st.session_state["predictions"] = []
        st.session_state["predictions"].append(
            input_data.assign(prediksi=prediction)
        )

    # Tampilkan hasil jika ada
    if "last_prediction" in st.session_state:
        pred_info = st.session_state["last_prediction"]
        st.success(f"Prediksi Magnitudo: {pred_info['prediction']:.2f}")

        # Peta
        m = folium.Map(location=[pred_info["latitude"], pred_info["longitude"]], zoom_start=6)
        folium.Marker(
            [pred_info["latitude"], pred_info["longitude"]],
            popup=f"Prediksi Magnitudo: {pred_info['prediction']:.2f}"
        ).add_to(m)
        st_folium(m, width=700, height=500)

        # Tombol download CSV
        all_data = pd.concat(st.session_state["predictions"], ignore_index=True)
        csv = all_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Hasil Prediksi (CSV)",
            csv,
            "prediksi_gempa.csv",
            "text/csv"
        )
