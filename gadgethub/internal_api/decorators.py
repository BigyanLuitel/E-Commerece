from functools import wraps
from django.conf import settings
from django.http import JsonResponse


def require_internal_key(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        provided = request.headers.get('X-Internal-Key')
        if not provided or provided != settings.INTERNAL_API_KEY:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper