from django.shortcuts import redirect
from .models import Loan
from django.contrib import messages


def lost_article(request):
    if request.method == 'POST':
        loan_ids = request.POST.getlist('loan')
        try:
            for loan_id in loan_ids:
                loan = Loan.objects.get(id=loan_id)
                article = loan.article
                article.state = 'L'
                article.save()
                msg = 'El artículo se ha reportado perdido. Los administradores se pondrán en contacto con usted.'
                messages.warning(request, msg)
        except Exception as e:
            print("Error:", e)
            messages.warning(request, 'Ha ocurrido un error y el artículo no se ha reportado perdido')

        return redirect('/user/user_data')