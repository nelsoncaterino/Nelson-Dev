# app/middleware.py
from app.signals import track_visit

class TrackIPVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Appelle après la réponse (ou avant selon besoin)
        track_visit(request)
        return response
