from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reservationsApp.models import Reservation
from loansApp.models import Loan
from articlesApp.models import Article
from spacesApp.models import Space
from mainApp.models import User
from datetime import datetime, timedelta, date
import pytz
from django.utils.timezone import localtime


@login_required
def user_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_panel.html', context)


@login_required
def items_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    articles = Article.objects.all()
    spaces = Space.objects.all()
    context = {
        'articles': articles,
        'spaces': spaces
    }
    return render(request, 'items_panel.html', context)


@login_required
def actions_panel(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')
    #  current week
    try:
        current_week = \
        datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[
            1]
        current_date = request.GET["date"]
    except:
        current_date = date.today().strftime("%Y-%m-%d")
        current_week = date.today().isocalendar()[1]

    reservations = Reservation.objects.filter(state='P').order_by(
        'starting_date_time')
    
    # controls
    move_controls = list()
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(
            weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(
            weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(
            weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(
            weeks=4)).strftime("%Y-%m-%d"))

    # this monday
    delta = (datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
    monday = (
        (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(
            days=delta)).strftime("%d/%m/%Y"))

    context = {
        'reservations_query': reservations,
        'loans': queryLoans(request),
        'reservations': queryCalendarData(current_week),
        'current_date': current_date,
        'controls': move_controls,
        'actual_monday': monday
    }
    return render(request, 'actions_panel.html', context)


def modify_reservations(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')

    if "selected" not in request.POST:
        return redirect('/admin/actions-panel')
    
    if request.method == "POST":

        accept = True if (request.POST["accept"] == "1") else False
        reservations = Reservation.objects.filter(
            id__in=request.POST.getlist("selected"))
        if accept:
            for reservation in reservations:
                reservation.state = 'A'
                reservation.save()
        else:
            for reservation in reservations:
                reservation.state = 'R'
                reservation.save()

    return redirect('/admin/actions-panel')

def modify_loans(request):
    user = request.user
    if not (user.is_superuser and user.is_staff):
        return redirect('/')

    if "selected" not in request.POST:
        return redirect('/admin/actions-panel')
    
    if request.method == "POST":

        loans = Loan.objects.filter(id__in=request.POST.getlist("selected"))

        if request.POST["returned"] == "1":
            for loan in loans:
                loan.article.state = 'D'
                loan.article.save()
        else:
            for loan in loans:
                loan.article.state = 'L'
                loan.article.save()


    return redirect('/admin/actions-panel')

def remove_article(request):
    if request.method == "POST":
        artId = request.POST["article_id"]
        art = Article.objects.get(id=artId)
        art.delete()
    
    return redirect('/admin/items-panel')

def remove_space(request):
    if request.method == "POST":
        artId = request.POST["space_id"]
        art = Space.objects.get(id=artId)
        art.delete()
    
    return redirect('/admin/items-panel')



############################################
########### building queries ###########
############################################
def queryCalendarData(current_week):
    current_week_reservations = Reservation.objects.filter(
        starting_date_time__week=current_week)

    colores_resv = {'A': 'rgba(0,153,0,0.7)',
            'P': 'rgba(51,51,204,0.7)',
            'R': 'rgba(153, 0, 0,0.7)'} 

    colores_loans = {'A': 'rgba(0,153,0,0.7)',
            'P': 'rgba(51,51,204,0.7)',
            'R': 'rgba(153, 0, 0,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    
    for r in current_week_reservations:
        reserv = list()
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores_resv[r.state])
        reserv.append(r.get_state_display())
        # link
        reserv.append('/space/'+ str(r.id))
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

    current_week_loans = Loan.objects.filter(
        starting_date_time__week=current_week)
    for r in current_week_loans:
        reserv = list()
        reserv.append(r.article.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores_loans[r.state])
        reserv.append(r.get_state_display())
        # link
        reserv.append('/article/'+ str(r.id))
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)
    return res_list
    
def queryLoans(request):
    actual_date = datetime.now(tz=pytz.utc)
    try:
        if request.method == "GET":
            if request.GET["filter"] == 'vigentes':
                loans = Loan.objects.filter(
                    ending_date_time__gt=actual_date).order_by(
                    'starting_date_time')
            elif request.GET["filter"] == 'caducados':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date,
                                            ).order_by(
                    'starting_date_time')
            elif request.GET["filter"] == 'perdidos':
                loans = Loan.objects.filter(ending_date_time__lt=actual_date,
                                            article__state='L').order_by(
                    'starting_date_time')
            else:
                loans = Loan.objects.all().order_by('starting_date_time')
    except:
        loans = Loan.objects.all().order_by('starting_date_time')

    return loans

