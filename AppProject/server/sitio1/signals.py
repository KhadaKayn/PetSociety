# sitio1/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name == 'sitio1':
        # Verificar si ya existe un superusuario
        if not User.objects.filter(is_superuser=True).exists():
            # Crear un superusuario si no existe
            User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')