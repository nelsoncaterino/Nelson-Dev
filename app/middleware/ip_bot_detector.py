import socket
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from app.models import IPVisit
import logging

logger = logging.getLogger(__name__)

class IPBotDetectorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.known_bot_ips = set()
        self.ip_cache = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        is_bot = self.is_bot(ip, user_agent)

        # Log + Enregistrement DB
        IPVisit.objects.create(
            ip_address=ip,
            path=request.path,
            user_agent=user_agent,
            is_bot=is_bot
        )

        if is_bot:
            self.known_bot_ips.add(ip)
            self.send_alert_email(ip, request)
            return HttpResponseForbidden("Accès refusé")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def is_bot(self, ip, user_agent):
        if ip in self.known_bot_ips:
            return True
        if ip in self.ip_cache:
            return self.ip_cache[ip]

        ua = user_agent.lower()
        bot_keywords = [
            'bot', 'crawler', 'spider', 'slurp',
            'baiduspider', 'yandex', 'ahrefs', 'mj12', 'semrush'
        ]
        if any(bot in ua for bot in bot_keywords):
            self.ip_cache[ip] = True
            return True

        try:
            hostname = socket.gethostbyaddr(ip)[0]
            bot_domains = ['googlebot.com', 'crawl.baidu.com', 'yandex.com']
            if any(domain in hostname for domain in bot_domains):
                self.ip_cache[ip] = True
                return True
        except Exception:
            pass

        self.ip_cache[ip] = False
        return False

    def send_alert_email(self, ip, request):
        subject = f"Bot détecté - IP {ip}"
        message = (
            f"Un robot a été détecté :\n\n"
            f"- IP: {ip}\n"
            f"- Heure: {datetime.now()}\n"
            f"- Path: {request.path}\n"
            f"- User-Agent: {request.META.get('HTTP_USER_AGENT', 'Inconnu')}"
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True
        )
