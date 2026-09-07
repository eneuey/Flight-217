# Build Zero analysis record

## Analysis contract

- **Audience:** Elena Park, Aster network operations controller, using this as a teaching-case analysis.
- **Question:** Using information available four hours before scheduled gate arrival, will a synthetic Aster 217 service day finish at least 30 minutes late to the gate?
- **Descriptive story mode:** Describe represented conditions and eventual outcomes in the synthetic service-day table.
- **Predictive story mode:** Classify a represented synthetic service day as `late_30` or not from the permitted four-hour snapshot features.
- **Possible action:** A human may use a warning to inspect arrival plans and constraints. It does not authorize an automated gate assignment or operational decision.
- **Prediction boundary:** Four hours before scheduled gate arrival.
- **Unsupported claim:** This evidence cannot establish that the tree understands flight delays, explains their causes, works for a real airline, or should control an operational decision.

Each row represents one synthetic Aster 217 service day. The table combines information available at a common four-hour prediction snapshot with outcomes that became known later. Known snapshot fields include the identifier and date, snapshot timing metadata, `departure_delay_min`, `headwind_kts`, `destination_weather_index`, `arrival_demand_index`, and `weather_snapshot_age_min`. `final_gate_wait_min`, `arrival_delay_min`, and the derived label `late_30` are known only later. Therefore, the latter three fields are not model features.

## Descriptive story and artifact

**Question:** In the synthetic service-day records, how do estimated route headwind and eventual gate-arrival delay appear together?

The chart [`build_zero_scatter.png`](build_zero_scatter.png) plots estimated headwind against the later gate-arrival delay. Stronger headwinds tend to appear alongside larger delays, but flights at similar headwind values occur on both sides of the 30-minute threshold. This is a descriptive pattern in the generated dataset; it does not show that headwind alone determines or causes delay.

## Predictive story, baseline, and result

The target is `late_30`: whether the later gate-arrival delay was at least 30 minutes. The only features are `departure_delay_min`, `headwind_kts`, `destination_weather_index`, and `arrival_demand_index`, all designated as available at the four-hour snapshot. The program uses the supplied stratified 75/25 random split (`random_state=217`) and a depth-4 decision tree (`random_state=217`).

The majority class is chosen from training labels and predicts **not late** for every held-out row. On the 180 held-out rows, its accuracy is **0.828** (149/180). The shallow tree accuracy is **0.850** (153/180), an increase of **0.022** or four correctly classified held-out rows.

The tree confusion matrix, with rows as actual and columns as predicted, is:

| Actual / predicted | Not late | Late |
| --- | ---: | ---: |
| Not late | 143 (TN) | 6 (FP) |
| Late | 21 (FN) | 10 (TP) |

The labeled count display is [`build_zero_confusion_matrix.png`](build_zero_confusion_matrix.png). The warranted conclusion is only: **the fitted tree classified held-out synthetic rows under this split.**

## Agent contribution and review

**Exact instruction given to the agent:**

> In the supplied Build Zero program, add a readable confusion-matrix display. Do not change the dataset, feature list, target, split, random seed, model, or predictions. Show me the proposed edit and explain how I can test that the underlying four counts did not change.

**Bounded change:** The program retains the existing `confusion_matrix` calculation and adds a `ConfusionMatrixDisplay` using those same count values. It writes a labeled figure with raw integer counts, explicit actual/predicted axes, and the `Not late (< 30 min)` and `Late (>= 30 min)` labels.

**Visible result:** `build_zero_confusion_matrix.png` shows the four counts 143, 6, 21, and 10.

**Check 1 -- same predictive procedure:** The feature list, target, split size, stratification, random seed, depth-4 tree, and `predictions = tree.predict(X_test)` statement remain unchanged. The display consumes `counts` produced from those predictions; it does not fit or predict again.

**Check 2 -- count integrity and labels:** The printed matrix and the display both contain `[[143, 6], [21, 10]]`. These four cells sum to 180, the held-out test-set size. The declared row/column orientation makes those cells TN=143, FP=6, FN=21, and TP=10 rather than an ambiguous label order.

**Judgment:** Accepted. The change is bounded to presentation, retains raw counts, and makes the four outcomes readable without changing the model or its predictions.

## Demonstrated capability

The program can fit an inspectable shallow decision tree to permitted four-hour snapshot fields, evaluate it on held-out synthetic rows, display the four error types, and classify the supplied fictional current-flight snapshot.

## Questions the score does not answer

1. Does a random split provide an honest evaluation of a future service day when conditions may change over time?
2. How were the forecast-derived headwind, weather, and demand fields produced, and how do stale or incorrect inputs affect the result?
3. Which error type matters more to passengers and operations: a false warning or missing a late flight?
4. Does the tree-leaf late share behave like a calibrated probability?
5. Which gate, corridor, passenger, crew, and authority constraints are absent from this represented predictive task?
