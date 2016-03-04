from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'published_date', 'author_id')

admin.site.register(Post, PostAdmin)
