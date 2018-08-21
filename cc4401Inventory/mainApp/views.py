from django.shortcuts import render
from django.utils.timezone import localtime
import datetime
from articlesApp.models import Article
from reservationsApp.models import Reservation
from django.contrib.auth.decorators import login_required

from spacesApp.models import Space


@login_required
def landing_articles(request):
    context = {}
    return render(request, 'articulos.html', context)


@login_required
def landing_spaces(request, date=None, filtered=[]):
    spaces_list = Space.objects.all()
    if date:
        current_date = date
        current_week = datetime.datetime.strptime(current_date, "%Y-%m-%d").date().isocalendar()[1]
    else:
        try:
            current_week = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d").date().isocalendar()[1]
            current_date = request.GET["date"]
        except:
            current_week = datetime.date.today().isocalendar()[1]
            current_date = datetime.date.today().strftime("%Y-%m-%d")

    if not filtered:
        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'])

    else:
        reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'],
                                                  space__name__in=filtered)

    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)'}

    res_list = []
    for i in range(5):
        res_list.append(list())
    for r in reservations:
        reserv = []
        reserv.append(r.space.name)
        reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
        reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
        reserv.append(colores[r.state])
        res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

    move_controls = list()
    move_controls.append(
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-4)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=-1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=1)).strftime("%Y-%m-%d"))
    move_controls.append(
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(weeks=4)).strftime("%Y-%m-%d"))

    delta = (datetime.datetime.strptime(current_date, "%Y-%m-%d").isocalendar()[2]) - 1
    monday = (
        (datetime.datetime.strptime(current_date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%d/%m/%Y"))
    context = {'reservations': res_list,
               'current_date': current_date,
               'controls': move_controls,
               'actual_monday': monday,
               'filtered': filtered,
               'spaces': spaces_list}

    return render(request, 'espacios.html', context)


@login_required
def landing_search(request, products):
    if not products:
        return landing_articles(request)
    else:
        context = {'productos': products,
                   'colores': {'D': '#009900',
                               'R': '#ffcc00',
                               'P': '#3333cc',
                               'L': '#cc0000'}
                   }
        return render(request, 'articulos.html', context)


@login_required
def search(request):
    if request.method == "GET":
        query = request.GET['query']
        a_state = request.GET['estado']
        date = request.GET['fecha']
        article_id = request.GET['id']

        articles = Article.objects.all()
        if not (a_state == "A"):
            articles = articles.filter(state=a_state)
        if not (query == ''):
            articles = articles.filter(name__icontains=query.lower())
        if not (article_id == ''):
            articles = articles.filter(id=article_id)
        return landing_search(request, articles)

global_spaces = []
global_date = ''

@login_required
def select_spaces(request):
    get_date(request)
    global global_spaces
    if request.method == "POST":
        spaces_list = request.POST.getlist('checkbox')

        global_spaces = spaces_list

        return landing_spaces(request, date=global_date, filtered=global_spaces)
    else:
        return landing_spaces(request, date=global_date, filtered=global_spaces)

@login_required
def get_date(request):
    global global_date
    if request.method == "GET":
        date = request.GET.get('date')
        global_date = date
        return global_date


