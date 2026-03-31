# Convert Excel to Payment File - Agent Guidelines

## Project Overview

A Python application that converts an input Excel file to a fixed-width text payment file for banking system import.

- **Language**: Python 3.9+
- **Excel Processing**: openpyxl
- **Packaging**: PyInstaller
- **Testing**: pytest
- **Type Checking**: mypy
- **Formatting**: black + isort

## Project Structure

```
convert_payment/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── converter.py         # Core conversion logic
│   ├── validators.py       # Input validation
│   ├── models.py           # Data models
│   └── constants.py        # Bank codes, field specs
├── tests/
│   ├── __init__.py
│   ├── test_converter.py
│   └── test_validators.py
├── example_data/           # Sample input files
└── output/                  # Generated payment files
```

## Build & Run Commands

```bash
# Installation
pip install -e ".[dev]"
pip install pytest mypy black isort pyinstaller openpyxl

# Run the application
python -m src.main --input path/to/input.xlsx

# Testing
pytest                                    # Run all tests
pytest tests/test_converter.py           # Single test file
pytest tests/test_converter.py::test_name  # Single test function
pytest -k "test_convert"                 # Tests matching pattern
pytest -v                                 # Verbose output

# Linting & Type Checking
black src/ tests/           # Format code
isort src/ tests/          # Sort imports
mypy src/                  # Check types

# Build executable
pyinstaller --onefile --name ConvertPayment src/main.py
```

## Code Style Guidelines

### General Rules
- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use 4 spaces for indentation (no tabs)
- Use trailing commas in multi-line structures
- Use f-strings for string formatting

### Imports (use isort to enforce)
1. Standard library (`os`, `datetime`, `re`)
2. Third-party packages (`openpyxl`, `pandas`)
3. Local application modules (`src.models`, `src.constants`)

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Functions/variables | snake_case | `payment_date` |
| Classes | PascalCase | `PaymentConverter` |
| Constants | UPPER_SNAKE_CASE | `MAX_AMOUNT` |
| Private members | Leading underscore | `_validate()` |

### Type Hints
- Always use type hints for function signatures
- Use `Optional[X]` instead of `X | None` for Python 3.9 compatibility
- Use `List`, `Dict`, `Tuple` from typing

```python
from typing import Optional, List, Dict
from dataclasses import dataclass

@dataclass
class PaymentRecord:
    bank_code: str
    payment_date: str
    amount: float

def convert_payment(records: List[PaymentRecord]) -> Dict[str, int]:
    pass
```

### Error Handling
- Use custom exception classes for domain-specific errors
- Log errors before raising
- Validate early, fail fast

```python
class ConversionError(Exception):
    pass

class ValidationError(ConversionError):
    pass
```

## Data Validation Rules

- **BankName**: Must match one of: KTB, SCB, Mobile Banking (Alpha), PromptPay, TCRB, Lotus, 7-11
- **PaymentDate**: Exactly 8 characters in DDMMYYYY format
- **PaymentTime**: Exactly 6 characters in HH24MISS format
- **CustomerName**: Maximum 50 characters
- **Account**: Maximum 20 digits, numbers only
- **Amt**: 13 digits with 2 decimal places (no decimal point)

### Bank Code Mapping
| Code | Bank Name | Account |
|------|-----------|---------|
| 006 | KTB | 2783003832 |
| 014 | SCB | 2783003832 |
| 011 | Mobile Banking (Alpha) | 2783003832 |
| 909 | PromptPay | 1814003005 |
| 071 | TCRB | 1814003005 |
| 997 | Lotus | 1814003005 |
| 982 | 7-11 | 1814003005 |

## Output File Format

- Filename: `COLLECTION_DDMMYYYY.txt`
- Total line length: 256 characters
- Sections: Header (1 line), Body (multiple lines), Trailer (1 line)

### Header Format (256 chars)
| Field | Pos | Length |
|-------|-----|--------|
| RecordType | 1 | 1 (H) |
| SeqNo | 2-7 | 6 |
| BankCode | 8-10 | 3 |
| CompanyAccount | 11-20 | 10 |
| CompanyName | 21-60 | 40 |
| EffDate | 61-68 | 8 (DDMMYYYY) |
| Empty | 69-256 | 188 |

### Body Format (256 chars per line)
| Field | Pos | Length |
|-------|-----|--------|
| RecordType | 1 | 1 (D) |
| SeqNo | 2-7 | 6 |
| BankCode | 8-10 | 3 |
| PaymentDate | 21-28 | 8 |
| PaymentTime | 29-34 | 6 |
| CustomerName | 35-84 | 50 |
| Account | 85-104 | 20 |
| Ref2 | 105-124 | 20 (spaces) |
| Ref3 | 125-144 | 20 (spaces) |
| Branch | 145-148 | 4 (0901) |
| Teller | 149-152 | 4 (0000) |
| KindTran | 153 | 1 (C) |
| TranCode | 154-156 | 3 (CSH) |
| ChequeNo | 157-163 | 7 (0000000) |
| Amt | 164-176 | 13 |

### Trailer Format (256 chars)
| Field | Pos | Length |
|-------|-----|--------|
| RecordType | 1 | 1 (T) |
| SeqNo | 2-7 | 6 (total lines) |
| BankCode | 8-10 | 3 |
| CompanyAccount | 11-20 | 10 |
| SumDebit | 21-33 | 13 (0000000000000) |
| CountDebit | 34-39 | 6 (000000) |
| SumCredit | 40-52 | 13 |
| ChqBankCode | 177-179 | 3 (000) |
| Empty | 180-256 | 77 |

## Testing Guidelines

- Use descriptive test names: `test_should_raise_error_for_invalid_date`
- Use fixtures for reusable test data
- Test both happy path and error cases
- Use `pytest.mark.parametrize` for multiple input scenarios

## Logging

- Use `logging` module with `__name__` as logger name
- DEBUG (development), INFO (normal), ERROR (failures)

```python
import logging
logger = logging.getLogger(__name__)
logger.info(f"Processing file: {input_path}")
```
