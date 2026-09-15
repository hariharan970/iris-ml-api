from prometheus_client import Counter


predictions_total = Counter(
    "iris_predictions_total",
    "Total number of successful Iris predictions",
    ["predicted_class"],
)
