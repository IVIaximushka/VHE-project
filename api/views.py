from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def start_view(request):
    return JsonResponse({'status': 'ok'})
