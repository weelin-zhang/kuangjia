from django.contrib import admin
from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')

    # 我们通过使用prepopulated_fields属性告诉Django通过输入的标题来填充slug字段
    prepopulated_fields = {'slug': ('title',)}

    # author字段弄成可搜索的
    raw_id_fields = ('author', )

    # 搜索框的下方，有个可以通过时间层快速导航的栏，该栏通过定义date_hierarchy属性出现
    date_hierarchy = 'publish'

    # 默认排序
    ordering = ['status', 'publish']



admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    date_hierarchy = 'created'

admin.site.register(Comment, CommentAdmin)
