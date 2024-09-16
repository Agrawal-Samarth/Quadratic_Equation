"""
Advanced Equation Solver with Performance Optimizations
Provides high-performance equation solving with caching and advanced algorithms
"""

import logging
import time
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from scipy import optimize, linalg
import pandas as pd
from .performance_optimizer import (
    performance_monitor, cache_manager, math_processor, data_analyzer
)
from .quadratic_solver import QuadraticEquationSolver

logger = logging.getLogger(__name__)


class AdvancedQuadraticSolver:
    """High-performance quadratic equation solver with advanced features"""
    
    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.solve_times = []
    
    @cache_manager.cache_equation_result
    @performance_monitor.time_function('solve_equation_advanced')
    def solve_equation_advanced(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """Solve quadratic equation with advanced algorithms and caching"""
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero for quadratic equation")
        
        start_time = time.time()
        
        # Use numpy for high-precision calculations
        a_np, b_np, c_np = np.float64(a), np.float64(b), np.float64(c)
        
        # Calculate discriminant with high precision
        discriminant = b_np**2 - 4 * a_np * c_np
        
        # Calculate roots using optimized algorithms
        if discriminant >= 0:
            # Real roots - use numerically stable formula
            sqrt_disc = np.sqrt(discriminant)
            if b_np >= 0:
                root1 = (-b_np - sqrt_disc) / (2 * a_np)
                root2 = (2 * c_np) / (-b_np - sqrt_disc)
            else:
                root1 = (2 * c_np) / (-b_np + sqrt_disc)
                root2 = (-b_np + sqrt_disc) / (2 * a_np)
            roots = [float(root1), float(root2)]
        else:
            # Complex roots
            sqrt_disc = np.sqrt(-discriminant)
            real_part = -b_np / (2 * a_np)
            imag_part = sqrt_disc / (2 * a_np)
            roots = [
                {'real': float(real_part), 'imag': float(imag_part)},
                {'real': float(real_part), 'imag': float(-imag_part)}
            ]
        
        # Calculate vertex
        vertex_x = -b_np / (2 * a_np)
        vertex_y = a_np * vertex_x**2 + b_np * vertex_x + c_np
        
        # Calculate axis of symmetry
        axis_of_symmetry = vertex_x
        
        # Determine direction
        direction = "upward" if a_np > 0 else "downward"
        
        # Determine roots type
        if discriminant > 0:
            roots_type = "Two distinct real roots"
        elif discriminant == 0:
            roots_type = "One repeated real root"
        else:
            roots_type = "Two complex conjugate roots"
        
        # Calculate discriminant info
        discriminant_info = self._get_discriminant_info(discriminant)
        
        # Format equation
        equation_string = self._format_equation(a, b, c)
        
        solve_time = time.time() - start_time
        self.solve_times.append(solve_time)
        
        result = {
            'equation': equation_string,
            'coefficients': {'a': a, 'b': b, 'c': c},
            'discriminant': float(discriminant),
            'roots': roots,
            'vertex': [float(vertex_x), float(vertex_y)],
            'axis_of_symmetry': float(axis_of_symmetry),
            'direction': direction,
            'roots_type': roots_type,
            'discriminant_info': discriminant_info,
            'solve_time': solve_time,
            'precision': 'high'
        }
        
        return result
    
    def _get_discriminant_info(self, discriminant: float) -> Dict[str, Any]:
        """Get detailed discriminant information"""
        if discriminant > 0:
            return {
                'type': 'positive',
                'description': 'Two distinct real roots',
                'geometric_meaning': 'Parabola intersects x-axis at two points'
            }
        elif discriminant == 0:
            return {
                'type': 'zero',
                'description': 'One repeated real root',
                'geometric_meaning': 'Parabola is tangent to x-axis'
            }
        else:
            return {
                'type': 'negative',
                'description': 'Two complex conjugate roots',
                'geometric_meaning': 'Parabola does not intersect x-axis'
            }
    
    def _format_equation(self, a: float, b: float, c: float) -> str:
        """Format equation string with proper signs"""
        terms = []
        
        # Handle x² term
        if a == 1:
            terms.append("x²")
        elif a == -1:
            terms.append("-x²")
        else:
            terms.append(f"{a}x²")
        
        # Handle x term
        if b > 0:
            if b == 1:
                terms.append("+ x")
            else:
                terms.append(f"+ {b}x")
        elif b < 0:
            if b == -1:
                terms.append("- x")
            else:
                terms.append(f"- {abs(b)}x")
        
        # Handle constant term
        if c > 0:
            terms.append(f"+ {c}")
        elif c < 0:
            terms.append(f"- {abs(c)}")
        
        return " ".join(terms) + " = 0"
    
    @performance_monitor.time_function('batch_solve_equations')
    def batch_solve_equations(self, equations: List[Dict[str, float]]) -> List[Dict[str, Any]]:
        """Solve multiple equations efficiently"""
        return math_processor.batch_solve_equations(equations)
    
    @performance_monitor.time_function('find_equation_relationships')
    def find_equation_relationships(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Find mathematical relationships between equations"""
        relationships = {
            'similar_discriminants': [],
            'parallel_parabolas': [],
            'intersecting_parabolas': [],
            'nested_parabolas': []
        }
        
        for i in range(len(equations)):
            for j in range(i + 1, len(equations)):
                eq1, eq2 = equations[i], equations[j]
                
                # Check for similar discriminants
                if abs(eq1['discriminant'] - eq2['discriminant']) < 1e-6:
                    relationships['similar_discriminants'].append([i, j])
                
                # Check for parallel parabolas (same 'a' coefficient)
                if abs(eq1['coefficients']['a'] - eq2['coefficients']['a']) < 1e-6:
                    relationships['parallel_parabolas'].append([i, j])
                
                # Check for intersecting parabolas
                intersections = self._find_intersections(eq1, eq2)
                if intersections:
                    relationships['intersecting_parabolas'].append({
                        'equations': [i, j],
                        'intersections': intersections
                    })
        
        return relationships
    
    def _find_intersections(self, eq1: Dict, eq2: Dict) -> List[Dict[str, float]]:
        """Find intersection points between two equations"""
        a1, b1, c1 = eq1['coefficients']['a'], eq1['coefficients']['b'], eq1['coefficients']['c']
        a2, b2, c2 = eq2['coefficients']['a'], eq2['coefficients']['b'], eq2['coefficients']['c']
        
        # Calculate difference equation: (a1-a2)x² + (b1-b2)x + (c1-c2) = 0
        a_diff = a1 - a2
        b_diff = b1 - b2
        c_diff = c1 - c2
        
        if abs(a_diff) < 1e-10:  # Linear case
            if abs(b_diff) < 1e-10:  # Parallel lines
                return []
            else:
                x = -c_diff / b_diff
                y = a1 * x**2 + b1 * x + c1
                return [{'x': x, 'y': y}]
        else:  # Quadratic case
            discriminant = b_diff**2 - 4 * a_diff * c_diff
            if discriminant >= 0:
                sqrt_disc = np.sqrt(discriminant)
                x1 = (-b_diff + sqrt_disc) / (2 * a_diff)
                x2 = (-b_diff - sqrt_disc) / (2 * a_diff)
                y1 = a1 * x1**2 + b1 * x1 + c1
                y2 = a1 * x2**2 + b1 * x2 + c1
                return [{'x': x1, 'y': y1}, {'x': x2, 'y': y2}]
            else:
                return []
    
    @performance_monitor.time_function('optimize_equation_parameters')
    def optimize_equation_parameters(self, target_properties: Dict[str, Any]) -> Dict[str, float]:
        """Find equation parameters that best match target properties"""
        def objective(params):
            a, b, c = params
            if a == 0:
                return float('inf')
            
            # Calculate properties
            discriminant = b**2 - 4*a*c
            vertex_x = -b / (2*a)
            vertex_y = a * vertex_x**2 + b * vertex_x + c
            
            # Calculate error
            error = 0
            if 'discriminant' in target_properties:
                error += (discriminant - target_properties['discriminant'])**2
            if 'vertex_x' in target_properties:
                error += (vertex_x - target_properties['vertex_x'])**2
            if 'vertex_y' in target_properties:
                error += (vertex_y - target_properties['vertex_y'])**2
            
            return error
        
        # Use optimization to find best parameters
        result = optimize.minimize(
            objective,
            x0=[1.0, 0.0, 0.0],
            method='BFGS',
            bounds=[(-10, 10), (-10, 10), (-10, 10)]
        )
        
        if result.success:
            a, b, c = result.x
            return {'a': a, 'b': b, 'c': c}
        else:
            return {'a': 1.0, 'b': 0.0, 'c': 0.0}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get solver performance statistics"""
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0,
            'average_solve_time': sum(self.solve_times) / len(self.solve_times) if self.solve_times else 0,
            'total_solves': len(self.solve_times),
            'performance_report': performance_monitor.get_performance_report()
        }


class EquationPatternAnalyzer:
    """Advanced pattern analysis for quadratic equations"""
    
    def __init__(self):
        self.patterns_cache = {}
    
    @performance_monitor.time_function('analyze_equation_patterns')
    def analyze_equation_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in a collection of equations"""
        patterns = {
            'coefficient_patterns': self._analyze_coefficient_patterns(equations),
            'geometric_patterns': self._analyze_geometric_patterns(equations),
            'algebraic_patterns': self._analyze_algebraic_patterns(equations),
            'statistical_patterns': self._analyze_statistical_patterns(equations)
        }
        
        return patterns
    
    def _analyze_coefficient_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in coefficients"""
        a_values = [eq['coefficients']['a'] for eq in equations]
        b_values = [eq['coefficients']['b'] for eq in equations]
        c_values = [eq['coefficients']['c'] for eq in equations]
        
        return {
            'integer_coefficients': sum(1 for a in a_values if a.is_integer()),
            'positive_a': sum(1 for a in a_values if a > 0),
            'negative_a': sum(1 for a in a_values if a < 0),
            'zero_b': sum(1 for b in b_values if b == 0),
            'zero_c': sum(1 for c in c_values if c == 0),
            'coefficient_ranges': {
                'a_range': [min(a_values), max(a_values)],
                'b_range': [min(b_values), max(b_values)],
                'c_range': [min(c_values), max(c_values)]
            }
        }
    
    def _analyze_geometric_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze geometric patterns"""
        upward_parabolas = sum(1 for eq in equations if eq['direction'] == 'upward')
        downward_parabolas = sum(1 for eq in equations if eq['direction'] == 'downward')
        
        vertex_positions = [eq['vertex'] for eq in equations]
        vertex_x_values = [v[0] for v in vertex_positions]
        vertex_y_values = [v[1] for v in vertex_positions]
        
        return {
            'upward_parabolas': upward_parabolas,
            'downward_parabolas': downward_parabolas,
            'vertex_distribution': {
                'x_range': [min(vertex_x_values), max(vertex_x_values)],
                'y_range': [min(vertex_y_values), max(vertex_y_values)],
                'quadrant_distribution': self._analyze_vertex_quadrants(vertex_positions)
            }
        }
    
    def _analyze_vertex_quadrants(self, vertices: List[List[float]]) -> Dict[str, int]:
        """Analyze distribution of vertices across quadrants"""
        quadrants = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'axes': 0}
        
        for x, y in vertices:
            if x == 0 or y == 0:
                quadrants['axes'] += 1
            elif x > 0 and y > 0:
                quadrants['I'] += 1
            elif x < 0 and y > 0:
                quadrants['II'] += 1
            elif x < 0 and y < 0:
                quadrants['III'] += 1
            else:
                quadrants['IV'] += 1
        
        return quadrants
    
    def _analyze_algebraic_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze algebraic patterns"""
        perfect_squares = sum(1 for eq in equations if abs(eq['discriminant']) < 1e-10)
        real_roots = sum(1 for eq in equations if eq['roots_type'] == 'real')
        complex_roots = sum(1 for eq in equations if eq['roots_type'] == 'complex')
        
        return {
            'perfect_squares': perfect_squares,
            'real_roots': real_roots,
            'complex_roots': complex_roots,
            'factorable_equations': self._count_factorable_equations(equations)
        }
    
    def _count_factorable_equations(self, equations: List[Dict[str, Any]]) -> int:
        """Count equations that can be factored"""
        factorable = 0
        for eq in equations:
            if eq['roots_type'] == 'real':
                roots = eq['roots']
                if all(isinstance(r, (int, float)) and r.is_integer() for r in roots):
                    factorable += 1
        return factorable
    
    def _analyze_statistical_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze statistical patterns"""
        return data_analyzer.generate_statistical_report(equations)


# Global instances
advanced_solver = AdvancedQuadraticSolver()
pattern_analyzer = EquationPatternAnalyzer()
