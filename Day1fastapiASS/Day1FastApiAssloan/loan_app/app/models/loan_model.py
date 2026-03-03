class LoanApplication:
    def __init__(self, id, applicant_name, income, loan_amount, status="PENDING"):
        self.id = id
        self.applicant_name = applicant_name
        self.income = income
        self.loan_amount = loan_amount
        self.status = status
