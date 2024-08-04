"""
Equation Intersection Calculator
Calculates intersection points between quadratic equations
"""

import numpy as np
from typing import List, Tuple, Dict, Any
import json


class EquationIntersectionCalculator:
    """Calculate intersection points between quadratic equations"""
    
    def __init__(self):
        pass
    
    def find_intersections(self, eq1: Dict[str, float], eq2: Dict[str, float]) -> Dict[str, Any]:
        """
        Find intersection points between two quadratic equations
        
        Args:
            eq1: First equation coefficients {'a': float, 'b': float, 'c': float}
            eq2: Second equation coefficients {'a': float, 'b': float, 'c': float}
        
        Returns:
            Dictionary with intersection information
        """
        a1, b1, c1 = eq1['a'], eq1['b'], eq1['c']
        a2, b2, c2 = eq2['a'], eq2['b'], eq2['c']
        
        # Calculate the difference equation: (a1-a2)x² + (b1-b2)x + (c1-c2) = 0
        diff_a = a1 - a2
        diff_b = b1 - b2
        diff_c = c1 - c2
        
        result = {
            'equation1': f"{a1}x² + {b1}x + {c1} = 0",
            'equation2': f"{a2}x² + {b2}x + {c2} = 0",
            'difference_equation': f"{diff_a}x² + {diff_b}x + {diff_c} = 0",
            'intersections': [],
            'intersection_count': 0,
            'analysis': {}
        }
        
        # Case 1: Both equations are identical
        if diff_a == 0 and diff_b == 0 and diff_c == 0:
            result['analysis']['type'] = 'identical'
            result['analysis']['description'] = 'The equations are identical - infinite intersections'
            result['intersection_count'] = float('inf')
            return result
        
        # Case 2: Linear difference (diff_a = 0)
        if diff_a == 0:
            if diff_b == 0:
                # No intersections (parallel lines)
                result['analysis']['type'] = 'no_intersection'
                result['analysis']['description'] = 'No intersections - equations are parallel'
                result['intersection_count'] = 0
            else:
                # One intersection (linear equation)
                x = -diff_c / diff_b
                y = a1 * x**2 + b1 * x + c1
                result['intersections'].append({
                    'x': x,
                    'y': y,
                    'type': 'linear_intersection'
                })
                result['intersection_count'] = 1
                result['analysis']['type'] = 'linear'
                result['analysis']['description'] = 'One intersection - linear difference'
        
        # Case 3: Quadratic difference (diff_a ≠ 0)
        else:
            # Use quadratic formula on difference equation
            discriminant = diff_b**2 - 4 * diff_a * diff_c
            
            if discriminant < 0:
                # No real intersections
                result['analysis']['type'] = 'no_real_intersection'
                result['analysis']['description'] = 'No real intersections - complex roots'
                result['intersection_count'] = 0
                result['analysis']['discriminant'] = discriminant
                
            elif discriminant == 0:
                # One intersection (tangent)
                x = -diff_b / (2 * diff_a)
                y = a1 * x**2 + b1 * x + c1
                result['intersections'].append({
                    'x': x,
                    'y': y,
                    'type': 'tangent'
                })
                result['intersection_count'] = 1
                result['analysis']['type'] = 'tangent'
                result['analysis']['description'] = 'One intersection - equations are tangent'
                result['analysis']['discriminant'] = discriminant
                
            else:
                # Two intersections
                sqrt_discriminant = np.sqrt(discriminant)
                x1 = (-diff_b + sqrt_discriminant) / (2 * diff_a)
                x2 = (-diff_b - sqrt_discriminant) / (2 * diff_a)
                
                y1 = a1 * x1**2 + b1 * x1 + c1
                y2 = a1 * x2**2 + b1 * x2 + c1
                
                result['intersections'].extend([
                    {
                        'x': x1,
                        'y': y1,
                        'type': 'quadratic_intersection'
                    },
                    {
                        'x': x2,
                        'y': y2,
                        'type': 'quadratic_intersection'
                    }
                ])
                result['intersection_count'] = 2
                result['analysis']['type'] = 'two_intersections'
                result['analysis']['description'] = 'Two intersections'
                result['analysis']['discriminant'] = discriminant
        
        return result
    
    def find_multiple_intersections(self, equations: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Find all intersection points between multiple equations
        
        Args:
            equations: List of equation coefficients
        
        Returns:
            Dictionary with all intersection information
        """
        n = len(equations)
        all_intersections = []
        intersection_pairs = []
        
        # Find intersections between all pairs
        for i in range(n):
            for j in range(i + 1, n):
                pair_result = self.find_intersections(equations[i], equations[j])
                
                intersection_pairs.append({
                    'equation1_index': i,
                    'equation2_index': j,
                    'equation1': pair_result['equation1'],
                    'equation2': pair_result['equation2'],
                    'intersections': pair_result['intersections'],
                    'count': pair_result['intersection_count'],
                    'analysis': pair_result['analysis']
                })
                
                # Add intersections to master list
                for intersection in pair_result['intersections']:
                    intersection['pair'] = f"Eq{i+1} & Eq{j+1}"
                    all_intersections.append(intersection)
        
        # Remove duplicate intersections (within tolerance)
        unique_intersections = self._remove_duplicate_intersections(all_intersections)
        
        return {
            'total_equations': n,
            'total_pairs': len(intersection_pairs),
            'all_intersections': unique_intersections,
            'intersection_pairs': intersection_pairs,
            'unique_intersection_count': len(unique_intersections)
        }
    
    def _remove_duplicate_intersections(self, intersections: List[Dict], tolerance: float = 1e-6) -> List[Dict]:
        """Remove duplicate intersections within tolerance"""
        unique = []
        
        for intersection in intersections:
            is_duplicate = False
            for existing in unique:
                if (abs(intersection['x'] - existing['x']) < tolerance and 
                    abs(intersection['y'] - existing['y']) < tolerance):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(intersection)
        
        return unique
    
    def analyze_intersection_patterns(self, equations: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Analyze patterns in equation intersections
        
        Args:
            equations: List of equation coefficients
        
        Returns:
            Analysis of intersection patterns
        """
        intersection_data = self.find_multiple_intersections(equations)
        
        analysis = {
            'total_equations': len(equations),
            'intersection_summary': {},
            'common_intersections': [],
            'patterns': []
        }
        
        # Count intersection types
        type_counts = {}
        for pair in intersection_data['intersection_pairs']:
            intersection_type = pair['analysis']['type']
            type_counts[intersection_type] = type_counts.get(intersection_type, 0) + 1
        
        analysis['intersection_summary'] = type_counts
        
        # Find common intersection points
        intersection_counts = {}
        for intersection in intersection_data['all_intersections']:
            key = (round(intersection['x'], 3), round(intersection['y'], 3))
            intersection_counts[key] = intersection_counts.get(key, 0) + 1
        
        # Find points where multiple equations intersect
        for point, count in intersection_counts.items():
            if count > 1:
                analysis['common_intersections'].append({
                    'x': point[0],
                    'y': point[1],
                    'equation_count': count
                })
        
        # Identify patterns
        if len(analysis['common_intersections']) > 0:
            analysis['patterns'].append({
                'type': 'concurrent_intersections',
                'description': f"Found {len(analysis['common_intersections'])} points where multiple equations intersect"
            })
        
        if type_counts.get('tangent', 0) > 0:
            analysis['patterns'].append({
                'type': 'tangent_equations',
                'description': f"{type_counts['tangent']} pairs of equations are tangent to each other"
            })
        
        return analysis
    
    def generate_intersection_report(self, equations: List[Dict[str, float]]) -> str:
        """
        Generate a human-readable report of intersections
        
        Args:
            equations: List of equation coefficients
        
        Returns:
            Formatted report string
        """
        intersection_data = self.find_multiple_intersections(equations)
        analysis = self.analyze_intersection_patterns(equations)
        
        report = f"""
INTERSECTION ANALYSIS REPORT
============================

Total Equations: {len(equations)}
Total Pairs Analyzed: {intersection_data['total_pairs']}
Unique Intersection Points: {intersection_data['unique_intersection_count']}

INTERSECTION SUMMARY:
"""
        
        for pair in intersection_data['intersection_pairs']:
            report += f"\n{pair['equation1']} & {pair['equation2']}"
            report += f"\n  Type: {pair['analysis']['description']}"
            report += f"\n  Intersections: {pair['count']}"
            
            for intersection in pair['intersections']:
                report += f"\n    Point: ({intersection['x']:.3f}, {intersection['y']:.3f})"
        
        if analysis['common_intersections']:
            report += f"\n\nCOMMON INTERSECTION POINTS:"
            for point in analysis['common_intersections']:
                report += f"\n  ({point['x']:.3f}, {point['y']:.3f}) - {point['equation_count']} equations"
        
        if analysis['patterns']:
            report += f"\n\nPATTERNS DETECTED:"
            for pattern in analysis['patterns']:
                report += f"\n  - {pattern['description']}"
        
        return report
