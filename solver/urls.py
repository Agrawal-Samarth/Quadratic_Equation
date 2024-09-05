from django.urls import path
from . import views
from . import analytics_views

app_name = 'solver'

urlpatterns = [
    path('', views.QuadraticSolverView.as_view(), name='index'),
    path('history/', views.equation_history, name='history'),
    path('equation/<int:equation_id>/', views.equation_detail, name='detail'),
    
    # Analytics URLs
    path('analytics/', analytics_views.analytics_dashboard, name='analytics'),
    path('api/intersections/', analytics_views.calculate_intersections, name='calculate_intersections'),
]
