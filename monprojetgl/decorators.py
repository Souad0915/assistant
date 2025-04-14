from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def ajax_csrf_exempt(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return csrf_exempt(view_func)(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return wrapper