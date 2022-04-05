from django.contrib import admin
from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_on')
class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
