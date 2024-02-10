from .models import Blockchain
class BlockchainMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tender_id = request.GET.get('tender_id', None)  # Assuming the tenderid is passed via GET parameter
        block_list = None
        if tender_id:
            block_list = Blockchain.objects.filter(tenderid=tender_id)
            request.block_list = block_list
        else:
            request.block_list = None
        response = self.get_response(request)
        return response
