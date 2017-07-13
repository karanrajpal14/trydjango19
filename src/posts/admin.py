# Register your models here.
from .models import Post
from django.contrib import admin

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title","posted","last_updated","slug"]
	list_display_links = ["last_updated"]
	list_filter = ["posted","last_updated"]
	list_editable = ["title"]
	search_fields = ["title", "content"]
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)