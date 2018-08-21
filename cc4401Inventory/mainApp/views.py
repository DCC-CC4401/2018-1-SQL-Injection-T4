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
def landing_spaces(request, date=None):
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

    reservations = Reservation.objects.filter(starting_date_time__week=current_week, state__in=['P', 'A'])
    colores = {'A': 'rgba(0,153,0,0.7)',
               'P': 'rgba(51,51,204,0.7)'}

    try:
        select_spaces = []
        for space in Space.objects.all():
            select_spaces.append(request.POST[space.name])
        res_list = []
        for i in range(5):
            res_list.append(list())
        for r in reservations:
            if r.space.name in select_spaces:
                reserv = []
                reserv.append(r.space.name)
                reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
                reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
                reserv.append(colores[r.state])
                res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)
    except:
        select_spaces = []
        for space in Space.objects.all():
            select_spaces.append(space.name)
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
               'actual_monday': monday}

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

def space_request_select(request):
    if request.method == 'POST' and 'picked-date' in request.POST:
        if request.user.enabled:
            try:
                space = Space.objects.get(name=request.POST['space'])

                string_inicio = request.POST['picked-date'] + " " + \
                                request.POST['picked-start-time']
                start_date_time = datetime.datetime.strptime(string_inicio,
                                                    '%d/%m/%Y %H:%M')
                string_fin = request.POST['picked-date'] + " " + request.POST[
                    'picked-end-time']
                end_date_time = datetime.datetime.strptime(string_fin, '%d/%m/%Y %H:%M')

                if start_date_time > end_date_time:
                    messages.warning(request,
                                     'La reserva debe terminar después de iniciar.')
                elif start_date_time - datetime.datetime.now() < timedelta(hours=1):
                    messages.warning(request,
                                     'Los pedidos deben ser hechos al menos con una hora de anticipación.')
                elif start_date_time.date() != end_date_time.date():
                    messages.warning(request,
                                     'Los pedidos deben ser devueltos el mismo día que se entregan.')
                elif not verificar_horario_habil(start_date_time, end_date_time, space_id):
                    messages.warning(request,
                                     'Los pedidos deben ser hechos en horario hábil.')
                else:
                    reservation = Reservation(space=space,
                                              starting_date_time=start_date_time,
                                              ending_date_time=end_date_time,
                                              user=request.user)
                    reservation.save()
                    messages.success(request, 'Pedido realizado con éxito')
            except Exception as e:
                print(e)
                messages.warning(request, 'Ingrese una fecha y hora válida.')
        else:
            messages.warning(request, 'Usuario no habilitado para pedir préstamos')

    return redirect('landing_spaces')
