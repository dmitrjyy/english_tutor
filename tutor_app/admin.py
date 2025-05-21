from django.contrib import admin
from .models import Student, Lesson, Grade, Test, Question, Answer, TestResult

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category')
    list_filter = ('level', 'category')
    search_fields = ('title', 'description')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class', 'telegram', 'phone')
    list_filter = ('student_class',)
    search_fields = ('name', 'telegram', 'phone')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'short_plan')
    list_filter = ('date', 'student__student_class')
    search_fields = ('student__name', 'plan', 'homework', 'comment')
    date_hierarchy = 'date'
    
    def short_plan(self, obj):
        return obj.plan[:50] + '...' if len(obj.plan) > 50 else obj.plan
    short_plan.short_description = 'План урока'

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'score')
    list_filter = ('score', 'student__student_class')
    search_fields = ('student__name', 'lesson__plan')

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'date_taken')
    list_filter = ('test', 'date_taken')
    search_fields = ('student__name', 'test__title')

admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult, TestResultAdmin)