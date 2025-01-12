# expenses/models.py
from django.db import models

class Trip(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the primary key
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the primary key
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="participants")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.trip.name})"

class Expense(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the primary key
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="expenses")
    description = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="paid_expenses")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - ${self.total_amount}"

class Contribution(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining the primary key
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="contributions")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.participant.name} contributed ${self.amount} to {self.expense.description}"
