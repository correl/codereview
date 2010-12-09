from codereview.review.models import *
from django.contrib import admin

class CommentInline(admin.StackedInline):
    model = Comment
class ItemInline(admin.StackedInline):
    model = Item
    inlines = [CommentInline]

class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline
    ]
admin.site.register(Review, ReviewAdmin)
