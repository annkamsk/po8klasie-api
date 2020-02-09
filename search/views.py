from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.contrib.postgres.search import TrigramSimilarity

from search.serializers import *


def index(request):
    return HttpResponse("Hello")


@api_view(['GET'])
def public_school_list(request):
    if request.method == 'GET':
        public_schools = PublicSchool.objects.all()
        serializer = PublicSchoolSerializer(public_schools, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def high_school_list_by_name(request):
    if request.method == 'GET' and request.GET.get('name') is not None:
        name = request.GET.get('name')
        public_schools = PublicSchool.objects \
            .filter(school_type='liceum ogólnokształcące') \
            .annotate(similarity=TrigramSimilarity('school_name', name)) \
            .filter(similarity__gte=0.06) \
            .order_by('-similarity')
        private_schools = PrivateSchool.objects \
            .filter(school_type='liceum ogólnokształcące') \
            .annotate(similarity=TrigramSimilarity('school_name', name)) \
            .filter(similarity__gte=0.06) \
            .order_by('-similarity')
        serializer_public = PublicSchoolSerializer(public_schools, many=True)
        serializer_private = PrivateSchoolSerializer(private_schools, many=True)
        return JsonResponse(serializer_public.data + serializer_private.data, safe=False)
