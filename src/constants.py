BANK_CODES_FOR_TCB = {
    "SCB": {"code": "988", "account": "2783003832"},
    "KBANK": {"code": "989", "account": "0028221371"},  
    "KrungSri": {"code": "987", "account": "6840000684"},    
    "TCRB": {"code": "986", "account": "7771007779"},
    "BBL": {"code": "985", "account": "2153037755"},
    "BIGC": {"code": "983", "account": "1814003005"},
    "DUMMY": {"code": "984", "account": "1814003005"},
    "Lotus": {"code": "981", "account": "1814003005"},
    "7-11": {"code": "982", "account": "1814003005"},
}

BANK_CODES_FOR_CUSTOMER = {
    "SCB": {"code": "014", "account": "2783003832"},
    "KTB": {"code": "006", "account": "0028221371"},    
    "TTB": {"code": "011", "account": "6840000684"},    
    "Mobile Banking (Alpha)": {"code": "909", "account": "2783003832"},
    "PromptPay": {"code": "071", "account": "1814003005"},
    "TCRB": {"code": "071", "account": "1814003005"},
    "Lotus": {"code": "997", "account": "1814003005"},
    "7-11": {"code": "982", "account": "1814003005"},
}

COMPANY_NAME = "TCRB"
DEFAULT_BANK_CODE = "071"
DEFAULT_COMPANY_ACCOUNT = "1814003005"

LINE_LENGTH = 256

HEADER_SPEC = {
    "record_type": {"pos": 1, "length": 1, "value": "H"},
    "seq_no": {"pos": 2, "length": 6, "value": "000001"},
    "bank_code": {"pos": 8, "length": 3},
    "company_account": {"pos": 11, "length": 10},
    "company_name": {"pos": 21, "length": 40},
    "eff_date": {"pos": 61, "length": 8},
    "empty": {"pos": 69, "length": 188},
}

BODY_SPEC = {
    "record_type": {"pos": 1, "length": 1, "value": "D"},
    "seq_no": {"pos": 2, "length": 6},
    "bank_code": {"pos": 8, "length": 3},
    "payment_date": {"pos": 21, "length": 8},
    "payment_time": {"pos": 29, "length": 6},
    "customer_name": {"pos": 35, "length": 50},
    "account": {"pos": 85, "length": 20},
    "ref2": {"pos": 105, "length": 20, "value": " " * 20},
    "ref3": {"pos": 125, "length": 20, "value": " " * 20},
    "branch": {"pos": 145, "length": 4, "value": "0901"},
    "teller": {"pos": 149, "length": 4, "value": "0000"},
    "kind_tran": {"pos": 153, "length": 1, "value": "C"},
    "tran_code": {"pos": 154, "length": 3, "value": "CSH"},
    "cheque_no": {"pos": 157, "length": 7, "value": "0000000"},
    "amt": {"pos": 164, "length": 13},
}

TRAILER_SPEC = {
    "record_type": {"pos": 1, "length": 1, "value": "T"},
    "seq_no": {"pos": 2, "length": 6},
    "bank_code": {"pos": 8, "length": 3},
    "company_account": {"pos": 11, "length": 10},
    "sum_debit": {"pos": 21, "length": 13, "value": "0000000000000"},
    "count_debit": {"pos": 34, "length": 6, "value": "000000"},
    "sum_credit": {"pos": 40, "length": 13},
    "chq_bank_code": {"pos": 177, "length": 3, "value": "000"},
    "empty": {"pos": 180, "length": 77},
}

VALID_BANK_NAMES_FOR_CUSTOMER = list(BANK_CODES_FOR_CUSTOMER.keys())
VALID_BANK_NAMES_FOR_TCB = list(BANK_CODES_FOR_TCB.keys())