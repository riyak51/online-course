from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Course,
    Lesson,
    Learner,
    Question,
    Choice,
    Submission,
    Enrollment
)


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


@login_required
def submit(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    learner, created = Learner.objects.get_or_create(
        user=request.user
    )

    enrollment, created = Enrollment.objects.get_or_create(
        learner=learner,
        course=course
    )

    # Create a submission
    lesson = course.lessons.first()

    if lesson is None:
        return redirect("course_details", course_id=course.id)

    submission = Submission.objects.create(
        enrollment=enrollment,
        learner=learner,
        lesson=lesson,
        score=0,
        total_questions=course.questions.count()
    )

    # Save selected choices
    selected_choices = []

    for question in course.questions.all():

        selected_choice_ids = request.POST.getlist(
            f"question_{question.id}"
        )

        choices = Choice.objects.filter(
            id__in=selected_choice_ids,
            question=question
        )

        selected_choices.extend(choices)

    submission.choices.set(selected_choices)

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(Course, id=course_id)

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment__learner__user=request.user,
        enrollment__course=course
    )

    questions = course.questions.prefetch_related(
        "choices"
    )

    score = 0
    total_grade = 0

    for question in questions:

        total_grade += question.grade

        selected_ids = submission.choices.filter(
            question=question
        ).values_list("id", flat=True)

        if question.is_get_score(selected_ids):
            score += question.grade

    percentage = (
        (score / total_grade) * 100
        if total_grade > 0 else 0
    )

    submission.score = score
    submission.total_questions = questions.count()
    submission.save()

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "questions": questions,
            "selected_choices": submission.choices.all(),
            "score": score,
            "total_grade": total_grade,
            "percentage": percentage,
        }
    )
