import pytest

from src.validators import (
    ValidationError,
    format_amount,
    get_bank_info,
    validate_account,
    validate_amount,
    validate_bank_name,
    validate_customer_name,
    validate_excel_headers,
    validate_payment_date,
    validate_payment_time,
)


class TestValidateBankName:
    def test_valid_bank_name(self):
        assert validate_bank_name("KTB") == "KTB"
        assert validate_bank_name("SCB") == "SCB"
        assert validate_bank_name("PromptPay") == "PromptPay"
        assert validate_bank_name("TCRB") == "TCRB"
        assert validate_bank_name("7-11") == "7-11"

    def test_invalid_bank_name(self):
        with pytest.raises(ValidationError):
            validate_bank_name("InvalidBank")
        with pytest.raises(ValidationError):
            validate_bank_name("")
        with pytest.raises(ValidationError):
            validate_bank_name("   ")


class TestGetBankInfo:
    def test_get_bank_info_scb(self):
        info = get_bank_info("SCB")
        assert info["code"] == "014"
        assert info["account"] == "2783003832"

    def test_get_bank_info_tcrb(self):
        info = get_bank_info("TCRB")
        assert info["code"] == "071"
        assert info["account"] == "1814003005"


class TestValidatePaymentDate:
    def test_valid_payment_date(self):
        assert validate_payment_date("05022018") == "05022018"
        assert validate_payment_date("31122020") == "31122020"

    def test_invalid_payment_date_length(self):
        with pytest.raises(ValidationError):
            validate_payment_date("050220")
        with pytest.raises(ValidationError):
            validate_payment_date("050220188")

    def test_invalid_payment_date_nondigit(self):
        with pytest.raises(ValidationError):
            validate_payment_date("05ab2018")

    def test_invalid_payment_date_month(self):
        with pytest.raises(ValidationError):
            validate_payment_date("01142018")

    def test_invalid_payment_date_day(self):
        with pytest.raises(ValidationError):
            validate_payment_date("32022018")
        with pytest.raises(ValidationError):
            validate_payment_date("00022018")


class TestValidatePaymentTime:
    def test_valid_payment_time(self):
        assert validate_payment_time("101102") == "101102"
        assert validate_payment_time("235959") == "235959"

    def test_invalid_payment_time_length(self):
        with pytest.raises(ValidationError):
            validate_payment_time("10110")
        with pytest.raises(ValidationError):
            validate_payment_time("1011022")

    def test_invalid_payment_time_nondigit(self):
        with pytest.raises(ValidationError):
            validate_payment_time("10ab02")

    def test_invalid_payment_time_hour(self):
        with pytest.raises(ValidationError):
            validate_payment_time("251102")

    def test_invalid_payment_time_minute(self):
        with pytest.raises(ValidationError):
            validate_payment_time("106102")


class TestValidateCustomerName:
    def test_valid_customer_name(self):
        assert validate_customer_name("John Doe") == "John Doe"
        assert validate_customer_name("A") == "A"

    def test_customer_name_trimmed(self):
        assert validate_customer_name("  John Doe  ") == "John Doe"

    def test_invalid_customer_name_empty(self):
        with pytest.raises(ValidationError):
            validate_customer_name("")
        with pytest.raises(ValidationError):
            validate_customer_name("   ")

    def test_invalid_customer_name_too_long(self):
        with pytest.raises(ValidationError):
            validate_customer_name("A" * 51)


class TestValidateAccount:
    def test_valid_account(self):
        assert validate_account("1234567890") == "1234567890"
        assert validate_account("001234567890")

    def test_account_trimmed(self):
        assert validate_account("  1234567890  ") == "1234567890"

    def test_invalid_account_empty(self):
        with pytest.raises(ValidationError):
            validate_account("")
        with pytest.raises(ValidationError):
            validate_account("   ")

    def test_invalid_account_too_long(self):
        with pytest.raises(ValidationError):
            validate_account("1" * 21)

    def test_invalid_account_nondigit(self):
        with pytest.raises(ValidationError):
            validate_account("123456789a")


class TestValidateAmount:
    def test_valid_amount(self):
        assert validate_amount("1234.50") == 1234.50
        assert validate_amount("1234") == 1234.0
        assert validate_amount("1,234.50") == 1234.50

    def test_invalid_amount(self):
        with pytest.raises(ValidationError):
            validate_amount("")
        with pytest.raises(ValidationError):
            validate_amount("abc")
        with pytest.raises(ValidationError):
            validate_amount("-100")


class TestFormatAmount:
    def test_format_amount_with_decimals(self):
        assert format_amount(1234.50) == "0000000123450"
        assert format_amount(1000.00) == "0000000100000"

    def test_format_amount_zero(self):
        assert format_amount(0.0) == "0000000000000"

    def test_format_amount_large(self):
        assert format_amount(363600000.00) == "0036360000000"


class TestValidateExcelHeaders:
    def test_validate_excel_headers_valid(self):
        headers = ["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"]
        assert validate_excel_headers(headers) is True

    def test_validate_excel_headers_wrong_order(self):
        headers = ["PaymentDate", "BankName", "PaymentTime", "CustomerName", "Account", "Amt"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)

    def test_validate_excel_headers_extra_columns(self):
        headers = ["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt", "Extra"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)

    def test_validate_excel_headers_missing_columns(self):
        headers = ["BankName", "PaymentDate", "CustomerName", "Account"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)

    def test_validate_excel_headers_empty_header(self):
        headers = ["BankName", "", "PaymentTime", "CustomerName", "Account", "Amt"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)

    def test_validate_excel_headers_case_sensitive(self):
        headers = ["bankname", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)

    def test_validate_excel_headers_case_sensitive_2(self):
        headers = ["BankName", "paymentdate", "PaymentTime", "CustomerName", "Account", "Amt"]
        with pytest.raises(ValidationError):
            validate_excel_headers(headers)


class TestValidateBankNameLength:
    def test_validate_bank_name_max_length_100(self):
        bank_name = "TCRB"
        assert validate_bank_name(bank_name) == bank_name

    def test_validate_bank_name_over_length_100(self):
        bank_name_101 = "A" * 101
        with pytest.raises(ValidationError):
            validate_bank_name(bank_name_101)


class TestValidateAmountLength:
    def test_validate_amount_exact_length_13(self):
        assert format_amount(1234.50) == "0000000123450"
        assert format_amount(0.0) == "0000000000000"
        assert format_amount(363600000.00) == "0036360000000"

    def test_validate_amount_exact_length_13_edge_cases(self):
        assert format_amount(0.01) == "0000000000001"
        assert format_amount(999999999.99) == "0099999999999"
