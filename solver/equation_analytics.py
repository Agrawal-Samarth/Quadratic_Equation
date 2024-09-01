"""
Advanced Equation Analytics Module
Provides statistical analysis and insights for quadratic equations
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.db.models import Count, Avg, Q
from .models import QuadraticEquation
import json
from collections import defaultdict


class EquationAnalytics:
    """Advanced analytics for quadratic equations"""
    
    def __init__(self):
        self.equations = QuadraticEquation.objects.all()
    
    def get_equation_statistics(self):
        """Get comprehensive statistics about solved equations"""
        total_equations = self.equations.count()
        
        if total_equations == 0:
            return {"error": "No equations found"}
        
        # Basic statistics
        stats = {
            "total_equations": total_equations,
            "real_roots_count": self.equations.filter(discriminant__gte=0).count(),
            "complex_roots_count": self.equations.filter(discriminant__lt=0).count(),
            "perfect_squares": self.equations.filter(discriminant=0).count(),
            "upward_parabolas": self.equations.filter(a__gt=0).count(),
            "downward_parabolas": self.equations.filter(a__lt=0).count(),
        }
        
        # Coefficient statistics
        stats.update({
            "avg_coefficient_a": float(self.equations.aggregate(avg=Avg('a'))['avg'] or 0),
            "avg_coefficient_b": float(self.equations.aggregate(avg=Avg('b'))['avg'] or 0),
            "avg_coefficient_c": float(self.equations.aggregate(avg=Avg('c'))['avg'] or 0),
            "avg_discriminant": float(self.equations.aggregate(avg=Avg('discriminant'))['avg'] or 0),
        })
        
        # Recent activity
        last_24h = datetime.now() - timedelta(days=1)
        stats["recent_equations"] = self.equations.filter(created_at__gte=last_24h).count()
        
        return stats
    
    def get_coefficient_distribution(self):
        """Analyze distribution of coefficients"""
        a_values = [eq.a for eq in self.equations]
        b_values = [eq.b for eq in self.equations]
        c_values = [eq.c for eq in self.equations]
        
        return {
            "a_distribution": {
                "min": min(a_values) if a_values else 0,
                "max": max(a_values) if a_values else 0,
                "mean": np.mean(a_values) if a_values else 0,
                "std": np.std(a_values) if a_values else 0,
            },
            "b_distribution": {
                "min": min(b_values) if b_values else 0,
                "max": max(b_values) if b_values else 0,
                "mean": np.mean(b_values) if b_values else 0,
                "std": np.std(b_values) if b_values else 0,
            },
            "c_distribution": {
                "min": min(c_values) if c_values else 0,
                "max": max(c_values) if c_values else 0,
                "mean": np.mean(c_values) if c_values else 0,
                "std": np.std(c_values) if c_values else 0,
            }
        }
    
    def get_equation_patterns(self):
        """Identify common patterns in equations"""
        patterns = {
            "perfect_squares": [],
            "factorable_equations": [],
            "integer_coefficients": [],
            "decimal_coefficients": [],
        }
        
        for eq in self.equations:
            # Perfect squares (discriminant = 0)
            if eq.discriminant == 0:
                patterns["perfect_squares"].append({
                    "id": eq.id,
                    "equation": eq.get_equation_string(),
                    "root": eq.root1_real if eq.root1_real else 0
                })
            
            # Factorable equations (integer roots)
            if eq.root1_real and eq.root1_imag == 0 and eq.root2_real and eq.root2_imag == 0:
                if eq.root1_real.is_integer() and eq.root2_real.is_integer():
                    patterns["factorable_equations"].append({
                        "id": eq.id,
                        "equation": eq.get_equation_string(),
                        "roots": [eq.root1_real, eq.root2_real]
                    })
            
            # Integer vs decimal coefficients
            if eq.a.is_integer() and eq.b.is_integer() and eq.c.is_integer():
                patterns["integer_coefficients"].append(eq.id)
            else:
                patterns["decimal_coefficients"].append(eq.id)
        
        return patterns
    
    def get_usage_trends(self, days=30):
        """Analyze usage trends over time"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        daily_counts = defaultdict(int)
        for eq in self.equations.filter(created_at__gte=start_date):
            date_key = eq.created_at.date()
            daily_counts[date_key] += 1
        
        # Convert to list format for JSON serialization
        trends = []
        current_date = start_date.date()
        while current_date <= end_date.date():
            trends.append({
                "date": current_date.isoformat(),
                "count": daily_counts[current_date]
            })
            current_date += timedelta(days=1)
        
        return trends
    
    def get_equation_complexity_analysis(self):
        """Analyze complexity of equations"""
        complexity_data = {
            "simple": 0,      # a=1, small integers
            "moderate": 0,    # a≠1, integers
            "complex": 0,     # decimals, large numbers
        }
        
        for eq in self.equations:
            if eq.a == 1 and abs(eq.b) <= 10 and abs(eq.c) <= 10:
                complexity_data["simple"] += 1
            elif eq.a.is_integer() and eq.b.is_integer() and eq.c.is_integer():
                complexity_data["moderate"] += 1
            else:
                complexity_data["complex"] += 1
        
        return complexity_data
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "statistics": self.get_equation_statistics(),
            "coefficient_distribution": self.get_coefficient_distribution(),
            "patterns": self.get_equation_patterns(),
            "usage_trends": self.get_usage_trends(),
            "complexity_analysis": self.get_equation_complexity_analysis(),
        }
        
        return report


class EquationBatchProcessor:
    """Process multiple equations in batch"""
    
    def __init__(self):
        self.solver = None  # Will be imported to avoid circular imports
    
    def process_equation_list(self, equations_list):
        """Process a list of equations"""
        results = []
        errors = []
        
        for i, eq_data in enumerate(equations_list):
            try:
                a, b, c = eq_data['a'], eq_data['b'], eq_data['c']
                
                # Import here to avoid circular imports
                from .quadratic_solver import QuadraticEquationSolver
                solver = QuadraticEquationSolver(a, b, c)
                
                result = {
                    "index": i,
                    "equation": f"{a}x² + {b}x + {c} = 0",
                    "discriminant": solver.get_discriminant(),
                    "roots": solver.get_roots(),
                    "vertex": solver.get_vertex(),
                    "roots_type": solver.get_roots_type(),
                    "direction": solver.get_direction(),
                }
                results.append(result)
                
            except Exception as e:
                errors.append({
                    "index": i,
                    "equation": eq_data,
                    "error": str(e)
                })
        
        return {
            "successful": results,
            "errors": errors,
            "total_processed": len(equations_list),
            "success_rate": len(results) / len(equations_list) * 100 if equations_list else 0
        }
    
    def generate_sample_equations(self, count=10, difficulty="mixed"):
        """Generate sample equations for testing"""
        import random
        
        equations = []
        
        for _ in range(count):
            if difficulty == "easy":
                a = random.choice([1, -1])
                b = random.randint(-10, 10)
                c = random.randint(-10, 10)
            elif difficulty == "hard":
                a = round(random.uniform(-5, 5), 1)
                while a == 0:
                    a = round(random.uniform(-5, 5), 1)
                b = round(random.uniform(-10, 10), 1)
                c = round(random.uniform(-10, 10), 1)
            else:  # mixed
                if random.choice([True, False]):
                    a = random.choice([1, -1])
                    b = random.randint(-10, 10)
                    c = random.randint(-10, 10)
                else:
                    a = round(random.uniform(-3, 3), 1)
                    while a == 0:
                        a = round(random.uniform(-3, 3), 1)
                    b = round(random.uniform(-8, 8), 1)
                    c = round(random.uniform(-8, 8), 1)
            
            equations.append({"a": a, "b": b, "c": c})
        
        return equations


class EquationExporter:
    """Export equations and results to various formats"""
    
    def __init__(self):
        self.equations = QuadraticEquation.objects.all()
    
    def export_to_json(self, filename=None):
        """Export equations to JSON format"""
        if not filename:
            filename = f"equations_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = []
        for eq in self.equations:
            data.append({
                "id": eq.id,
                "equation": eq.get_equation_string(),
                "coefficients": {"a": eq.a, "b": eq.b, "c": eq.c},
                "discriminant": eq.discriminant,
                "roots": {
                    "root1": {"real": eq.root1_real, "imag": eq.root1_imag},
                    "root2": {"real": eq.root2_real, "imag": eq.root2_imag}
                },
                "vertex": {"x": eq.vertex_x, "y": eq.vertex_y},
                "roots_type": eq.get_roots_type(),
                "direction": eq.get_direction(),
                "created_at": eq.created_at.isoformat(),
                "ip_address": eq.ip_address
            })
        
        return {
            "filename": filename,
            "data": data,
            "export_date": datetime.now().isoformat(),
            "total_equations": len(data)
        }
    
    def export_to_csv(self, filename=None):
        """Export equations to CSV format"""
        if not filename:
            filename = f"equations_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        csv_data = []
        csv_data.append([
            "ID", "Equation", "A", "B", "C", "Discriminant", 
            "Root1_Real", "Root1_Imag", "Root2_Real", "Root2_Imag",
            "Vertex_X", "Vertex_Y", "Roots_Type", "Direction", "Created_At"
        ])
        
        for eq in self.equations:
            csv_data.append([
                eq.id,
                eq.get_equation_string(),
                eq.a, eq.b, eq.c,
                eq.discriminant,
                eq.root1_real, eq.root1_imag,
                eq.root2_real, eq.root2_imag,
                eq.vertex_x, eq.vertex_y,
                eq.get_roots_type(),
                eq.get_direction(),
                eq.created_at.isoformat()
            ])
        
        return {
            "filename": filename,
            "data": csv_data,
            "export_date": datetime.now().isoformat(),
            "total_equations": len(csv_data) - 1  # Subtract header row
        }
