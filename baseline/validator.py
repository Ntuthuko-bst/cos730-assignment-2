# =============================================================================
# BASELINE IMPLEMENTATION - Task 1
# Traceability: Validator lifeline in sequence diagram
# Message received: validateFormat(data)
# Message returned: valid/invalid
# NO optimisations - matches diagram exactly
# =============================================================================
 
class Validator:
    """
    Responsible for validating the format of submitted research data.
    Diagram lifeline: Validator
    """
 
    def validateFormat(self, data: dict) -> bool:
        """
        Diagram message: SubmissionController -> Validator: validateFormat(data)
        Returns: valid/invalid (True/False) back to SubmissionController
        """
        print("[Validator] validateFormat() called")
 
        # Check that data is not empty
        if not data:
            print("[Validator] Result: INVALID - data is empty")
            return False
 
        # Check required fields are present
        required_fields = ["title", "author", "content"]
        for field in required_fields:
            if field not in data or not data[field]:
                print(f"[Validator] Result: INVALID - missing field: {field}")
                return False
 
        # Check content length is acceptable
        if len(data.get("content", "")) < 10:
            print("[Validator] Result: INVALID - content too short")
            return False
 
        print("[Validator] Result: VALID")
        return True