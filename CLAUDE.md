# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the application
python -m src.main --input path/to/input.xlsx
python -m src.main -i path/to/input.xlsx -o output/ -v   # verbose with custom output dir

# Testing
pytest                                                    # all tests
pytest tests/test_converter.py                           # single file
pytest tests/test_converter.py::TestBuildHeaderLine::test_build_header_line  # single test
pytest -k "test_convert"                                 # pattern match

# Code quality
black src/ tests/     # format (line length: 100)
isort src/ tests/     # sort imports
mypy src/             # type checking

# Build standalone executable
pyinstaller --onefile --name ConvertPayment src/main.py
```

## Architecture

This CLI tool converts Excel payment data into fixed-width text files for banking system import.

**Module dependency chain:**
```
main.py → converter.py → validators.py
                       → constants.py
                       → models.py
```

- `src/constants.py` — Bank code mappings (`BANK_CODES_FOR_CUSTOMER`, `BANK_CODES_FOR_TCB`), field specs, and fixed values (default company account `1814003005`, `LINE_LENGTH = 256`)
- `src/models.py` — `PaymentRecord` and `ConversionResult` dataclasses
- `src/validators.py` — All input validation; raises `ValidationError` on failure. Also contains `format_amount()` which converts a float to the 13-digit fixed-width string required in output
- `src/converter.py` — Reads Excel via openpyxl, validates rows, builds all three line types (H/D/T), writes output file
- `src/main.py` — Argparse CLI; exits 0 on success, 1 on failure

**Data flow:**
1. `read_excel()` opens the XLSX, validates headers, validates each row, returns `List[PaymentRecord]`
2. `build_header_line()` creates the H record (seq=1)
3. `build_body_line()` creates one D record per payment (seq=2..N)
4. `build_trailer_line()` creates the T record with summed credit amount
5. Output written to `COLLECTION_DDMMYYYY.txt` (date = generation date)

## Output Format

Every line is exactly **256 characters**. Three record types:

| Type | Marker | Key fields |
|------|--------|------------|
| Header | `H` | SeqNo(6), BankCode(3), CompanyAccount(10), CompanyName(40), EffDate(8) |
| Body | `D` | SeqNo(6), BankCode(3), PayDate(8), PayTime(6), CustomerName(50), Account(20), Branch=0901, Teller=0000, KindTran=C, TranCode=CSH, ChequeNo=0000000, Amt(13) |
| Trailer | `T` | TotalLines(6), BankCode(3), CompanyAccount(10), SumDebit=13×0, CountDebit=6×0, SumCredit(13), ChqBankCode=000 |

## Input Excel Format

Columns must appear in this exact order with these exact names:

| Column | Constraints |
|--------|-------------|
| `BankName` | One of: KTB, SCB, TTB, Mobile Banking (Alpha), PromptPay, TCRB, Lotus, 7-11 |
| `PaymentDate` | DDMMYYYY (8 chars) |
| `PaymentTime` | HHMMSS / HH24MISS (6 chars, 24-hour) |
| `CustomerName` | Max 50 chars |
| `Account` | Numeric only, max 20 digits |
| `Amt` | Decimal, 2 decimal places; stored as 13-digit integer string (no decimal point) |

## Code Style

- Python 3.9+ — use `Optional[X]`, `List`, `Dict` from `typing` (not `X | None` syntax)
- Type hints required on all function signatures
- `logging.getLogger(__name__)` for logging; DEBUG for dev, INFO for normal, ERROR for failures
- Custom exceptions: `ValidationError` (defined in `validators.py`) for domain errors
