import pytest
from src.api.geo_api import GeoAPI
from src.models.commune import Commune

def test_search_communes():
    api = GeoAPI()
    results = api.search_communes("Paris")
    assert len(results) > 0
    # Check if Paris is in results
    paris_found = False
    for c in results:
        if c.nom == "Paris" and "75056" in c.code: # 75056 is INSEE code for Paris
            paris_found = True
            assert c.population > 2000000
            break
    assert paris_found

def test_get_communes_by_dept():
    api = GeoAPI()
    results = api.get_communes_by_dept("75")
    assert len(results) > 0
    # All should have codeDepartement 75
    for c in results:
        assert c.codeDepartement == "75"

def test_commune_density():
    c = Commune(nom="Test", code="00000", population=1000, surface=1000.0) # 1000 ha = 10 km2
    # Density = 1000 / 10 = 100
    assert c.density == 100.0

def test_commune_density_zero():
    c = Commune(nom="Test", code="00000", population=1000, surface=0.0)
    assert c.density == 0.0
