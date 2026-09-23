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
```

### Recall

```text
TP / (TP + FN)
69 / (69 + 1)
= 98.57%
```

## Error analysis

There was one false negative.

The corresponding fixture contains the following phone-like value:

```text
+44 7700 900123
```

The value is rejected by `phonenumbers` validation.

The implementation intentionally keeps `is_valid_number()` validation enabled
instead of weakening validation to improve the synthetic recall score. This
helps prevent ordinary numeric identifiers from being classified as phone
numbers.

The evaluation therefore demonstrates the current behavior of the deterministic
pipeline rather than attempting to optimize the result for this particular
synthetic dataset.

## Interpretation

The current implementation produced zero false positives on this evaluation
dataset.

This is useful for the MVP because the task is specifically to identify
vacancies where an employer has actually published a phone number.

The reported metrics apply only to this 110-record synthetic evaluation dataset
and should not be interpreted as production metrics for HH.ru.

## Reproducibility

Run:

```bash
resumetto analyze fixtures_eval --output-dir output_eval
python evaluation/evaluate_results.py output_eval/results.json
```

The expected evaluation result is:

```text
Gold:      110
Results:   110
TP:        69
FP:        0
FN:        1
TN:        40
Precision: 100.00%
Recall:    98.57%
```
