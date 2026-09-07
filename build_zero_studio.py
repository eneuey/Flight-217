#!/usr/bin/env python3
"""Build Zero: fit a model before we know enough to trust it."""

# %% Imports and data
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


DATA = Path(__file__).with_name("flight217_build_zero.csv")
FIGURE = Path(__file__).with_name("build_zero_scatter.png")
flights = pd.read_csv(DATA)

print("Shape:", flights.shape)
print(flights.head(3).to_string(index=False))

# %% Inspect before fitting
print("\nMissing values:")
print(flights.isna().sum().to_string())
print("\nLabel proportions:")
print(flights["late_30"].value_counts(normalize=True).sort_index().to_string())

# %% Draw one relationship
colors = flights["late_30"].map({0: "#4C78A8", 1: "#E45756"})
axis = flights.plot.scatter(
    x="headwind_kts",
    y="arrival_delay_min",
    c=colors,
    alpha=0.55,
    figsize=(8, 5),
)
axis.axhline(30, color="black", linestyle="--", linewidth=1)
axis.set_title("Synthetic Aster 217 service days")
axis.set_xlabel("Estimated route headwind (knots)")
axis.set_ylabel("Gate-arrival delay (minutes)")
axis.figure.tight_layout()
axis.figure.savefig(FIGURE, dpi=160)
plt.close(axis.figure)
print(f"\nSaved {FIGURE.name}")

# %% Establish a baseline
majority_class = int(flights["late_30"].mode().iloc[0])
baseline_accuracy = float((flights["late_30"] == majority_class).mean())
print(f"\nMajority class: {majority_class}")
print(f"Baseline accuracy: {baseline_accuracy:.3f}")

# %% Define a provisional predictive task
features = [
    "departure_delay_min",
    "headwind_kts",
    "destination_weather_index",
    "arrival_demand_index",
]
X = flights[features]
y = flights["late_30"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=217,
    stratify=y,
)

# %% Fit an inspectable model
tree = DecisionTreeClassifier(max_depth=4, random_state=217)
tree.fit(X_train, y_train)
predictions = tree.predict(X_test)

print(f"\nTree accuracy: {accuracy_score(y_test, predictions):.3f}")
print("Confusion matrix [[TN, FP], [FN, TP]]:")
print(confusion_matrix(y_test, predictions))
print("\nLearned rules:")
print(export_text(tree, feature_names=features))

# %% Apply it to the current fictional Flight 217 snapshot
current_flight = pd.DataFrame(
    [
        {
            "departure_delay_min": 0,
            "headwind_kts": 48,
            "destination_weather_index": 7.5,
            "arrival_demand_index": 8.5,
        }
    ]
)
prediction = int(tree.predict(current_flight)[0])
probability = float(tree.predict_proba(current_flight)[0, 1])
print(f"Current Flight 217 predicted late_30: {prediction}")
print(f"Current Flight 217 tree-leaf late share: {probability:.3f}")

# %% Questions to answer before acting
questions = [
    "Does a random split give an honest test of a future service day?",
    "What exactly produced each forecast-derived feature?",
    "Which errors matter to passengers and operations?",
    "Does the leaf proportion behave like a calibrated probability?",
    "Who, if anyone, may act on this output?",
]
print("\nUnresolved questions:")
for number, question in enumerate(questions, start=1):
    print(f"{number}. {question}")
