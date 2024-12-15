from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from crud.database import execute_query
from polls.forms import CrudForm


def index(request):

    if request.method == "POST":
        form = CrudForm(request.POST)
        today = timezone.now()
        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            query = "INSERT INTO polls_question (question_text, pub_date) VALUES (%s, %s)"
            execute_query(query, (question_text, today))
            messages.success(request, "Registro creado.")
        else:
            messages.error(request, "Hubo un error en el formulario.")
    else:
        form = CrudForm()

    query = "SELECT * FROM polls_question ORDER BY pub_date DESC LIMIT 5"
    latest_question_list = execute_query(query, fetch=True)
    context = {
        "form": form,
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    query = "SELECT * FROM polls_question WHERE id = %s"
    question = execute_query(query, (question_id,), fetch=True)

    if not question:
        messages.error(request, "El registro no existe.")
        return redirect(reverse("polls:index"))

    question = question[0]

    if request.method == "POST":
        form = CrudForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            query = "UPDATE polls_question SET question_text = %s WHERE id = %s"
            execute_query(query, (question_text, question_id))
            messages.success(request, "Registro actualizado.")
            return redirect(reverse("polls:index"))
        else:
            messages.error(request, "Error al editar el registro.")
    else:
        form = CrudForm(initial={"question_text": question["question_text"]})

    return render(
        request,
        "polls/detail.html",
        {
            "form": form,
            "question": question
        },
    )


def delete(request, question_id):
    query = "SELECT * FROM polls_question WHERE id = %s"
    question = execute_query(query, (question_id,), fetch=True)
    if not question:
        messages.error(request, "El registro que se intentó borrar no existe.")
        return redirect(reverse("polls:index"))

    question = question[0]
    if request.method == "POST":
        try:
            q_id = int(request.POST.get("question_id", None))
        except Exception:
            messages.error(request, "Hubo un error inesperado. Intenta de nuevo.")
            return redirect(reverse("index"))

        if question_id != q_id:
            messages.error(request, "Hubo un error inesperado. Intenta de nuevo.")
            return redirect(reverse("index"))

        question_text = question["question_text"]
        query = "DELETE FROM polls_question WHERE id = %s"
        execute_query(query, (question_id,))
        messages.success(request, "El registro '%s' fue eliminado" % question_text)
        return redirect(reverse("polls:index"))

    elif request.method == "GET":
        return render(
            request,
            "polls/delete.html",
            {"question": question}
        )
