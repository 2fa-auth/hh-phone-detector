import json
from pathlib import Path

from app.models import VacancyInput


def load_fixtures(path: str | Path) -> list[VacancyInput]:
    root = Path(path)
    files = sorted(root.glob("*.json"))

    vacancies: list[VacancyInput] = []

    for file in files:
        data = json.loads(file.read_text(encoding="utf-8"))

        if isinstance(data, dict):
            data = [data]

        for item in data:
            vacancies.append(VacancyInput.model_validate(item))

    return vacancies
