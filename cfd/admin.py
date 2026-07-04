from django.contrib import admin
from .models import login_cfd
from .models import ApplicationSettings



# Register your models here.
admin.site.register(login_cfd)
admin.site.register(ApplicationSettings)

