from __future__ import annotations
import abc
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from blackbox.abc import Solution


class Problem(abc.ABC):
    eval_count: int = None

    @abc.abstractmethod
    def evaluate(self, s: Solution) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError()

