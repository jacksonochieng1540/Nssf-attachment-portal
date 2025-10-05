from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Attachment, Company, StudentProfile
from .forms import AttachmentForm, CompanyRegistrationForm, StudentProfileForm, AdminCompanyForm
from nssf.models import NSSFDetail, NSSFReturn


@login_required
def dashboard(request):
    context = {}
    
    if request.user.role == 'student':
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            attachments = Attachment.objects.filter(student=student_profile)
            nssf_details = NSSFDetail.objects.filter(student=student_profile).first()
            
            context.update({
                'student_profile': student_profile,
                'attachments': attachments,
                'nssf_details': nssf_details,
                'pending_attachments': attachments.filter(status='pending').count(),
                'approved_attachments': attachments.filter(status='approved').count(),
                'rejected_attachments': attachments.filter(status='rejected').count(),
                'completed_attachments': attachments.filter(status='completed').count(),
            })
        except StudentProfile.DoesNotExist:
            messages.warning(request, 'Please complete your student profile to access all features.')
            
    elif request.user.role == 'company':
        try:
            company = Company.objects.get(user=request.user)
            attachments = Attachment.objects.filter(company=company)
            nssf_returns = NSSFReturn.objects.filter(company=company)
            
            context.update({
                'company': company,
                'attachments': attachments,
                'nssf_returns': nssf_returns,
                'pending_attachments': attachments.filter(status='pending').count(),
                'approved_attachments': attachments.filter(status='approved').count(),
                'rejected_attachments': attachments.filter(status='rejected').count(),
                'completed_attachments': attachments.filter(status='completed').count(),
            })
        except Company.DoesNotExist:
            messages.warning(request, 'Please complete your company profile to access all features.')
            
    elif request.user.role == 'admin':
        students = StudentProfile.objects.count()
        companies = Company.objects.count()
        attachments = Attachment.objects.count()
        pending_attachments = Attachment.objects.filter(status='pending').count()
        approved_attachments = Attachment.objects.filter(status='approved').count()
        nssf_returns = NSSFReturn.objects.count()
        processed_returns = NSSFReturn.objects.filter(is_processed=True).count()
        

        recent_attachments = Attachment.objects.all().order_by('-id')[:5]
        recent_returns = NSSFReturn.objects.all().order_by('-submitted_on')[:5]
        
        context.update({
            'students_count': students,
            'companies_count': companies,
            'attachments_count': attachments,
            'pending_attachments_count': pending_attachments,
            'approved_attachments_count': approved_attachments,
            'nssf_returns_count': nssf_returns,
            'processed_returns_count': processed_returns,
            'recent_attachments': recent_attachments,
            'recent_returns': recent_returns,
        })
    
    return render(request, 'attachments/dashboard.html', context)

@login_required
def attachment_list(request):
    try:
        if request.user.role == 'student':
            # Handle missing student profile gracefully
            try:
                student_profile = StudentProfile.objects.get(user=request.user)
                attachments = Attachment.objects.filter(student=student_profile)
            except StudentProfile.DoesNotExist:
                messages.error(request, 'Student profile not found. Please complete your student profile first.')
                return redirect('create_student_profile')
                
        elif request.user.role == 'company':
            # Handle missing company profile gracefully
            try:
                company = Company.objects.get(user=request.user)
                attachments = Attachment.objects.filter(company=company)
            except Company.DoesNotExist:
                messages.error(request, 'Company profile not found. Please complete your company profile.')
                return redirect('company_register')
                
        else:  
            attachments = Attachment.objects.all()
        
        # Filter by status if provided
        status_filter = request.GET.get('status')
        if status_filter:
            attachments = attachments.filter(status=status_filter)
        
        # Search functionality
        search_query = request.GET.get('q')
        if search_query:
            if request.user.role == 'student':
                attachments = attachments.filter(
                    Q(company__name__icontains=search_query) |
                    Q(supervisor_name__icontains=search_query)
                )
            elif request.user.role == 'company':
                attachments = attachments.filter(
                    Q(student__user__username__icontains=search_query) |
                    Q(student__student_id__icontains=search_query) |
                    Q(supervisor_name__icontains=search_query)
                )
            else:  
                attachments = attachments.filter(
                    Q(student__user__username__icontains=search_query) |
                    Q(student__student_id__icontains=search_query) |
                    Q(company__name__icontains=search_query) |
                    Q(supervisor_name__icontains=search_query)
                )
        
        return render(request, 'attachments/attachment_list.html', {
            'attachments': attachments,
            'status_filter': status_filter,
            'search_query': search_query or ''
        })
    
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('dashboard')

@login_required
def attachment_create(request):
    if request.user.role not in ['student', 'admin']:
        messages.error(request, 'Only students and administrators can create attachments.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AttachmentForm(request.user, request.POST)
        if form.is_valid():
            attachment = form.save(commit=False)
            
            # Set student if user is a student
            if request.user.role == 'student':
                try:
                    student_profile = StudentProfile.objects.get(user=request.user)
                    attachment.student = student_profile
                except StudentProfile.DoesNotExist:
                    messages.error(request, 'Student profile not found. Please complete your student profile first.')
                    return redirect('create_student_profile')
            
            attachment.save()
            messages.success(request, 'Attachment created successfully!')
            return redirect('attachment_list')
    else:
        form = AttachmentForm(request.user)
    
    return render(request, 'attachments/attachment_form.html', {
        'form': form, 
        'title': 'Create Attachment'
    })

@login_required
def attachment_detail(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk)
    
    # Check permissions
    if request.user.role == 'student' and attachment.student.user != request.user:
        messages.error(request, 'You do not have permission to view this attachment.')
        return redirect('attachment_list')
    elif request.user.role == 'company' and attachment.company.user != request.user:
        messages.error(request, 'You do not have permission to view this attachment.')
        return redirect('attachment_list')
    
    return render(request, 'attachments/attachment_detail.html', {'attachment': attachment})

@login_required
def attachment_update(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk)
    
    # Check permissions
    if request.user.role == 'student' and attachment.student.user != request.user:
        messages.error(request, 'You do not have permission to update this attachment.')
        return redirect('attachment_list')
    elif request.user.role == 'company' and attachment.company.user != request.user:
        messages.error(request, 'You do not have permission to update this attachment.')
        return redirect('attachment_list')
    elif request.user.role == 'admin':
        # Admin can update any attachment
        pass
    
    if request.method == 'POST':
        form = AttachmentForm(request.user, request.POST, instance=attachment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attachment updated successfully!')
            return redirect('attachment_detail', pk=attachment.pk)
    else:
        form = AttachmentForm(request.user, instance=attachment)
    
    return render(request, 'attachments/attachment_form.html', {
        'form': form, 
        'title': 'Update Attachment',
        'attachment': attachment
    })

@login_required
def attachment_delete(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk)
    
    # Check permissions
    if request.user.role == 'student' and attachment.student.user != request.user:
        messages.error(request, 'You do not have permission to delete this attachment.')
        return redirect('attachment_list')
    elif request.user.role == 'company' and attachment.company.user != request.user:
        messages.error(request, 'You do not have permission to delete this attachment.')
        return redirect('attachment_list')
    elif request.user.role == 'admin':
        # Admin can delete any attachment
        pass
    
    if request.method == 'POST':
        attachment.delete()
        messages.success(request, 'Attachment deleted successfully!')
        return redirect('attachment_list')
    
    return render(request, 'attachments/attachment_confirm_delete.html', {'attachment': attachment})

@login_required
def attachment_approve(request, pk):
    if request.user.role not in ['company', 'admin']:
        messages.error(request, 'Only companies and administrators can approve attachments.')
        return redirect('dashboard')
    
    attachment = get_object_or_404(Attachment, pk=pk)
    
    # Check if company owns this attachment
    if request.user.role == 'company' and attachment.company.user != request.user:
        messages.error(request, 'You can only approve attachments for your company.')
        return redirect('attachment_list')
    
    attachment.status = 'approved'
    attachment.save()
    messages.success(request, 'Attachment approved successfully!')
    return redirect('attachment_list')

@login_required
def attachment_reject(request, pk):
    if request.user.role not in ['company', 'admin']:
        messages.error(request, 'Only companies and administrators can reject attachments.')
        return redirect('dashboard')
    
    attachment = get_object_or_404(Attachment, pk=pk)
    
    # Check if company owns this attachment
    if request.user.role == 'company' and attachment.company.user != request.user:
        messages.error(request, 'You can only reject attachments for your company.')
        return redirect('attachment_list')
    
    attachment.status = 'rejected'
    attachment.save()
    messages.success(request, 'Attachment rejected.')
    return redirect('attachment_list')

@login_required
def company_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can view companies.')
        return redirect('dashboard')
    
    companies = Company.objects.all()
    return render(request, 'attachments/company_list.html', {'companies': companies})

@login_required
def company_create(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can create companies.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminCompanyForm(request.POST)
        if form.isvalid():
            company = form.save()
            messages.success(request, f'Company "{company.name}" created successfully!')
            return redirect('company_list')
    else:
        form = AdminCompanyForm()
    
    return render(request, 'attachments/company_form.html', {
        'form': form,
        'title': 'Create Company'
    })

@login_required
def company_register(request):
    """View for users to register their own company"""
    if request.user.role != 'company':
        messages.error(request, 'Only company users can register companies.')
        return redirect('dashboard')
    
    # Check if user already has a company
    if hasattr(request.user, 'company'):
        messages.warning(request, 'You already have a company profile.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, f'Company "{company.name}" registered successfully!')
            return redirect('dashboard')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'attachments/company_form.html', {
        'form': form,
        'title': 'Register Your Company'
    })
    
@login_required
def company_update(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can update companies.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        form = AdminCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f'Company "{company.name}" updated successfully!')
            return redirect('company_list')
    else:
        form = AdminCompanyForm(instance=company)
    
    return render(request, 'attachments/company_form.html', {
        'form': form,
        'title': f'Update {company.name}',
        'company': company
    })

@login_required
def company_delete(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can delete companies.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Company "{company_name}" deleted successfully!')
        return redirect('company_list')
    
    return render(request, 'attachments/company_confirm_delete.html', {'company': company})

@login_required
def student_list(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can view students.')
        return redirect('dashboard')
    
    students = StudentProfile.objects.all()
    return render(request, 'attachments/student_list.html', {'students': students})

@login_required
def student_profile_create(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can create student profiles.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            student_profile = form.save()
            messages.success(request, f'Student profile for "{student_profile.user.username}" created successfully!')
            return redirect('student_list')
    else:
        form = StudentProfileForm()
    
    return render(request, 'attachments/student_profile_form.html', {
        'form': form,
        'title': 'Create Student Profile'
    })

@login_required
def student_profile_update(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can update student profiles.')
        return redirect('dashboard')
    
    student_profile = get_object_or_404(StudentProfile, pk=pk)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student profile for "{student_profile.user.username}" updated successfully!')
            return redirect('student_list')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    return render(request, 'attachments/student_profile_form.html', {
        'form': form,
        'title': f'Update {student_profile.user.username} Profile',
        'student_profile': student_profile
    })

@login_required
def student_profile_delete(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can delete student profiles.')
        return redirect('dashboard')
    
    student_profile = get_object_or_404(StudentProfile, pk=pk)
    
    if request.method == 'POST':
        username = student_profile.user.username
        student_profile.delete()
        messages.success(request, f'Student profile for "{username}" deleted successfully!')
        return redirect('student_list')
    
    return render(request, 'attachments/student_profile_confirm_delete.html', {'student_profile': student_profile})

@login_required
def attachment_stats(request):
    if request.user.role != 'admin':
        messages.error(request, 'Only administrators can view attachment statistics.')
        return redirect('dashboard')
    
    # Get statistics
    status_counts = Attachment.objects.values('status').annotate(count=Count('status'))
    monthly_counts = Attachment.objects.extra(
        select={'month': "strftime('%%Y-%%m', start_date)"}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Get company-wise statistics
    company_stats = Company.objects.annotate(
        attachment_count=Count('attachment'),
        pending_count=Count('attachment', filter=Q(attachment__status='pending')),
        approved_count=Count('attachment', filter=Q(attachment__status='approved')),
        completed_count=Count('attachment', filter=Q(attachment__status='completed'))
    )
    
    return render(request, 'attachments/attachment_stats.html', {
        'status_counts': status_counts,
        'monthly_counts': monthly_counts,
        'company_stats': company_stats
    })
    
@login_required
def create_student_profile(request):
    # Check if profile already exists
    if StudentProfile.objects.filter(user=request.user).exists():
        messages.info(request, 'You already have a student profile.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Student profile created successfully!')
            return redirect('attachment_list')  # Redirect to attachments list
    else:
        form = StudentProfileForm()
    
    return render(request, 'attachments/create_student_profile.html', {'form': form})