from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Learner, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


@login_required
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method != "POST":
        return redirect(
            "course_details",
            course_id=lesson.course.id
        )

    learner, created = Learner.objects.get_or_create(
        user=request.user
    )

    score = 0
    total_questions = lesson.questions.count()

    for question in lesson.questions.all():
        selected_choice_id = request.POST.get(
            f"question_{question.id}"
        )

        if selected_choice_id:
            selected_choice = Choice.objects.filter(
                id=selected_choice_id,
                question=question
            ).first()

            if selected_choice and selected_choice.is_correct:
                score += 1

    submission = Submission.objects.create(
        learner=learner,
        lesson=lesson,
        score=score,
        total_questions=total_questions
    )

    return redirect(
        "show_exam_result",
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        learner__user=request.user
    )

    questions = submission.lesson.questions.prefetch_related(
        "choices"
    )

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "submission": submission,
            "questions": questions,
        }
    )
