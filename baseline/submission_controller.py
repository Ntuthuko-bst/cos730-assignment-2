# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# 
# Traceability: SubmissionController lifeline in sequence diagram
#
# Messages received:
#   - submit(data) from UI
#
# Messages sent:
#   - validateFormat(data) to Validator 
#   - saveSubmission(data) to Database
#   - getAvailableReviewers() to ReviewerManager 
#   - assignReview() to Reviewer
#   - startEvaluation() to EvaluationManager
#
# Returns:
#   - return error to UI (if invalid - alt block]
#
# DESIGN FLAWS from the diagram:
#   - Tightly coupled to ALL other components
#   - Manages the reviewer assignment loop itself (should be delegated)
#   - Drives Database, ReviewerManager AND EvaluationManager directly
# =============================================================================
 
from baseline.validator  import Validator
from baseline.database import Database
from baseline.reviewer_manager import ReviewerManager
from baseline.evaluation_manager import EvaluationManager
 
 
class SubmissionController:
    """
    Central orchestrator for the full submission workflow.
    In diagram lifeline: SubmissionController
    """
 
    def __init__(
        self,
        validator:Validator,
        database:  Database,
        reviewer_manager:   ReviewerManager,
        evaluation_manager: EvaluationManager,
    ):
        self._validator = validator
        self._database  = database
        self._reviewer_manager= reviewer_manager
        self._evaluation_manager = evaluation_manager
 
    def submit(self, data: dict) -> str:
        """
        Diagram message 2: UI -> SubmissionController: submit(data)
 
        Full flow:
          msg 3:  -> Validator:  validateFormat(data)
          msg 4:  <- Validator:   valid/invalid
          [invalid] -> return error to UI
          [valid]
          msg 5:  -> Database:  saveSubmission(data)
          msg 6:  <- Database:    confirmation
          msg 7:  -> ReviewerManager: getAvailableReviewers()
          msg 12: <- ReviewerManager: filteredReviewers
          loop [assign reviewers]:
            msg 13: -> Reviewer: assignReview()
          [end loop]
          msg 14: -> EvaluationManager: startEvaluation()  <- ONCE after loop
        """
        print("\n[SubmissionController] submit() called  [msg 2]")
 
        # msg 3: SubmissionController -> Validator: validateFormat(data)
        is_valid = self._validator.validateFormat(data)
 
        # alt [invalid]
        if not is_valid:
            # return error -> UI
            print("[SubmissionController] alt[invalid]: returning error to UI")
            return "ERROR: Submission format is invalid."
 
        # alt [valid] - continue
 
        # msg 5: SubmissionController -> Database: saveSubmission(data)
        confirmation = self._database.saveSubmission(data)
        print(f"[SubmissionController] Database confirmation received: {confirmation}  [msg 6]")
 
        # msg 7: SubmissionController -> ReviewerManager: getAvailableReviewers()
        filtered_reviewers = self._reviewer_manager.getAvailableReviewers(data)
        print(f"[SubmissionController] filteredReviewers received: {len(filtered_reviewers)}  [msg 12]")
 
        # loop [assign reviewers]
        assigned_reviewers = []
        for reviewer in filtered_reviewers[:3]:
            # msg 13: SubmissionController -> Reviewer: assignReview()
            reviewer.assignReview()
            assigned_reviewers.append(reviewer)
        #end loop 
 
        print(f"[SubmissionController] {len(assigned_reviewers)} reviewers assigned")
 
        # msg 14: SubmissionController -> EvaluationManager: startEvaluation()
        
        outcome = self._evaluation_manager.startEvaluation(
            assigned_reviewers, confirmation
        )
 
        return outcome