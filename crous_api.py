"""
Module de communication avec l'API interne du CROUS (trouverunlogement.lescrous.fr).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import requests


@dataclass
class Accommodation:
    """Représentation structurée d'un logement CROUS."""
    id: int
    title: str
    residence_name: str
    address: str
    city: str
    rent_min: float
    rent_max: float
    area_min: float
    area_max: float
    equipments: List[str] = field(default_factory=list)
    transports: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    url: str = "https://trouverunlogement.lescrous.fr"

    @property
    def rent_formatted(self) -> str:
        """Retourne le loyer formaté en euros."""
        if self.rent_min == self.rent_max:
            return f"{self.rent_min:.2f} €/mois"
        return f"{self.rent_min:.2f} € à {self.rent_max:.2f} €/mois"

    @property
    def area_formatted(self) -> str:
        """Retourne la surface formatée en m²."""
        if self.area_min == self.area_max:
            return f"{self.area_min} m²"
        return f"{self.area_min} à {self.area_max} m²"


class CrousAPI:
    """Client pour interroger l'API REST de TrouverUnLogement."""

    BASE_URL = "https://trouverunlogement.lescrous.fr"
    SEARCH_ENDPOINT = f"{BASE_URL}/api/fr/search/47"

    DEFAULT_HEADERS = {
        "accept": "application/ld+json, application/json",
        "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": BASE_URL,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    def __init__(self, phpsessid: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        if phpsessid:
            self.session.cookies.set("PHPSESSID", phpsessid, domain="trouverunlogement.lescrous.fr")

    def search(
        self,
        bounds: Optional[str] = None,
        max_price: Optional[float] = None,
        page: int = 1,
        page_size: int = 24
    ) -> Tuple[int, List[Accommodation]]:
        """
        Effectue une recherche de logements CROUS.
        
        :param bounds: Bounding box sous la forme 'lon1_lat1_lon2_lat2' ou None pour toute la France.
        :param max_price: Prix maximum en euros (ex: 600).
        :param page: Numéro de page (1 par défaut).
        :param page_size: Nombre de résultats par page (24 par défaut).
        :return: (total_trouvé, liste_de_logements)
        """
        payload = {
            "idTool": 47,
            "need_aggregation": True,
            "page": page,
            "pageSize": page_size,
            "sector": None,
            "occupationModes": [],
            "residence": None,
            "precision": 5,
            "equipment": [],
            "area": {"min": 0},
            "adaptedPmr": False,
            "toolMechanism": "residual"
        }

        # Conversion du prix en centimes d'euros
        if max_price is not None and max_price > 0:
            payload["price"] = {"max": int(max_price * 100)}
        else:
            payload["price"] = {"max": 10000000}

        # Conversion des coordonnées géographiques
        if bounds:
            try:
                coords = [float(c) for c in bounds.split("_")]
                if len(coords) == 4:
                    payload["location"] = [
                        {"lon": coords[0], "lat": coords[1]},
                        {"lon": coords[2], "lat": coords[3]}
                    ]
            except ValueError:
                payload["location"] = None
        else:
            payload["location"] = None

        response = self.session.post(self.SEARCH_ENDPOINT, json=payload, timeout=15)
        response.raise_for_status()

        data = response.json()
        total = data.get("results", {}).get("total", {}).get("value", 0)
        raw_items = data.get("results", {}).get("items", [])

        accommodations = []
        for item in raw_items:
            residence = item.get("residence", {})
            entity = residence.get("entity", {})

            # Loyers (en centimes dans l'API)
            rents = [
                m.get("rent", {}).get("min", 0) / 100
                for m in item.get("occupationModes", [])
                if m.get("rent")
            ]
            rent_min = min(rents) if rents else 0.0
            rent_max = max(rents) if rents else rent_min

            # Surfaces
            area_info = item.get("area", {})
            area_min = float(area_info.get("min", 0.0))
            area_max = float(area_info.get("max", area_min))

            # Équipements
            equipments = [eq.get("label") for eq in item.get("equipments", []) if eq.get("label")]

            # Transports
            transports = []
            for pt in residence.get("publicTransports", []):
                desc = pt.get("description")
                if desc:
                    transports.append(desc)

            # Photos
            medias = item.get("medias") or residence.get("medias") or []
            image_url = None
            if medias and isinstance(medias, list) and len(medias) > 0:
                src = medias[0].get("src")
                if src:
                    image_url = f"{self.BASE_URL}/resources/{src}"

            acc = Accommodation(
                id=item.get("id"),
                title=item.get("label", "Logement"),
                residence_name=residence.get("label", "Résidence CROUS"),
                address=residence.get("address", "Adresse non précisée"),
                city=entity.get("name", ""),
                rent_min=rent_min,
                rent_max=rent_max,
                area_min=area_min,
                area_max=area_max,
                equipments=equipments,
                transports=transports,
                image_url=image_url,
                url=f"{self.BASE_URL}/tools/47/search"
            )
            accommodations.append(acc)

        return total, accommodations
