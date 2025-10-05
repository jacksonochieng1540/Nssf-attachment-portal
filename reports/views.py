# reports/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from attachments.models import Attachment, Company, StudentProfile
from nssf.models import NSSFReturn

@login_required
def generate_report(request):
    if request.user.role != 'admin':
        return render(request, 'errors/403.html', status=403)
    
    context = {
        'report_types': [
            {'value': 'students', 'label': 'Students Report'},
            {'value': 'companies', 'label': 'Companies Report'},
            {'value': 'attachments', 'label': 'Attachments Report'},
            {'value': 'nssf_returns', 'label': 'NSSF Returns Report'},
        ]
    }
    
    return render(request, 'reports/generate_report.html', context)

@login_required
def download_report(request, report_type):
    if request.user.role != 'admin':
        return render(request, 'errors/403.html', status=403)
    
    # Get report parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    
    # Generate report based on type
    if report_type == 'students':
        students = StudentProfile.objects.all()
        context = {'students': students, 'report_type': 'Students'}
        html_string = render_to_string('reports/students_report.html', context)
        
    elif report_type == 'companies':
        companies = Company.objects.all()
        context = {'companies': companies, 'report_type': 'Companies'}
        html_string = render_to_string('reports/companies_report.html', context)
        
    elif report_type == 'attachments':
        attachments = Attachment.objects.all()
        if start_date and end_date:
            attachments = attachments.filter(start_date__gte=start_date, end_date__lte=end_date)
        if status:
            attachments = attachments.filter(status=status)
        
        context = {'attachments': attachments, 'report_type': 'Attachments'}
        html_string = render_to_string('reports/attachments_report.html', context)
        
    elif report_type == 'nssf_returns':
        returns = NSSFReturn.objects.all()
        if start_date and end_date:
            returns = returns.filter(month__gte=start_date, month__lte=end_date)
        
        context = {'returns': returns, 'report_type': 'NSSF Returns'}
        html_string = render_to_string('reports/nssf_returns_report.html', context)
        
    else:
        return HttpResponse("Invalid report type", status=400)
    
    # Generate PDF
    html = HTML(string=html_string)
    result = html.write_pdf()
    
    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.pdf"'
    response.write(result)
    
    return response