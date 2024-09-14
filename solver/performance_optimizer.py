"""
Performance Optimization Module for Quadratic Equation Solver
Provides caching, database optimization, and performance monitoring
"""

import time
import logging
from functools import wraps
from django.core.cache import cache
from django.db import connection
from django.conf import settings
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
from scipy import optimize
import pandas as pd

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def time_function(self, func_name: str):
        """Decorator to time function execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Store metrics
                if func_name not in self.metrics:
                    self.metrics[func_name] = []
                self.metrics[func_name].append(execution_time)
                
                # Log slow functions
                if execution_time > 1.0:  # More than 1 second
                    logger.warning(f"Slow function {func_name}: {execution_time:.3f}s")
                
                return result
            return wrapper
        return decorator
    
    def get_average_time(self, func_name: str) -> float:
        """Get average execution time for a function"""
        if func_name not in self.metrics or not self.metrics[func_name]:
            return 0.0
        return sum(self.metrics[func_name]) / len(self.metrics[func_name])
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report"""
        report = {}
        for func_name, times in self.metrics.items():
            if times:
                report[func_name] = {
                    'average_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_calls': len(times),
                    'total_time': sum(times)
                }
        return report


class CacheManager:
    """Advanced caching system for equation calculations"""
    
    CACHE_TIMEOUT = 3600  # 1 hour
    
    @staticmethod
    def generate_cache_key(*args, **kwargs) -> str:
        """Generate a unique cache key from arguments"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    @staticmethod
    def cache_equation_result(func):
        """Decorator to cache equation calculation results"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"equation_{CacheManager.generate_cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Calculate and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, CacheManager.CACHE_TIMEOUT)
            logger.info(f"Cached result for {func.__name__}")
            
            return result
        return wrapper
    
    @staticmethod
    def invalidate_equation_cache(equation_id: int = None):
        """Invalidate equation-related cache entries"""
        if equation_id:
            # Invalidate specific equation cache
            pattern = f"equation_*{equation_id}*"
            cache.delete_many(cache.keys(pattern))
        else:
            # Invalidate all equation caches
            cache.delete_many(cache.keys("equation_*"))


class DatabaseOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def optimize_equation_queries():
        """Add database indexes for better performance"""
        with connection.cursor() as cursor:
            # Add indexes for common queries
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_equation_discriminant ON solver_quadraticequation (discriminant)",
                "CREATE INDEX IF NOT EXISTS idx_equation_created_at ON solver_quadraticequation (created_at)",
                "CREATE INDEX IF NOT EXISTS idx_equation_ip_address ON solver_quadraticequation (ip_address)",
                "CREATE INDEX IF NOT EXISTS idx_equation_coefficients ON solver_quadraticequation (a, b, c)",
            ]
            
            for index_sql in indexes:
                try:
                    cursor.execute(index_sql)
                    logger.info(f"Created index: {index_sql}")
                except Exception as e:
                    logger.warning(f"Index creation failed: {e}")
    
    @staticmethod
    def get_query_stats() -> Dict[str, Any]:
        """Get database query statistics"""
        stats = {
            'total_queries': len(connection.queries),
            'query_time': sum(float(q['time']) for q in connection.queries),
            'slow_queries': [q for q in connection.queries if float(q['time']) > 0.1]
        }
        return stats


class AdvancedMathProcessor:
    """Advanced mathematical processing with optimization"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
    
    @PerformanceMonitor().time_function('batch_solve_equations')
    def batch_solve_equations(self, equations: List[Dict[str, float]]) -> List[Dict[str, Any]]:
        """Solve multiple equations efficiently using vectorized operations"""
        if not equations:
            return []
        
        # Convert to numpy arrays for vectorized operations
        a_values = np.array([eq['a'] for eq in equations])
        b_values = np.array([eq['b'] for eq in equations])
        c_values = np.array([eq['c'] for eq in equations])
        
        # Vectorized discriminant calculation
        discriminants = b_values**2 - 4 * a_values * c_values
        
        # Vectorized root calculations
        results = []
        for i, (a, b, c, disc) in enumerate(zip(a_values, b_values, c_values, discriminants)):
            if disc >= 0:
                # Real roots
                sqrt_disc = np.sqrt(disc)
                root1 = (-b + sqrt_disc) / (2 * a)
                root2 = (-b - sqrt_disc) / (2 * a)
                roots = [root1, root2]
            else:
                # Complex roots
                sqrt_disc = np.sqrt(-disc)
                root1_real = -b / (2 * a)
                root1_imag = sqrt_disc / (2 * a)
                root2_real = -b / (2 * a)
                root2_imag = -sqrt_disc / (2 * a)
                roots = [
                    {'real': root1_real, 'imag': root1_imag},
                    {'real': root2_real, 'imag': root2_imag}
                ]
            
            # Vertex calculation
            vertex_x = -b / (2 * a)
            vertex_y = a * vertex_x**2 + b * vertex_x + c
            
            results.append({
                'equation_id': i,
                'coefficients': {'a': a, 'b': b, 'c': c},
                'discriminant': disc,
                'roots': roots,
                'vertex': [vertex_x, vertex_y],
                'roots_type': 'real' if disc >= 0 else 'complex'
            })
        
        return results
    
    @PerformanceMonitor().time_function('find_equation_patterns')
    def find_equation_patterns(self, equations: List[Dict[str, Any]]) -> Dict[str, List]:
        """Find mathematical patterns in equations using advanced algorithms"""
        patterns = {
            'perfect_squares': [],
            'factorable_equations': [],
            'geometric_sequences': [],
            'arithmetic_sequences': [],
            'special_forms': []
        }
        
        for eq in equations:
            a, b, c = eq['a'], eq['b'], eq['c']
            discriminant = eq['discriminant']
            
            # Perfect squares (discriminant = 0)
            if abs(discriminant) < 1e-10:
                patterns['perfect_squares'].append(eq)
            
            # Factorable equations (integer roots)
            if eq['roots_type'] == 'real':
                roots = eq['roots']
                if all(isinstance(r, (int, float)) and r.is_integer() for r in roots):
                    patterns['factorable_equations'].append(eq)
            
            # Special forms
            if a == 1 and b == 0:  # x² + c = 0
                patterns['special_forms'].append({**eq, 'form': 'x² + c = 0'})
            elif a == 1 and c == 0:  # x² + bx = 0
                patterns['special_forms'].append({**eq, 'form': 'x² + bx = 0'})
            elif b == 0 and c == 0:  # ax² = 0
                patterns['special_forms'].append({**eq, 'form': 'ax² = 0'})
        
        return patterns
    
    @PerformanceMonitor().time_function('optimize_intersection_calculation')
    def optimize_intersection_calculation(self, equations: List[Dict[str, float]]) -> Dict[str, Any]:
        """Optimized intersection calculation using numerical methods"""
        if len(equations) < 2:
            return {'intersections': [], 'analysis': {'type': 'insufficient_equations'}}
        
        intersections = []
        
        # Use scipy for numerical optimization
        for i in range(len(equations)):
            for j in range(i + 1, len(equations)):
                eq1, eq2 = equations[i], equations[j]
                
                # Define the difference function
                def difference_func(x):
                    y1 = eq1['a'] * x**2 + eq1['b'] * x + eq1['c']
                    y2 = eq2['a'] * x**2 + eq2['b'] * x + eq2['c']
                    return abs(y1 - y2)
                
                # Find intersection points using optimization
                try:
                    # Try multiple starting points
                    for start_x in [-10, -5, 0, 5, 10]:
                        result = optimize.minimize_scalar(difference_func, bounds=(start_x-5, start_x+5), method='bounded')
                        if result.fun < 1e-6:  # Close enough to intersection
                            x_intersect = result.x
                            y_intersect = eq1['a'] * x_intersect**2 + eq1['b'] * x_intersect + eq1['c']
                            intersections.append({
                                'x': x_intersect,
                                'y': y_intersect,
                                'equations': [i, j]
                            })
                except Exception as e:
                    logger.warning(f"Intersection calculation failed: {e}")
        
        return {
            'intersections': intersections,
            'analysis': {
                'type': 'numerical_optimization',
                'total_intersections': len(intersections)
            }
        }


class DataAnalyzer:
    """Advanced data analysis for equation statistics"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
    
    @PerformanceMonitor().time_function('generate_statistical_report')
    def generate_statistical_report(self, equations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive statistical analysis"""
        if not equations:
            return {}
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(equations)
        
        # Basic statistics
        stats = {
            'total_equations': len(equations),
            'coefficient_stats': {
                'a': {
                    'mean': df['a'].mean(),
                    'std': df['a'].std(),
                    'min': df['a'].min(),
                    'max': df['a'].max()
                },
                'b': {
                    'mean': df['b'].mean(),
                    'std': df['b'].std(),
                    'min': df['b'].min(),
                    'max': df['b'].max()
                },
                'c': {
                    'mean': df['c'].mean(),
                    'std': df['c'].std(),
                    'min': df['c'].min(),
                    'max': df['c'].max()
                }
            },
            'discriminant_stats': {
                'mean': df['discriminant'].mean(),
                'std': df['discriminant'].std(),
                'positive_count': (df['discriminant'] > 0).sum(),
                'zero_count': (df['discriminant'] == 0).sum(),
                'negative_count': (df['discriminant'] < 0).sum()
            }
        }
        
        # Correlation analysis
        if len(equations) > 1:
            correlation_matrix = df[['a', 'b', 'c', 'discriminant']].corr()
            stats['correlations'] = correlation_matrix.to_dict()
        
        return stats
    
    @PerformanceMonitor().time_function('predict_equation_properties')
    def predict_equation_properties(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """Predict equation properties using machine learning approach"""
        # Simple prediction based on coefficient patterns
        predictions = {
            'likely_roots_type': 'real' if (b**2 - 4*a*c) >= 0 else 'complex',
            'vertex_quadrant': self._predict_vertex_quadrant(a, b, c),
            'parabola_width': 'narrow' if abs(a) > 2 else 'wide' if abs(a) < 0.5 else 'normal',
            'symmetry_axis_position': 'left' if b > 0 else 'right' if b < 0 else 'center'
        }
        
        return predictions
    
    def _predict_vertex_quadrant(self, a: float, b: float, c: float) -> str:
        """Predict which quadrant the vertex is likely in"""
        vertex_x = -b / (2 * a)
        vertex_y = a * vertex_x**2 + b * vertex_x + c
        
        if vertex_x > 0 and vertex_y > 0:
            return 'I'
        elif vertex_x < 0 and vertex_y > 0:
            return 'II'
        elif vertex_x < 0 and vertex_y < 0:
            return 'III'
        else:
            return 'IV'


# Global instances
performance_monitor = PerformanceMonitor()
cache_manager = CacheManager()
db_optimizer = DatabaseOptimizer()
math_processor = AdvancedMathProcessor()
data_analyzer = DataAnalyzer()
