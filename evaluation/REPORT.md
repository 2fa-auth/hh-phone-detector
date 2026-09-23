# Evaluation Report

## Dataset

The evaluation dataset contains 110 synthetic vacancy records:

- 70 vacancies with a phone number;
- 40 vacancies without a phone number.

Each vacancy has a manually defined expected `has_phone` value in
`evaluation/gold.csv`.

The dataset is intended to validate the implementation and is not
representative of the full HH.ru vacancy population.

## Method

The pipeline:

1. checks structured `contacts`;
2. extracts phone candidates from the vacancy description;
3. validates candidates with `phonenumbers`;
4. normalizes valid numbers to E.164;
5. deduplicates numbers after normalization.

No external web search is performed and no phone numbers are generated.

## Results

| Metric | Value |
|---|---:|
| Gold records | 110 |
| Results | 110 |
| True Positive | 69 |
| False Positive | 0 |
| False Negative | 1 |
| True Negative | 40 |
| Precision | 100.00% |
| Recall | 98.57% |

### Precision

```text
TP / (TP + FP)
69 / (69 + 0)
= 100.00%
