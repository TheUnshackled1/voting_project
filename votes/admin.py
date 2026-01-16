from django.contrib import admin
from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ("voter_name", "voter_email", "candidate", "created_at")
	search_fields = ("voter_name", "voter_email")
	list_filter = ("candidate", "created_at")
	ordering = ("-created_at",)
	date_hierarchy = "created_at"
