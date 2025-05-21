from django import forms
from .models import Student, Lesson, Grade, Test, Question, Answer

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_class', 'telegram', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'ФИО ученика'}),
            'telegram': forms.TextInput(attrs={'placeholder': '@username'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7XXXXXXXXXX'}),
        }
        labels = {
            'student_class': 'Класс',
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['student', 'date', 'plan', 'homework', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'plan': forms.Textarea(attrs={'rows': 3, 'placeholder': 'План урока'}),
            'homework': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Домашнее задание'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Комментарии к уроку'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'score']
        widgets = {
            'score': forms.Select(choices=[
                (5, '5 (Отлично)'),
                (4, '4 (Хорошо)'),
                (3, '3 (Удовлетворительно)'),
                (2, '2 (Неудовлетворительно)'),
                (1, '1 (Плохо)'),
            ]),
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'level', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Текст ответа'}),
        }