from django.urls import path
from .views import paper_list,upload_paper
from django.conf.urls.static import static
from django.conf import settings



app_name = "repository" 

urlpatterns = [
    path('papers/', paper_list, name='paper_list'),
    path('upload/', upload_paper, name='upload_paper'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
