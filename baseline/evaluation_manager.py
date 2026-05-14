# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# 
# Traceability: EvaluationManager lifeline in sequence diagram
#
# Messages received:
#   - startEvaluation() from SubmissionController  
#   - submitScore(score) from Reviewer              
#
# Messages sent:
#   - saveScore(score)  to Database             
#   - notifyAcceptance()  to NotificationService  
#   - notifyRejection() to NotificationService  
#   - notifyRevision()    to NotificationService 
#
# Self-calls:
#   - calculateAverage()  
#   - checkConsensus()    
#   - applyRules()        
#
# INTENTIONAL DESIGN FLAWS preserved from diagram:
#   - calculateAverage, checkConsensus, applyRules are all self-calls on one class
#   - Decision logic buried inside applyRules with no centralised decision engine
#   - EvaluationManager directly drives NotificationService 
# =============================================================================
 
import statistics
from baseline.database import Database
from baseline.notification_service import NotificationService
from baseline.reviewer  import Reviewer
 
 
class EvaluationManager:
    """
    Manages the full evaluation process: scoring, consensus checking, and outcome.
    EvaluationManager of the diagram.

    """
 
    ACCEPT_THRESHOLD = 70    # average score needed for acceptance
    REJECT_THRESHOLD = 50    # average below this means rejection
    CONSENSUS_MARGIN = 20    # max spread between scores to count as consensus
 
    def __init__(self, database: Database, notification_service: NotificationService):
        self._database = database
        self._notification_service = notification_service
        self._scores   = []
 
    def startEvaluation(self, reviewers: list, submission_id: str) -> str:
        """
        Diagram message 14: SubmissionController -> EvaluationManager: startEvaluation()
 
        Inner flow:
          loop [each reviewer]:
            msg 15: Reviewer -> EvaluationManager: submitScore(score)
            msg 16: EvaluationManager -> Database:  saveScore(score)
          [end loop]
 
          msg 17: self.calculateAverage()  <- ONCE after loop
          msg 18: self.checkConsensus() <- ONCE after loop
          msg 19: self.applyRules() <- ONCE after loop
 
          alt [accepted]: msg 20a -> NotificationService: notifyAcceptance()
          alt [rejected]: msg 20b -> NotificationService: notifyRejection()
          alt [revision]: msg 20c -> NotificationService: notifyRevision()
        """
        print("[EvaluationManager] startEvaluation() called  [msg 14, called once]")
        self._scores = []
 
        # loop - each reviewer
        for reviewer in reviewers:
            raw_score = reviewer.generateScore()
 
            # msg 15: Reviewer -> EvaluationManager: submitScore(score)
            score = reviewer.submitScore(raw_score)
 
            # msg 16: EvaluationManager -> Database: saveScore(score)
            score_record = {
                "submission_id": submission_id,
                "reviewer_id":   reviewer.id,
                "reviewer_name": reviewer.name,
                "score": score,
            }
            self._database.saveScore(score_record)
            self._scores.append(score)
        # end loop 
 
        # msg 17: self-call - calculateAverage() 
        average = self.calculateAverage()
 
        # msg 18: self-call - checkConsensus() 
        consensus = self.checkConsensus()
 
        # msg 19: self-call - applyRules() 
        outcome = self.applyRules(average, consensus)
 
        # alt block [accepted / rejected / revision]
        if outcome == "accepted":
            # msg 20a: EvaluationManager -> NotificationService: notifyAcceptance()
            message = self._notification_service.notifyAcceptance()
        elif outcome == "rejected":
            # msg 20b: EvaluationManager -> NotificationService: notifyRejection()
            message = self._notification_service.notifyRejection()
        else:
            # msg 20c: EvaluationManager -> NotificationService: notifyRevision()
            message = self._notification_service.notifyRevision()
 
        # msg 21: NotificationService -> Researcher: sendNotification()
        self._notification_service.sendNotification(message)
 
        return outcome
 
    def calculateAverage(self) -> float:
        """
        Diagram msg 17: EvaluationManager -> EvaluationManager: calculateAverage()
        
        """
        print("[EvaluationManager] calculateAverage() called  [msg 17]")
        if not self._scores:
            return 0.0
        avg = statistics.mean(self._scores)
        print(f"[EvaluationManager] Scores: {self._scores} | Average: {avg:.2f}")
        return avg
 
    def checkConsensus(self) -> bool:
        """
        Diagram msg 18: EvaluationManager -> EvaluationManager: checkConsensus()
        
        """
        print("[EvaluationManager] checkConsensus() called  [msg 18]")
        if not self._scores:
            return False
        spread = max(self._scores) - min(self._scores)
        consensus = spread <= self.CONSENSUS_MARGIN
        print(f"[EvaluationManager] Score spread: {spread} | Consensus reached: {consensus}")
        return consensus
 
    def applyRules(self, average: float, consensus: bool) -> str:
        """
        Diagram msg 19: EvaluationManager -> EvaluationManager: applyRules()
        The alt [accepted/rejected/revision] branching lives inside this single method.
        """
        print("[EvaluationManager] applyRules() called  [msg 19]")
 
        # Decision logic matching the alt block in the sequence diagram
        if average >= self.ACCEPT_THRESHOLD and consensus:
            outcome = "accepted"
        elif average < self.REJECT_THRESHOLD:
            outcome = "rejected"
        else:
            outcome = "revision"
 
        print(f"[EvaluationManager] Outcome: {outcome.upper()}")
        return outcome