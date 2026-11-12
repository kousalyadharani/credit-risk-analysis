# Credit Risk Analysis

Reconstructed from the portfolio's Python/Pandas/SQL data cleaning, clustering and segmentation, and Power BI reporting description. No original credit dataset or customer data is included.

## Run

Provide a CSV and numeric feature names: `python3 credit_risk.py data.csv --features income,utilization --clusters 3`. Incomplete/non-finite rows are excluded and returned records retain an input ID/source row. A deterministic standardized k-means implementation assigns segment labels; cluster labels are arbitrary and are not credit decisions.

No risk score, lending recommendation, protected-class feature, or validation metric is inferred from the portfolio description. Any real use needs documented data provenance, leakage checks, stability analysis, and domain review.

## Verify

`python3 -m unittest -v`
