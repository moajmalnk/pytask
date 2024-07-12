import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer


@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                cache.delete('all_users')  # Invalidate cache
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def read_users(request):
    if request.method == "GET":
        users = cache.get("all_users")
        if not users:
            users_queryset = User.objects.all()
            users = UserSerializer(users_queryset, many=True).data
            cache.set("all_users", users, timeout=3600)  # Cache for 1 hour
        return JsonResponse({"users": users})
    return HttpResponseBadRequest({"error": "Invalid request method"}, status=400)
