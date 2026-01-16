from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Vote
import re


@login_required
def home(request):
    # Handle vote submission — persist into Vote model
    if request.method == "POST":
        candidate = request.POST.get("candidate")
        voter_name = request.POST.get("voter_name", "").strip()
        # capture email when the user is authenticated, or fallback to form value
        if request.user.is_authenticated:
            voter_email = request.user.email
        else:
            voter_email = request.POST.get("voter_email", "").strip()

        if candidate in ("mj", "lebron"):
            # If the user didn't enter a name, use the authenticated user's name when available,
            # otherwise fall back to "Anonymous" for unauthenticated voters.
            if not voter_name:
                if request.user.is_authenticated:
                    voter_name = request.user.get_full_name() or request.user.username
                else:
                    # If anonymous but supplied an email, derive a display name from the
                    # local-part of the email (e.g. 'mary.leianne' -> 'Mary Leianne').
                    if voter_email:
                        local = voter_email.split("@", 1)[0]
                        # replace common separators with spaces and title-case words
                        name = " ".join([p.capitalize() for p in re.split(r"[._\-]+", local) if p])
                        voter_name = name or "Anonymous"
                    else:
                        voter_name = "Anonymous"

            # create Vote record
            Vote.objects.create(voter_name=voter_name, voter_email=voter_email, candidate=candidate)
            request.session["has_voted"] = True
            messages.success(
                request,
                f"Thanks {voter_name}, your vote for {'Michael Jordan' if candidate == 'mj' else 'LeBron James'} was recorded.",
            )
        return redirect(reverse("home"))

    # Query DB for current polling data
    mj_votes = Vote.objects.filter(candidate="mj").count()
    lebron_votes = Vote.objects.filter(candidate="lebron").count()
    total = mj_votes + lebron_votes if (mj_votes + lebron_votes) > 0 else 1
    mj_percent = round(mj_votes * 100 / total)
    lebron_percent = 100 - mj_percent

    recent_votes = Vote.objects.all()[:8]

    context = {
        "mj": {
            "name": "MICHAEL JORDAN",
            "votes": mj_votes,
            "percent": mj_percent,
            "image": "images/michael.png",
        },
        "lebron": {
            "name": "LEBRON JAMES",
            "votes": lebron_votes,
            "percent": lebron_percent,
            "image": "images/lebron.png",
        },
        "voters": [{"name": v.voter_name, "candidate": v.candidate, "email": v.voter_email} for v in recent_votes],
        "has_voted": request.session.get("has_voted", False),
    }

    return render(request, "home.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_username()}!")
            return redirect(reverse("home"))
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(reverse("login"))

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(reverse("home"))
