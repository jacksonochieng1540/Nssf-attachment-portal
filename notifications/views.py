# notifications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm

# notifications/views.py (update notification_list view)
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    
    # Check if empty
    if not notifications.exists():
        return render(request, 'notifications/empty.html')
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Mark all as read if requested
    if request.GET.get('mark_all_read'):
        notifications.update(is_read=True)
        return redirect('notifications:list')
    
    return render(request, 'notifications/list.html', {
        'page_obj': page_obj,
        'unread_count': notifications.filter(is_read=False).count(),
    })
    
@login_required
def notification_detail(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    
    # Mark as read when viewing
    if not notification.is_read:
        notification.mark_as_read()
    
    return render(request, 'notifications/detail.html', {
        'notification': notification
    })

@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notifications:list')

@login_required
def notification_preferences(request):
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification preferences updated successfully!')
            return redirect('notifications:preferences')
    else:
        form = NotificationPreferenceForm(instance=preference)
    
    return render(request, 'notifications/preferences.html', {
        'form': form
    })

@login_required
def get_unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})