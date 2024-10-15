import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random

# Fonction de prétraitement pour uniformiser les fichiers CSv
def preprocess_data(df):
    df = df.melt(id_vars=["Province/State", "Country/Region", "Lat", "Long"], 
                 var_name="Date", value_name="Count")
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    return df

# Chargement des fichiers CSV
confirmed_df = pd.read_csv("time_series_covid19_confirmed_global.csv")
deaths_df = pd.read_csv("time_series_covid19_deaths_global.csv")
recovered_df = pd.read_csv("time_series_covid19_recovered_global.csv")

# Prétraitement des données
confirmed_df = preprocess_data(confirmed_df)
deaths_df = preprocess_data(deaths_df)
recovered_df = preprocess_data(recovered_df)

# Configuration de la page Streamlit
st.set_page_config(page_title="Tableau de Bord COVID-19", layout="wide")
st.title("📊 Tableau de Bord COVID-19")

# En-tête
st.markdown("<h1 style='text-align: center; color: #007bff;'>Analyse de la Pandémie COVID-19</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Section : Affichage des Données Brutes avec filtres
st.header("Affichage des Données Brutes")

# Option pour sélectionner le jeu de données à afficher
dataset_choice = st.selectbox("Sélectionnez le jeu de données à afficher", 
                              ["Cas Confirmés", "Décès", "Guérisons"])

# Sélection du jeu de données en fonction du choix
if dataset_choice == "Cas Confirmés":
    df_to_display = confirmed_df
elif dataset_choice == "Décès":
    df_to_display = deaths_df
else:
    df_to_display = recovered_df

# Options pour sélectionner les colonnes à afficher
st.markdown("#### Sélectionnez les colonnes à afficher")
columns = st.multiselect("", df_to_display.columns.tolist(), default=df_to_display.columns.tolist())

# Option pour sélectionner le nombre de lignes à afficher
st.markdown("#### Sélectionnez le nombre de lignes à afficher")
rows = st.slider('', min_value=5, max_value=len(df_to_display), value=10)

# Options de filtrage
st.markdown("#### Filtrer les données par Pays")
countries = df_to_display['Country/Region'].unique().tolist()
selected_countries = st.multiselect("", options=countries, default=[])

# Filtrage par date
st.markdown("#### Filtrer les données par Date")
date_range = st.date_input("Sélectionnez une plage de dates", 
                           [df_to_display['Date'].min(), df_to_display['Date'].max()])

# Filtrer les données en fonction des pays et de la plage de dates sélectionnés
filterData = df_to_display

if selected_countries:
    filterData = filterData[filterData['Country/Region'].isin(selected_countries)]

if len(date_range) == 2:
    start_date, end_date = date_range
    filterData = filterData[(filterData['Date'] >= pd.to_datetime(start_date)) & (filterData['Date'] <= pd.to_datetime(end_date))]

# Affichage des données filtrées
if columns:
    with st.expander("Aperçu des données filtrées"):
        st.dataframe(filterData[columns].head(rows).style.set_table_styles(
            [{'selector': 'th', 'props': [('background-color', '#f2f2f2')]}]
        ))
else:
    st.warning("Sélectionnez des colonnes pour afficher les données.")

st.markdown("<hr>", unsafe_allow_html=True)

# Section 1 : Informations sur un Pays Sélectionné
st.header("1. Informations sur un Pays Sélectionné")

# Sélection du pays à analyser
country = st.selectbox("🔍 Sélectionnez un pays", confirmed_df['Country/Region'].unique())

# Filtrer les données par pays
confirmed_country = confirmed_df[confirmed_df['Country/Region'] == country]
deaths_country = deaths_df[deaths_df['Country/Region'] == country]
recovered_country = recovered_df[recovered_df['Country/Region'] == country]

# Calculer les totaux
total_confirmed = confirmed_country['Count'].sum()
total_deaths = deaths_country['Count'].sum()
total_recovered = recovered_country['Count'].sum()

# Affichage des totaux dans des cartes stylisées avec icônes
st.markdown(f"<h2 style='text-align: center;'>Statistiques COVID-19 pour {country}</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #007bff;'>🦠 Cas Confirmés</h3>"
                 f"<h2 style='color: #007bff;'>{total_confirmed}</h2>"
                 f"</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #dc3545;'>☠️ Décès</h3>"
                 f"<h2 style='color: #dc3545;'>{total_deaths}</h2>"
                 f"</div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='background-color: #d4edda; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #28a745;'>💊 Guérisons</h3>"
                 f"<h2 style='color: #28a745;'>{total_recovered}</h2>"
                 f"</div>", unsafe_allow_html=True)

# Section 4 : Évolution des Cas pour le pays sélectionné
st.header(f"4. Évolution des Cas pour {country}")

# Graphique pour l'évolution des cas confirmés du pays sélectionné
fig_country_confirmed = px.line(confirmed_country, x='Date', y='Count', 
                                 title=f'Évolution des Cas Confirmés - {country}',
                                 labels={'Count': 'Nombre de Cas Confirmés', 'Date': 'Date'},
                                 template='plotly_white')
st.plotly_chart(fig_country_confirmed)

# Graphique pour l'évolution des décès du pays sélectionné
fig_country_deaths = px.line(deaths_country, x='Date', y='Count', 
                              title=f'Évolution des Décès - {country}',
                              labels={'Count': 'Nombre de Décès', 'Date': 'Date'},
                              template='plotly_white')
st.plotly_chart(fig_country_deaths)

# Graphique pour l'évolution des guérisons du pays sélectionné
fig_country_recovered = px.line(recovered_country, x='Date', y='Count', 
                                 title=f'Évolution des Guérisons - {country}',
                                 labels={'Count': 'Nombre de Guérisons', 'Date': 'Date'},
                                 template='plotly_white')
st.plotly_chart(fig_country_recovered)

# Section 2 : Répartition Mondiale des Cas, Décès et Guérisons
st.header("2. Répartition Mondiale des Cas, Décès et Guérisons")

# Répartition mondiale des cas confirmés
fig_world_cases = px.choropleth(confirmed_df.groupby('Country/Region').agg({'Count':'sum'}).reset_index(),
                                locations='Country/Region', locationmode='country names', 
                                color='Count', title='🌍 Cas Confirmés par Pays', 
                                color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig_world_cases)

# Répartition mondiale des décès
fig_world_deaths = px.choropleth(deaths_df.groupby('Country/Region').agg({'Count':'sum'}).reset_index(),
                                 locations='Country/Region', locationmode='country names', 
                                 color='Count', title='🌍 Décès par Pays', 
                                 color_continuous_scale=px.colors.sequential.Reds)
st.plotly_chart(fig_world_deaths)

# Répartition mondiale des guérisons
fig_world_recovered = px.choropleth(recovered_df.groupby('Country/Region').agg({'Count':'sum'}).reset_index(),
                                    locations='Country/Region', locationmode='country names', 
                                    color='Count', title='🌍 Guérisons par Pays', 
                                    color_continuous_scale=px.colors.sequential.Greens)
st.plotly_chart(fig_world_recovered)

# Section 3 : Comparaison Temporelle entre Pays
st.header("3. Comparaison Temporelle des Pays")

# Sélection des pays à comparer
default_countries = ["Senegal", "Angola"]
selected_countries = st.multiselect("🔗 Sélectionnez des pays à comparer", 
                                     options=confirmed_df['Country/Region'].unique(), 
                                     default=default_countries)

# Générer une couleur unique pour chaque pays
def generate_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        colors.append(f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.6)')
    return colors

# Dictionnaire pour stocker les couleurs des pays
country_colors = {country: color for country, color in zip(selected_countries, generate_colors(len(selected_countries)))}

# Graphique comparatif des cas confirmés
fig_temp_confirmed = go.Figure()

for country in selected_countries:
    country_data = confirmed_df[confirmed_df['Country/Region'] == country]
    fig_temp_confirmed.add_trace(go.Scatter(x=country_data['Date'], 
                                            y=country_data['Count'], 
                                            mode='lines+markers', 
                                            name=f'Cas Confirmés - {country}',
                                            line=dict(width=2, color=country_colors[country]),
                                            marker=dict(size=6)))

fig_temp_confirmed.update_layout(title="📈 Évolution des Cas Confirmés dans le Temps",
                                  xaxis_title='Date',
                                  yaxis_title='Nombre de Cas Confirmés',
                                  template='plotly_white')
st.plotly_chart(fig_temp_confirmed)

# Graphique comparatif des décès
fig_temp_deaths = go.Figure()

for country in selected_countries:
    country_data = deaths_df[deaths_df['Country/Region'] == country]
    fig_temp_deaths.add_trace(go.Scatter(x=country_data['Date'], 
                                         y=country_data['Count'], 
                                         mode='lines+markers', 
                                         name=f'Décès - {country}',
                                         line=dict(color=country_colors[country], width=2),
                                         marker=dict(size=6)))

fig_temp_deaths.update_layout(title="⚰️ Évolution des Décès dans le Temps",
                              xaxis_title='Date',
                              yaxis_title='Nombre de Décès',
                              template='plotly_white')
st.plotly_chart(fig_temp_deaths)

# Graphique comparatif des guérisons
fig_temp_recovered = go.Figure()

for country in selected_countries:
    country_data = recovered_df[recovered_df['Country/Region'] == country]
    fig_temp_recovered.add_trace(go.Scatter(x=country_data['Date'], 
                                            y=country_data['Count'], 
                                            mode='lines+markers', 
                                            name=f'Guérisons - {country}',
                                            line=dict(color=country_colors[country], width=2),
                                            marker=dict(size=6)))

fig_temp_recovered.update_layout(title="💊 Évolution des Guérisons dans le Temps",
                                  xaxis_title='Date',
                                  yaxis_title='Nombre de Guérisons',
                                  template='plotly_white')
st.plotly_chart(fig_temp_recovered)


# Section 4 : Taux d'Infection et de Mortalité
st.header("4. Taux d'Infection et de Mortalité")

# Taux d'infection et de mortalité pour les cinq pays les plus touchés
top_countries = confirmed_df.groupby('Country/Region')['Count'].max().nlargest(5).index.tolist()
fig_variations = go.Figure()

for country in top_countries:
    country_data = confirmed_df[confirmed_df['Country/Region'] == country]
    mortality_rate = (deaths_df[deaths_df['Country/Region'] == country]['Count'] / country_data['Count']) * 100
    infection_rate = (country_data['Count'] / country_data['Count'].sum()) * 100
    fig_variations.add_trace(go.Bar(x=[country], y=[mortality_rate.values[-1]], name='Taux de Mortalité (%)',
                                     marker_color='red'))
    fig_variations.add_trace(go.Bar(x=[country], y=[infection_rate.values[-1]], name='Taux d\'Infection (%)',
                                     marker_color='blue'))

fig_variations.update_layout(barmode='group', title="📊 Taux d'Infection et de Mortalité des 5 Pays les Plus Touchés",
                             xaxis_title='Pays', yaxis_title='Taux (%)')

st.plotly_chart(fig_variations)

# Section 5 : Taux de Mortalité et de Guérison Global
st.header("5. Taux de Mortalité et de Guérison Global")

# Calcul des taux globaux
global_mortality_rate = (total_deaths / total_confirmed) * 100 if total_confirmed > 0 else 0
global_recovery_rate = (total_recovered / total_confirmed) * 100 if total_confirmed > 0 else 0

# Cartes pour les taux de mortalité et de guérison
col10, col11 = st.columns(2)

with col10:
    st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #dc3545;'>Taux de Mortalité (%)</h3>"
                 f"<h2 style='color: #dc3545;'>{global_mortality_rate:.2f}%</h2>"
                 f"</div>", unsafe_allow_html=True)

with col11:
    st.markdown(f"<div style='background-color: #d4edda; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #28a745;'>Taux de Guérison (%)</h3>"
                 f"<h2 style='color: #28a745;'>{global_recovery_rate:.2f}%</h2>"
                 f"</div>", unsafe_allow_html=True)

# Section 6 : Totaux Globaux
st.header("6. Totaux Globaux")

# Affichage des totaux globaux pour les cas confirmés, décès et guérisons
col12, col13, col14 = st.columns(3)

with col12:
    st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #007bff;'>🦠Total Cas Confirmés</h3>"
                 f"<h2 style='color: #007bff;'>{total_confirmed}</h2>"
                 f"</div>", unsafe_allow_html=True)

with col13:
    st.markdown(f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #dc3545'>☠️Total Décès</h3>"
                 f"<h2 style='color: #dc3545'>{total_deaths}</h2>"
                 f"</div>", unsafe_allow_html=True)

with col14:
    st.markdown(f"<div style='background-color: #d4edda; border-radius: 10px; padding: 20px; text-align: center;'>"
                 f"<h3 style='color: #28a745;'>💊Total Guérisons</h3>"
                 f"<h2 style='color: #28a745;'>{total_recovered}</h2>"
                 f"</div>", unsafe_allow_html=True)



# Ajout d'un pied de page
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='text-align: center; color: #777;'>"
             "Universite Cheikh Anta Diop de Dakar <br>"
             "Créé avec ❤️ par Samba SY", unsafe_allow_html=True)