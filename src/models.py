from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentRecord:
    bank_name: str
    bank_code: str
    company_account: str
    payment_date: str
    payment_time: str
    customer_name: str
    account: str
    amount: float
    amount_formatted: str


@dataclass
class ConversionResult:
    success: bool
    output_path: Optional[str] = None
    record_count: int = 0
    total_amount: float = 0.0
    error_message: Optional[str] = None
