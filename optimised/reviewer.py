# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: Reviewer lifeline in optimised sequence diagram
#
# Minor improvement: assignReview() now returns a confirmation
# 
# =============================================================================
 
import random
 
class Reviewer:
    """
    Represents a single reviewer assigned to evaluate a submission.
    Single responsibility: perform review and submit score.
    """
 
    def __init__(self, reviewer_data: dict):
        self.id = reviewer_data["id"]
        self.name = reviewer_data["name"]
        self.workload = reviewer_data["workload"]
        self.field = reviewer_data["field"]
 
    def assignReview(self) -> str:
        """
        Diagram message: ReviewerManager -> Reviewer: assignReview()
        Returns: confirmed  (as shown in optimised diagram)
        IMPROVEMENT: Assignment is now called by ReviewerManager,
        not SubmissionController. 
        """
        print(f"[Reviewer:{self.name}] assignReview() called")
        return "confirmed"
 
    def submitScore(self, score: int) -> int:
        """
        Diagram message: Reviewer -> EvaluationManager: submitScore(score)
        """
        print(f"[Reviewer:{self.name}] submitScore() - score: {score}")
        return score
 
    def generateScore(self) -> int:
        """Helper: produces a simulated review score."""
        return random.randint(40, 100)