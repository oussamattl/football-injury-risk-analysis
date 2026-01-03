import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration
st.set_page_config(page_title="Injury Data Analysis - Foot", layout="wide")

st.title("⚽ Injury Risk Predictor : L'Intelligence au Service du Terrain")
st.markdown("---")

# --- LOGIQUE DE CALCUL ---
def calculer_score(age, minutes, repos, historique):
    # Ta pondération personnalisée
    score_charge = (minutes / 300) * 30 
    score_repos = (1 / repos) * 20 if repos > 0 else 20
    score_hist = (historique / 25) * 40 
    score_age = (age / 35) * 10 
    return min(score_charge + score_repos + score_hist + score_age, 100)

# --- SIDEBAR : INPUTS ---
st.sidebar.header("🕹️ Contrôle des Données")
choix_joueur = st.sidebar.selectbox("Sélectionner un profil", ["Kylian Mbappé", "Paul Pogba", "Neymar Jr.", "Créer un profil personnalisé"])

# Initialisation des variables
if choix_joueur == "Créer un profil personnalisé":
    # On permet ici de taper son propre nom !
    nom_affiche = st.sidebar.text_input("Nom du joueur", "Mon Joueur")
    age = st.sidebar.slider("Âge", 18, 40, 25)
    minutes = st.sidebar.number_input("Minutes jouées (7 derniers jours)", 0, 500, 180)
    repos = st.sidebar.slider("Jours de repos inter-match", 1, 10, 3)
    historique = st.sidebar.number_input("Nombre de blessures passées", 0, 50, 5)
else:
    # Données pré-remplies
    data = {
        "Kylian Mbappé": {"age": 26, "min": 285, "repos": 3, "hist": 2},
        "Paul Pogba": {"age": 32, "min": 20, "repos": 3, "hist": 15},
        "Neymar Jr.": {"age": 33, "min": 270, "repos": 2, "hist": 26},
    }
    p = data[choix_joueur]
    nom_affiche = choix_joueur
    age, minutes, repos, historique = p['age'], p['min'], p['repos'], p['hist']

# --- CALCUL ---
risk_score = calculer_score(age, minutes, repos, historique)

# --- AFFICHAGE PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📊 Analyse de Risque : {nom_affiche}")
    
    # Cartes d'indicateurs
    st.metric(label="Score de Risque Global", value=f"{risk_score:.1f}%")
    
    if risk_score > 60:
        st.error("⚠️ ALERTE ROUGE : Repos forcé préconisé.")
    elif risk_score > 40:
        st.warning("🟠 RISQUE MODÉRÉ : Surveillance accrue.")
    else:
        st.success("✅ RISQUE FAIBLE : Prêt pour le prochain match.")

    # Détails sous forme de tableau propre
    st.write("**Détails du profil :**")
    stats_df = pd.DataFrame({
        "Paramètre": ["Âge", "Charge de travail", "Récupération", "Fragilité"],
        "Valeur": [f"{age} ans", f"{minutes} min", f"{repos} jours", f"{historique} blessures"]
    })
    st.table(stats_df)

with col2:
    # La Jauge Plotly
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score,
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps' : [
                {'range': [0, 40], 'color': "#00cc96"},
                {'range': [40, 60], 'color': "#ffa15a"},
                {'range': [60, 100], 'color': "#ef553b"}],
        }
    ))
    fig.update_layout(margin=dict(t=30, b=0, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- SECTION MÉTHODOLOGIE (Ton Tableau 1 amélioré) ---
st.subheader("🧪 Méthodologie du Modèle de Pondération")
st.markdown("""
Pour que ce modèle soit utilisé par un staff pro, chaque variable a été filtrée selon 4 critères de fiabilité. 
Voici comment j'ai construit mon indice :
""")

# Tableau explicatif au lieu de chiffres bruts
methodo_df = pd.DataFrame({
    "Variable": ["Minutes Jouées", "Jours de Repos", "Âge", "Historique Blessures"],
    "Mesurable": ["✅", "✅", "✅", "✅"],
    "Pertinence": ["Directe (Charge)", "Directe (Récup)", "Structurelle", "Médicale"],
    "Score de Confiance": ["⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐"]
})

st.dataframe(methodo_df, use_container_width=True, hide_index=True)

st.info("**Note du développeur :** Ce modèle a été conçu dans le cadre d'un module à l'insa hdf pour démontrer l'importance de la Data dans la prévention des blessures.")