from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import QuestionPaper, Tag

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'course', 'year', 'difficulty', 'uploaded_by', 'uploaded_at')
    list_filter = ('subject', 'course', 'year', 'difficulty')
    search_fields = ('title', 'subject', 'course', 'year')
    ordering = ('-uploaded_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
