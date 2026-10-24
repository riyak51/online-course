from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="instructors"
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="learners"
    )
    courses = models.ManyToManyField(
        "Course",
        related_name="learners",
        blank=True
    )
    interests = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="course_images/", blank=True)
    description = models.CharField(max_length=200)
    pub_date = models.DateField(null=True, blank=True)
    instructors = models.ManyToManyField(
        Instructor,
        related_name="courses",
        blank=True
    )
    users = models.ManyToManyField(
        User,
        related_name="courses_joined",
        blank=True
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    content = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.learner} - {self.lesson} "
            f"({self.score}/{self.total_questions})"
        )
