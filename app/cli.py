import argparse
import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from .pipeline import PhoneAnalyzer, analyze_batch
from .sources.fixtures import load_fixtures


def write_results_json(path: Path, results) -> None:
    path.write_text(
        json.dumps(
            [result.model_dump() for result in results],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def write_results_csv(path: Path, results) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "vacancy_id",
                "url",
                "title",
                "company",
                "has_phone",
                "phones",
            ],
        )
        writer.writeheader()

        for result in results:
            writer.writerow(
                {
                    "vacancy_id": result.vacancy_id,
                    "url": result.url or "",
                    "title": result.title,
                    "company": result.company,
                    "has_phone": result.has_phone,
                    "phones": "; ".join(
                        phone.normalized for phone in result.phones
                    ),
                }
            )


def write_errors_csv(path: Path, errors) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["vacancy_id", "error"])
        writer.writeheader()
        writer.writerows(errors)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find valid phone numbers in vacancy fixtures."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("input_dir", type=Path)
    analyze.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
    )
    analyze.add_argument(
        "--only-with-phone",
        action="store_true",
    )

    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        vacancies = load_fixtures(args.input_dir)

        analyzer = PhoneAnalyzer(
            default_region=os.getenv("DEFAULT_PHONE_REGION", "RU")
        )

        results, errors = analyze_batch(vacancies, analyzer)

        phone_vacancies = sum(result.has_phone for result in results)

        if args.only_with_phone:
            results = [result for result in results if result.has_phone]

        args.output_dir.mkdir(parents=True, exist_ok=True)

        write_results_json(args.output_dir / "results.json", results)
        write_results_csv(args.output_dir / "results.csv", results)
        write_errors_csv(args.output_dir / "errors.csv", errors)

        print(f"Received:  {len(vacancies)}")
        print(f"Processed: {len(vacancies) - len(errors)}")
        print(f"With phone: {phone_vacancies}")
        print(f"Errors:    {len(errors)}")
        print(f"Output:    {args.output_dir.resolve()}")
