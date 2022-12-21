from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'psychologist', 'is_active', 'created_at']
    list_select_related = ['psychologist']
    raw_id_fields = ['psychologist']
    search_fields = ['title', 'psychologist__email', 'psychologist__first_name', 'psychologist__last_name']

admin.site.register(Article, ArticleAdmin)
