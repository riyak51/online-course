from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "course", "lesson")
    search_fields = ("question_text",)


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ("title", "course")
    search_fields = ("title",)


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "pub_date")
    search_fields = ("name",)


class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time", "total_learners")


class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "interests")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "learner",
        "lesson",
        "score",
        "total_questions",
        "submitted_at",
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner, LearnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
