from django.shortcuts import render, redirect
from .models import Reservation
from django.contrib import messages


def delete(request):
    if request.method == 'POST':
        reservation_ids = request.POST.getlist('reservation')
        try:
            for reservation_id in reservation_ids:
                reservation = Reservation.objects.get(id=reservation_id)
                if reservation.state == 'P':
                    reservation.delete()
        except:
            messages.warning(request, 'Ha ocurrido un error y la reserva no se ha eliminado')

        return redirect('http://127.0.0.1:8000/user/user_data', u_id=request.user.id)


def reserve_sheet(request):
    return redirect('/')