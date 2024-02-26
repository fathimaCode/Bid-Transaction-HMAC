from .models import particpants
class userMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        userList = None
        getUsers = particpants.objects.all()
        request.userList = getUsers
        response = self.get_response(request)
        return response