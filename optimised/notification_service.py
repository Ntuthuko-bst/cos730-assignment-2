# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: NotificationService lifeline in optimised sequence diagram
#
# No structural changes from baseline. NotificationService already had a clear single responsibility.
# =============================================================================
 
class NotificationService:
    """
    Handles sending outcome notifications directly to the Researcher.
    Single responsibility: notification delivery only.
    """
 
    def notifyAcceptance(self) -> str:
        """
        Diagram message: EvaluationManager -> NotificationService: notifyAcceptance()
        Called inside alt [accepted] branch.
        """
        print("[NotificationService] notifyAcceptance() called")
        message = "Your submission has been ACCEPTED. Congratulations!"
        print(f"[NotificationService] Message prepared: '{message}'")
        return message
 
    def notifyRejection(self) -> str:
        """
        Diagram message: EvaluationManager -> NotificationService: notifyRejection()
        Called inside alt [rejected] branch.
        """
        print("[NotificationService] notifyRejection() called")
        message = "Your submission has been REJECTED. Please review the feedback."
        print(f"[NotificationService] Message prepared: '{message}'")
        return message
 
    def notifyRevision(self) -> str:
        """
        Diagram message: EvaluationManager -> NotificationService: notifyRevision()
        Called inside alt [revision] branch.
        """
        print("[NotificationService] notifyRevision() called")
        message = "Your submission requires REVISION. Please address reviewer comments."
        print(f"[NotificationService] Message prepared: '{message}'")
        return message
 
    def sendNotification(self, message: str) -> None:
        """
        Diagram message: NotificationService -> Researcher: sendNotification()
        
        """
        print(f"\n[NotificationService] sendNotification() -> Researcher")
        print(f"[NotificationService] >>> Researcher receives: '{message}'")