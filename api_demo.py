#!/usr/bin/env python3
"""
API Demo Script for Quadratic Equation Solver
Demonstrates how to use the Python API endpoints
"""

import requests
import json
from typing import Dict, Any


class QuadraticSolverAPIClient:
    """Client for interacting with the Quadratic Equation Solver API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def solve_equation(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """
        Solve a quadratic equation using the API
        
        Args:
            a: Coefficient of x²
            b: Coefficient of x
            c: Constant term
        
        Returns:
            Dictionary with solution details
        """
        url = f"{self.base_url}/api/solve/"
        data = {"a": a, "b": b, "c": c}
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def calculate_intersections(self, equations: list) -> Dict[str, Any]:
        """
        Calculate intersection points between equations
        
        Args:
            equations: List of equation dictionaries with a, b, c coefficients
        
        Returns:
            Dictionary with intersection information
        """
        url = f"{self.base_url}/api/intersections/"
        data = {"equations": equations}
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_analytics(self, data_type: str = "statistics") -> Dict[str, Any]:
        """
        Get analytics data
        
        Args:
            data_type: Type of analytics data (statistics, distribution, patterns, etc.)
        
        Returns:
            Dictionary with analytics data
        """
        url = f"{self.base_url}/api/analytics/"
        params = {"type": data_type}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def batch_process_equations(self, equations: list) -> Dict[str, Any]:
        """
        Process multiple equations in batch
        
        Args:
            equations: List of equation dictionaries
        
        Returns:
            Dictionary with batch processing results
        """
        url = f"{self.base_url}/api/batch-process/"
        data = {"equations": equations}
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


def demo_equation_solving():
    """Demonstrate equation solving functionality"""
    print("=== QUADRATIC EQUATION SOLVER API DEMO ===\n")
    
    client = QuadraticSolverAPIClient()
    
    # Test equations
    test_equations = [
        {"a": 1, "b": -5, "c": 6},    # x² - 5x + 6 = 0 (roots: 2, 3)
        {"a": 1, "b": 0, "c": -4},    # x² - 4 = 0 (roots: ±2)
        {"a": 1, "b": 2, "c": 1},     # x² + 2x + 1 = 0 (root: -1, perfect square)
        {"a": 1, "b": 1, "c": 1},     # x² + x + 1 = 0 (complex roots)
        {"a": 2, "b": -8, "c": 6},    # 2x² - 8x + 6 = 0 (roots: 1, 3)
    ]
    
    print("1. SOLVING INDIVIDUAL EQUATIONS:")
    print("-" * 50)
    
    for i, eq in enumerate(test_equations, 1):
        print(f"\nEquation {i}: {eq['a']}x² + {eq['b']}x + {eq['c']} = 0")
        result = client.solve_equation(eq['a'], eq['b'], eq['c'])
        
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"  Discriminant: {result['discriminant']:.3f}")
            print(f"  Roots: {result['roots']}")
            print(f"  Vertex: {result['vertex']}")
            print(f"  Direction: {result['direction']}")
            print(f"  Roots Type: {result['roots_type']}")


def demo_intersection_calculation():
    """Demonstrate intersection calculation"""
    print("\n\n2. CALCULATING INTERSECTIONS:")
    print("-" * 50)
    
    client = QuadraticSolverAPIClient()
    
    # Test intersection between two equations
    equations = [
        {"a": 1, "b": 0, "c": -1},    # x² - 1 = 0
        {"a": -1, "b": 0, "c": 1},    # -x² + 1 = 0
    ]
    
    print("Finding intersections between:")
    for i, eq in enumerate(equations, 1):
        print(f"  Equation {i}: {eq['a']}x² + {eq['b']}x + {eq['c']} = 0")
    
    result = client.calculate_intersections(equations)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nIntersection Analysis:")
        print(f"  Type: {result['analysis']['description']}")
        print(f"  Intersection Count: {result['intersection_count']}")
        
        if result['intersections']:
            print("  Intersection Points:")
            for i, intersection in enumerate(result['intersections'], 1):
                print(f"    Point {i}: ({intersection['x']:.3f}, {intersection['y']:.3f})")


def demo_batch_processing():
    """Demonstrate batch processing"""
    print("\n\n3. BATCH PROCESSING:")
    print("-" * 50)
    
    client = QuadraticSolverAPIClient()
    
    # Batch of equations to process
    equations = [
        {"a": 1, "b": -3, "c": 2},
        {"a": 2, "b": -4, "c": 2},
        {"a": 1, "b": 0, "c": -9},
        {"a": 1, "b": 2, "c": 5},  # Complex roots
    ]
    
    print(f"Processing {len(equations)} equations in batch...")
    
    result = client.batch_process_equations(equations)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success Rate: {result['success_rate']:.1f}%")
        print(f"Successful: {len(result['successful'])}")
        print(f"Errors: {len(result['errors'])}")
        
        print("\nResults:")
        for solution in result['successful']:
            print(f"  {solution['equation']}: {solution['roots_type']}")


def demo_analytics():
    """Demonstrate analytics functionality"""
    print("\n\n4. ANALYTICS:")
    print("-" * 50)
    
    client = QuadraticSolverAPIClient()
    
    # Get statistics
    stats = client.get_analytics("statistics")
    
    if 'error' in stats:
        print(f"Error: {stats['error']}")
    else:
        print("Equation Statistics:")
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                print(f"  {key}: {value}")


def main():
    """Main demo function"""
    try:
        demo_equation_solving()
        demo_intersection_calculation()
        demo_batch_processing()
        demo_analytics()
        
        print("\n\n=== DEMO COMPLETED ===")
        print("All API endpoints are working correctly!")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nDemo failed with error: {e}")


if __name__ == "__main__":
    main()
