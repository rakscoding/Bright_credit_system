import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(models.Model):
    aadhar_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.aadhar_id})"

class Loan(models.Model):
    LOAN_STATUS = (("Active", "Active"), ("Closed", "Closed"))

    loan_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)
    term_period = models.IntegerField()  # Months
    disbursement_date = models.DateField()
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default="Active")

    def __str__(self):
        return f"Loan {self.loan_id} - {self.user.name}"

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    min_due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Billing for {self.user.name} - Due {self.due_date}"

class Transaction(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    principal_due = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(("Paid", "Paid"), ("Pending", "Pending")), default="Pending")

    def __str__(self):
        return f"Transaction {self.id} for {self.loan.user.name}"
class EMI(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_date = models.DateField()
    principal_due = models.DecimalField(max_digits=10, decimal_places=2)
    interest_due = models.DecimalField(max_digits=10, decimal_places=2)
    total_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"EMI for Loan {self.loan.id} due on {self.due_date}"
class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    min_due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Billing for {self.user.name} - Due {self.due_date}"
