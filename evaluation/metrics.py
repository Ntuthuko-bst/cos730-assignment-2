# =============================================================================
# EMPIRICAL EVALUATION - Task 6
# 
# Purpose: Measures code complexity and interaction metrics for both systems
# =============================================================================
 
import inspect
import sys
import os
 
#Baseline imports
from baseline.validator import Validator as B_Validator
from baseline.database  import Database as B_Database
from baseline.reviewer import Reviewer as B_Reviewer
from baseline.reviewer_manager import ReviewerManager as B_ReviewerManager
from baseline.evaluation_manager import EvaluationManager as B_EvaluationManager
from baseline.notification_service import NotificationService as B_NotificationService
from baseline.submission_controller import SubmissionController as B_SubmissionController
from baseline.ui import UI as B_UI
 
# Optimised imports
from optimised.validator   import Validator  as O_Validator
from optimised.database   import Database as O_Database
from optimised.reviewer   import Reviewer as O_Reviewer
from optimised.reviewer_manager import ReviewerManager as O_ReviewerManager
from optimised.evaluation_manager import EvaluationManager as O_EvaluationManager
from optimised.notification_service import NotificationService as O_NotificationService
from optimised.submission_controller import SubmissionController as O_SubmissionController
from optimised.decision_engine import DecisionEngine as O_DecisionEngine
from optimised.ui import UI  as O_UI
 
 
def count_methods(cls) -> int:
    """Count number of public methods in a class."""
    return len([
        name for name, member in inspect.getmembers(cls, predicate=inspect.isfunction)
        if not name.startswith("__")
    ])
 
 
def count_lines(cls) -> int:
    """Count number of non-empty, non-comment lines in a class."""
    try:
        source = inspect.getsource(cls)
        lines  = source.split("\n")
        count  = sum(
            1 for line in lines
            if line.strip() and not line.strip().startswith("#")
        )
        return count
    except Exception:
        return 0
 
 
def get_method_sizes(cls) -> dict:
    """Return a dict of method name -> line count for each method."""
    sizes = {}
    try:
        for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
            if not name.startswith("__"):
                source = inspect.getsource(member)
                lines  = [
                    l for l in source.split("\n")
                    if l.strip() and not l.strip().startswith("#")
                ]
                sizes[name] = len(lines)
    except Exception:
        pass
    return sizes
 
 
def count_dependencies(cls) -> int:
    try:
        sig    = inspect.signature(cls.__init__)
        params = [
            p for p in sig.parameters
            if p not in ("self", "args", "kwargs")
        ]
        return len(params)
    except Exception:
        return 0
 
 
def analyse_system(label: str, classes: list) -> dict:
    """
    Run all complexity metrics on a list of classes.
    Returns a structured results dictionary.
    """
    print(f"\n{'='*60}")
    print(f"  ANALYSING: {label}")
    print(f"{'='*60}")
 
    results = {
        "label":        label,
        "classes":      [],
        "total_methods": 0,
        "total_lines":  0,
        "total_deps":   0,
    }
 
    for cls in classes:
        method_sizes = get_method_sizes(cls)
        avg_method_size = (
            round(sum(method_sizes.values()) / len(method_sizes), 1)
            if method_sizes else 0
        )
        entry = {
            "class":          cls.__name__,
            "methods":        count_methods(cls),
            "lines":          count_lines(cls),
            "dependencies":   count_dependencies(cls),
            "method_sizes":   method_sizes,
            "avg_method_size": avg_method_size,
        }
        results["classes"].append(entry)
        results["total_methods"] += entry["methods"]
        results["total_lines"]   += entry["lines"]
        results["total_deps"]    += entry["dependencies"]
 
        print(f"\n  Class: {cls.__name__}")
        print(f"    Public methods   : {entry['methods']}")
        print(f"    Lines of code    : {entry['lines']}")
        print(f"    Dependencies     : {entry['dependencies']}")
        print(f"    Avg method size  : {avg_method_size} lines")
        for method, size in method_sizes.items():
            print(f"      - {method}(): {size} lines")
 
    print(f"\n  TOTALS for {label}:")
    print(f"    Total methods    : {results['total_methods']}")
    print(f"    Total lines      : {results['total_lines']}")
    print(f"    Total deps       : {results['total_deps']}")
 
    return results
 
 
def run_complexity_analysis() -> tuple:
        
 
    baseline_classes = [
        B_UI,
        B_SubmissionController,
        B_Validator,
        B_Database,
        B_ReviewerManager,
        B_Reviewer,
        B_EvaluationManager,
        B_NotificationService,
    ]
 
    optimised_classes = [
        O_UI,
        O_SubmissionController,
        O_Validator,
        O_Database,
        O_ReviewerManager,
        O_Reviewer,
        O_EvaluationManager,
        O_NotificationService,
        O_DecisionEngine,
    ]
 
    baseline_results  = analyse_system("BASELINE",  baseline_classes)
    optimised_results = analyse_system("OPTIMISED", optimised_classes)
 
    return baseline_results, optimised_results
 
 
#Interaction count
 
BASELINE_INTERACTIONS = {
    "submitResearchOutput(data)":   "Researcher -> UI",
    "submit(data)":                 "UI -> SubmissionController",
    "validateFormat(data)":         "SubmissionController -> Validator",
    "valid/invalid":                "Validator -> SubmissionController",
    "return error":                 "SubmissionController -> UI [alt invalid]",
    "saveSubmission(data)":         "SubmissionController -> Database",
    "confirmation":                 "Database -> SubmissionController",
    "getAvailableReviewers()":      "SubmissionController -> ReviewerManager",
    "fetchReviewers()":             "ReviewerManager -> Database",
    "reviewerList":                 "Database -> ReviewerManager",
    "filterConflicts()":            "ReviewerManager -> ReviewerManager [self-call]",
    "checkWorkload()":              "ReviewerManager -> ReviewerManager [self-call]",
    "filteredReviewers":            "ReviewerManager -> SubmissionController",
    "assignReview() [loop]":        "SubmissionController -> Reviewer",
    "startEvaluation()":            "SubmissionController -> EvaluationManager",
    "submitScore() [loop]":         "Reviewer -> EvaluationManager",
    "saveScore() [loop]":           "EvaluationManager -> Database",
    "calculateAverage()":           "EvaluationManager -> EvaluationManager [self-call]",
    "checkConsensus()":             "EvaluationManager -> EvaluationManager [self-call]",
    "applyRules()":                 "EvaluationManager -> EvaluationManager [self-call]",
    "notifyAcceptance/Rejection/Revision()": "EvaluationManager -> NotificationService",
    "sendNotification()":           "NotificationService -> Researcher",
}
 
OPTIMISED_INTERACTIONS = {
    "submitResearchOutput(data)":   "Researcher -> UI",
    "submit(data)":                 "UI -> SubmissionController",
    "validateFormat(data)":         "SubmissionController -> Validator",
    "valid/invalid":                "Validator -> SubmissionController",
    "return error":                 "SubmissionController -> UI [alt invalid]",
    "saveSubmission(data)":         "SubmissionController -> Database",
    "confirmation":                 "Database -> SubmissionController",
    "assignReviewers(submission)":  "SubmissionController -> ReviewerManager",
    "fetchReviewers()":             "ReviewerManager -> Database",
    "reviewerList":                 "Database -> ReviewerManager",
    "assignReview() [loop]":        "ReviewerManager -> Reviewer",
    "assignedReviewers":            "ReviewerManager -> SubmissionController",
    "startEvaluation()":            "SubmissionController -> EvaluationManager",
    "submitScore() [loop]":         "Reviewer -> EvaluationManager",
    "saveScore() [loop]":           "EvaluationManager -> Database",
    "determineOutcome(scores)":     "EvaluationManager -> DecisionEngine",
    "outcome":                      "DecisionEngine -> EvaluationManager",
    "notifyAcceptance/Rejection/Revision()": "EvaluationManager -> NotificationService",
    "sendNotification()":           "NotificationService -> Researcher",
}
 
 
def print_interaction_comparison():
    """Print a side by side interaction count comparison."""
    print(f"\n{'='*60}")
    print("  INTERACTION COUNT COMPARISON")
    print(f"{'='*60}")
    print(f"  Baseline  interactions : {len(BASELINE_INTERACTIONS)}")
    print(f"  Optimised interactions : {len(OPTIMISED_INTERACTIONS)}")
    print(f"  Reduction              : {len(BASELINE_INTERACTIONS) - len(OPTIMISED_INTERACTIONS)} messages removed")
    print(f"\n  Baseline self-calls  : 5")
    print(f"  Optimised self-calls : 0")
    print(f"  Self-calls removed   : 5")