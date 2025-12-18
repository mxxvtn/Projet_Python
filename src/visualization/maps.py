import folium
from typing import List
from src.models.commune import Commune
from folium.plugins import MarkerCluster

def create_map(communes: List[Commune], center_coords=[46.603354, 1.888334], zoom=6) -> folium.Map:
    """
    Creates a folium map with markers for the given communes.
    """
    m = folium.Map(location=center_coords, zoom_start=zoom)

    marker_cluster = MarkerCluster().add_to(m)

    for commune in communes:
        if commune.centre and 'coordinates' in commune.centre:
            # GeoJSON Point coordinates are [lon, lat], Folium wants [lat, lon]
            lon, lat = commune.centre['coordinates']

            tooltip_text = f"{commune.nom} ({commune.code})"
            popup_text = f"""
            <b>{commune.nom}</b><br>
            Population: {commune.population}<br>
            Densité: {commune.density} hab/km²<br>
            Surface: {commune.surface} ha
            """

            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                tooltip=tooltip_text
            ).add_to(marker_cluster)

    return m
