from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Exam


# =========================
# HOME (SAFE REDIRECT)
# =========================
def home(request):

    if request.session.get('admin'):
        return redirect('/dashboard/')

    if request.session.get('student_id'):
        return redirect('/exam/')

    return redirect('/login/')


# =========================
# REGISTER
# =========================
def register(request):

    if request.session.get('student_id'):
        return redirect('/exam/')

    if request.session.get('admin'):
        return redirect('/dashboard/')

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Username check
        if Student.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists ❌'
            })

        # Email check
        if Student.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already exists ❌'
            })

        # Password check
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Password not matched ❌'
            })

        # Create student
        Student.objects.create(
            fullname=request.POST['fullname'],
            username=username,
            email=email,
            department=request.POST['department'],
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


# =========================
# STUDENT LOGIN
# =========================
def login(request):

    if request.session.get('student_id'):
        return redirect('/exam/')

    if request.session.get('admin'):
        return redirect('/dashboard/')

    if request.method == "POST":

        student = Student.objects.filter(
            username=request.POST['username'],
            password=request.POST['password']
        ).first()

        if student:

            request.session.flush()

            request.session['student_id'] = student.id
            request.session['department'] = student.department

            return redirect('/exam/')

        return render(request, 'login.html', {
            'error': 'Invalid login ❌'
        })

    return render(request, 'login.html')


# =========================
# STUDENT EXAM VIEW
# =========================
def view_exam(request):

    if not request.session.get('student_id'):
        return redirect('/login/')

    # Student department
    student_department = request.session.get('department')

    # Default exam list
    exams = Exam.objects.filter(
        department=student_department
    )

    # Filter values
    department = request.GET.get('department')
    semester = request.GET.get('semester')

    # Department filter
    if department:
        exams = exams.filter(department=department)

    # Semester filter
    if semester:
        exams = exams.filter(semester=semester)

    return render(request, 'view-exam.html', {
        'exams': exams
    })


# =========================
# ADMIN LOGIN
# =========================
def admin_login(request):

    if request.session.get('admin'):
        return redirect('/dashboard/')

    if request.session.get('student_id'):
        return redirect('/exam/')

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == "admin@ugv.edu" and password == "admin123":

            request.session.flush()

            request.session['admin'] = True

            return redirect('/dashboard/')

        return render(request, 'admin-login.html', {
            'error': 'Invalid admin login ❌'
        })

    return render(request, 'admin-login.html')


# =========================
# DASHBOARD
# =========================
def dashboard(request):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    return render(request, 'dashboard.html')


# =========================
# ADD EXAM
# =========================
def add_exam(request):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    if request.method == "POST":

        Exam.objects.create(
            subject=request.POST['subject'],
            exam_date=request.POST['exam_date'],
            exam_time=request.POST['exam_time'],
            room=request.POST['room'],
            department=request.POST['department'],
            semester=request.POST['semester'],
        )

        return redirect('/admin-exam/')

    return render(request, 'add-exam.html')


# =========================
# ADMIN VIEW EXAM
# =========================
def admin_view_exam(request):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    exams = Exam.objects.all()

    return render(request, 'admin-view-exam.html', {
        'exams': exams
    })


# =========================
# DELETE EXAM
# =========================
def delete_exam(request, id):

    if not request.session.get('admin'):
        return redirect('/admin-login/')

    exam = get_object_or_404(Exam, id=id)

    exam.delete()

    return redirect('/admin-exam/')


# =========================
# LOGOUT STUDENT
# =========================
def logout(request):

    request.session.flush()

    return redirect('/login/')


# =========================
# LOGOUT ADMIN
# =========================
def admin_logout(request):

    request.session.flush()

    return redirect('/admin-login/')