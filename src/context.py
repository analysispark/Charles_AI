from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TaskContext:

    goal: str = ""

    research: str = ""

    coding: str = ""

    writing: str = ""

    review: str = ""

    metadata: dict = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda:
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
