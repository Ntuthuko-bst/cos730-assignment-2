# =============================================================================
# OPTIMISED IMPLEMENTATION - Task 5
# 
# Traceability: Validator lifeline in optimised sequence diagram
#
# No changes from baseline — Validator already had a single, well-defined responsibility
# =============================================================================
 
class Validator:
    """
    Responsible for validating the format of submitted research data.
    Single responsibility: format validation only.
    """
 
    def validateFormat(self, data: dict) -> bool:
        """
        Diagram message: SubmissionController -> Validator: validateFormat(data)
        Returns: valid/invalid back to SubmissionController
        """
        print("[Validator] validateFormat() called")
 
        if not data:
            print("[Validator] Result: INVALID - data is empty")
            return False
 
        required_fields = ["title", "author", "content"]
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"[Validator] Result: INVALID - missing field: {field}")
                return False
 
        if len(data.get("content", "")) < 10:
            print("[Validator] Result: INVALID - content too short")
            return False
 
        print("[Validator] Result: VALID")
        return True