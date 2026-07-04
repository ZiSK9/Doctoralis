"""
Demo mode: lets portfolio visitors browse every space without credentials.

When DEMO_MODE is on and no user is authenticated, this middleware silently
logs in a representative demo user based on which space is being visited, so
that @login_required views and views relying on request.user keep working —
while the backend (real data, charts, workflows) stays fully dynamic.
"""
from django.conf import settings
from django.contrib.auth import login

# Doctorant pages that need request.user to be a doctorant
DOCTORANT_URL_NAMES = {
    'inscription', 'reinscription', 'changement', 'etat_d`avencement',
    'point', 'testPoint', 'passage_annee', 'indexDoctorant',
}

# Encadreur pages that need request.user to be an encadreur
ENCADREUR_URL_NAMES = {
    'situations', 'listeDoctorans', 'etat', 'demandeSoutenance',
}

_DEMO_BACKEND = 'django.contrib.auth.backends.ModelBackend'


def _demo_doctorant_user():
    from pages.models import Doctorant, edition_pv
    # Prefer a doctorant that actually has an evaluation, so the demo looks alive.
    pv = edition_pv.objects.select_related('doctorant__user').exclude(doctorant__isnull=True).first()
    if pv and pv.doctorant:
        return pv.doctorant.user
    d = (Doctorant.objects.filter(validation=True).select_related('user').first()
         or Doctorant.objects.select_related('user').first())
    return d.user if d else None


def _demo_encadreur_user():
    from django.db.models import Count
    from encadreur.models import Encadreur
    # Pick the encadreur supervising the most doctorants for a fuller demo.
    e = (Encadreur.objects.annotate(n=Count('doctorants')).order_by('-n')
         .select_related('user').first())
    return e.user if e else None


class DemoAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not getattr(settings, 'DEMO_MODE', False):
            return None
        match = getattr(request, 'resolver_match', None)
        if match is None:
            return None
        name = match.url_name

        desired = None
        if name in DOCTORANT_URL_NAMES:
            desired = _demo_doctorant_user()
        elif name in ENCADREUR_URL_NAMES:
            desired = _demo_encadreur_user()

        if desired is None:
            return None

        # Log in (or switch to) the correct demo user for this space
        current = getattr(request, 'user', None)
        if current is None or not current.is_authenticated or current.pk != desired.pk:
            login(request, desired, backend=_DEMO_BACKEND)
        return None
