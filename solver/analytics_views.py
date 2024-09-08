"""
Analytics Views for Quadratic Equation Solver
Provides data analysis and insights
"""

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json
from datetime import datetime
from .equation_analytics import EquationAnalytics, EquationBatchProcessor, EquationExporter
from .equation_intersection import EquationIntersectionCalculator


def analytics_dashboard(request):
    """Main analytics dashboard"""
    analytics = EquationAnalytics()
    
    context = {
        'stats': analytics.get_equation_statistics(),
        'patterns': analytics.get_equation_patterns(),
        'complexity': analytics.get_equation_complexity_analysis(),
        'trends': analytics.get_usage_trends(days=7),  # Last 7 days
    }
    
    return render(request, 'solver/analytics.html', context)


@require_http_methods(["GET"])
def get_analytics_data(request):
    """API endpoint for analytics data"""
    analytics = EquationAnalytics()
    
    data_type = request.GET.get('type', 'statistics')
    
    if data_type == 'statistics':
        data = analytics.get_equation_statistics()
    elif data_type == 'distribution':
        data = analytics.get_coefficient_distribution()
    elif data_type == 'patterns':
        data = analytics.get_equation_patterns()
    elif data_type == 'trends':
        days = int(request.GET.get('days', 30))
        data = analytics.get_usage_trends(days=days)
    elif data_type == 'complexity':
        data = analytics.get_equation_complexity_analysis()
    elif data_type == 'full_report':
        data = analytics.generate_analytics_report()
    else:
        return JsonResponse({'error': 'Invalid data type'}, status=400)
    
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def batch_process_equations(request):
    """Process multiple equations in batch"""
    try:
        data = json.loads(request.body)
        equations_list = data.get('equations', [])
        
        if not equations_list:
            return JsonResponse({'error': 'No equations provided'}, status=400)
        
        processor = EquationBatchProcessor()
        results = processor.process_equation_list(equations_list)
        
        return JsonResponse(results)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def solve_equation_api(request):
    """Standalone API endpoint for solving quadratic equations"""
    try:
        data = json.loads(request.body)
        a = data.get('a')
        b = data.get('b')
        c = data.get('c')
        
        if a is None or b is None or c is None:
            return JsonResponse({'error': 'Missing coefficients a, b, or c'}, status=400)
        
        try:
            a, b, c = float(a), float(b), float(c)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid coefficient values'}, status=400)
        
        if a == 0:
            return JsonResponse({'error': 'Coefficient a cannot be zero'}, status=400)
        
        # Import here to avoid circular imports
        from .quadratic_solver import QuadraticEquationSolver
        solver = QuadraticEquationSolver(a, b, c)
        
        result = {
            'equation': f"{a}x² + {b}x + {c} = 0",
            'coefficients': {'a': a, 'b': b, 'c': c},
            'discriminant': solver.get_discriminant(),
            'roots': solver.get_roots(),
            'vertex': solver.get_vertex(),
            'axis_of_symmetry': solver.get_axis_of_symmetry(),
            'direction': solver.get_direction(),
            'roots_type': solver.get_roots_type(),
            'discriminant_info': solver.get_discriminant_info(),
            'solved_at': datetime.now().isoformat()
        }
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def generate_sample_equations(request):
    """Generate sample equations for testing"""
    count = int(request.GET.get('count', 10))
    difficulty = request.GET.get('difficulty', 'mixed')
    
    processor = EquationBatchProcessor()
    equations = processor.generate_sample_equations(count=count, difficulty=difficulty)
    
    return JsonResponse({
        'equations': equations,
        'count': len(equations),
        'difficulty': difficulty
    })


@require_http_methods(["GET"])
def export_equations(request):
    """Export equations to various formats"""
    format_type = request.GET.get('format', 'json')
    
    exporter = EquationExporter()
    
    if format_type == 'json':
        data = exporter.export_to_json()
        response = JsonResponse(data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="{data["filename"]}"'
        return response
        
    elif format_type == 'csv':
        data = exporter.export_to_csv()
        
        # Convert to CSV string
        csv_content = '\n'.join([','.join(map(str, row)) for row in data['data']])
        
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{data["filename"]}"'
        return response
        
    else:
        return JsonResponse({'error': 'Invalid format. Use json or csv'}, status=400)


@require_http_methods(["GET"])
def equation_insights(request):
    """Get insights and recommendations based on equation patterns"""
    analytics = EquationAnalytics()
    stats = analytics.get_equation_statistics()
    patterns = analytics.get_equation_patterns()
    complexity = analytics.get_equation_complexity_analysis()
    
    insights = []
    
    # Analyze patterns and provide insights
    if stats['total_equations'] > 0:
        real_roots_percentage = (stats['real_roots_count'] / stats['total_equations']) * 100
        
        if real_roots_percentage > 70:
            insights.append({
                'type': 'pattern',
                'title': 'High Real Roots Percentage',
                'description': f'{real_roots_percentage:.1f}% of equations have real roots. This suggests users prefer equations with real solutions.',
                'recommendation': 'Consider adding more complex equations with imaginary roots for educational purposes.'
            })
        
        if complexity['simple'] > complexity['complex']:
            insights.append({
                'type': 'complexity',
                'title': 'Preference for Simple Equations',
                'description': f'Users solve {complexity["simple"]} simple equations vs {complexity["complex"]} complex ones.',
                'recommendation': 'Gradually introduce more complex equations to challenge users.'
            })
        
        if len(patterns['perfect_squares']) > 0:
            insights.append({
                'type': 'educational',
                'title': 'Perfect Square Equations Detected',
                'description': f'Found {len(patterns["perfect_squares"])} perfect square equations.',
                'recommendation': 'Highlight these as special cases for educational content.'
            })
    
    return JsonResponse({
        'insights': insights,
        'total_insights': len(insights),
        'generated_at': analytics.get_equation_statistics().get('total_equations', 0)
    })


@require_http_methods(["GET"])
def equation_comparison(request):
    """Compare multiple equations and find relationships"""
    try:
        # Get equation IDs from query parameters
        equation_ids = request.GET.getlist('ids')
        
        if len(equation_ids) < 2:
            return JsonResponse({'error': 'At least 2 equation IDs required'}, status=400)
        
        from .models import QuadraticEquation
        equations = QuadraticEquation.objects.filter(id__in=equation_ids)
        
        if len(equations) != len(equation_ids):
            return JsonResponse({'error': 'Some equation IDs not found'}, status=404)
        
        comparison_data = []
        for eq in equations:
            comparison_data.append({
                'id': eq.id,
                'equation': eq.get_equation_string(),
                'discriminant': eq.discriminant,
                'roots_type': eq.get_roots_type(),
                'vertex': [eq.vertex_x, eq.vertex_y],
                'direction': eq.get_direction(),
                'coefficients': {'a': eq.a, 'b': eq.b, 'c': eq.c}
            })
        
        # Find relationships
        relationships = []
        
        # Check for similar discriminants
        discriminants = [eq.discriminant for eq in equations]
        if len(set(discriminants)) < len(discriminants):
            relationships.append({
                'type': 'discriminant',
                'description': 'Multiple equations have the same discriminant',
                'equations': [eq.id for eq in equations if discriminants.count(eq.discriminant) > 1]
            })
        
        # Check for same direction
        directions = [eq.get_direction() for eq in equations]
        if len(set(directions)) == 1:
            relationships.append({
                'type': 'direction',
                'description': f'All equations open {directions[0]}',
                'equations': [eq.id for eq in equations]
            })
        
        return JsonResponse({
            'equations': comparison_data,
            'relationships': relationships,
            'total_compared': len(equations)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def calculate_intersections(request):
    """Calculate intersection points between equations"""
    try:
        data = json.loads(request.body)
        equations = data.get('equations', [])
        
        if len(equations) < 2:
            return JsonResponse({'error': 'At least 2 equations required'}, status=400)
        
        calculator = EquationIntersectionCalculator()
        
        if len(equations) == 2:
            # Calculate intersections between two equations
            result = calculator.find_intersections(equations[0], equations[1])
        else:
            # Calculate intersections between multiple equations
            result = calculator.find_multiple_intersections(equations)
            # Add pattern analysis
            result['pattern_analysis'] = calculator.analyze_intersection_patterns(equations)
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def solve_equation_api(request):
    """Standalone API endpoint for solving quadratic equations"""
    try:
        data = json.loads(request.body)
        a = data.get('a')
        b = data.get('b')
        c = data.get('c')
        
        if a is None or b is None or c is None:
            return JsonResponse({'error': 'Missing coefficients a, b, or c'}, status=400)
        
        try:
            a, b, c = float(a), float(b), float(c)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid coefficient values'}, status=400)
        
        if a == 0:
            return JsonResponse({'error': 'Coefficient a cannot be zero'}, status=400)
        
        # Import here to avoid circular imports
        from .quadratic_solver import QuadraticEquationSolver
        solver = QuadraticEquationSolver(a, b, c)
        
        result = {
            'equation': f"{a}x² + {b}x + {c} = 0",
            'coefficients': {'a': a, 'b': b, 'c': c},
            'discriminant': solver.get_discriminant(),
            'roots': solver.get_roots(),
            'vertex': solver.get_vertex(),
            'axis_of_symmetry': solver.get_axis_of_symmetry(),
            'direction': solver.get_direction(),
            'roots_type': solver.get_roots_type(),
            'discriminant_info': solver.get_discriminant_info(),
            'solved_at': datetime.now().isoformat()
        }
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
