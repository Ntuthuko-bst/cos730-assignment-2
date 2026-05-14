# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# Traceability: Reviewer lifeline in sequence diagram
# Messages received: assignReview(), submitScore(score)
# NO optimisations - matches diagram exactly
# =============================================================================
 
import random
 
class Reviewer:
    """
    Represents a single reviewer assigned to evaluate a submission.
    Diagram lifeline:Reviewer
    """
 
    def __init__(self, reviewer_data: dict):
        self.id = reviewer_data["id"]
        self.name= reviewer_data["name"]
        self.workload= reviewer_data["workload"]
        self.field = reviewer_data["field"]
 
    def assignReview(self) -> None:
        """
        Diagram message: SubmissionController -> Reviewer: assignReview()
        Called inside loop [assign reviewers]
        
        """
        print(f"[Reviewer:{self.name}] assignReview() called - review assigned")
 
    def submitScore(self, score: int) -> int:
        """
        Diagram message: Reviewer -> EvaluationManager: submitScore(score)
        Called inside loop [each reviewer]  
        """
        print(f"[Reviewer:{self.name}] submitScore() called - submitting score: {score}")
        return score
 
    def generateScore(self) -> int:
        
        return random.randint(40, 100)