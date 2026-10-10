from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TaskContext:

    goal: str = ""

    artifacts: dict = field(
        default_factory=lambda: {
            "research": "",
            "coding": "",
            "writing": "",
            "review": "",
            "revision": "",
            "qa_review": "",
            "qa_status": ""
        }
    )

    metadata: dict = field(
        default_factory=lambda: {
            "max_revision_attempts": 2
        }
    )

    created_at: str = field(
        default_factory=lambda:
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
