from django.urls import path
from .views import create_report_view, ReportListView, ReportDetailView,UploadReportView, render_pdf_view, csv_upload_view

app_name = 'reports'

urlpatterns = [
    path('', ReportListView.as_view(), name = 'main'),
    path('save/', create_report_view, name = 'create-report'),
    path('from_file/', UploadReportView.as_view(), name = 'from-file'),
    path('upload/',csv_upload_view, name = 'upload'),
    path('<pk>/', ReportDetailView.as_view(), name = 'detail'),
    path('<pk>/pdf/', render_pdf_view, name = 'pdf'),
]