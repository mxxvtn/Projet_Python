import requests
from typing import List, Optional
from src.models.commune import Commune
from src.cache.cache_manager import get_session

BASE_URL = "https://geo.api.gouv.fr"

class GeoAPI:
    def __init__(self):
        self.session = get_session()

    def get_communes(self, params: dict = None) -> List[Commune]:
        """
        Fetch communes based on parameters.
        Common params: nom, codePostal, codeDepartement, codeRegion.
        We force fields to include population, surface, centre.
        """
        if params is None:
            params = {}

        # Always request these fields
        fields = ["nom", "code", "codesPostaux", "codeDepartement", "codeRegion", "population", "surface", "centre"]
        params["fields"] = ",".join(fields)

        try:
            response = self.session.get(f"{BASE_URL}/communes", params=params)
            response.raise_for_status()
            data = response.json()

            communes = []
            for item in data:
                # Handle potential missing fields gracefully
                communes.append(Commune(**item))
            return communes
        except requests.RequestException as e:
            print(f"Error fetching communes: {e}")
            return []

    def search_communes(self, query: str) -> List[Commune]:
        """
        Search communes by name (partial match).
        """
        return self.get_communes({"nom": query, "boost": "population"})

    def get_communes_by_dept(self, code_dept: str) -> List[Commune]:
        return self.get_communes({"codeDepartement": code_dept})

    def get_communes_by_region(self, code_region: str) -> List[Commune]:
        return self.get_communes({"codeRegion": code_region})

    def get_communes_by_postal_code(self, postal_code: str) -> List[Commune]:
        return self.get_communes({"codePostal": postal_code})

    def get_all_communes(self) -> List[Commune]:
        """
        Be careful, this might be heavy.
        """
        return self.get_communes({})
