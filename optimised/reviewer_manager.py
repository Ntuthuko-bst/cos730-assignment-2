# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: ReviewerManager lifeline in optimised sequence diagram
#
# IMPROVEMENTS over baseline:
#   BASELINE:  getAvailableReviewers() — returns list to SubmissionController
#              filterConflicts()  — self-call (visible on diagram)
#              checkWorkload() — self-call (visible on diagram)
#              assignReview() loop   — managed by SubmissionController
#
#   OPTIMISED: assignReviewers(submission) — one method does everything
#              _filterConflicts() — private internal method
#              _checkWorkload() — private internal method
#              assignReview() loop — managed here, not by controller
#
# SubmissionController no longer knows individual Reviewer objects exist.
# Single responsibility: manage the full reviewer assignment process.
# =============================================================================
 
from optimised.database import Database
from optimised.reviewer import Reviewer
 
 
class ReviewerManager:
    """
    Manages the complete reviewer selection and assignment process.
    Diagram lifeline: ReviewerManager
 
    IMPROVEMENT: All reviewer logic is encapsulated here.
    SubmissionController makes one call and gets back assigned reviewers.
    """
 
    MAX_WORKLOAD = 4
 
    def __init__(self, database: Database):
        self._database = database
 
    def assignReviewers(self, submission: dict) -> list:
        """
        Diagram message: SubmissionController -> ReviewerManager: assignReviewers(submission)
        Returns: assignedReviewers back to SubmissionController
 
        IMPROVEMENT: Replaces three separate baseline interactions:
          - getAvailableReviewers() call from SubmissionController
          - filterConflicts() self-call on ReviewerManager
          - checkWorkload() self-call on ReviewerManager
          - assignReview() loop managed by SubmissionController
 
        All of the above now happen internally inside this one method.
        """
        print("[ReviewerManager] assignReviewers() called")
 
        # Diagram message: ReviewerManager -> Database: fetchReviewers()
        reviewer_list = self._database.fetchReviewers()
        print(f"[ReviewerManager] Received reviewerList: {len(reviewer_list)} reviewers")
 
        # Internal — no longer self-calls visible on diagram
        reviewer_list = self._filterConflicts(reviewer_list, submission)
        reviewer_list = self._checkWorkload(reviewer_list)
 
        # Build Reviewer objects
        reviewers = [Reviewer(r) for r in reviewer_list[:3]]
 
        # loop [assign reviewers] — now managed here, not in SubmissionController
        assigned = []
        for reviewer in reviewers:
            # Diagram message: ReviewerManager -> Reviewer: assignReview()
            confirmation = reviewer.assignReview()
            print(f"[ReviewerManager] Reviewer {reviewer.name}: {confirmation}")
            assigned.append(reviewer)
 
        print(f"[ReviewerManager] Returning {len(assigned)} assignedReviewers")
        # Diagram return: assignedReviewers -> SubmissionController
        return assigned
 
    def _filterConflicts(self, reviewer_list: list, submission: dict) -> list:
        """
        Private internal method — not visible as a self-call on the optimised diagram.
        IMPROVEMENT: Conflict filtering is an internal concern of ReviewerManager only.
        Implements Decision Table 2, condition 1: reviewer is not the submitting author.
        """
        print("[ReviewerManager] _filterConflicts() - internal")
        author   = submission.get("author", "")
        filtered = [r for r in reviewer_list if r["name"] != author]
        print(f"[ReviewerManager] After conflict filter: {len(filtered)} remain")
        return filtered
 
    def _checkWorkload(self, reviewer_list: list) -> list:
        """
        Private internal method — not visible as a self-call on the optimised diagram.
        IMPROVEMENT: Workload checking is an internal concern of ReviewerManager only.
        Implements Decision Table 2, condition 2: workload below maximum.
        """
        print("[ReviewerManager] _checkWorkload() - internal")
        available = [r for r in reviewer_list if r["workload"] < self.MAX_WORKLOAD]
        print(f"[ReviewerManager] After workload filter: {len(available)} available")
        return available