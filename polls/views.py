from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from polls.forms import CrudForm
from polls.models import Question


def index(request):

    if request.method == "POST":
        form = CrudForm(request.POST)
        today = timezone.now()
        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            Question.objects.create(question_text=question_text, pub_date=today)
            return redirect(reverse("polls:index"))
    else:
        form = CrudForm()

    latest_question_list = Question.objects.order_by("-pub_date")
    context = {
        "form": form,
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        messages.error(request, "El registro no existe.")
        return redirect(reverse("polls:index"))

    if request.method == "POST":
        form = CrudForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            question.question_text = question_text
            question.save()
            messages.success(request, "Registro actualizado.")
            return redirect(reverse("polls:index"))
        else:
            return render(
                request,
                "polls/detail.html",
                {
                    "form": form,
                    "question": question
                },
            )
    else:
        return render(
            request,
            "polls/detail.html",
            {
                "form": CrudForm(),
                "question": question
            },
        )


def confirm_delete(request, question_id):
    if request.method == "POST":
        q_id = request.POST.get("question_id", None)
        return redirect(reverse("polls:delete", args=(q_id,)))

    return render(
        request,
        "polls/confirm_delete.html",
        {"question_id": question_id}
    )


def delete(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        question_text = question.question_text
    except Question.DoesNotExist:
        messages.error(request, "El registro que se intentó borrar no existe.")
        return redirect(reverse("polls:index"))

    if request.method == "POST":
        try:
            q_id = int(request.POST.get("question_id", None))
        except Exception:
            messages.error(request, "Hubo un error inesperado. Intenta de nuevo.")
            return redirect(reverse("index"))

        if question_id != q_id:
            messages.error(request, "Hubo un error inesperado. Intenta de nuevo.")
            return redirect(reverse("index"))

        question.delete()
        messages.success(request, "El registro '%s' fue eliminado" % question_text)
        return redirect(reverse("polls:index"))

    elif request.method == "GET":
        return render(
            request,
            "polls/delete.html",
            {"question": question}
        )


# def results(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404()
    
#     return render(request, "polls/results.html", {"question": question})


# def vote(request, question_id):
#     try:
#         choice = request.POST["choice"]
#         question = Question.objects.get(pk=question_id)
#         selected_choice = question.choice_set.get(pk=choice)
#     except (KeyError, Question.DoesNotExist):
#         return render(request, "polls/detail.html", {
#             "question": question,
#             "error_message": "No seleccionaste una opción.",
#         })

#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(
#             reverse("polls:results", args=(question.id,))
#         )
