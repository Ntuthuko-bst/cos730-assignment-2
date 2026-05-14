# =============================================================================
# EMPIRICAL EVALUATION - Task 6
# 
# Purpose: Benchmarks execution time of both systems over repeated runs
# =============================================================================
 
import timeit
import statistics
import sys
import os
 
# Suppressing print output during benchmarking for clean timing results
import io
from contextlib import redirect_stdout
 
 
#Building baseline system 
def build_baseline():
    from baseline.database import Database
    from baseline.validator   import Validator
    from baseline.reviewer_manager import ReviewerManager
    from baseline.notification_service import NotificationService
    from baseline.evaluation_manager import EvaluationManager
    from baseline.submission_controller import SubmissionController
    from baseline.ui import UI
 
    database  = Database()
    validator = Validator()
    notification_service = NotificationService()
    reviewer_manager= ReviewerManager(database)
    evaluation_manager= EvaluationManager(database, notification_service)
    submission_controller = SubmissionController(
        validator, database, reviewer_manager, evaluation_manager
    )
    return UI(submission_controller)
 
 
#Building optimised system
def build_optimised():
    from optimised.database import Database
    from optimised.validator import Validator
    from optimised.decision_engine import DecisionEngine
    from optimised.notification_service import NotificationService
    from optimised.reviewer_manager import ReviewerManager
    from optimised.evaluation_manager import EvaluationManager
    from optimised.submission_controller import SubmissionController
    from optimised.ui import UI
 
    database = Database()
    validator = Validator()
    decision_engine  = DecisionEngine()
    notification_service = NotificationService()
    reviewer_manager  = ReviewerManager(database)
    evaluation_manager  = EvaluationManager(
        database, notification_service, decision_engine
    )
    submission_controller = SubmissionController(
        validator, database, reviewer_manager, evaluation_manager
    )
    return UI(submission_controller)
 
 
#Test data
VALID_SUBMISSION = {
    "title":   "Deep Learning for Software Engineering",
    "author":  "Dr. Researcher",
    "content": "This paper explores neural networks in automated code review...",
}
 
INVALID_SUBMISSION = {
    "title":   "",
    "author":  "Dr. Researcher",
    "content": "Some content",
}
 
 
def run_benchmark(label: str, build_fn, data: dict, runs: int = 100) -> dict:
    
    times = []
 
    for i in range(runs):
        ui = build_fn()
 
        start = timeit.default_timer()
        with redirect_stdout(io.StringIO()):  # suppress print output
            ui.submitResearchOutput(data)
        end = timeit.default_timer()
 
        elapsed_ms = (end - start) * 1000
        times.append(elapsed_ms)
 
    results = {
        "label":   label,
        "runs":    runs,
        "mean_ms": round(statistics.mean(times), 4),
        "min_ms":  round(min(times), 4),
        "max_ms":  round(max(times), 4),
        "stdev_ms": round(statistics.stdev(times), 4),
        "median_ms": round(statistics.median(times), 4),
    }
 
    print(f"\n  Results for: {label}")
    print(f"    Runs         : {runs}")
    print(f"    Mean time    : {results['mean_ms']} ms")
    print(f"    Median time  : {results['median_ms']} ms")
    print(f"    Min time     : {results['min_ms']} ms")
    print(f"    Max time     : {results['max_ms']} ms")
    print(f"    Std deviation: {results['stdev_ms']} ms")
 
    return results
 
 
def run_all_benchmarks(runs: int = 100) -> dict:
    """Run benchmarks for both systems on valid and invalid submissions."""
 
    print(f"\n{'='*60}")
    print(f"  EXECUTION TIME BENCHMARKS  ({runs} runs each)")
    print(f"{'='*60}")
 
    results = {}
 
    # Valid submission benchmarks
    print("\n  -- Valid Submission --")
    results["baseline_valid"]  = run_benchmark(
        "Baseline  — Valid submission",  build_baseline,  VALID_SUBMISSION,  runs
    )
    results["optimised_valid"] = run_benchmark(
        "Optimised — Valid submission",  build_optimised, VALID_SUBMISSION,  runs
    )
 
    # Invalid submission benchmarks
    print("\n  -- Invalid Submission --")
    results["baseline_invalid"]  = run_benchmark(
        "Baseline  — Invalid submission", build_baseline,  INVALID_SUBMISSION, runs
    )
    results["optimised_invalid"] = run_benchmark(
        "Optimised — Invalid submission", build_optimised, INVALID_SUBMISSION, runs
    )
 
    # Summary comparison
    print(f"\n{'='*60}")
    print("  TIMING SUMMARY")
    print(f"{'='*60}")
 
    bv = results["baseline_valid"]["mean_ms"]
    ov = results["optimised_valid"]["mean_ms"]
    bi = results["baseline_invalid"]["mean_ms"]
    oi = results["optimised_invalid"]["mean_ms"]
 
    diff_valid   = round(bv - ov, 4)
    diff_invalid = round(bi - oi, 4)
 
    pct_valid   = round((diff_valid   / bv * 100), 2) if bv > 0 else 0
    pct_invalid = round((diff_invalid / bi * 100), 2) if bi > 0 else 0
 
    print(f"\n  Valid submission:")
    print(f"    Baseline  mean : {bv} ms")
    print(f"    Optimised mean : {ov} ms")
    print(f"    Difference     : {diff_valid} ms  ({pct_valid}% change)")
 
    print(f"\n  Invalid submission:")
    print(f"    Baseline  mean : {bi} ms")
    print(f"    Optimised mean : {oi} ms")
    print(f"    Difference     : {diff_invalid} ms  ({pct_invalid}% change)")
 
    results["summary"] = {
        "diff_valid_ms":    diff_valid,
        "diff_invalid_ms":  diff_invalid,
        "pct_valid":        pct_valid,
        "pct_invalid":      pct_invalid,
    }
 
    return results