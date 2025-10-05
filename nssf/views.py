from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from attachments.models import StudentProfile, Company
from .models import NSSFDetail, NSSFReturn
from nssf.forms import NSSFDetailForm, NSSFReturnForm

@login_required
def nssf_detail(request):
    try:
        if request.user.role != 'student':
            messages.error(request, 'Only students can access NSSF details.')
            return redirect('dashboard')
        
        # Try to get the student profile, but handle DoesNotExist gracefully
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Student profile not found. Please complete your student profile first.')
            return redirect('create_student_profile')  # This should point to the attachments app URL
        
        nssf_detail_instance, created = NSSFDetail.objects.get_or_create(student=student_profile)
        
        if request.method == 'POST':
            form = NSSFDetailForm(request.POST, request.FILES, instance=nssf_detail_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'NSSF details updated successfully!')
                return redirect('profile')  # Make sure this URL exists
        else:
            form = NSSFDetailForm(instance=nssf_detail_instance)
        
        return render(request, 'nssf/nssf_detail.html', {'form': form})
    
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('dashboard')
    
    
# nssf/views.py
@login_required
def nssf_detail_update(request):
    try:
        if request.user.role != 'student':
            messages.error(request, 'Only students can update NSSF details.')
            return redirect('dashboard')
        
        # Get the student profile
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Student profile not found. Please complete your student profile first.')
            return redirect('create_student_profile')
        
        # Get or create NSSF detail instance
        nssf_detail_instance, created = NSSFDetail.objects.get_or_create(student=student_profile)
        
        if request.method == 'POST':
            form = NSSFDetailForm(request.POST, request.FILES, instance=nssf_detail_instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'NSSF details updated successfully!')
                return redirect('nssf_detail')
        else:
            form = NSSFDetailForm(instance=nssf_detail_instance)
        
        return render(request, 'nssf/nssf_detail_form.html', {'form': form})
    
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('dashboard')
    
    
    
@login_required
def nssf_return_list(request):
    if request.user.role != 'company':
        messages.error(request, 'Only companies can access NSSF returns.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, user=request.user)
    returns = NSSFReturn.objects.filter(company=company).order_by('-month')
    
    return render(request, 'nssf/nssf_returns.html', {'returns': returns})

@login_required
def nssf_return_create(request):
    if request.user.role != 'company':
        messages.error(request, 'Only companies can submit NSSF returns.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, user=request.user)
    
    if request.method == 'POST':
        form = NSSFReturnForm(request.POST, request.FILES)
        if form.is_valid():
            return_instance = form.save(commit=False)
            return_instance.company = company
            return_instance.save()
            messages.success(request, 'NSSF return submitted successfully!')
            return redirect('nssf_return_list')
    else:
        form = NSSFReturnForm()
    
    return render(request, 'nssf/nssf_return_form.html', {'form': form})

@login_required
def nssf_return_detail(request, pk):
    if request.user.role != 'company':
        messages.error(request, 'Only companies can view NSSF return details.')
        return redirect('dashboard')
    
    company = get_object_or_404(Company, user=request.user)
    return_instance = get_object_or_404(NSSFReturn, pk=pk, company=company)
    
    return render(request, 'nssf/nssf_return_detail.html', {'return_instance': return_instance})