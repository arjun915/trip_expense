from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trip, Participant, Expense
from .forms import TripForm, ParticipantForm, ExpenseForm
from django.http import HttpResponse
from django.db.models import Sum


# expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip, Participant, Expense, Contribution
from .forms import TripForm, ParticipantForm, ExpenseForm, ContributionForm

def add_expense(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip = trip
            expense.save()
            cleaned_data = form.cleaned_data
            contribution = cleaned_data['total_amount']
            paid_by = cleaned_data['paid_by']  # The participant who paid for the expense
            participant_name = paid_by.name
            participant = trip.participants.filter(name=participant_name).first()
            Contribution.objects.create(
                expense=expense,           # Expense object you already have
                participant=participant,   # The participant object filtered by name
                amount=float(contribution)  # Amount contributed by the participant
            )

            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form, 'trip': trip})

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    participants = trip.participants.all()
    expenses = trip.expenses.all()

    # Calculate balances
    total_expense = sum(expense.total_amount for expense in expenses)
    participant_count = participants.count()
    individual_share = total_expense / participant_count if participant_count else 0
    balances = {p.name: -individual_share for p in participants}
    
    # Calculate the balance considering contributions
    for expense in expenses:
        for contribution in expense.contributions.all():
            balances[contribution.participant.name] += contribution.amount
    context = {
        'trip': trip,
        # 'participants': participants,
        'expenses': expenses,
        'balances': balances,
    }

    return render(request, 'expenses/trip_details.html', context)

def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trip_list')
    else:
        form = TripForm()

    return render(request, 'expenses/create_trip.html', {'form': form})

def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'expenses/trip_list.html', {'trips': trips})

def add_participant(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        # Create a new Participant
        participant = Participant(name=name, trip=trip)
        participant.save()
        
        # Redirect to the trip details page
        return redirect('trip_detail', trip_id=trip.id)
    return HttpResponse('Invalid request', status=400)

def trip_summary(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    participants = trip.participants.all()
    
    # Calculate total expenses for the trip
    
    total_expenses = Expense.objects.filter(trip=trip).aggregate(total=Sum('total_amount'))['total'] or 0.0

    # Prepare data for each participant
    participant_data = []
    for participant in participants:
        # Fetch all contributions related to the current participant for the specific trip
        contributions = Contribution.objects.filter(participant=participant, expense__trip=trip)
        # print(contributions.query, "Query for contributions")  # Debug the query
        # print(contributions,"@@@@@@@")
        # Print out the contributions for the participant to see if they are distinct
        # for contribution in contributions:
        #     print(f"Contribution: {contribution.expense.total_amount} for Expense: {contribution.expense.description}")
        
        # Calculate total contribution from the participant's contributions
        total_contribution = contributions.aggregate(total=Sum('amount'))['total'] or 0.0
        # print(f"Total Contribution for {participant.name}: {total_contribution}")

        # Calculate total expenses for the trip (sum of all expenses)
        total_expenses = trip.expenses.aggregate(total=Sum('total_amount'))['total'] or 0.0
        # print(f"Total Expenses for Trip '{trip.name}': {total_expenses}")

        # Calculate amount owed (split equally among all participants)
        amount_owed = total_expenses / participants.count() if participants.exists() else 0.0
        # print(f"Amount Owed per Participant: {amount_owed}")

        # Calculate dues (negative if overpaid, positive if underpaid)
        dues = int(amount_owed) - int(total_contribution)
        abs_dues = abs(dues)

        participant_data.append({
            'name': participant.name,
            'total_contribution': total_contribution,
            'amount_owed': round(amount_owed,2),
            'dues': dues,
            'abs_dues': abs_dues,
        })

    context = {
        'trip': trip,
        'total_expenses': total_expenses,
        'participant_data': participant_data,
    }
    return render(request, 'expenses/trip_summary.html', context)