from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Vote


def home(request):
    # Handle vote submission — persist into Vote model
    if request.method == "POST":
        candidate = request.POST.get("candidate")
        voter_name = request.POST.get("voter_name", "").strip()

        if candidate in ("mj", "lebron"):
            # allow anonymous votes when no name provided
            if not voter_name:
                voter_name = "Anonymous"

            # create Vote record
            Vote.objects.create(voter_name=voter_name, candidate=candidate)
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
        "voters": [{"name": v.voter_name, "candidate": v.candidate} for v in recent_votes],
        "has_voted": request.session.get("has_voted", False),
    }

    return render(request, "home.html", context)
