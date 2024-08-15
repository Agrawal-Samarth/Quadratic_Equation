import matplotlib.pyplot as plt
import numpy as np
import math
import cmath
from typing import Tuple, Union, Optional

class QuadraticEquation:
    """A class to handle quadratic equations and their analysis."""
    
    def __init__(self, a: float, b: float, c: float):
        """Initialize quadratic equation ax² + bx + c = 0"""
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation")
        
        self.a = a
        self.b = b
        self.c = c
        self.discriminant = self.b**2 - 4*self.a*self.c
    
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

def get_user_input() -> Tuple[float, float, float]:
    """Get coefficients from user input with validation."""
    print("Enter the coefficients for the quadratic equation ax² + bx + c = 0")
    
    while True:
        try:
            a = float(input("Enter coefficient 'a' (cannot be 0): "))
            if a == 0:
                print("Error: Coefficient 'a' cannot be zero for a quadratic equation. Please try again.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number for coefficient 'a'.")
    
    while True:
        try:
            b = float(input("Enter coefficient 'b': "))
            break
        except ValueError:
            print("Error: Please enter a valid number for coefficient 'b'.")
    
    while True:
        try:
            c = float(input("Enter coefficient 'c': "))
            break
        except ValueError:
            print("Error: Please enter a valid number for coefficient 'c'.")
    
    return a, b, c

def plot_quadratic(equation: QuadraticEquation, x_range: Tuple[float, float] = None):
    """Plot the quadratic equation with enhanced visualization."""
    
    # Calculate smart x_range based on vertex and roots
    vertex_x = equation.get_axis_of_symmetry()
    roots = equation.get_roots()
    
    # Determine appropriate x range
    if x_range is None:
        # Find all real x-values of interest
        x_values = [vertex_x]
        for root in roots:
            if isinstance(root, complex):
                if root.imag == 0:  # Real part of complex number
                    x_values.append(root.real)
            else:
                x_values.append(root)
        
        if x_values:
            x_center = sum(x_values) / len(x_values)
            x_spread = max([abs(x - x_center) for x in x_values]) if len(x_values) > 1 else 5
            x_spread = max(x_spread, 3)  # Minimum spread
            x_min = x_center - x_spread * 1.5
            x_max = x_center + x_spread * 1.5
        else:
            x_min, x_max = -10, 10
    else:
        x_min, x_max = x_range
    
    x = np.linspace(x_min, x_max, 1000)
    y = equation.a * x**2 + equation.b * x + equation.c
    
    # Create figure with better styling
    plt.figure(figsize=(12, 8))
    plt.style.use('seaborn-v0_8')
    
    # Plot the quadratic function
    plt.plot(x, y, linewidth=2.5, label=f'y = {equation.format_equation().replace(" = 0", "")}', color='#2E86AB')
    
    # Get roots and plot them
    real_roots = []
    
    for root in roots:
        if isinstance(root, complex):
            if root.imag == 0:  # Real part of complex number
                real_roots.append(root.real)
        else:
            real_roots.append(root)
    
    # Plot real roots
    for root in real_roots:
        if x_min <= root <= x_max:
            plt.scatter(root, 0, color='red', s=100, zorder=5, label=f'Root: x = {root:.3f}')
    
    # Plot vertex
    vertex_x, vertex_y = equation.get_vertex()
    if x_min <= vertex_x <= x_max:
        plt.scatter(vertex_x, vertex_y, color='green', s=100, zorder=5, 
                   marker='^', label=f'Vertex: ({vertex_x:.3f}, {vertex_y:.3f})')
    
    # Add axis lines
    plt.axhline(0, color='black', linewidth=0.8, alpha=0.7)
    plt.axvline(0, color='black', linewidth=0.8, alpha=0.7)
    
    # Smart y-axis limits
    y_min, y_max = min(y), max(y)
    y_range = y_max - y_min
    
    # If y range is very small, expand it
    if y_range < 0.1:
        y_center = (y_max + y_min) / 2
        y_min = y_center - 2
        y_max = y_center + 2
    else:
        # Add padding
        y_padding = y_range * 0.15
        y_min -= y_padding
        y_max += y_padding
    
    # Ensure we include y=0 if it's within a reasonable range
    if y_min <= 0 <= y_max:
        pass  # y=0 is already included
    elif abs(y_min) < abs(y_max):
        y_min = min(y_min, -abs(y_max) * 0.1)
    else:
        y_max = max(y_max, abs(y_min) * 0.1)
    
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    # Enhanced styling
    plt.title(f'Graph of Quadratic Equation: {equation.format_equation()}', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Add text box with equation properties
    info_text = f"""Equation Properties:
Discriminant: {equation.discriminant:.3f}
{equation.get_discriminant_info()}
Direction: Opens {equation.get_direction()}
Axis of Symmetry: x = {equation.get_axis_of_symmetry():.3f}"""
    
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
             fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.show()

def print_analysis(equation: QuadraticEquation):
    """Print detailed analysis of the quadratic equation."""
    print("\n" + "="*60)
    print("QUADRATIC EQUATION ANALYSIS")
    print("="*60)
    print(f"Equation: {equation.format_equation()}")
    print(f"Discriminant: {equation.discriminant:.6f}")
    print(f"Nature of roots: {equation.get_discriminant_info()}")
    print(f"Direction: Opens {equation.get_direction()}")
    
    vertex_x, vertex_y = equation.get_vertex()
    print(f"Vertex: ({vertex_x:.6f}, {vertex_y:.6f})")
    print(f"Axis of symmetry: x = {equation.get_axis_of_symmetry():.6f}")
    
    print("\nRoots:")
    roots = equation.get_roots()
    for i, root in enumerate(roots, 1):
        if isinstance(root, complex):
            print(f"  Root {i}: {root.real:.6f} + {root.imag:.6f}i")
        else:
            print(f"  Root {i}: {root:.6f}")
    
    print("="*60)

def main():
    """Main function to run the quadratic equation solver and visualizer."""
    print("🎯 Quadratic Equation Solver and Visualizer")
    print("=" * 50)
    
    try:
        # Get user input
        a, b, c = get_user_input()
        
        # Create equation object
        equation = QuadraticEquation(a, b, c)
        
        # Print analysis
        print_analysis(equation)
        
        # Plot the equation
        plot_quadratic(equation)
        
        # Ask if user wants to try another equation
        while True:
            try_again = input("\nWould you like to solve another equation? (y/n): ").lower().strip()
            if try_again in ['y', 'yes']:
                main()
                break
            elif try_again in ['n', 'no']:
                print("Thank you for using the Quadratic Equation Solver! 👋")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
                
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
