from .models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')[:5]
    else:
        notifications = []
    return {'notifications': notifications}