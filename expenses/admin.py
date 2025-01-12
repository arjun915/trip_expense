from django.contrib import admin

# Register your models here.
from .models import Participant,Expense,Trip,Contribution

admin.site.register(Participant)
admin.site.register(Expense)
admin.site.register(Trip)
admin.site.register(Contribution)

