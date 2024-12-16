from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from crud.database2 import execute_query
from polls.forms import CreateForm, UpdateForm, DeleteForm


def index(request):

    if request.method == "POST":
        form = CreateForm(request.POST)
        today = timezone.now()
        if form.is_valid():
            question_text = form.cleaned_data["question_text"]
            query = "INSERT INTO polls_product (question_text, pub_date) VALUES (%s, %s)"
            execute_query(query, (question_text, today))
            messages.success(request, "Registro creado.")
        else:
            messages.error(request, "Hubo un error en el formulario.")
    else:
        form = CreateForm()

    query = "SELECT * FROM polls_product ORDER BY pub_date DESC LIMIT 5"
    latest_question_list = execute_query(query, fetch=True)
    context = {
        "form": form,
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


def edit(request, question_id):
    query = "SELECT * FROM polls_product WHERE id = %s"
    question = execute_query(query, (question_id,), fetch=True)

    if not question:
        messages.error(request, "El registro no existe.")
        return redirect(reverse("polls:index"))

    question = question[0]

    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text")
            query = "UPDATE polls_product SET question_text = %s WHERE id = %s"
            execute_query(query, (question_text, question_id))
            messages.success(request, "Registro actualizado.")
            return redirect(reverse("polls:index"))
        else:
            messages.error(request, "Error al editar el registro.")
    else:
        form = UpdateForm(initial={"question_text": question["question_text"]})

    return render(
        request,
        "polls/detail.html",
        {
            "form": form,
            "question": question
        },
    )


def delete(request, question_id):
    query = "SELECT * FROM polls_product WHERE id = %s"
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
        query = "DELETE FROM polls_product WHERE id = %s"
        execute_query(query, (question_id,))
        messages.success(request, "El registro '%s' fue eliminado" % question_text)
        return redirect(reverse("polls:index"))

    elif request.method == "GET":
        return render(
            request,
            "polls/delete.html",
            {"question": question}
        )


def index2(request):
    form = CreateForm()

    if request.method == "POST":
        today = timezone.now()
        form = CreateForm(request.POST)

        if not form.is_valid():
            messages.error(request, "No se pudo crear el registro.")
            return redirect(reverse("polls:index"))

        question_text = form.cleaned_data.get("question_text")
        query = "INSERT INTO polls_product (question_text, pub_date) VALUES (%s, %s)"
        success, result = execute_query(query, (question_text,))
        if not success:
            messages.error(request, "No se pudo crear el registro.")
            return redirect(reverse("polls:index"))

        messages.success(request, f"Se creó el registro '{question_text}'.")
        return redirect(reverse("polls:index"))

    query = "SELECT * FROM polls_product ORDER BY pub_date DESC"
    success, questions = execute_query(query, fetch=True)

    return render(
        request,
        "polls/index.html",
        {
            "latest_question_list": questions,
            "form": form,
        }
    )


def edit2(request, question_id):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data.get("question_text", "")
            question_id_cleaned = form.cleaned_data.get("question_id", None)
            if not question_id or (question_id != question_id_cleaned):
                messages.error(request, "Error al editar el registro.")
                return redirect(reverse("polls:index"))

            query = "UPDATE polls_product SET question_text = %s WHERE id = %s"
            success, result = execute_query(query, (question_text, question_id))
            messages.success(request, "El registro se editó correctamente.")
        else:
            messages.error(request, "Error al editar el registro.")

        return redirect(reverse("polls:index"))
    else:
        form = UpdateForm()

    query = "SELECT * FROM polls_product WHERE id = %s"
    success, question = execute_query(query, (question_id,), fetch=True)
    question = question[0]

    return render(
        request,
        "polls/detail.html",
        {
            "question": question,
            "form": form,
        }
    )


def delete2(request, question_id):
    form = DeleteForm()

    if request.method == "POST":
        form = DeleteForm(request.POST)
        if not form.is_valid():
            print(f"[delete2] -> CrudForm - Error: {form.errors}")
            messages.error(request, "El registro no pudo borrarse.")
            return redirect(reverse("polls:index"))

        question_id_form = form.cleaned_data.get("question_id")
        if question_id_form != question_id:
            messages.error(request, "Error al editar el registro.")
            return redirect(reverse("polls:index"))

        query = "DELETE FROM polls_product WHERE id = %s"
        success, result = execute_query(query, (question_id,))
        if not success:
            print(f"Error: {result}")
            messages.error(request, "El registro no pudo borrarse.")
            return redirect(reverse("polls:index"))

        messages.success(request, "El registro se borró correctamente.")
        return redirect(reverse("polls:index"))

    query = "SELECT * FROM polls_product WHERE id = %s"
    success, question = execute_query(query, (question_id,), fetch=True)
    if not success or len(question) == 0:
        messages.error(request, "El registro que intentas borrar no existe.")
        return redirect(reverse("polls:index"))

    question = question[0]

    return render(
        request,
        "polls/delete.html",
        {
            "question": question,
            "form": form,
        }
    )
