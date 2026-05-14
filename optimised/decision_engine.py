# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: DecisionEngine lifeline in optimised sequence diagram
#
# NEW CLASS, not in baseline.
#
# IMPROVEMENT: Replaces the three self-calls on EvaluationManager:
#   BASELINE:  EM -> EM: calculateAverage()
#              EM -> EM: checkConsensus()
#              EM -> EM: applyRules()
#   OPTIMISED: EM -> DecisionEngine: determineOutcome(scores)
#
# direct implementation of Decision Table 3 from Task 3.
# Single responsibility: receive scores, return outcome. Nothing else.
# =============================================================================
 
import statistics
 
 
class DecisionEngine:
    """
    Centralises all decision logic for determining submission outcomes.
    Directly implements Decision Table 3 from Task 3.
 
    IMPROVEMENT over baseline:
    - Decision logic is no longer buried inside EvaluationManager
    - All three rules (average, consensus, outcome) live in one place
    - Independently testable without touching any other class
    - If rules change, only this class needs to be modified
    """
 
    ACCEPT_THRESHOLD = 70   # average score needed for acceptance
    REJECT_THRESHOLD = 50   # average below this means rejection
    CONSENSUS_MARGIN = 20   # max spread between scores for consensus
 
    def determineOutcome(self, scores: list) -> str:
        """
        Diagram message: EvaluationManager -> DecisionEngine: determineOutcome(scores)
        Returns: outcome (accepted / rejected / revision) to EvaluationManager
 
        Internally runs all three steps from Decision Table 3:
          1. calculateAverage()
          2. checkConsensus()
          3. applyRules()
        """
        print("[DecisionEngine] determineOutcome() called")
 
        average = self._calculateAverage(scores)
        consensus = self._checkConsensus(scores)
        outcome = self._applyRules(average, consensus)
 
        print(f"[DecisionEngine] Returning outcome: {outcome.upper()}")
        return outcome
 
    def _calculateAverage(self, scores: list) -> float:
        """
        Internal method — implements Decision Table 3 condition: average score.
        Private to DecisionEngine. Not callable from outside.
        """
        print("[DecisionEngine] _calculateAverage() - internal")
        if not scores:
            return 0.0
        avg = statistics.mean(scores)
        print(f"[DecisionEngine] Scores: {scores} | Average: {avg:.2f}")
        return avg
 
    def _checkConsensus(self, scores: list) -> bool:
        """
        Internal method — implements Decision Table 3 condition: consensus.
        Private to DecisionEngine. Not callable from outside.
        """
        print("[DecisionEngine] _checkConsensus() - internal")
        if not scores:
            return False
        spread    = max(scores) - min(scores)
        consensus = spread <= self.CONSENSUS_MARGIN
        print(f"[DecisionEngine] Spread: {spread} | Consensus: {consensus}")
        return consensus
 
    def _applyRules(self, average: float, consensus: bool) -> str:
        """
        Internal method — implements Decision Table 3 actions directly.
        Private to DecisionEngine. Not callable from outside.
 
        Decision Table 3 mapping:
          avg >= 70 AND consensus -> accepted
          avg <  50               -> rejected
          everything else         -> revision
        """
        print("[DecisionEngine] _applyRules() - internal")
 
        if average >= self.ACCEPT_THRESHOLD and consensus:
            return "accepted"
        elif average < self.REJECT_THRESHOLD:
            return "rejected"
        else:
            return "revision"