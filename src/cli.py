import os
import argparse
from .exceptions import CSVProcessingError, FileValidationError


def validate_args(args):
    if not os.path.exists(args.file):
        raise FileValidationError(f"File not found: {args.file}")

    if not args.file.lower().endswith('.csv'):
        raise FileValidationError("Only CSV files are supported")

    if args.where is not None:
        operators = ['>', '<', '=', '>=', '<=', '!=']
        if not any(op in args.where for op in operators):
            raise ValueError(
                f"Invalid filter format: '{args.where}'. "
                "Use operators: >, <, =, >=, <=, !=. "
                "Example: 'price>500'"
            )

        if args.where.startswith(tuple(operators)) or args.where.endswith(tuple(operators)):
            raise ValueError(
                f"Invalid filter format: '{args.where}'. "
                "Operator should be between column name and value."
            )

    if args.aggregate is not None:
        if '=' not in args.aggregate:
            raise ValueError(
                f"Invalid aggregation format: '{args.aggregate}'. "
                "Use format: column=function. Example: 'price=avg'"
            )

        parts = args.aggregate.split('=', 1)
        col = parts[0].strip()
        func = parts[1].strip().lower() if len(parts) > 1 else ''

        if not col or not func:
            raise ValueError(
                f"Invalid aggregation format: '{args.aggregate}'. "
                "Use format: column=function. Example: 'price=avg'"
            )

        if func not in ('avg', 'min', 'max'):
            raise ValueError(
                f"Unsupported aggregation function: '{func}'. "
                "Use: avg, min, max"
            )

    if args.order_by is not None:
        if '=' not in args.order_by:
            raise ValueError(
                f"Invalid sort format: '{args.order_by}'. "
                "Use format: column=direction. Example: 'price=desc'"
            )

        parts = args.order_by.split('=', 1)
        col = parts[0].strip()
        direction = parts[1].strip().lower() if len(parts) > 1 else ''

        if not col or not direction:
            raise ValueError(
                f"Invalid sort format: '{args.order_by}'. "
                "Use format: column=direction. Example: 'price=desc'"
            )

        if direction not in ('asc', 'desc'):
            raise ValueError(
                f"Unsupported sort direction: '{direction}'. "
                "Use: asc or desc"
            )


def parse_args():
    parser = argparse.ArgumentParser(
        description='Process CSV files with filtering, aggregation and sorting'
    )
    parser.add_argument('--file', type=str, required=True,
                        help='Path to CSV file (required)')
    parser.add_argument('--where', type=str, default=None,
                        help='Filter condition (e.g. "price>500")')
    parser.add_argument('--aggregate', type=str, default=None,
                        help='Aggregation operation (e.g. "rating=avg")')
    parser.add_argument('--order-by', type=str, default=None,
                        help='Sorting operation (e.g. "price=desc")')

    args = parser.parse_args()

    validate_args(args)

    return args
