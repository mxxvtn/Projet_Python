from pydantic import BaseModel, Field
from typing import List, Optional

class Commune(BaseModel):
    nom: str
    code: str
    codeDepartement: Optional[str] = None
    codeRegion: Optional[str] = None
    codesPostaux: Optional[List[str]] = []
    population: Optional[int] = 0
    surface: Optional[float] = 0.0  # En hectares
    centre: Optional[dict] = Field(default_factory=dict) # GeoJSON Point or similar structure

    @property
    def density(self) -> float:
        if self.surface and self.surface > 0 and self.population:
            # surface is in hectares. 1 hectare = 0.01 km2.
            surface_km2 = self.surface / 100
            return round(self.population / surface_km2, 1)
        return 0.0
