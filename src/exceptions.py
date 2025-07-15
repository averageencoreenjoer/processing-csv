class CSVProcessingError(Exception):
    def __init__(self, message, code=100):
        super().__init__(message)
        self.code = code
        self.message = message

    def __str__(self):
        return f"[{self.code}] {self.message}"


class FileValidationError(CSVProcessingError):
    def __init__(self, message):
        super().__init__(f"File error: {message}", code=101)


class ArgumentError(CSVProcessingError):
    def __init__(self, message):
        super().__init__(f"Argument error: {message}", code=102)


class FilterError(CSVProcessingError):
    def __init__(self, message):
        super().__init__(f"Filter error: {message}", code=201)


class AggregationError(CSVProcessingError):
    def __init__(self, message):
        super().__init__(f"Aggregation error: {message}", code=301)


class ColumnNotFoundError(CSVProcessingError):
    def __init__(self, column, available_columns=None):
        message = f"Column '{column}' not found"
        if available_columns:
            message += f". Available columns: {', '.join(available_columns)}"
        super().__init__(message, code=401)


class SortError(CSVProcessingError):
    def __init__(self, message):
        super().__init__(f"Sort error: {message}", code=501)


class EmptyDataError(CSVProcessingError):
    def __init__(self, operation):
        super().__init__(f"Cannot perform {operation} on empty dataset", code=601)


class TypeConversionError(CSVProcessingError):
    def __init__(self, value, column, expected_type):
        message = (
            f"Value '{value}' in column '{column}' "
            f"cannot be converted to {expected_type}"
        )
        super().__init__(message, code=701)