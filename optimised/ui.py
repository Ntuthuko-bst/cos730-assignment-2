# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: UI lifeline in optimised sequence diagram
#
# No structural changes from baseline. UI already had a clear single responsibility — entry point only.
# =============================================================================
 
from optimised.submission_controller import SubmissionController
 
 
class UI:
    """
    The user interface layer. Entry point for Researcher interactions.
    Diagram lifeline: UI
    """
 
    def __init__(self, submission_controller: SubmissionController):
        self._submission_controller = submission_controller
 
    def submitResearchOutput(self, data: dict) -> str:
        """
        Diagram message: Researcher -> UI: submitResearchOutput(data)
        Sends: UI -> SubmissionController: submit(data)
        """
        print("\n" + "=" * 60)
        print("[UI] submitResearchOutput() called by Researcher")
        print("=" * 60)
 
        result = self._submission_controller.submit(data)
 
        if result.startswith("ERROR"):
            print(f"\n[UI] Returning error to Researcher: {result}")
 
        return result