from app.core import config
from app.models.loan_model import LoanApplication

def create_loan(applicant_name, income, loan_amount):
    loan = LoanApplication(
        config.loan_id_counter,
        applicant_name,
        income,
        loan_amount
    )
    config.loans[config.loan_id_counter] = loan
    config.loan_id_counter += 1
    return loan

def get_loan_by_id(loan_id):
    return config.loans.get(loan_id)

def list_loans():
    return list(config.loans.values())

def update_status(loan_id, status):
    loan = config.loans.get(loan_id)
    if loan:
        loan.status = status
    return loan
