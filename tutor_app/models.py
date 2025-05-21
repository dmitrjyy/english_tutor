from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    CLASS_CHOICES = [
        (1, '1 класс'),
        (2, '2 класс'),
        (3, '3 класс'),
        (4, '4 класс'),
        (5, '5 класс'),
        (6, '6 класс'),
        (7, '7 класс'),
        (8, '8 класс'),
        (9, '9 класс'),
        (10, '10 класс'),
        (11, '11 класс'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя ученика")
    student_class = models.IntegerField(choices=CLASS_CHOICES, verbose_name="Класс")
    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    
    def __str__(self):
        return f"{self.name} ({self.get_student_class_display()})"
    
    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"
        ordering = ['student_class', 'name']

class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons', verbose_name="Ученик")
    date = models.DateField(verbose_name="Дата урока")
    plan = models.TextField(verbose_name="План урока")
    homework = models.TextField(verbose_name="Домашнее задание", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.date.strftime('%d.%m.%Y')}"
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['-date']

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name="Ученик")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades', verbose_name="Урок")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    
    def __str__(self):
        return f"{self.student.name} - {self.score} ({self.lesson.date.strftime('%d.%m.%Y')})"
    
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['-lesson__date']

class Test(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    CATEGORY_CHOICES = [
        ('grammar', 'Грамматика'),
        ('vocabulary', 'Лексика'),
        ('listening', 'Аудирование'),
        ('reading', 'Чтение'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста", blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name="Уровень сложности")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")
    
    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}..."
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    
    def __str__(self):
        return f"{self.question.text[:30]}... - {self.text[:30]}..."
    
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class TestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_results', verbose_name="Ученик")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results', verbose_name="Тест")
    score = models.IntegerField(verbose_name="Результат (%)")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")
    
    def __str__(self):
        return f"{self.student.name} - {self.test.title} ({self.score}%)"
    
    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
        ordering = ['-date_taken']