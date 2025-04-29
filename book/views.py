from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView

from main.models import BookOffer
from user.models import Favorite


# Create your views here.
@require_http_methods(['POST'])
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {'status': 'error', 'message': 'Требуется вход в систему'},
            status=403
        )

    offer_id = request.POST.get('offer_id')
    try:
        offer = BookOffer.objects.get(id=offer_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, offer=offer)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
        return JsonResponse({'status': 'success', 'is_favorite': is_favorite})
    except BookOffer.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Книга не найдена'}, status=404)


class ShowBookAnnouncement(DetailView):
    template_name = 'book/advertisement.html'
    model = BookOffer
    context_object_name = 'offer'

    def get_object(self, **kwargs):
        return get_object_or_404(BookOffer, uuid_post=self.kwargs['uuid_post'], is_published=True)
