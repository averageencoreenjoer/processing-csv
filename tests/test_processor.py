import pytest
import os
from src.csv_processor import read_csv, infer_type, apply_filter, aggregate_data
from src.exceptions import ColumnNotFoundError, FilterError, AggregationError, CSVProcessingError, FileValidationError
from src.operations import OPERATIONS_REGISTRY, register_operation
from src.cli import validate_args
from unittest.mock import MagicMock


class TestOperation:
    def execute(self, data, arg):
        return [{"modified": True}]


@pytest.fixture
def sample_csv_path():
    return "tests/test_data/products.csv"


def test_read_csv(sample_csv_path):
    data = read_csv(sample_csv_path)
    assert len(data) == 10

    assert data[0] == {
        "name": "iphone 15 pro",
        "brand": "apple",
        "price": "999",
        "rating": "4.9"
    }

    assert data[-1] == {
        "name": "iphone 13 mini",
        "brand": "apple",
        "price": "599",
        "rating": "4.5"
    }


def test_infer_type():
    assert infer_type("100") == 100
    assert infer_type("3.14") == 3.14
    assert infer_type("-5") == -5

    assert infer_type("apple") == "apple"
    assert infer_type("  spaced value  ") == "spaced value"

    assert infer_type("") == ""
    assert infer_type("123abc") == "123abc"
    assert infer_type("12.3.4") == "12.3.4"


def test_apply_filter(sample_csv_path):
    data = read_csv(sample_csv_path)

    filtered = apply_filter(data, "price>500")
    assert len(filtered) == 5
    assert {row["name"] for row in filtered} == {
        "iphone 15 pro",
        "galaxy s23 ultra",
        "iphone 14",
        "galaxy z flip 5",
        "iphone 13 mini"
    }

    filtered = apply_filter(data, "brand=apple")
    assert len(filtered) == 4
    assert all(row["brand"].lower() == "apple" for row in filtered)

    filtered = apply_filter(data, "rating>=4.5")
    assert len(filtered) == 6
    assert {row["name"] for row in filtered} == {
        "iphone 15 pro",
        "galaxy s23 ultra",
        "redmi note 12",
        "iphone 14",
        "galaxy z flip 5",
        "iphone 13 mini"
    }

    filtered = apply_filter(data, "brand=Apple")
    assert len(filtered) == 4
    assert all(row["brand"].lower() == "apple" for row in filtered)

    filtered = apply_filter(data, "brand!=apple")
    assert len(filtered) == 6
    assert all(row["brand"].lower() != "apple" for row in filtered)


def test_filter_errors(sample_csv_path):
    data = read_csv(sample_csv_path)

    with pytest.raises(ColumnNotFoundError):
        apply_filter(data, "invalid_column>100")

    with pytest.raises(FilterError):
        apply_filter(data, "price?100")

    with pytest.raises(FilterError):
        apply_filter(data, "name>100")


def test_empty_file():
    empty_path = os.path.join(os.path.dirname(__file__), "test_data/empty.csv")
    data = read_csv(empty_path)
    assert len(data) == 0
    assert apply_filter(data, "price>100") == []


def test_all_operators(sample_csv_path):
    data = read_csv(sample_csv_path)

    cases = [
        ("price>500", 5),
        ("price>=500", 5),
        ("price<300", 3),
        ("price<=300", 3),
        ("brand=apple", 4),
        ("brand!=apple", 6),
        ("rating>4.5", 5),
        ("rating<=4.2", 3)
    ]

    for condition, expected_count in cases:
        filtered = apply_filter(data, condition)
        assert len(filtered) == expected_count, \
            f"Failed for {condition}: expected {expected_count}, got {len(filtered)}"


def test_rating_filter(sample_csv_path):
    data = read_csv(sample_csv_path)

    filtered = apply_filter(data, "rating>=4.5")
    ratings = {float(row["rating"]) for row in filtered}
    assert ratings == {4.9, 4.8, 4.6, 4.7, 4.6, 4.5}

    names = {row["name"] for row in filtered}
    assert names == {
        "iphone 15 pro",
        "galaxy s23 ultra",
        "redmi note 12",
        "iphone 14",
        "galaxy z flip 5",
        "iphone 13 mini"
    }

    brands = {row["brand"].lower() for row in filtered}
    assert brands == {"apple", "samsung", "xiaomi"}


def test_aggregate_data(sample_csv_path):
    data = read_csv(sample_csv_path)

    assert aggregate_data(data, "price=avg") == pytest.approx(602.0, abs=0.1)

    assert aggregate_data(data, "price=min") == 149
    assert aggregate_data(data, "rating=min") == 4.1

    assert aggregate_data(data, "price=max") == 1199
    assert aggregate_data(data, "rating=max") == 4.9

    with pytest.raises(AggregationError):
        aggregate_data([], "price=avg")

    with pytest.raises(ColumnNotFoundError):
        aggregate_data(data, "invalid=avg")

    with pytest.raises(AggregationError):
        aggregate_data(data, "name=avg")

    with pytest.raises(AggregationError):
        aggregate_data(data, "price=invalid")


def test_operation_registration():
    initial_count = len(OPERATIONS_REGISTRY)
    register_operation("test", TestOperation())
    assert "test" in OPERATIONS_REGISTRY
    assert len(OPERATIONS_REGISTRY) == initial_count + 1


def test_sort_operation(sample_csv_path):
    from src.csv_processor import read_csv
    data = read_csv(sample_csv_path)

    sort_op = OPERATIONS_REGISTRY["order_by"]

    sorted_data = sort_op.execute(data, "price=desc")
    prices = [int(row["price"]) for row in sorted_data]
    assert prices == sorted(prices, reverse=True)

    sorted_data = sort_op.execute(data, "rating=asc")
    ratings = [float(row["rating"]) for row in sorted_data]
    assert ratings == sorted(ratings)

    with pytest.raises(CSVProcessingError):
        sort_op.execute(data, "invalid_column=asc")

    with pytest.raises(CSVProcessingError):
        sort_op.execute(data, "price=invalid")


def test_file_validation(tmp_path):
    valid_file = tmp_path / "valid.csv"
    valid_file.touch()

    args = MagicMock(file=str(valid_file), where=None, aggregate=None, order_by=None)
    validate_args(args)

    args = MagicMock(file="nonexistent.csv", where=None, aggregate=None, order_by=None)
    with pytest.raises(FileValidationError) as excinfo:
        validate_args(args)

    txt_file = tmp_path / "data.txt"
    txt_file.touch()

    args = MagicMock(file=str(txt_file), where=None, aggregate=None, order_by=None)
    with pytest.raises(FileValidationError) as excinfo:
        validate_args(args)
    assert "Only CSV files are supported" in str(excinfo.value)
    assert excinfo.value.code == 101


def test_filter_validation(tmp_path):
    valid_file = tmp_path / "valid.csv"
    valid_file.touch()

    args = MagicMock(file=str(valid_file), where="price>100", aggregate=None, order_by=None)
    validate_args(args)

    invalid_formats = ["price?100", "price 100", "price==", "invalid"]
    for fmt in invalid_formats:
        args = MagicMock(file=str(valid_file), where=fmt, aggregate=None, order_by=None)
        with pytest.raises(ValueError) as excinfo:
            validate_args(args)
        assert "Invalid filter format" in str(excinfo.value)


def test_aggregate_validation(tmp_path):
    valid_file = tmp_path / "valid.csv"
    valid_file.touch()

    args = MagicMock(file=str(valid_file), where=None, aggregate="price=avg", order_by=None)
    validate_args(args)

    invalid_formats = ["price:avg", "price avg", "price=", "=avg", "invalid"]
    for fmt in invalid_formats:
        args = MagicMock(file=str(valid_file), where=None, aggregate=fmt, order_by=None)
        with pytest.raises(ValueError) as excinfo:
            validate_args(args)
        assert "Invalid aggregation format" in str(excinfo.value) or "Unsupported aggregation function" in str(
            excinfo.value)

    args = MagicMock(file=str(valid_file), where=None, aggregate="price=sum", order_by=None)
    with pytest.raises(ValueError) as excinfo:
        validate_args(args)
    assert "Unsupported aggregation function" in str(excinfo.value)


def test_sort_validation(tmp_path):
    valid_file = tmp_path / "valid.csv"
    valid_file.touch()

    args = MagicMock(file=str(valid_file), where=None, aggregate=None, order_by="price=asc")
    validate_args(args)

    invalid_formats = ["price asc", "price=", "=asc", "price top", "invalid"]
    for fmt in invalid_formats:
        args = MagicMock(file=str(valid_file), where=None, aggregate=None, order_by=fmt)
        with pytest.raises(ValueError) as excinfo:
            validate_args(args)
        assert "Invalid sort format" in str(excinfo.value) or "Unsupported sort direction" in str(excinfo.value)
