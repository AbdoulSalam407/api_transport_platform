from django.contrib import admin
from .models import Marque, Modele, Vehicule

admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Vehicule)