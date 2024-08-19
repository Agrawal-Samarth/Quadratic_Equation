from django.urls import path
from . import views

app_name = 'solver'

urlpatterns = [
    path('', views.QuadraticSolverView.as_view(), name='index'),
    path('history/', views.equation_history, name='history'),
    path('equation/<int:equation_id>/', views.equation_detail, name='detail'),
]
