import fitz  # PyMuPDF
import re
from .models import Tag, QuestionPaper

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

def extract_questions(text):
    """Extract numbered questions ending with a question mark."""
    return re.findall(r"\d+\..*?\?", text, re.DOTALL)

def find_repeated_questions(new_paper_text, all_papers):
    """Find repeated questions by comparing new paper with existing papers."""
    new_questions = set(extract_questions(new_paper_text))
    repeated = set()

    for paper in all_papers:
        paper_questions = set(extract_questions(paper))
        repeated.update(new_questions.intersection(paper_questions))

    return list(repeated)

def assign_repeated_question_tags(new_paper):
    """Assign tags for repeated questions in new paper."""
    new_paper_text = extract_text_from_pdf(new_paper.file.path)
    
    all_existing_texts = [
        extract_text_from_pdf(paper.file.path) for paper in QuestionPaper.objects.exclude(id=new_paper.id)
    ]
    
    repeated_questions = find_repeated_questions(new_paper_text, all_existing_texts)

    # Convert repeated questions into tags
    for question in repeated_questions:
        tag_name = question[:50]  # First 50 chars as tag
        tag, created = Tag.objects.get_or_create(name=tag_name)
        new_paper.tags.add(tag)
