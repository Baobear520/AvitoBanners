
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from banners.models import Banner
from banners.serializers import BannerSerializer
# Create your views here.

@csrf_exempt
def banner_list(request):
    """
    List all banners, or create a new banner.
    """
    if request.method == 'GET':
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BannerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def banner_detail(request, pk):
    """
    Retrieve, update or delete a banner.
    """
    try:
        snippet = Banner.objects.get(pk=pk)
    except Banner.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BannerSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BannerSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)