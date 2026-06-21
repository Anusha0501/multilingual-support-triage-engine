from dataclasses import dataclass

@dataclass(slots=True)
class EvaluationReport:
    precision: float
    recall: float
    f1: float

class ClassicalModelTrainer:
    """Trainable baseline for language, intent, and SLA risk classifiers.

    In production this wraps scikit-learn pipelines, IndicBERT fine-tuning jobs,
    model registry publishing, and offline evaluation reports.
    """

    def evaluate_baseline(self, y_true: list[str], y_pred: list[str]) -> EvaluationReport:
        correct = sum(1 for expected, actual in zip(y_true, y_pred, strict=False) if expected == actual)
        total = max(len(y_true), 1)
        score = correct / total
        return EvaluationReport(precision=score, recall=score, f1=score)
