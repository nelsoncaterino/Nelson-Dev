from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now
from app.models import IPVisit
from app.utils import get_geo_info, parse_user_agent

@receiver(post_save, sender=IPVisit)
def update_duration(sender, instance, created, **kwargs):
    if not created or not instance.session_id:
        return
    # Calcule la durée de session (simplifié)
    visits = IPVisit.objects.filter(session_id=instance.session_id).order_by('timestamp')
    if visits.count() > 1:
        duration = (visits.last().timestamp - visits.first().timestamp).total_seconds()
        IPVisit.objects.filter(session_id=instance.session_id).update(duration_seconds=int(duration))

# Exemple fonction pour créer IPVisit depuis une vue ou un middleware
def track_visit(request):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    path = request.path
    session_id = request.session.session_key or None
    user = request.user if request.user.is_authenticated else None

    geo_info = get_geo_info(ip)
    ua_info = parse_user_agent(user_agent)

    visit = IPVisit.objects.create(
        ip_address=ip,
        path=path,
        user_agent=user_agent,
        country=geo_info['country'],
        city=geo_info['city'],
        isp=geo_info['isp'],
        os_type=ua_info['os_type'],
        browser=ua_info['browser'],
        device_type=ua_info['device_type'],
        session_id=session_id,
        user=user
    )
    return visit

def get_client_ip(request):
    # Essaye de récupérer IP client (X-Forwarded-For si derrière proxy)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
