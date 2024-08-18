from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import QuadraticEquation
from .quadratic_solver import QuadraticEquationSolver
import json
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

class QuadraticSolverView(View):
    """Main view for quadratic equation solver."""
    
    def get(self, request):
        """Display the solver form."""
        recent_equations = QuadraticEquation.objects.all()[:10]
        return render(request, 'solver/index.html', {
            'recent_equations': recent_equations
        })
    
    def post(self, request):
        """Process the equation solving request."""
        try:
            a = float(request.POST.get('a', 0))
            b = float(request.POST.get('b', 0))
            c = float(request.POST.get('c', 0))
            
            if a == 0:
                return JsonResponse({
                    'error': 'Coefficient "a" cannot be zero for a quadratic equation'
                }, status=400)
            
            # Solve the equation
            solver = QuadraticEquationSolver(a, b, c)
            result = solver.solve()
            
            # Save to database
            equation = QuadraticEquation.objects.create(
                a=a, b=b, c=c,
                discriminant=result['discriminant'],
                root1=result['root1'].real if hasattr(result['root1'], 'real') else result['root1'],
                root2=result['root2'].real if hasattr(result['root2'], 'real') else result['root2'],
                root1_imag=result['root1'].imag if hasattr(result['root1'], 'imag') else 0,
                root2_imag=result['root2'].imag if hasattr(result['root2'], 'imag') else 0,
                vertex_x=result['vertex'][0],
                vertex_y=result['vertex'][1],
                ip_address=self.get_client_ip(request)
            )
            
            # Generate plot
            plot_data = self.generate_plot(solver, result)
            
            return JsonResponse({
                'success': True,
                'equation': equation.get_equation_string(),
                'discriminant': result['discriminant'],
                'roots_type': result['roots_type'],
                'direction': result['direction'],
                'vertex': result['vertex'],
                'axis_of_symmetry': result['axis_of_symmetry'],
                'roots': result['roots'],
                'plot': plot_data,
                'equation_id': equation.id
            })
            
        except ValueError as e:
            return JsonResponse({
                'error': 'Please enter valid numbers for all coefficients'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': f'An error occurred: {str(e)}'
            }, status=500)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def generate_plot(self, solver, result):
        """Generate base64 encoded plot."""
        try:
            # Create plot
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Calculate x range
            vertex_x = result['vertex'][0]
            x_min = vertex_x - 5
            x_max = vertex_x + 5
            x = np.linspace(x_min, x_max, 1000)
            y = solver.a * x**2 + solver.b * x + solver.c
            
            # Plot the function
            ax.plot(x, y, 'b-', linewidth=2, label=f'y = {solver.format_equation()}')
            
            # Plot real roots
            for root in result['roots']:
                if isinstance(root, complex):
                    if root.imag == 0 and x_min <= root.real <= x_max:
                        ax.scatter(root.real, 0, color='red', s=100, zorder=5)
                else:
                    if x_min <= root <= x_max:
                        ax.scatter(root, 0, color='red', s=100, zorder=5)
            
            # Plot vertex
            vertex_x, vertex_y = result['vertex']
            if x_min <= vertex_x <= x_max:
                ax.scatter(vertex_x, vertex_y, color='green', s=100, 
                          marker='^', zorder=5, label=f'Vertex: ({vertex_x:.2f}, {vertex_y:.2f})')
            
            # Add axis lines
            ax.axhline(0, color='black', linewidth=0.8, alpha=0.7)
            ax.axvline(0, color='black', linewidth=0.8, alpha=0.7)
            
            # Set limits
            y_min, y_max = min(y), max(y)
            y_padding = (y_max - y_min) * 0.1
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min - y_padding, y_max + y_padding)
            
            # Styling
            ax.set_title(f'Graph: {solver.format_equation()}', fontsize=14, fontweight='bold')
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.getvalue()).decode()
            plt.close(fig)
            
            return plot_data
            
        except Exception as e:
            return None

def equation_history(request):
    """View for displaying equation history."""
    equations = QuadraticEquation.objects.all()[:50]
    return render(request, 'solver/history.html', {
        'equations': equations
    })

def equation_detail(request, equation_id):
    """View for displaying detailed equation information."""
    try:
        equation = QuadraticEquation.objects.get(id=equation_id)
        return render(request, 'solver/detail.html', {
            'equation': equation
        })
    except QuadraticEquation.DoesNotExist:
        return render(request, 'solver/404.html', status=404)
