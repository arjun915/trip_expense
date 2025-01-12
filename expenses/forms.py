# expenses/forms.py
from django import forms
from .models import Trip, Participant, Expense, Contribution

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'total_amount', 'paid_by']
        # widgets = {
        #     'date': forms.DateInput(attrs={'type': 'date'}),
        # }

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['participant', 'amount']
