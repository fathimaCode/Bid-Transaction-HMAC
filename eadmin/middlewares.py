from .models import particpants

class ParticipantInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        participant_info = None
        if user_id:
            try:
                # Retrieve participant info based on user_id
                participant_info = particpants.objects.get(pk=user_id)
            except particpants.DoesNotExist:
                # Handle the case where the participant does not exist
                pass
        # Add participant_info to the request object
        request.participant_info = participant_info
        response = self.get_response(request)
        return response
