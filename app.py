import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Thesis Framework: Sensor Reliability",
    page_icon="📡",
    layout="wide"
)

# --- HEADER ---
st.title("📡 Cadre Méthodologique pour la Fiabilisation des Capteurs")
st.markdown("""
**Sujet de Thèse :** *Développement d'un cadre méthodologique pour la fiabilisation de réseaux de capteurs 
de pollution de l'air : de la fiabilisation en laboratoire à la maintenance dynamique in-situ.*
""")

# --- NAVIGATION ---
tab_context, tab_phase1, tab_phase2, tab_phase3 = st.tabs([
    "🏠 Contexte & Enjeux", 
    "Phase 1 : Métrologie", 
    "Phase 2 : Calibration IA", 
    "Phase 3 : Fusion de Données"
])

# ==================================================
# ONGLET 0 : CONTEXTE
# ==================================================
with tab_context:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("Le Défi des Capteurs Low-Cost")
        st.write("""
        La pollution atmosphérique est un enjeu sanitaire majeur[cite: 3]. 
        Pour la surveiller, les capteurs low-cost offrent une couverture spatiale inédite[cite: 13, 14].
        
        Cependant, leur déploiement massif est freiné par trois limites techniques majeures :
        """)
        st.warning("1. Sensibilité aux facteurs environnementaux (T°, Humidité) [cite: 18]")
        st.warning("2. Dérive temporelle et vieillissement des composants [cite: 19]")
        st.warning("3. Faible sélectivité (incapacité à discriminer certains polluants) [cite: 20]")
        
    with col2:
        st.info("🎯 Objectifs de la thèse")
        st.markdown("""
        Ce projet vise à développer un **cadre méthodologique complet** [cite: 44] pour :
        1.  **Qualifier** la fiabilité d'une donnée brute.
        2.  **Corriger** le signal via des algorithmes d'IA.
        3.  **Valider** la mesure via le contexte réseau.
        """)

# ==================================================
# PHASE 1 : METROLOGIE
# ==================================================
with tab_phase1:
    st.header("Phase 1 : Quantification de la Fiabilité")
    
    # --- LE "POURQUOI" (MÉTHODOLOGIE) ---
    with st.expander("📘 Méthodologie : Comment définit-on une mesure fiable ?"):
        st.markdown("""
        Avant de corriger, il faut mesurer l'erreur. Cette phase établit un protocole rigoureux pour comparer 
        le capteur low-cost à un instrument de référence[cite: 54, 56].
        
        Nous utilisons principalement deux métriques :
        * **La Justesse (Biais) :** L'écart moyen par rapport à la réalité.
        * **L'Incertitude (Précision) :** La dispersion des mesures, souvent évaluée par méthodes de Monte-Carlo ou bayésiennes[cite: 30].
        """)
        st.latex(r'''
        RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_{pred,i} - y_{ref,i})^2}
        ''')

    # --- LA DÉMO ---
    st.write("### 🛠️ Banc d'essai virtuel")
    
    # Génération de données
    dates = pd.date_range("2024-01-01", periods=100, freq="h")
    ref = np.sin(np.linspace(0, 10, 100)) * 10 + 20
    sensor = ref * 0.8 + 5 + np.random.normal(0, 2, 100)
    df_p1 = pd.DataFrame({"Date": dates, "Reference": ref, "LowCost": sensor})
    
    col_metrics, col_plot = st.columns([1, 3])
    with col_metrics:
        bias = np.mean(df_p1["LowCost"] - df_p1["Reference"])
        rmse = np.sqrt(np.mean((df_p1["LowCost"] - df_p1["Reference"])**2))
        st.metric("Biais (Justesse)", f"{bias:.2f}")
        st.metric("RMSE (Incertitude)", f"{rmse:.2f}")
    with col_plot:
        st.line_chart(df_p1.set_index("Date"))

# ==================================================
# PHASE 2 : CALIBRATION IA
# ==================================================
with tab_phase2:
    st.header("Phase 2 : Algorithmes de Fiabilisation")

    # --- LE "COMMENT" (MÉTHODOLOGIE) ---
    with st.expander("📘 Méthodologie : Pourquoi l'IA est-elle nécessaire ?"):
        st.markdown("""
        Les méthodes classiques (régression linéaire) échouent car la relation entre le signal et la pollution 
        est **non-linéaire** et dépend des interférences.
        
        **L'approche proposée :**
        Utiliser l'apprentissage automatique (Réseaux de neurones, Random Forest) pour apprendre cette complexité 
        à partir de données labellisées[cite: 23, 24].
        """)
        st.latex(r'''
        C_{est} = f(S_{raw}, T, RH, P)
        ''')
        st.caption("Où f est une fonction non-linéaire apprise par le modèle.")

    # --- LA DÉMO ---
    st.info("Simulation interactive de la correction algorithmique.")
    gain = st.slider("Facteur de correction simulé", 0.5, 1.5, 1.0)
    df_p1["Corrected"] = df_p1["LowCost"] * gain
    st.line_chart(df_p1.set_index("Date")[["Reference", "Corrected"]])

# ==================================================
# PHASE 3 : FUSION DE DONNÉES
# ==================================================
with tab_phase3:
    st.header("Phase 3 : Maintenance Dynamique & Réseau")
    
    # --- LE "POURQUOI" (MÉTHODOLOGIE) ---
    with st.expander("📘 Méthodologie : La force du réseau"):
        st.markdown("""
        Un capteur seul est vulnérable. En réseau, chaque capteur bénéficie du contexte de ses voisins.
        La méthodologie repose sur la **fusion de données hétérogènes** [cite: 33] pour :
        1.  Capturer les dynamiques spatio-temporelles de la pollution.
        2.  Détecter les anomalies (ex: un capteur dérive seul vs un pic de pollution global)[cite: 34].
        """)
    
    st.write("*Simulation de réseau à venir...*")