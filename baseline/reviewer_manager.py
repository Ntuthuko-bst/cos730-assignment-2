# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# Traceability: ReviewerManager lifeline in sequence diagram
# Messages received : getAvailableReviewers()
# Messages sent: fetchReviewers() to Database
# Self-calls: filterConflicts(reviewerList), checkWorkload(reviewerList)
# Returns: filteredReviewers to SubmissionController
#
#  DESIGN FLAWS 
#   - filterConflicts() and checkWorkload() are BOTH self-calls on ReviewerManager
#     violating Single Responsibility Principle
#   - ReviewerManager does filtering, conflict detection AND workload checking
# =============================================================================
 
from baseline.database import Database
from baseline.reviewer import Reviewer
 
class ReviewerManager:
    """
    Manages retrieval, filtering and workload checking of reviewers.
    Diagram lifeline: ReviewerManager
 
    FLAW: This class has too many responsibilities.
    """
 
    #Maximum workload a reviewer can have to still be assigned
    MAX_WORKLOAD = 4
 
    def __init__(self, database: Database):
        self._database = database
 
    def getAvailableReviewers(self, submission: dict) -> list:
        """
        Diagram message: SubmissionController -> ReviewerManager: getAvailableReviewers()
 
        Internally orchestrates like how it was shown on diagram:
          1. ReviewerManager -> Database: fetchReviewers()
          2. Database -> ReviewerManager: reviewerList
          3. ReviewerManager -> ReviewerManager: filterConflicts(reviewerList)  [self-call]
          4. ReviewerManager -> ReviewerManager: checkWorkload(reviewerList) [self-call]
          Returns: filteredReviewers to SubmissionController
        """
        print("[ReviewerManager] getAvailableReviewers() called")
 
        # Diagram message-ReviewerManager-> Database: fetchReviewers()
        reviewer_list = self._database.fetchReviewers()
        print(f"[ReviewerManager] Received reviewerList: {len(reviewer_list)} reviewers")
 
        # Diagram self-call -ReviewerManager ->ReviewerManager: filterConflicts(reviewerList)
        reviewer_list = self.filterConflicts(reviewer_list, submission)
 
        #Diagram self-call - ReviewerManager -> ReviewerManager: checkWorkload(reviewerList)
        reviewer_list = self.checkWorkload(reviewer_list)
 
        print(f"[ReviewerManager] Returning filteredReviewers: {len(reviewer_list)} available")
        # Diagram return: filteredReviewers -> SubmissionController
        return [Reviewer(r) for r in reviewer_list]
 
    def filterConflicts(self, reviewer_list: list, submission: dict) -> list:
        """
        Diagram self-call: ReviewerManager -> ReviewerManager: filterConflicts(reviewerList)
 
        """
        print("[ReviewerManager] filterConflicts() called (self-call)")
        author = submission.get("author", "")
        # Remove any reviewer who is the same person as the author
        filtered = [r for r in reviewer_list if r["name"] != author]
        print(f"[ReviewerManager] After conflict filter: {len(filtered)} reviewers remain")
        return filtered
 
    def checkWorkload(self, reviewer_list: list) -> list:
        """
        Diagram self-call: ReviewerManager -> ReviewerManager: checkWorkload(reviewerList)
 
        ***come back here******  
        """
        print("[ReviewerManager] checkWorkload() called (self-call)")
        available = [r for r in reviewer_list if r["workload"] < self.MAX_WORKLOAD]
        print(f"[ReviewerManager] After workload filter: {len(available)} reviewers available")
        return available