import csv
import os
import tempfile
from unittest.mock import MagicMock, patch

import openpyxl
import pytest

from src.converter import (
    build_body_line,
    build_header_line,
    build_trailer_line,
    convert_to_payment,
    read_csv,
    read_excel,
)
from src.models import PaymentRecord


class TestBuildHeaderLine:
    def test_build_header_line(self):
        line = build_header_line(1, "13032026", "071")
        assert len(line) == 256
        assert line[0] == "H"
        assert line[1:7] == "000001"
        assert line[7:10] == "071"
        assert line[10:20] == "1814003005"
        assert line[20:60] == "TCRB".ljust(40)
        assert line[60:68] == "13032026"


class TestBuildBodyLine:
    def test_build_body_line(self):
        record = PaymentRecord(
            bank_name="TCRB",
            bank_code="071",
            company_account="1814003005",
            payment_date="05022018",
            payment_time="101102",
            customer_name="John Doe",
            account="1234567890",
            amount=1234.50,
            amount_formatted="0000000123450",
        )
        line = build_body_line(2, record)
        assert len(line) == 256
        assert line[0] == "D"
        assert line[1:7] == "000002"
        assert line[7:10] == "071"
        assert line[20:28] == "05022018"
        assert line[28:34] == "101102"
        assert line[34:84] == "John Doe".ljust(50)
        assert line[84:104] == "1234567890".ljust(20)
        assert line[144:148] == "0901"
        assert line[148:152] == "0000"
        assert line[152] == "C"
        assert line[153:156] == "CSH"
        assert line[156:163] == "0000000"
        assert line[163:176] == "0000000123450"


class TestBuildTrailerLine:
    def test_build_trailer_line(self):
        line = build_trailer_line(3, "071", "0000000123450")
        assert len(line) == 256
        assert line[0] == "T"
        assert line[1:7] == "000003"
        assert line[7:10] == "071"
        assert line[10:20] == "1814003005"
        assert line[20:33] == "0000000000000"
        assert line[33:39] == "000000"
        assert line[39:52] == "0000000123450"
        assert line[176:179] == "000"


class TestReadExcel:
    @pytest.fixture
    def temp_excel_file(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
        ws.append(["TCRB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
        ws.append(["SCB", "06022018", "102030", "Jane Smith", "0987654321", "500.00"])
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            wb.save(f.name)
            yield f.name
        os.unlink(f.name)

    def test_read_excel_wrong_bank_name(self, temp_excel_file):
        records = read_excel(temp_excel_file)
        assert len(records) == 2
        assert records[0].bank_name == "TCRB"
        # assert records[0].bank_code == "071"
        assert records[0].payment_date == "05022018"
        assert records[1].bank_name == "SCB"
        # assert records[1].bank_code == "987"   


class TestConvertExcelToPayment:
    @pytest.fixture
    def temp_excel_file(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
        ws.append(["SCB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
        ws.append(["TTB", "06022018", "102030", "Jane Smith", "0987654321", "500.00"])
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            wb.save(f.name)
            yield f.name
        os.unlink(f.name)

    def test_convert_excel_to_payment(self, temp_excel_file):
        result = convert_to_payment(temp_excel_file, "output")
        assert result.success is True
        assert result.record_count == 2
        assert result.total_amount == 1734.50
        assert os.path.exists(result.output_path)
        with open(result.output_path, "r") as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
            assert len(lines) == 4
            assert len(lines[0]) == 256
            assert len(lines[1]) == 256
            assert len(lines[2]) == 256
            assert len(lines[3]) == 256
            assert lines[0][0] == "H"
            assert lines[1][0] == "D"
            assert lines[2][0] == "D"
            assert lines[3][0] == "T"
        os.unlink(result.output_path)

    def test_convert_with_custom_filename(self, temp_excel_file):
        result = convert_to_payment(temp_excel_file, "output", output_filename="my_output.txt")
        assert result.success is True
        assert result.output_path.endswith("my_output.txt")
        assert os.path.exists(result.output_path)
        os.unlink(result.output_path)

    def test_convert_default_filename(self, temp_excel_file):
        import re
        result = convert_to_payment(temp_excel_file, "output")
        assert result.success is True
        assert re.match(r"COLLECTION_\d{8}\.txt", os.path.basename(result.output_path))
        os.unlink(result.output_path)


class TestReadCsv:
    @pytest.fixture
    def temp_csv_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
            writer.writerow(["TCRB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
            writer.writerow(["SCB", "06022018", "102030", "Jane Smith", "0987654321", "500.00"])
            name = f.name
        yield name
        os.unlink(name)

    def test_read_csv_returns_records(self, temp_csv_file):
        records = read_csv(temp_csv_file)
        assert len(records) == 2
        assert records[0].bank_name == "TCRB"
        assert records[0].payment_date == "05022018"
        assert records[0].payment_time == "101102"
        assert records[0].customer_name == "John Doe"
        assert records[0].account == "1234567890"
        assert records[1].bank_name == "SCB"

    def test_read_csv_skips_empty_rows(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
            writer.writerow(["TCRB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
            writer.writerow(["", "", "", "", "", ""])
            writer.writerow(["SCB", "06022018", "102030", "Jane Smith", "0987654321", "500.00"])
            name = f.name
        try:
            records = read_csv(name)
            assert len(records) == 2
        finally:
            os.unlink(name)

    def test_read_csv_invalid_headers_raises(self):
        from src.validators import ValidationError
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["WrongHeader", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
            writer.writerow(["TCRB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
            name = f.name
        try:
            with pytest.raises(ValidationError):
                read_csv(name)
        finally:
            os.unlink(name)

    def test_read_csv_invalid_bank_name_raises(self):
        from src.validators import ValidationError
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
            writer.writerow(["INVALID_BANK", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
            name = f.name
        try:
            with pytest.raises(ValidationError):
                read_csv(name)
        finally:
            os.unlink(name)


class TestConvertCsvToPayment:
    @pytest.fixture
    def temp_csv_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"])
            writer.writerow(["SCB", "05022018", "101102", "John Doe", "1234567890", "1234.50"])
            writer.writerow(["TTB", "06022018", "102030", "Jane Smith", "0987654321", "500.00"])
            name = f.name
        yield name
        os.unlink(name)

    def test_convert_csv_to_payment(self, temp_csv_file):
        result = convert_to_payment(temp_csv_file, "output")
        assert result.success is True
        assert result.record_count == 2
        assert result.total_amount == 1734.50
        assert os.path.exists(result.output_path)
        with open(result.output_path, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
            assert len(lines) == 4
            assert all(len(line) == 256 for line in lines)
            assert lines[0][0] == "H"
            assert lines[1][0] == "D"
            assert lines[2][0] == "D"
            assert lines[3][0] == "T"
        os.unlink(result.output_path)

    def test_convert_unsupported_extension_returns_error(self):
        result = convert_to_payment("input.txt", "output")
        assert result.success is False
        assert "Unsupported file type" in result.error_message
