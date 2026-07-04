from django.contrib import admin

from .models import reinscription
from .models import situation_doctorant
from .models import edition_pv
from .models import Doctorant
from .models import inscription
from .models import Soutenance
from .models import Passage

#from .models import inscription ---> inscription c`est Tablename 
# Register your models here.
#admin.site.register(inscription) ---> inscription c`est le nom de la table
 

admin.site.register(inscription)
admin.site.register(reinscription)
admin.site.register(situation_doctorant)
admin.site.register(edition_pv)
admin.site.register(Doctorant)
admin.site.register(Soutenance)
admin.site.register(Passage)







