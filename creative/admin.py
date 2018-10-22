from django.contrib import admin

from .models import Genre
from .models import Language
from .models import Comments
from .models import Story

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Comments)
admin.site.register(Story)