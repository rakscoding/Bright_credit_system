from django.contrib import admin
from .models import User, Loan, Billing, Transaction
# Register your models here.
admin.site.register(User)
admin.site.register(Loan)
admin.site.register(Billing)
admin.site.register(Transaction)