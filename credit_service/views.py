from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import uuid
from django.http import JsonResponse
from datetime import timedelta
from .models import EMI
from django.utils.timezone import now

def home_page(request):
    return render(request, 'index.html')
def api_home(request):
    return JsonResponse({"message": "Welcome to Bright Credit Service API!", "endpoints": [
        "/api/register-user/",
        "/api/apply-loan/",
        "/api/make-payment/",
        "/api/get-statement/"
    ]})
    
def home_redirect(request):
    return redirect('/api/')

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "unique_user_id": str(uuid.uuid4()),
                "error": None
            }, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ApplyLoan(APIView):
    def post(self, request):
        user_id = request.data.get("unique_user_id")
        user = User.objects.filter(id=user_id).first()

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user.credit_score < 450:
            return Response({"error": "Credit score too low"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan = serializer.save(user=user)
            calculate_emi(loan)  
            return Response({"Loan_id": serializer.data['loan_id'], "error": None}, status=status.HTTP_200_OK)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def calculate_emi(loan):
    """Generate EMI schedule for a loan"""
    principal = loan.loan_amount
    rate = loan.interest_rate / 100 / 12  # Convert annual rate to monthly rate
    months = loan.term_period

    if rate > 0:
        emi_amount = (principal * rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
    else:
        emi_amount = principal / months

    due_date = loan.disbursement_date
    for _ in range(months):
        interest_due = principal * rate
        principal_due = emi_amount - interest_due
        EMI.objects.create(
            loan=loan,
            due_date=due_date,
            principal_due=round(principal_due, 2),
            interest_due=round(interest_due, 2),
            total_due=round(emi_amount, 2),
            is_paid=False
        )
        due_date += timedelta(days=30)
        principal -= principal_due
class MakePayment(APIView):
    def post(self, request):
        loan_id = request.data.get("Loan_id")
        amount = request.data.get("Amount")

        loan = Loan.objects.filter(loan_id=loan_id).first()
        if not loan:
            return Response({"error": "Loan not found"}, status=status.HTTP_400_BAD_REQUEST)

        pending_emis = EMI.objects.filter(loan=loan, is_paid=False).order_by("due_date")

        for emi in pending_emis:
            if amount >= emi.total_due:
                amount -= emi.total_due
                emi.is_paid = True
                emi.save()
            else:
                emi.total_due -= amount
                amount = 0
                emi.save()
                break

        return Response({"message": "Payment recorded successfully"}, status=status.HTTP_200_OK)


def generate_billing():
    today = now().date()
    loans = Loan.objects.all()

    for loan in loans:
        last_billing = Billing.objects.filter(loan=loan).order_by('-billing_date').first()
        next_billing_date = last_billing.billing_date + timedelta(days=30) if last_billing else loan.disbursement_date

        if today >= next_billing_date:
            due_date = next_billing_date + timedelta(days=15)
            pending_emis = EMI.objects.filter(loan=loan, is_paid=False)
            min_due = sum(emi.total_due for emi in pending_emis[:1])  # First EMI amount

            Billing.objects.create(
                user=loan.user,
                loan=loan,
                billing_date=next_billing_date,
                min_due_amount=min_due,
                due_date=due_date,
                is_paid=False
            )
class GetStatement(APIView):
    def get(self, request, loan_id):
        loan = Loan.objects.filter(loan_id=loan_id).first()
        if not loan:
            return Response({"error": "Loan not found"}, status=status.HTTP_400_BAD_REQUEST)

        transactions = EMI.objects.filter(loan=loan).order_by('due_date')
        response = {
            "Past_transactions": list(transactions.values()),
            "Upcoming_transactions": list(EMI.objects.filter(loan=loan, is_paid=False).values())
        }
        return Response(response, status=status.HTTP_200_OK)
