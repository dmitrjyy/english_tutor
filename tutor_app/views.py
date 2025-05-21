from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Student, Lesson, Grade, Test, Question, Answer, TestResult 
from django.views.decorators.http import require_GET


def diary_view(request):
    active_tab = request.POST.get('active_tab') or request.GET.get('active_tab') or 'students'
    
    # Students tab
    students = Student.objects.all()
    search_query = ""
    
    if 'search' in request.POST and request.POST.get('active_tab') == 'students':
        search_query = request.POST.get('query', '')
        students = students.filter(name__icontains=search_query)
    
    # Lessons tab
    lessons = Lesson.objects.select_related('student').all()
    lesson_search_query = ""
    
    if 'lesson_search' in request.POST and request.POST.get('active_tab') == 'lessons':
        lesson_search_query = request.POST.get('lesson_query', '')
        lessons = lessons.filter(student__name__icontains=lesson_search_query)
    
    # Grades tab
    grades = Grade.objects.select_related('student', 'lesson').all()
    grade_search_query = ""
    
    if 'grade_search' in request.POST and request.POST.get('active_tab') == 'grades':
        grade_search_query = request.POST.get('grade_query', '')
        grades = grades.filter(student__name__icontains=grade_search_query)
    
    # Tests tab
    tests = Test.objects.prefetch_related('questions').all()
    

    if request.method == 'POST':
        # Student operations
        if 'create' in request.POST:
            name = request.POST.get('name')
            student_class = request.POST.get('student_class')
            telegram = request.POST.get('telegram')
            phone = request.POST.get('phone')
            
            Student.objects.create(
                name=name,
                student_class=student_class,
                telegram=telegram if telegram else None,
                phone=phone if phone else None
            )
            messages.success(request, 'Ученик успешно добавлен')
            return redirect('diary')
        
        elif 'update' in request.POST:
            student_id = request.POST.get('id')
            student = Student.objects.get(id=student_id)
            student.name = request.POST.get('name')
            student.student_class = request.POST.get('student_class')
            student.telegram = request.POST.get('telegram') or None
            student.phone = request.POST.get('phone') or None
            student.save()
            messages.success(request, 'Данные ученика обновлены')
            return redirect('diary')
        
        elif 'delete' in request.POST:
            student_id = request.POST.get('id')
            Student.objects.get(id=student_id).delete()
            messages.success(request, 'Ученик удален')
            return redirect('diary')
        
        # Lesson operations
        elif 'create_lesson' in request.POST:
            student_id = request.POST.get('student')
            date = request.POST.get('date')
            plan = request.POST.get('plan')
            homework = request.POST.get('homework') or None
            comment = request.POST.get('comment') or None
            
            Lesson.objects.create(
                student_id=student_id,
                date=date,
                plan=plan,
                homework=homework,
                comment=comment
            )
            messages.success(request, 'Урок успешно добавлен')
            return redirect('diary')
        
        elif 'update_lesson' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.student_id = request.POST.get('student')
            lesson.date = request.POST.get('date')
            lesson.plan = request.POST.get('plan')
            lesson.homework = request.POST.get('homework') or None
            lesson.comment = request.POST.get('comment') or None
            lesson.save()
            messages.success(request, 'Урок обновлен')
            return redirect('diary')
        
        elif 'delete_lesson' in request.POST:
            lesson_id = request.POST.get('lesson_id')
            Lesson.objects.get(id=lesson_id).delete()
            messages.success(request, 'Урок удален')
            return redirect('diary')
        
        # Grade operations
        elif 'create_grade' in request.POST:
            student_id = request.POST.get('student')
            lesson_id = request.POST.get('lesson')
            score = request.POST.get('score')
            
            Grade.objects.create(
                student_id=student_id,
                lesson_id=lesson_id,
                score=score
            )
            messages.success(request, 'Оценка добавлена')
            return redirect('diary')
        
        elif 'update_grade' in request.POST:
            grade_id = request.POST.get('grade_id')
            grade = Grade.objects.get(id=grade_id)
            grade.student_id = request.POST.get('student')
            grade.lesson_id = request.POST.get('lesson')
            grade.score = request.POST.get('score')
            grade.save()
            messages.success(request, 'Оценка обновлена')
            return redirect('diary')
        
        elif 'delete_grade' in request.POST:
            grade_id = request.POST.get('grade_id')
            Grade.objects.get(id=grade_id).delete()
            messages.success(request, 'Оценка удалена')
            return redirect('diary')
        
        # Test operations
        elif 'create_test' in request.POST:
       
            pass
    
    context = {
        'active_tab': active_tab,
        'students': students,
        'search_query': search_query,
        'lessons': lessons,
        'lesson_search_query': lesson_search_query,
        'grades': grades,
        'grade_search_query': grade_search_query,
        'tests': tests,
    }
    
    return render(request, 'tutor_app/index.html', context)


@require_GET
def get_lessons(request):
    student_id = request.GET.get('student_id')
    lessons = Lesson.objects.filter(student_id=student_id).order_by('-date')
    
    lessons_data = [{
        'id': lesson.id,
        'date': lesson.date.strftime('%d.%m.%Y')
    } for lesson in lessons]
    
    return JsonResponse({'lessons': lessons_data})

