from django.contrib import admin

from .models import Math, Result


@admin.register(Math)
class MathAdmin(admin.ModelAdmin):
    list_display = ("operation", "a", "b", "result", "created")
    list_filter = ("operation",)
    search_fields = ("operation",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("value", "error")
    search_fields = ("value", "error")
