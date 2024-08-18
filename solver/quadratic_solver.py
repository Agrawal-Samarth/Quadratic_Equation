"""
Quadratic equation solver utility class for the Django web app.
This is adapted from the original main.py solver.
"""

import math
import cmath
from typing import Tuple, Union, Dict, Any

class QuadraticEquationSolver:
    """A class to handle quadratic equations and their analysis for web interface."""
    
    def __init__(self, a: float, b: float, c: float):
        """Initialize quadratic equation ax² + bx + c = 0"""
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation")
        
        self.a = a
        self.b = b
        self.c = c
        self.discriminant = self.b**2 - 4*self.a*self.c
    
    def solve(self) -> Dict[str, Any]:
        """Solve the quadratic equation and return comprehensive results."""
        roots = self.get_roots()
        vertex = self.get_vertex()
        
        return {
            'discriminant': self.discriminant,
            'roots': roots,
            'root1': roots[0],
            'root2': roots[1],
            'roots_type': self.get_discriminant_info(),
            'direction': self.get_direction(),
            'vertex': vertex,
            'axis_of_symmetry': self.get_axis_of_symmetry(),
            'equation_string': self.format_equation()
        }
    
    def get_roots(self) -> Tuple[Union[complex, float], Union[complex, float]]:
        """Calculate and return the roots of the quadratic equation."""
        if self.discriminant > 0:
            # Two distinct real roots
            root1 = (-self.b + math.sqrt(self.discriminant)) / (2 * self.a)
            root2 = (-self.b - math.sqrt(self.discriminant)) / (2 * self.a)
            return root1, root2
        elif self.discriminant == 0:
            # One real root (repeated)
            root = -self.b / (2 * self.a)
            return root, root
        else:
            # Two complex roots
            root1 = (-self.b + cmath.sqrt(self.discriminant)) / (2 * self.a)
            root2 = (-self.b - cmath.sqrt(self.discriminant)) / (2 * self.a)
            return root1, root2
    
    def get_vertex(self) -> Tuple[float, float]:
        """Calculate the vertex of the parabola."""
        x_vertex = -self.b / (2 * self.a)
        y_vertex = self.a * x_vertex**2 + self.b * x_vertex + self.c
        return x_vertex, y_vertex
    
    def get_axis_of_symmetry(self) -> float:
        """Get the axis of symmetry (x-coordinate of vertex)."""
        return -self.b / (2 * self.a)
    
    def get_direction(self) -> str:
        """Determine if the parabola opens upward or downward."""
        return "upward" if self.a > 0 else "downward"
    
    def get_discriminant_info(self) -> str:
        """Get information about the discriminant."""
        if self.discriminant > 0:
            return "Two distinct real roots"
        elif self.discriminant == 0:
            return "One real root (repeated)"
        else:
            return "Two complex roots"
    
    def format_equation(self) -> str:
        """Format the equation as a string."""
        terms = []
        
        # Handle x² term
        if self.a == 1:
            terms.append("x²")
        elif self.a == -1:
            terms.append("-x²")
        else:
            terms.append(f"{self.a}x²")
        
        # Handle x term
        if self.b > 0:
            if self.b == 1:
                terms.append("+ x")
            else:
                terms.append(f"+ {self.b}x")
        elif self.b < 0:
            if self.b == -1:
                terms.append("- x")
            else:
                terms.append(f"- {abs(self.b)}x")
        
        # Handle constant term
        if self.c > 0:
            terms.append(f"+ {self.c}")
        elif self.c < 0:
            terms.append(f"- {abs(self.c)}")
        
        return " ".join(terms) + " = 0"
    
    def format_roots_for_display(self) -> list:
        """Format roots for display in web interface."""
        roots = self.get_roots()
        formatted_roots = []
        
        for i, root in enumerate(roots, 1):
            if isinstance(root, complex):
                if root.imag == 0:
                    formatted_roots.append(f"Root {i}: {root.real:.6f}")
                else:
                    formatted_roots.append(f"Root {i}: {root.real:.6f} + {root.imag:.6f}i")
            else:
                formatted_roots.append(f"Root {i}: {root:.6f}")
        
        return formatted_roots
