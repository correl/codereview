from codereview.review.models import *
from django.contrib import admin

class CommentInline(admin.StackedInline):
    model = Comment

class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
admin.site.register(Review, ReviewAdmin)
