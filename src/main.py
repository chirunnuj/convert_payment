import argparse
import logging
import sys

from src.converter import convert_excel_to_payment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Excel file to payment file for banking system import"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to input Excel file",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="Output directory (default: output)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    input_path = args.input
    output_dir = args.output
    logger.info(f"Starting conversion: {input_path}")
    result = convert_excel_to_payment(input_path, output_dir)
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
