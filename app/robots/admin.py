from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated

from robots import models


class RobotPositionInline(TabularInlinePaginated):
    per_page = 20
    model = models.RobotPosition

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Robot)
class RobotAdmin(admin.ModelAdmin):
    inlines = (RobotPositionInline,)
