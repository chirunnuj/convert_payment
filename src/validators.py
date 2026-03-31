import logging
import re
from typing import Optional

from src.constants import BANK_CODES_FOR_CUSTOMER, BANK_CODES_FOR_TCB, VALID_BANK_NAMES_FOR_CUSTOMER

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    pass


def validate_bank_name(bank_name: str) -> str:
    if not bank_name or not bank_name.strip():
        raise ValidationError("BankName cannot be empty")
    bank_name = bank_name.strip()
    if len(bank_name) > 100:
        raise ValidationError(f"BankName must be 100 characters or less, got: {len(bank_name)}")
    if bank_name not in VALID_BANK_NAMES_FOR_CUSTOMER:
        raise ValidationError(
            f"Invalid BankName: '{bank_name}'. Must be one of: {', '.join(VALID_BANK_NAMES_FOR_CUSTOMER)}"
        )
    return bank_name


def get_bank_info(bank_name: str) -> dict:
    return BANK_CODES_FOR_CUSTOMER[bank_name]

def get_bank_info_for_tcb(bank_name: str) -> dict:
    return BANK_CODES_FOR_TCB[bank_name]

def validate_payment_date(payment_date: str) -> str:
    if not payment_date or len(payment_date) != 8:
        raise ValidationError(f"PaymentDate must be exactly 8 characters, got: '{payment_date}'")
    if not payment_date.isdigit():
        raise ValidationError(f"PaymentDate must contain only digits, got: '{payment_date}'")
    day = int(payment_date[0:2])
    month = int(payment_date[2:4])
    year = int(payment_date[4:8])
    if month < 1 or month > 12:
        raise ValidationError(f"PaymentDate has invalid month: {month}")
    if day < 1 or day > 31:
        raise ValidationError(f"PaymentDate has invalid day: {day}")
    if year < 1900 or year > 2100:
        raise ValidationError(f"PaymentDate has invalid year: {year}")
    return payment_date


def validate_payment_time(payment_time: str) -> str:
    if not payment_time or len(payment_time) != 6:
        raise ValidationError(f"PaymentTime must be exactly 6 characters, got: '{payment_time}'")
    if not payment_time.isdigit():
        raise ValidationError(f"PaymentTime must contain only digits, got: '{payment_time}'")
    hour = int(payment_time[0:2])
    minute = int(payment_time[2:4])
    second = int(payment_time[4:6])
    if hour > 23:
        raise ValidationError(f"PaymentTime has invalid hour: {hour}")
    if minute > 59:
        raise ValidationError(f"PaymentTime has invalid minute: {minute}")
    if second > 59:
        raise ValidationError(f"PaymentTime has invalid second: {second}")
    return payment_time


def validate_customer_name(customer_name: str) -> str:
    if not customer_name or not customer_name.strip():
        raise ValidationError("CustomerName cannot be empty")
    customer_name = customer_name.strip()
    if len(customer_name) > 50:
        raise ValidationError(f"CustomerName must be 50 characters or less, got: {len(customer_name)}")
    return customer_name


def validate_account(account: str) -> str:
    if not account or not account.strip():
        raise ValidationError("Account cannot be empty")
    account = account.strip()
    if len(account) > 20:
        raise ValidationError(f"Account must be 20 digits or less, got: {len(account)}")
    if not account.isdigit():
        raise ValidationError(f"Account must contain only digits, got: '{account}'")
    return account


def validate_amount(amount_str: str) -> float:
    if not amount_str or not amount_str.strip():
        raise ValidationError("Amount cannot be empty")
    amount_str = amount_str.strip()
    amount_str_clean = amount_str.replace(",", "").replace(" ", "")
    try:
        amount = float(amount_str_clean)
    except ValueError:
        raise ValidationError(f"Amount must be a valid number, got: '{amount_str}'")
    if amount < 0:
        raise ValidationError(f"Amount must be non-negative, got: {amount}")
    return amount


def format_amount(amount: float) -> str:
    amount_cents = int(round(amount * 100))
    formatted = str(amount_cents).zfill(13)
    if len(formatted) != 13:
        raise ValidationError(f"Formatted amount must be exactly 13 characters, got: {len(formatted)}")
    return formatted


def validate_excel_headers(headers: list) -> bool:
    expected_columns = ["BankName", "PaymentDate", "PaymentTime", "CustomerName", "Account", "Amt"]
    
    if len(headers) != 6:
        raise ValidationError(f"Expected 6 columns, got {len(headers)}")

    for i, expected in enumerate(expected_columns):
        actual = headers[i]
        if actual != expected:
            raise ValidationError(
                f"Column {i+1} should be '{expected}', got '{actual}'"
            )
    
    return True
