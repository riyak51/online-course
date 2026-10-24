
from django.urls import path
from . import views

urlpatterns = [
    path(
        "lessons/<int:lesson_id>/submit/",
        views.submit,
        name="submit",
    ),
    path(
        "courses/<int:course_id>/submission/<int:submission_id>/result/",
        views.show_exam_result,
        name="show_exam_result",
    ),
]
