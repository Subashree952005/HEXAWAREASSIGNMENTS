from app.repositories import loan_repository

ELIGIBILITY_MULTIPLIER = 10

def submit_loan(applicant_name, income, loan_amount):
    eligibility = income * ELIGIBILITY_MULTIPLIER
    if loan_amount > eligibility:
        raise ValueError("Loan amount exceeds eligibility limit")

    return loan_repository.create_loan(applicant_name, income, loan_amount)

def get_loan(loan_id):
    loan = loan_repository.get_loan_by_id(loan_id)
    if not loan:
        raise ValueError("Loan application not found")
    return loan

def get_all_loans():
    return loan_repository.list_loans()

def approve_loan(loan_id):
    loan = get_loan(loan_id)

    if loan.status != "PENDING":
        raise ValueError("Only pending loans can be approved")

    loan_repository.update_status(loan_id, "APPROVED")
    return loan

def reject_loan(loan_id):
    loan = get_loan(loan_id)

    if loan.status != "PENDING":
        raise ValueError("Only pending loans can be rejected")

    loan_repository.update_status(loan_id, "REJECTED")
    return loan
