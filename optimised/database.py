# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: Database lifeline in optimised sequence diagram
#
# No changes from baseline 
# =============================================================================
 
class Database:
    """
    Responsible for all persistence operations.
    Single responsibility: data storage and retrieval only.
    """
 
    def __init__(self):
        self._submissions = {}
        self._reviewers = [
            {"id": 1, "name": "Dr. Smith",   "workload": 2, "field": "AI"},
            {"id": 2, "name": "Dr. Jones",   "workload": 5, "field": "SE"},
            {"id": 3, "name": "Dr. Patel",   "workload": 1, "field": "AI"},
            {"id": 4, "name": "Dr. Nkosi",   "workload": 3, "field": "HCI"},
            {"id": 5, "name": "Dr. Mokoena", "workload": 6, "field": "SE"},
        ]
        self._scores = []
 
    def saveSubmission(self, data: dict) -> str:
        """
        Diagram message: SubmissionController -> Database: saveSubmission(data)
        Returns: confirmation
        """
        print("[Database] saveSubmission() called")
        submission_id = f"SUB-{len(self._submissions) + 1:04d}"
        self._submissions[submission_id] = data
        print(f"[Database] Saved with ID: {submission_id}")
        return submission_id
 
    def fetchReviewers(self) -> list:
        """
        Diagram message: ReviewerManager -> Database: fetchReviewers()
        Returns: reviewerList
        """
        print("[Database] fetchReviewers() called")
        print(f"[Database] Returning {len(self._reviewers)} reviewers")
        return list(self._reviewers)
 
    def saveScore(self, score: dict) -> None:
        """
        Diagram message: EvaluationManager -> Database: saveScore(score)
        """
        print(f"[Database] saveScore() called - score: {score}")
        self._scores.append(score)
        print("[Database] Score saved")