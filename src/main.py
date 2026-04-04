import argparse
import logging
import os
import sys
import textwrap

from src.converter import convert_to_payment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Excel or CSV file to payment file for banking system import",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              python -m src.main -i payments.xlsx
              python -m src.main -i payments.csv -o output/ -v
              python -m src.main -i payments.xlsx --output-dir output/ --output-filename payments_march.txt
            """),
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to input Excel (.xlsx) or CSV (.csv) file",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Output directory (default: output)",
    )
    parser.add_argument(
        "--output-filename",
        "-f",
        default=None,
        help="Output file name (default: COLLECTION_DDMMYYYY.txt)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()
    if args.output_filename is not None:
        _, ext = os.path.splitext(args.output_filename)
        if ext == "":
            args.output_filename = args.output_filename + ".txt"
        elif ext.lower() != ".txt":
            print(f"Error: --output-filename must have a .txt extension, got '{ext}'", file=sys.stderr)
            return 1
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    input_path = args.input
    output_dir = args.output_dir
    logger.info(f"Starting conversion: {input_path}")
    result = convert_to_payment(input_path, output_dir, args.output_filename)
    if result.success:
        logger.info(f"Conversion successful!")
        logger.info(f"Output: {result.output_path}")
        logger.info(f"Records: {result.record_count}")
        logger.info(f"Total amount: {result.total_amount:.2f}")
        print(f"Success: {result.output_path}")
        return 0
    else:
        logger.error(f"Conversion failed: {result.error_message}")
        print(f"Error: {result.error_message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
