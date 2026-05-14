# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# File: optimised/evaluation_manager.py
# Traceability: EvaluationManager lifeline in optimised sequence diagram
#
# IMPROVEMENTS over baseline:
#   BASELINE:  calculateAverage() — self-call
#              checkConsensus() — self-call
#              applyRules() — self-call
#              All decision logic buried inside this class
#
#   OPTIMISED: determineOutcome(scores) — delegated to DecisionEngine
#              EvaluationManager only orchestrates the scoring loop
#              No self-calls anywhere
#
# Single responsibility: controls the reviewer scoring loop only.
# =============================================================================
 
from optimised.database  import Database
from optimised.notification_service import NotificationService
from optimised.decision_engine import DecisionEngine
 
 
class EvaluationManager:
    """
    Orchestrates the reviewer scoring loop and delegates outcome
    determination to DecisionEngine.
    Diagram lifeline: EvaluationManager
 
    IMPROVEMENT: No longer a God Class. 
    """
 
    def __init__(
        self,
        database: Database,
        notification_service: NotificationService,
        decision_engine: DecisionEngine,
    ):
        self._database = database
        self._notification_service = notification_service
        self._decision_engine = decision_engine
 
    def startEvaluation(self, reviewers: list, submission_id: str) -> str:
        """
        Diagram message: SubmissionController -> EvaluationManager: startEvaluation()
        Called ONCE after reviewer assignment is complete.
 
        Flow:
          loop [each reviewer]:
            msg: Reviewer -> EvaluationManager: submitScore(score)
            msg: EvaluationManager-> Database:  saveScore(score)
          [end loop]
 
          msg: EvaluationManager -> DecisionEngine: determineOutcome(scores)
          msg: DecisionEngine -> EvaluationManager: outcome
 
          alt [accepted]: -> NotificationService: notifyAcceptance()
          alt [rejected]: -> NotificationService: notifyRejection()
          alt [revision]: -> NotificationService: notifyRevision()
 
          msg: NotificationService -> Researcher: sendNotification()
        """
        print("[EvaluationManager] startEvaluation() called")
        scores = []
 
        #loop-each reviewer
        for reviewer in reviewers:
            raw_score = reviewer.generateScore()
 
            # Diagram message: Reviewer -> EvaluationManager: submitScore(score)
            score = reviewer.submitScore(raw_score)
 
            # Diagram message: EvaluationManager -> Database: saveScore(score)
            score_record = {
                "submission_id": submission_id,
                "reviewer_id": reviewer.id,
                "reviewer_name": reviewer.name,
                "score":score,
            }
            self._database.saveScore(score_record)
            scores.append(score)
        #end loop
 
        # Diagram message: EvaluationManager -> DecisionEngine: determineOutcome(scores)
        # IMPROVEMENT: Decision logic fully delegated — no self-calls
        outcome = self._decision_engine.determineOutcome(scores)
 
        #alt block [accepted / rejected / revision] 
        if outcome == "accepted":
            message = self._notification_service.notifyAcceptance()
        elif outcome == "rejected":
            message = self._notification_service.notifyRejection()
        else:
            message = self._notification_service.notifyRevision()
 
        # Diagram message: NotificationService -> Researcher: sendNotification()
        self._notification_service.sendNotification(message)
 
        return outcome