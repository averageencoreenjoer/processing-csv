from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from .exceptions import CSVProcessingError


class Operation(ABC):
    @abstractmethod
    def execute(self, data: List[Dict[str, Any]], arg: str) -> Union[List[Dict[str, Any]], float]:
        pass


class FilterOperation(Operation):
    def execute(self, data: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
        from .csv_processor import apply_filter
        return apply_filter(data, condition)


class AggregateOperation(Operation):
    def execute(self, data: List[Dict[str, Any]], operation: str) -> float:
        from .csv_processor import aggregate_data
        return aggregate_data(data, operation)


class SortOperation(Operation):
    def execute(self, data: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
        from .csv_processor import apply_sort
        return apply_sort(data, condition)


OPERATIONS_REGISTRY = {
    'where': FilterOperation(),
    'aggregate': AggregateOperation(),
    'order_by': SortOperation()
}


def register_operation(name: str, operation: Operation):
    OPERATIONS_REGISTRY[name] = operation

