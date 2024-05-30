from functools import wraps
from .models import User
from django.http import JsonResponse
def managers_only(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user = User.objects.only("is_manager").filter(id=request.user.id).first()
        if not (user and user.is_manager):
            return JsonResponse({'error': 'Forbidden'}, status=403)
        return func(self, request, *args, **kwargs)
    return wrapper
