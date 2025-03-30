'''from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import QuestionPaper

def paper_list(request):
    query = request.GET.get("query", "")  # Search query
    subject_filter = request.GET.get("subject", "")
    course_filter = request.GET.get("course", "")
    difficulty_filter = request.GET.get("difficulty", "")
    year_filter = request.GET.get("year", "")

    papers = QuestionPaper.objects.all()


    if query:
        papers = papers.filter(title__icontains=query)

    if subject_filter:
        papers = papers.filter(subject=subject_filter)

    if course_filter:
        papers = papers.filter(course=course_filter)

    if difficulty_filter:
        papers = papers.filter(difficulty=difficulty_filter)

    if year_filter:
        papers = papers.filter(year=year_filter)

    context = {
        "papers": papers,
        "query": query,
        "subject_filter": subject_filter,
        "course_filter": course_filter,
        "difficulty_filter": difficulty_filter,
        "year_filter": year_filter,
    }
    return render(request, "repository/paper_list.html", context)



'''















from django.shortcuts import render
from django.core.paginator import Paginator
from .models import QuestionPaper

def paper_list(request):
    query = request.GET.get("query", "")
    subject_filter = request.GET.get("subject", "")
    course_filter = request.GET.get("course", "")
    difficulty_filter = request.GET.get("difficulty", "")
    year_filter = request.GET.get("year", "")

    papers = QuestionPaper.objects.all().order_by("-year") #order by newest year first

    if query:
        papers = papers.filter(title__icontains=query)

    if subject_filter:
        papers = papers.filter(subject=subject_filter)

    if course_filter:
        papers = papers.filter(course=course_filter)

    if difficulty_filter:
        papers = papers.filter(difficulty=difficulty_filter)

    if year_filter:
        papers = papers.filter(year=year_filter)

    paginator = Paginator(papers, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
        "subject_filter": subject_filter,
        "course_filter": course_filter,
        "difficulty_filter": difficulty_filter,
        "year_filter": year_filter,
        "subject_choices": QuestionPaper.SUBJECT_CHOICES,  # Pass subject choices to template
    }
    return render(request, "repository/paper_list.html", context)





































from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import QuestionPaper
from .forms import QuestionPaperForm
from .utils import assign_repeated_question_tags  # Import function

'''@login_required
def upload_paper(request):
    # Restrict upload access to teachers (gitam.edu emails only)
    if not request.user.email.endswith("@gitam.edu"):
        messages.error(request, "Only faculty members (gitam.edu) can upload papers.")
        return redirect("paper_list")

    if request.method == "POST":
        form = QuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.uploaded_by = request.user
            paper.save()

            # Assign repeated question tags
            assign_repeated_question_tags(paper)

            # Send email notification to all students
            students = User.objects.filter(email__endswith="@gitam.in")
            recipient_list = [student.email for student in students]

            send_mail(
                "New Question Paper Available!",
                f"A new question paper '{paper.title}' for {paper.subject} has been uploaded.",
                "admin@gitam.edu",
                recipient_list,
                fail_silently=True,
            )

            messages.success(request, "Paper uploaded successfully! Students will be notified.")
            return redirect("paper_list")
    else:
        form = QuestionPaperForm()

    return render(request, "repository/upload_paper.html", {"form": form})'''







from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from django.conf import settings
import threading

User = get_user_model()

def send_email_notification(subject, message, recipient_list):
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)
    except BadHeaderError:
        print("Invalid header found.")

@login_required
def upload_paper(request):
    if not request.user.email.endswith("@gitam.edu"):
        messages.error(request, "Only faculty members (gitam.edu) can upload papers.")
        return redirect("repository:paper_list")


    if request.method == "POST":
        form = QuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.uploaded_by = request.user
            paper.save()

            assign_repeated_question_tags(paper)

            # Fetch all students
            students = User.objects.filter(email__endswith="@gitam.in").values_list("email", flat=True)

            # Send email in a separate thread for performance
            email_thread = threading.Thread(
                target=send_email_notification,
                args=(
                    "New Question Paper Available!",
                    f"A new question paper '{paper.title}' for {paper.subject} has been uploaded.",
                    list(students),
                ),
            )
            email_thread.start()

            messages.success(request, "Paper uploaded successfully! Students will be notified.")
            return redirect("repository:paper_list")

    else:
        form = QuestionPaperForm()

    return render(request, "repository/upload_paper.html", {"form": form})
