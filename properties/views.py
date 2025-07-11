from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties 

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": str(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat(),
        }
        for p in properties
    ]
    return JsonResponse(data, safe=False)