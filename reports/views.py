import pandas as pd
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.dateparse import parse_date
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from sales.models import Position, Sale
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
from sales.models import CSV
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ReportListView(LoginRequiredMixin,ListView):
    model=Report
    template_name="reports/main.html"


class ReportDetailView(LoginRequiredMixin,DetailView):
    model=Report
    template_name="reports/detail.html"

class UploadReportView(TemplateView):
    template_name = "reports/from_file.html"


@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        image = request.POST.get("image")

        current_user = auth.get_user(request)
        image = get_report_image(image)
        author = Profile.objects.get(user = current_user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = image
            instance.author = author
            instance.save()

        return JsonResponse({"msg":"success"})
    return JsonResponse({})

@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if Download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if Display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_files_name = request.FILES.get('file').name
        csv_files = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name = csv_files_name)

        if created:
            obj.csv_file = csv_files
            obj.save()
            csv_df = pd.read_csv(obj.csv_file.path)
            current_user = auth.get_user(request)
            for index, row in  csv_df.iterrows():
                data = list(row)

                transaction_id = data[1]
                product = data[2]
                quantity = int(data[3])
                customer = data[4]
                date = datetime.datetime.strptime(data[5], "%d-%m-%Y").date()
                
                print(date)

                try:
                    product_obj = Product.objects.get(name__iexact = product)
                except:
                    product_obj = None
                
                if product_obj is not None:
                    customer_obj, _ = Customer.objects.get_or_create(name=customer)
                    salesman_obj = Profile.objects.get(user=current_user)
                    position_obj= Position.objects.create(product=product_obj, quantity=quantity, created=date)
                    print(position_obj)
                    sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, salesman=salesman_obj, customer=customer_obj, created=date)
                    sale_obj.position.add(position_obj)
                    sale_obj.save()
            return JsonResponse({"ex":False})

        print(obj.csv_file.path)
    return JsonResponse({"ex":True})