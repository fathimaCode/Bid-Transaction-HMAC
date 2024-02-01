from .models import tender
class TenderListMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenderList = None
        getTender = tender.objects.all()
        request.tenderList = getTender
        response = self.get_response(request)
        return response