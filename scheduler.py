from typing import Callable, Any, Optional, Dict, Union, List
from datetime import datetime
import logging
import threading
import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import heapq
import weakref
import functools
import uuid


class TaskState(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


@dataclass(order=True)
class Task:
    """Task class implementing comparable interface for priority queue"""
    prioriy: TaskPriority
    interval: int
    created_at: datetime
    task_id: str = field(compare=False)
    name: str = field(compare=False)
    state: TaskState = field(default=TaskState.PENDING, compare=False)
    func: Callable = field(compare=False)
    last_run: Optional[datetime] = field(default=None, compare=False)
    retries: int = field(default=0, compare=False)
    depends_on: List[str] = field(default_factory=list, compare=False)

    def __post_init__(self):
        # Validate Task parameters
        if self.interval <= 0:
            raise ValueError("Interval must a positive integer")
        if self.retries <= 0:
            raise ValueError("Number of retries should be positive")
