# Convert Excel to Payment File

A Python application that converts an input Excel file to a fixed-width text payment file for banking system import.

## Features

- Converts Excel payment data to fixed-width text format (256 characters per line)
- Validates input data according to banking system requirements
- Supports 7 bank codes: KTB, SCB, Mobile Banking (Alpha), PromptPay, TCRB, Lotus, 7-11
- Generates Header (H), Body (D), and Trailer (T) sections
- Comprehensive input validation with detailed error messages

## Requirements

- Python 3.9+
- openpyxl

## Installation

```bash
# Install dependencies
pip install openpyxl

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line

```bash
python -m src.main --input path/to/input.xlsx
python -m src.main --input path/to/input.xlsx --output output/
python -m src.main -i path/to/input.xlsx -o output/ -v
```

### Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--input` | `-i` | Path to input Excel file | Required |
| `--output` | `-o` | Output directory | `output` |
| `--verbose` | `-v` | Enable verbose logging | False |

## Input File Format

The input Excel file must have the following columns (header row required):

| Column | Length | Format | Required |
|--------|--------|--------|----------|
| BankName | 100 | Character (valid bank name) | Yes |
| PaymentDate | 8 | DDMMYYYY | Yes |
| PaymentTime | 6 | HH24MISS | Yes |
| CustomerName | 50 | Character | Yes |
| Account | 20 | Numeric | Yes |
| Amt | 13 | Decimal (2 decimal places) | Yes |

### Valid Bank Names

- KTB
- SCB
- Mobile Banking (Alpha)
- PromptPay
- TCRB
- Lotus
- 7-11

### Example Input

| BankName | PaymentDate | PaymentTime | CustomerName | Account | Amt |
|----------|-------------|-------------|--------------|---------|-----|
| TCRB | 05022018 | 101102 | John Doe | 1234567890 | 1234.50 |
| KTB | 06022018 | 102030 | Jane Smith | 0987654321 | 500.00 |

## Output File Format

The output file is a fixed-width text file with 256 characters per line.

### Filename Format
```
COLLECTION_DDMMYYYY.txt
```
Where DDMMYYYY is the file generation date.

### File Structure

1. **Header (1 line)** - Record type "H"
2. **Body (N lines)** - Record type "D" (one per payment)
3. **Trailer (1 line)** - Record type "T" with totals

### Example Output

```
H0000010711814003005TCRB                                    16032026                                                                                                                   
D000001071          05022018101102John Doe                                          1234567890                                                  09010000CCSH000000000123450                                                                           
D000002006          06022018 102030Jane Smith                                        0987654321                                                  09010000CCSH000000000500000                                                                           
T0000030711814003005000000000000000000000000000017345000000                                                                                                             000                                                                               
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_converter.py

# Run a single test function
pytest tests/test_converter.py::test_convert_excel_to_payment

# Run tests matching a pattern
pytest -k "test_convert"

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check types
mypy src/
```

### Building Executable

```bash
pyinstaller --onefile --name ConvertPayment src/main.py
```

## Project Structure

```
convert_payment/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── converter.py         # Core conversion logic
│   ├── validators.py        # Input validation
│   ├── models.py            # Data models
│   └── constants.py         # Bank codes, field specs
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   └── test_validators.py
├── example_data/            # Sample input files
├── output/                  # Generated payment files
├── pyproject.toml
└── README.md
```

## Error Handling

The application validates all input data and provides descriptive error messages:

- Invalid bank name
- Invalid date format (must be DDMMYYYY)
- Invalid time format (must be HH24MISS)
- Invalid customer name length (> 50 characters)
- Invalid account (non-numeric or > 20 digits)
- Invalid amount
- Missing or invalid header columns

## License

MIT License
# convert_payment
