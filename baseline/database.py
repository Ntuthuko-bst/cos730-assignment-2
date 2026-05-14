# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# Traceability: Database lifeline in sequence diagram
# Messages received: saveSubmission(data), fetchReviewers(), saveScore(score)
# Messages returned: confirmation, reviewerList
# NO optimisations 
# =============================================================================
 
class Database:
    """
    Responsible for all persistence operations.
    Diagram lifeline: Database
    """
 
    def __init__(self):
        # Simulated in-memory storage
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
        Returns: confirmation back to SubmissionController
        """
        print("[Database] saveSubmission() called")
        submission_id = f"SUB-{len(self._submissions) + 1:04d}"
        self._submissions[submission_id] = data
        print(f"[Database] Submission saved with ID: {submission_id}")
        # Diagram return: confirmation
        return submission_id  # acts as confirmation
 
    def fetchReviewers(self) -> list:
        """
        Diagram message: ReviewerManager -> Database: fetchReviewers()
        Returns: reviewerList back to ReviewerManager
        """
        print("[Database] fetchReviewers() called")
        print(f"[Database] Returning {len(self._reviewers)} reviewers")
        # Diagram return: reviewerList
        return list(self._reviewers)
 
    def saveScore(self, score: dict) -> None:
        """
        Diagram message: EvaluationManager -> Database: saveScore(score)
        No return value shown in diagram
        """
        print(f"[Database] saveScore() called - score: {score}")
        self._scores.append(score)
        print("[Database] Score saved")