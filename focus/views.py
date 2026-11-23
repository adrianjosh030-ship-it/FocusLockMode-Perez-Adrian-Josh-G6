from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CategoryForm, FocusSessionForm
from .models import Category, FocusSession


def is_admin(user):
    return user.is_superuser or getattr(user, "role", None) == "admin"


def _get_session(request, pk):
    """Students only get their own; admins get any."""
    qs = FocusSession.objects.all() if is_admin(request.user) else FocusSession.objects.filter(user=request.user)
    return get_object_or_404(qs, pk=pk)


@login_required
def session_list(request):
    qs = FocusSession.objects.select_related("user", "category")
    if not is_admin(request.user):
        qs = qs.filter(user=request.user)
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    return render(request, "focus/session_list.html",
                  {"sessions": qs, "is_admin": is_admin(request.user), "status": status})


@login_required
def session_create(request):
    form = FocusSessionForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        s = form.save(commit=False)
        s.user = request.user
        s.save()
        messages.success(request, "Focus session created.")
        return redirect("focus:detail", pk=s.pk)
    if request.method == "POST":
        messages.error(request, "Please fix the errors below.")
    return render(request, "focus/session_form.html", {"form": form, "title": "New focus session"})


@login_required
def session_detail(request, pk):
    return render(request, "focus/session_detail.html", {"s": _get_session(request, pk)})


@login_required
def session_update(request, pk):
    s = _get_session(request, pk)
    if s.status in (FocusSession.COMPLETED, FocusSession.ABANDONED):
        messages.error(request, "Finished sessions can't be edited.")
        return redirect("focus:detail", pk=s.pk)
    form = FocusSessionForm(request.POST or None, instance=s, user=s.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Focus session updated.")
        return redirect("focus:detail", pk=s.pk)
    if request.method == "POST":
        messages.error(request, "Please fix the errors below.")
    return render(request, "focus/session_form.html", {"form": form, "title": "Edit focus session"})


@login_required
def session_delete(request, pk):
    s = _get_session(request, pk)
    if request.method == "POST":
        s.delete()
        messages.success(request, "Focus session deleted.")
        return redirect("focus:list")
    return render(request, "focus/session_confirm_delete.html", {"s": s})


@login_required
def session_start(request, pk):
    s = _get_session(request, pk)
    if request.method != "POST":
        return redirect("focus:detail", pk=s.pk)
    if s.status != FocusSession.PLANNED:
        messages.error(request, "Only planned sessions can be started.")
    elif FocusSession.objects.filter(user=s.user, status=FocusSession.ACTIVE).exists():
        messages.error(request, "You already have an active session. Finish it first.")
    else:
        s.status, s.started_at = FocusSession.ACTIVE, timezone.now()
        s.save()
        messages.success(request, "Focus mode started. Stay locked in!")
    return redirect("focus:detail", pk=s.pk)


@login_required
def session_finish(request, pk, outcome):
    s = _get_session(request, pk)
    if request.method != "POST":
        return redirect("focus:detail", pk=s.pk)
    if s.status != FocusSession.ACTIVE:
        messages.error(request, "Only an active session can be finished.")
    else:
        s.status = FocusSession.COMPLETED if outcome == "complete" else FocusSession.ABANDONED
        s.ended_at = timezone.now()
        s.save()
        messages.success(request, f"Session marked {s.status}.")
    return redirect("focus:detail", pk=s.pk)


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"].strip()
        if Category.objects.filter(user=request.user, name__iexact=name).exists():
            messages.error(request, "You already have a category with that name.")
        else:
            Category.objects.create(user=request.user, name=name)
            messages.success(request, "Category added.")
            return redirect("focus:create")
    elif request.method == "POST":
        messages.error(request, "Please fix the errors below.")
    return render(request, "focus/category_form.html", {"form": form})