import csv
import os
import operator
from typing import List, Dict, Union, Callable, Any
from src.exceptions import ColumnNotFoundError, FilterError, AggregationError, SortError, CSVProcessingError
from src.operations import OPERATIONS_REGISTRY


def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def apply_filter(data: List[Dict[str, Any]], condition: str) -> List[Dict[str, Any]]:
    if not condition or not data:
        return data

    operators_map = {
        ">=": operator.ge,
        "<=": operator.le,
        "!=": operator.ne,
        ">": operator.gt,
        "<": operator.lt,
        "=": operator.eq
    }

    op_symbol = None
    for symbol in operators_map:
        if symbol in condition:
            op_symbol = symbol
            break

    if not op_symbol:
        raise FilterError(f"Invalid operator in condition: {condition}")

    col, value_str = condition.split(op_symbol, 1)
    col = col.strip()
    value_str = value_str.strip()

    if col not in data[0]:
        available = list(data[0].keys())
        raise ColumnNotFoundError(col, available)

    try:
        value = infer_type(value_str)
    except Exception as e:
        raise FilterError(f"Error parsing filter value: {e}")

    op_func = operators_map[op_symbol]
    filtered = []

    for row in data:
        try:
            row_value = infer_type(row[col])

            if isinstance(row_value, str) and op_symbol in ("=", "!="):
                if op_func(row_value.lower(), value.lower()):
                    filtered.append(row)
            else:
                if op_func(row_value, value):
                    filtered.append(row)
        except Exception as e:
            raise FilterError(f"Error comparing values in row: {e}")

    return filtered


def infer_type(value: str) -> Union[str, float, int]:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value.strip()


def aggregate_data(data: List[Dict[str, Any]], operation: str) -> float:
    if not data:
        raise AggregationError("Cannot aggregate empty dataset")

    if "=" not in operation:
        raise AggregationError(f"Invalid aggregation format: {operation}")

    col, func_name = operation.split("=", 1)
    col = col.strip()
    func_name = func_name.strip().lower()

    if col not in data[0]:
        raise ColumnNotFoundError(f"Column '{col}' not found in CSV")

    values = []
    for row in data:
        try:
            value = infer_type(row[col])
            if not isinstance(value, (int, float)):
                raise AggregationError(f"Column '{col}' contains non-numeric values")
            values.append(value)
        except Exception as e:
            raise AggregationError(f"Error processing value in row: {e}")

    if not values:
        raise AggregationError(f"No valid numeric values in column '{col}'")

    try:
        if func_name == "avg":
            return sum(values) / len(values)
        elif func_name == "min":
            return min(values)
        elif func_name == "max":
            return max(values)
        else:
            raise AggregationError(f"Unsupported aggregation function: {func_name}")
    except Exception as e:
        raise AggregationError(f"Aggregation error: {e}")


def process_csv(args) -> Union[List[Dict[str, Any]], float]:
    if not os.path.exists(args.file):
        raise FileNotFoundError(f"File not found: {args.file}")

    # Чтение данных
    data = read_csv(args.file)

    operations_order = ['where', 'order_by', 'aggregate']

    result = data
    for op_name in operations_order:
        arg_value = getattr(args, op_name, None)
        if arg_value:
            operation = OPERATIONS_REGISTRY.get(op_name)
            if not operation:
                raise CSVProcessingError(f"Unsupported operation: {op_name}")

            result = operation.execute(result, arg_value)

    return result


def apply_sort(data: List[Dict], condition: str) -> List[Dict]:

    if not data:
        return data

    if '=' not in condition:
        raise SortError(f"Invalid sort format: {condition}. Use 'column=asc|desc'")

    col, direction = condition.split('=', 1)
    col = col.strip()
    direction = direction.strip().lower()

    if direction not in ('asc', 'desc'):
        raise SortError(f"Invalid sort direction: {direction}. Use 'asc' or 'desc'")

    if col not in data[0]:
        raise ColumnNotFoundError(f"Column '{col}' not found in CSV")

    reverse = (direction == 'desc')

    try:
        return sorted(
            data,
            key=lambda x: infer_type(x[col]),
            reverse=reverse
        )
    except Exception as e:
        raise SortError(f"Sorting error: {e}")
