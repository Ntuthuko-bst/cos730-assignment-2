# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: SubmissionController lifeline in optimised sequence diagram
#
# IMPROVEMENTS over baseline:
#   BASELINE:  Depended on Validator, Database, ReviewerManager,
#              EvaluationManager AND individual Reviewer objects
#              Managed the reviewer assignment loop itself
#
#   OPTIMISED: Depends on Validator, Database, ReviewerManager,
#              and EvaluationManager only
#              No longer knows Reviewer objects exist
#              No longer manages any loops
#              Makes ONE call to ReviewerManager instead of many
#
# Single responsibility: coordinate the submission workflow only.
# =============================================================================
 
from optimised.validator import Validator
from optimised.database import Database
from optimised.reviewer_manager import ReviewerManager
from optimised.evaluation_manager import EvaluationManager
 
 
class SubmissionController:
    """
    Coordinates the submission workflow by delegating to specialist classes.
    Diagram lifeline: SubmissionController
 
    IMPROVEMENT: Significantly reduced coupling. No longer manages reviewer assignment loops or knows about individual Reviewer objects.

    """
 
    def __init__(
        self,
        validator:  Validator,
        database: Database,
        reviewer_manager: ReviewerManager,
        evaluation_manager: EvaluationManager,
    ):
        self._validator = validator
        self._database = database
        self._reviewer_manager = reviewer_manager
        self._evaluation_manager = evaluation_manager
 
    def submit(self, data: dict) -> str:
        """
        Diagram message: UI -> SubmissionController: submit(data)
 
        Flow:
          msg 1: -> Validator: validateFormat(data)
          msg 2: <- valid/invalid
          alt [invalid]: return error -> UI
          [valid]:
          msg 3: -> Database: saveSubmission(data)
          msg 4: <- confirmation
          msg 5: -> ReviewerManager: assignReviewers(submission)
          msg 6: <- assignedReviewers
          msg 7: -> EvaluationManager: startEvaluation(assignedReviewers)
          msg 8: <- outcome
        """
        print("\n[SubmissionController] submit() called")
 
        # msg 1+2: -> Validator: validateFormat(data)
        is_valid = self._validator.validateFormat(data)
 
        # alt [invalid]
        if not is_valid:
            print("[SubmissionController] alt[invalid]: returning error")
            return "ERROR: Submission format is invalid."
 
        # alt [valid]
 
        # msg 3+4: -> Database: saveSubmission(data)
        confirmation = self._database.saveSubmission(data)
        print(f"[SubmissionController] Confirmation: {confirmation}")
 
        # msg 5+6: -> ReviewerManager: assignReviewers(submission)
        # IMPROVEMENT: One call replaces getAvailableReviewers() +
        # the entire assignment loop that was here in the baseline
        assigned_reviewers = self._reviewer_manager.assignReviewers(data)
        print(f"[SubmissionController] {len(assigned_reviewers)} reviewers assigned")
 
        # msg 7+8: -> EvaluationManager: startEvaluation()
        outcome = self._evaluation_manager.startEvaluation(
            assigned_reviewers, confirmation
        )
 
        print(f"\n[SubmissionController] Final outcome: {outcome.upper()}")
        return outcome