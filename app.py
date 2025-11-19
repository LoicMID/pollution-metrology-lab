import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Sensor Calibration Framework",
    page_icon="📉",
    layout="wide"
)

# --- TITRE & CONTEXTE ---
st.title("🔬 Metrology & Calibration Framework")
st.markdown("""
**Context:** PhD Research on Low-Cost Sensor Reliability.
This dashboard demonstrates the **signal processing pipeline** applied to environmental data.
""")

# --- CHARGEMENT DES DONNÉES (CACHE) ---
@st.cache_data
def load_data():
    # On charge le fichier de démo que vous avez créé
    # Si le fichier est vide ou mal formaté, on génère une donnée synthétique de secours
    try:
        df = pd.read_csv("data/demo/test_sensor.csv")
        # On essaie de convertir le temps s'il existe
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
        return df
    except Exception as e:
        st.warning(f"Could not load CSV ({e}), generating synthetic data instead.")
        # Génération de secours pour que l'app ne plante jamais
        time_range = pd.date_range(start="2024-01-01", periods=100, freq="h")
        base_signal = np.sin(np.linspace(0, 10, 100)) * 10 + 20
        noise = np.random.normal(0, 2, 100)
        return pd.DataFrame({
            "time": time_range,
            "raw_value": base_signal + noise + 5 # On ajoute un biais artificiel
        })

# Chargement
df = load_data()

# --- BARRE LATÉRALE (CONTROLES) ---
st.sidebar.header("⚙️ Calibration Parameters")
st.sidebar.info("Use these sliders to simulate a correction algorithm.")

# Simulation d'un modèle de correction linéaire (y = ax + b)
gain = st.sidebar.slider("Gain (Slope correction)", 0.5, 1.5, 1.0, 0.01)
offset = st.sidebar.slider("Offset (Zero correction)", -10.0, 10.0, 0.0, 0.1)

show_raw = st.sidebar.checkbox("Show Raw Data", value=True)

# --- TRAITEMENT DU SIGNAL (LE CŒUR DE VOTRE THÈSE) ---
# Dans le futur, vous appellerez ici vos fonctions de 'src/calibration.py'
# Pour l'instant, on fait le calcul en direct :
if 'raw_value' not in df.columns:
    # Si votre CSV s'appelle 'value', on le renomme pour la suite
    df = df.rename(columns={'value': 'raw_value'})

df['calibrated_value'] = (df['raw_value'] * gain) + offset

# --- VISUALISATION ---
st.subheader("📊 Sensor Signal Analysis")

col1, col2 = st.columns([3, 1])

with col1:
    # Préparation du graphique
    chart_data = df[['time', 'calibrated_value']]
    if show_raw:
        chart_data['raw_value'] = df['raw_value']
    
    # Affichage du graphique interactif
    st.line_chart(chart_data.set_index('time'))

with col2:
    st.write("### Statistics")
    rmse = np.sqrt(np.mean((df['calibrated_value'] - df['raw_value'])**2))
    st.metric("Mean Value", f"{df['calibrated_value'].mean():.2f} µg/m³")
    st.metric("Correction Delta (RMSE)", f"{rmse:.2f}")
    
    st.write("---")
    st.caption("Data Source: Demo Folder")
    st.dataframe(df.head(5), hide_index=True)