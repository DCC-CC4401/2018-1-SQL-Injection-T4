from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from spacesApp.models import Space
from spacesApp.forms import SpaceForm
from reservationsApp.models import Reservation
from django.db import models
from datetime import timedelta
import datetime
from django.utils.timezone import localtime


import random, os
import pytz
from django.contrib import messages


@login_required
def space_data(request, space_id, date=None):
	try:
		space = Space.objects.get(id=space_id)
		space_request(request, space_id)

		if date:
			current_date = date
			current_week = datetime.datetime.strptime(current_date,
			                                          "%Y-%m-%d").date().isocalendar()[
				1]
		else:
			try:
				current_week = datetime.datetime.strptime(request.GET["date"],
				                                          "%Y-%m-%d").date().isocalendar()[
					1]
				current_date = request.GET["date"]
			except:
				current_week = datetime.date.today().isocalendar()[1]
				current_date = datetime.date.today().strftime("%Y-%m-%d")

		delta = (datetime.datetime.strptime(current_date,
		                                    "%Y-%m-%d").isocalendar()[2]) - 1
		monday = ((datetime.datetime.strptime(current_date,
		                                      "%Y-%m-%d") - datetime.timedelta(
			days=delta)).strftime("%d/%m/%Y"))
		move_controls = list()
		move_controls.append((datetime.datetime.strptime(current_date,
		                                                 "%Y-%m-%d") + datetime.timedelta(
			weeks=-4)).strftime("%Y-%m-%d"))
		move_controls.append((datetime.datetime.strptime(current_date,
		                                                 "%Y-%m-%d") + datetime.timedelta(
			weeks=-1)).strftime("%Y-%m-%d"))
		move_controls.append((datetime.datetime.strptime(current_date,
		                                                 "%Y-%m-%d") + datetime.timedelta(
			weeks=1)).strftime("%Y-%m-%d"))
		move_controls.append((datetime.datetime.strptime(current_date,
		                                                 "%Y-%m-%d") + datetime.timedelta(
			weeks=4)).strftime("%Y-%m-%d"))

		colores = {'A': 'rgba(0,153,0,0.7)',
		           'P': 'rgba(51,51,204,0.7)'}
		reservations = Reservation.objects.filter(space=space,
			starting_date_time__week=current_week, state__in=['P', 'A'])
		res_list = []
		for i in range(5):
			res_list.append(list())
		for r in reservations:
			try:
				print(r)
				reserv = []
				reserv.append(r.space.name)
				reserv.append(localtime(r.starting_date_time).strftime("%H:%M"))
				reserv.append(localtime(r.ending_date_time).strftime("%H:%M"))
				reserv.append(colores[r.state])
				res_list[r.starting_date_time.isocalendar()[2] - 1].append(reserv)

			except:
				pass

		context = {
			'space': space,
			'actual_monday': monday,
			'controls': move_controls,
			'reservations': res_list,
		}

		return render(request, 'space_data.html', context)
	except Exception as e:
		return redirect('/')


def verificar_horario_habil(init, end, space_id):
	if init.hour < 9 or end.hour > 18:
		return False
	if Reservation.objects.filter(starting_date_time__lte=init,
	                              ending_date_time__gte=init, space=space_id)\
			.exclude(state='R'):
		return False

	if Reservation.objects.filter(starting_date_time__gte=init,
	                                  ending_date_time__lte=end, space=space_id)\
			.exclude(state='R'):
		return False

	if init.weekday() > 4: # fin de semana
		return False

	return True


def space_request(request, space_id):
	if request.method == 'POST' and 'picked-date' in request.POST:
		space = Space.objects.get(id=space_id)

		if request.user.enabled:
			try:
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
			messages.warning(request,
			                 'Usuario no habilitado para pedir préstamos')


@login_required
def space_data_admin(request, space_id):
	if not request.user.is_staff:
		return redirect('/')
	else:
		try:
			space = Space.objects.get(id=space_id)
			context = {
				'space': space
			}
			return render(request, 'space_data_admin.html', context)
		except:
			return redirect('/')

@login_required
def space_data_admin_create(request):
    if not request.user.is_staff:
        return redirect('/')

    if request.method == "GET":
        context = {"states" : Space.STATES}
        return render(request, 'space_data_admin_create.html', context)
    if request.method == "POST":
        form = SpaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/admin/items-panel')
        else:
            context = {"states" : Space.STATES, "error": "Datos no validos, porfavor intente otra vez"}
            return redirect('/admin/items-panel')

@login_required
def space_edit_name(request, space_id):
	if request.method == "POST":
		a = Space.objects.get(id=space_id)
		a.name = request.POST["name"]
		a.save()
	return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_image(request, space_id):
	if request.method == "POST":
		u_file = request.FILES["image"]
		extension = os.path.splitext(u_file.name)[1]
		a = Space.objects.get(id=space_id)
		a.image.save(str(space_id) + "_image" + extension, u_file)
		a.save()

	return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_description(request, space_id):
	if request.method == "POST":
		a = Space.objects.get(id=space_id)
		a.description = request.POST["description"]
		a.save()

	return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_state(request, space_id):
	if request.method == "POST" \
			and request.POST["state"] in ['D', 'P', 'R', 'L']:
		a = Space.objects.get(id=space_id)
		a.state = request.POST["state"]
		a.save()

	return redirect('/space/' + str(space_id) + '/edit')


@login_required
def space_edit_capacity(request, space_id):
	if request.method == "POST":
		a = Space.objects.get(id=space_id)
		a.capacity = request.POST["capacidad"]
		a.save()

	return redirect('/space/' + str(space_id) + '/edit')
