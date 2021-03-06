import sys
from django.shortcuts import render, redirect, render_to_response, RequestContext, Http404
from django.http import HttpResponse
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.contrib import messages
from django.template import RequestContext
from rept.models import Order, PrintSheet, Operation, Detal
from rept.forms import NewOrderForm


TTY = '/dev/tty1'
sys.stdout = open(TTY, 'w')
sys.stderr = open(TTY, 'w')
#sys.stdout.write('filename'+'\n')

# Create your views here.

def login_redirect(request):
    messages.add_message(request, messages.INFO, 'Вы должны быть зарегистрированны для выполнения этой операции.')
    return redirect('grid')


def about(request):
    return render_to_response('about.html')


def login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        print('username', username)
        print('pass', password)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                messages.add_message(request, messages.INFO, 'You are sucessfully login!')
            else:
                #context['error'] = 'Non active user'
                messages.add_message(request, messages.INFO, 'Non active user')
        else:
            messages.add_message(request, messages.INFO, 'Wrong username or password')
    return redirect('grid')
    #return render_to_response('grid.html', ???)


def logout(request):
    django_logout(request)
    return redirect('/')


def create_new_order(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            pass  # Обрабатываем данные, производим запись в базу
    else:
        # Показываем пустую форму
        form = NewOrderForm()
    return render_to_response('new_order.html', {'form': form}, context)


def grid(request):
    context_instance = RequestContext(request)
    table = Order.objects.all()
    return render_to_response('grid.html', {'table': table}, context_instance)


def print_order(request, orderid):
    context = RequestContext(request)
    try:
        order = Order.objects.get(pk=orderid)
    except order.DoesNotExist:
        raise Http404

    return render_to_response('order_print.html', {'order': order})


def print_pdf(request, orderid):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, bottomup=1, pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    #p.translate(mm, mm)
    p.drawString(100*mm, 100*mm, "Hello world.")

    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    
    p.drawString(30,750,'OFFICIAL COMMUNIQUE')
    p.drawString(30,735,'OF ACME INDUSTRIES')
    p.drawString(500,750,"12/12/2010")
    p.line(480,747,580,747)
    
    p.drawString(275,725,'AMOUNT OWED:')
    p.drawString(500,725,"$1,000.00")
    p.line(378,723,580,723)
    
    p.drawString(30,703,'RECEIVED BY:')
    p.line(120,700,580,700)
    p.drawString(120,703,"JOHN DOE")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


def copy_order(request, orderid):
    from django.db.models import Max
    from copy import deepcopy

    try:
        order = Order.objects.get(pk=orderid)
    except order.DoesNotExist:
        raise Http404

    # Дублируем новый объект ЗАКАЗ
    new_order = deepcopy(order)
    new_order.id = None
    last_number = Order.objects.all().aggregate(Max('order'))['order__max']
    new_order.order = int(last_number) + 1
    new_order.save()

    # Итерация по печатным листам, каждый дублируем
    printsheets = PrintSheet.objects.filter(order_id=order.id)
    for printsheet in printsheets:
        new_printsheet = deepcopy(printsheet)
        new_printsheet.id = None
        new_printsheet.order_id = new_order.id
        new_printsheet.save()

        # Итерация по технологическим операциям, которые ИМЕЮТ ВЛАДЕЛЬЦА-ПЕЧАТНЫЙ ЛИСТ, каждую дублируем
        operations = Operation.objects.filter(order_id=order.id).filter(printsheet_id=printsheet.id)
        for operation in operations:
            new_operation = deepcopy(operation)
            new_operation.id = None
            new_operation.printsheet_id = new_printsheet.id
            new_operation.order_id = new_order.id
            new_operation.save()

        # Далее итерация по Деталям, они все имеют предка-владельца Печатный лист
        detals = Detal.objects.filter(printsheet_id=printsheet.id)
        for detal in detals:
            new_detal = deepcopy(detal)
            new_detal.id = None
            new_detal.printsheet_id = new_printsheet.id
            new_detal.save()

    # Итерация по технологическим операциям, которые НЕ ИМЕЮТ ПРЕДКА-ПЕЧАТНОГО ЛИСТА, каждую дублируем
    operations = Operation.objects.filter(order_id=order.id).filter(printsheet_id=None)
    for operation in operations:
        new_operation = deepcopy(operation)
        new_operation.id = None
        new_operation.order_id = new_order.id
        new_operation.save()

    return redirect('/')


