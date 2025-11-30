import time
import uuid

class BuildProcessAutomation:
    """
    Simulates SAP Build Process Automation.
    Handles workflow triggers and status checks.
    """
    def __init__(self):
        self.service_name = "SAP Build Process Automation"
        self.status = "Active"
        self.instances = {}

    def trigger_workflow(self, definition_id: str, context: dict) -> str:
        """Triggers a new workflow instance."""
        print(f"   [Build PA] 🚀 Triggering workflow '{definition_id}'...")
        instance_id = f"wf-{uuid.uuid4()}"
        self.instances[instance_id] = {
            "definition_id": definition_id,
            "status": "RUNNING",
            "context": context,
            "start_time": time.time()
        }
        return instance_id

    def get_workflow_status(self, instance_id: str) -> str:
        """Checks the status of a workflow instance."""
        if instance_id in self.instances:
            return self.instances[instance_id]["status"]
        return "NOT_FOUND"

    def get_status(self):
        return f"✅ {self.service_name} is {self.status}. Active instances: {len(self.instances)}."
