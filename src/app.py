import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import plotly.express as px
from src.api.geo_api import GeoAPI
from src.visualization.maps import create_map

# Initialize API
api = GeoAPI()

st.set_page_config(page_title="France Demographic Analyzer", layout="wide")

st.title("🇫🇷 France Demographic Analyzer")

st.sidebar.header("Filtres & Recherche")

# Search Type
search_type = st.sidebar.radio("Mode de recherche", ["Par Nom", "Par Code Postal", "Par Département", "Par Région"])

data = []
results_msg = ""

if search_type == "Par Nom":
    query = st.sidebar.text_input("Nom de la commune", "")
    if query:
        with st.spinner('Recherche...'):
            data = api.search_communes(query)
            results_msg = f"{len(data)} communes trouvées."

elif search_type == "Par Code Postal":
    postal_code = st.sidebar.text_input("Code Postal (ex: 75001, 33000)", "")
    if postal_code:
        with st.spinner('Recherche...'):
            data = api.get_communes_by_postal_code(postal_code)
            results_msg = f"{len(data)} communes trouvées pour le code postal {postal_code}."

elif search_type == "Par Département":
    dept_code = st.sidebar.text_input("Code Département (ex: 75, 33)", "")
    if dept_code:
        with st.spinner('Chargement...'):
            data = api.get_communes_by_dept(dept_code)
            results_msg = f"{len(data)} communes trouvées dans le département {dept_code}."

elif search_type == "Par Région":
    region_code = st.sidebar.text_input("Code Région (ex: 11, 84)", "")
    if region_code:
        with st.spinner('Chargement...'):
            data = api.get_communes_by_region(region_code)
            results_msg = f"{len(data)} communes trouvées dans la région {region_code}."

# Filtering on results
if data:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filtrage des résultats")

    # Create DataFrame for easier manipulation
    df = pd.DataFrame([c.dict() for c in data])
    # Add density column
    df['density'] = df.apply(lambda x: x['population'] / (x['surface']/100) if x['surface'] and x['population'] else 0, axis=1)
    df['density'] = df['density'].round(1)

    min_pop, max_pop = int(df['population'].min()), int(df['population'].max())
    if min_pop < max_pop:
        pop_range = st.sidebar.slider("Population", min_pop, max_pop, (min_pop, max_pop))
        df = df[(df['population'] >= pop_range[0]) & (df['population'] <= pop_range[1])]

    st.info(results_msg)

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Données & Classement", "🗺️ Carte", "📈 Statistiques & Densité", "⚖️ Comparateur"])

    with tab1:
        st.subheader("Données des communes")
        st.dataframe(df[['nom', 'code', 'codeDepartement', 'population', 'surface', 'density']].sort_values(by='population', ascending=False))

        # Download
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger en CSV", csv, "communes.csv", "text/csv")
        with col2:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Communes')
            processed_data = output.getvalue()
            st.download_button("Télécharger en Excel", processed_data, "communes.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with tab2:
        st.subheader("Carte Interactive")
        # Re-convert filtered df back to list of Commune objects for the map function (or update map function to handle df)
        # For simplicity, we just rebuild objects from filtered df or map logic to DF
        # Let's map only top 100 if there are too many to avoid lagging
        if len(df) > 500:
            st.warning("Affichage limité aux 500 communes les plus peuplées pour la performance.")
            map_df = df.sort_values(by='population', ascending=False).head(500)
        else:
            map_df = df

        # We need to reconstruct Commune objects for our create_map function or adapt it
        # Adapting create_map on the fly here or using the one from utils
        # Let's reconstruct small list
        from src.models.commune import Commune
        map_communes = [Commune(**row.to_dict()) for index, row in map_df.iterrows()]

        m = create_map(map_communes)
        st_folium(m, width=1200, height=600)

    with tab3:
        st.subheader("Analyse de la densité")
        if not df.empty:
            fig = px.scatter(df, x="surface", y="population", hover_name="nom", log_x=True, log_y=True,
                             title="Population vs Surface (échelle log)", size="density", color="density")
            st.plotly_chart(fig)

            st.subheader("Répartition de la population")
            fig2 = px.histogram(df, x="population", nbins=50, title="Distribution de la population")
            st.plotly_chart(fig2)

    with tab4:
        st.subheader("Comparateur de communes")
        communes_to_compare = st.multiselect("Sélectionnez les communes à comparer", df['nom'].unique())

        if communes_to_compare:
            comp_df = df[df['nom'].isin(communes_to_compare)]

            # Display stats side by side
            st.write("### Tableau comparatif")
            st.dataframe(comp_df[['nom', 'code', 'population', 'surface', 'density']].set_index('nom').T)

            # Bar chart comparison
            st.write("### Comparaison Population")
            fig_comp = px.bar(comp_df, x='nom', y='population', title="Comparaison Population", color='nom')
            st.plotly_chart(fig_comp)

            st.write("### Comparaison Densité")
            fig_dens = px.bar(comp_df, x='nom', y='density', title="Comparaison Densité (hab/km²)", color='nom')
            st.plotly_chart(fig_dens)

else:
    st.info("Veuillez effectuer une recherche pour afficher les résultats.")
    st.markdown("""
    ### Bienvenue sur France Demographic Analyzer

    Cette application vous permet de :
    - Rechercher des communes françaises
    - Visualiser leur population et densité
    - Voir leur emplacement sur une carte
    - Comparer différentes villes

    Utilisez le menu de gauche pour commencer !
    """)
