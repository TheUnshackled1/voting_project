"""Backfill script: replace 'Anonymous' voter_name with matching User name based on voter_email.
Run with: .\env\Scripts\python.exe scripts/backfill_votes.py
"""
import os
import sys
import django

# Ensure project root is on sys.path so Django can import the project package
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from votes.models import Vote

User = get_user_model()

updated = 0
for v in Vote.objects.filter(voter_name__iexact="Anonymous").exclude(voter_email__isnull=True).exclude(voter_email__exact=""):
    email = v.voter_email.strip()
    if not email:
        continue
    user = User.objects.filter(email__iexact=email).first()
    if user:
        new_name = user.get_full_name() or user.username
        if new_name and new_name != v.voter_name:
            v.voter_name = new_name
            v.save()
            updated += 1

print(f"Backfill complete. Updated {updated} Vote record(s).")
