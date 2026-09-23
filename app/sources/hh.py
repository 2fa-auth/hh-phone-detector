from typing import Any

import httpx

from app.models import VacancyInput


class HHClient:
    """
    Small adapter around HH.ru API.

    HH-specific response mapping is isolated here.
    The rest of the application works only with VacancyInput.
    """

    def __init__(
        self,
        token: str | None = None,
        timeout: float = 10.0,
        base_url: str = "https://api.hh.ru",
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.headers = {
            "User-Agent": "resumetto-phone-mvp/0.1",
            "Accept": "application/json",
        }

        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_vacancy(self, vacancy_id: str) -> VacancyInput:
        url = f"{self.base_url}/vacancies/{vacancy_id}"

        with httpx.Client(
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            payload = response.json()

        return self._map_vacancy(payload)

    @staticmethod
    def _map_vacancy(payload: dict[str, Any]) -> VacancyInput:
        employer = payload.get("employer") or {}

        return VacancyInput(
            id=str(payload["id"]),
            url=payload.get("alternate_url"),
            title=payload.get("name", ""),
            company=employer.get("name", ""),
            description=payload.get("description", "") or "",
            contacts=payload.get("contacts"),
        )
