from django.conf import settings


def demo_mode(request):
    """Expose DEMO_MODE to all templates."""
    return {'DEMO_MODE': getattr(settings, 'DEMO_MODE', False)}
