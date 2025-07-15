import sys
from tabulate import tabulate
from src.cli import parse_args
from src.csv_processor import process_csv
from src.exceptions import CSVProcessingError, FileValidationError, ArgumentError, FilterError, AggregationError, \
    ColumnNotFoundError, SortError, EmptyDataError, TypeConversionError


def print_error(message):
    RED = '\033[91m'
    ENDC = '\033[0m'
    print(f"{RED}Error: {message}{ENDC}", file=sys.stderr)


def main():
    try:
        args = parse_args()
        result = process_csv(args)

        if isinstance(result, list):
            if not result:
                print("No matching records found")
            else:
                printable = [{k: v for k, v in row.items()} for row in result]
                print(tabulate(printable, headers="keys", tablefmt="grid"))
        else:
            col, func = args.aggregate.split('=')
            func_name = {'avg': 'average', 'min': 'minimum', 'max': 'maximum'}.get(func, func)
            header = [f"{col} ({func_name})"]
            table = [[result]]
            print(tabulate(table, headers=header, tablefmt="grid", floatfmt=".2f"))

    except FileValidationError as e:
        print_error(str(e))
        sys.exit(e.code)
    except ArgumentError as e:
        print_error(str(e))
        sys.exit(e.code)
    except FilterError as e:
        print_error(str(e))
        sys.exit(e.code)
    except AggregationError as e:
        print_error(str(e))
        sys.exit(e.code)
    except ColumnNotFoundError as e:
        print_error(str(e))
        sys.exit(e.code)
    except SortError as e:
        print_error(str(e))
        sys.exit(e.code)
    except EmptyDataError as e:
        print_error(str(e))
        sys.exit(e.code)
    except TypeConversionError as e:
        print_error(str(e))
        sys.exit(e.code)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(99)


if __name__ == "__main__":
    main()
