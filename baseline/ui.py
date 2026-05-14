# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# 
# Traceability: UI lifeline in sequence diagram
#
# Messages received:
#   - submitResearchOutput(data)  from Researcher   
#   - return error   from SubmissionController [if invalid only]
#
# Messages sent:
#   - submit(data) to SubmissionController 
# =============================================================================
 
from baseline.submission_controller import SubmissionController
 
 
class UI:
    """
    The user interface layer. Entry point for Researcher interactions.
    Diagram lifeline: UI
    """
 
    def __init__(self, submission_controller: SubmissionController):
        self._submission_controller = submission_controller
 
    def submitResearchOutput(self, data: dict) -> str:
        """
        Diagram message 1: Researcher -> UI: submitResearchOutput(data)
 
        UI sends:
          msg 2: UI -> SubmissionController: submit(data)
 
        On invalid: SubmissionController returns error which UI passes to Researcher.
        On valid:   NotificationService handles the final message to Researcher directly.
        """
        print("\n" + "=" * 60)
        print("[UI] submitResearchOutput() called by Researcher  [msg 1]")
        print("=" * 60)
 
        # msg 2: UI -> SubmissionController: submit(data)
        result = self._submission_controller.submit(data)
 
        # Only the ERROR path comes back through UI to the Researcher.
        # The SUCCESS path is handled directly by NotificationService -> Researcher.
        if result.startswith("ERROR"):
            print(f"\n[UI] Returning error to Researcher: {result}")
 
        return result