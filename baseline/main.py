# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# =============================================================================#

 
from baseline.database  import Database
from baseline.validator  import Validator
from baseline.reviewer_manager  import ReviewerManager
from baseline.notification_service import NotificationService
from baseline.evaluation_manager import EvaluationManager
from baseline.submission_controller import SubmissionController
from baseline.ui import UI
 
 
def build_system() -> UI:
    
    database   = Database()
    validator  = Validator()
    notification_service = NotificationService()
    reviewer_manager = ReviewerManager(database)
    evaluation_manager = EvaluationManager(database, notification_service)
    submission_controller = SubmissionController(
        validator, database, reviewer_manager, evaluation_manager
    )
    return UI(submission_controller)
 
 
def run_scenario(label: str, data: dict, ui: UI):
    print(f"\n{'#' * 60}")
    print(f"# SCENARIO: {label}")
    print(f"{'#' * 60}")
    result = ui.submitResearchOutput(data)
    print(f"\n>>> FINAL RESULT: {result}")
 
 
if __name__ == "__main__":
 
    # Scenario 1: Valid submission 
    run_scenario(
        label="Valid submission",
        data={
            "title":   "Deep Learning for Software Engineering",
            "author":  "Dr. Researcher",
            "content": "This paper explores neural networks in automated code review...",
        },
        ui=build_system(),
    )
 
    # Scenario 2: Invalid - missing title
    run_scenario(
        label="Invalid submission - missing title",
        data={
            "title":   "",
            "author":  "Dr. Researcher",
            "content": "Some content here",
        },
        ui=build_system(),
    )
 
    # Scenario 3: Invalid - empty data
    run_scenario(
        label="Invalid submission - empty data",
        data={},
        ui=build_system(),
    )