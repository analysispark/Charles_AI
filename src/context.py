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
            "revision": ""
        }
    )

    metadata: dict = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda:
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
