#!/usr/bin/env python3
"""
Demo script for the Quadratic Equation Solver and Visualizer.
This script demonstrates various types of quadratic equations and their solutions.
"""

from main import QuadraticEquation, plot_quadratic, print_analysis
import matplotlib.pyplot as plt

def demo_equations():
    """Demonstrate different types of quadratic equations."""
    
    print("🎯 QUADRATIC EQUATION SOLVER DEMO")
    print("=" * 50)
    
    # Example equations to demonstrate
    examples = [
        {
            "name": "Two Real Roots",
            "equation": "x² - 5x + 6 = 0",
            "coefficients": (1, -5, 6),
            "description": "Discriminant > 0, two distinct real roots"
        },
        {
            "name": "One Repeated Root",
            "equation": "x² - 4x + 4 = 0", 
            "coefficients": (1, -4, 4),
            "description": "Discriminant = 0, one repeated real root"
        },
        {
            "name": "Complex Roots",
            "equation": "x² + 2x + 5 = 0",
            "coefficients": (1, 2, 5),
            "description": "Discriminant < 0, two complex roots"
        },
        {
            "name": "Downward Parabola",
            "equation": "-x² + 3x - 2 = 0",
            "coefficients": (-1, 3, -2),
            "description": "Negative leading coefficient, opens downward"
        },
        {
            "name": "Simple Case",
            "equation": "x² - 1 = 0",
            "coefficients": (1, 0, -1),
            "description": "Difference of squares, roots at x = ±1"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*60}")
        print(f"EXAMPLE {i}: {example['name']}")
        print(f"Equation: {example['equation']}")
        print(f"Description: {example['description']}")
        print('='*60)
        
        # Create equation object
        a, b, c = example['coefficients']
        equation = QuadraticEquation(a, b, c)
        
        # Print analysis
        print_analysis(equation)
        
        # Ask user if they want to see the plot
        try:
            show_plot = input(f"\nWould you like to see the graph for {example['name']}? (y/n): ").lower().strip()
            if show_plot in ['y', 'yes']:
                plot_quadratic(equation)
            elif show_plot in ['q', 'quit']:
                print("Demo ended by user.")
                break
        except KeyboardInterrupt:
            print("\nDemo interrupted by user.")
            break
        
        # Ask if user wants to continue
        if i < len(examples):
            try:
                continue_demo = input(f"\nContinue to next example? (y/n/q to quit): ").lower().strip()
                if continue_demo in ['n', 'no']:
                    print("Demo ended by user.")
                    break
                elif continue_demo in ['q', 'quit']:
                    print("Demo ended by user.")
                    break
            except KeyboardInterrupt:
                print("\nDemo interrupted by user.")
                break
    
    print(f"\n{'='*60}")
    print("🎉 DEMO COMPLETED!")
    print("Thank you for trying the Quadratic Equation Solver!")
    print("Run 'python main.py' to solve your own equations.")
    print("="*60)

def interactive_demo():
    """Interactive demo where user can try their own equations."""
    
    print("\n🎮 INTERACTIVE DEMO MODE")
    print("=" * 30)
    print("Try solving your own quadratic equations!")
    print("Enter 'quit' at any time to exit.")
    
    while True:
        try:
            print("\n" + "-"*40)
            equation_input = input("Enter your equation (e.g., '1 -5 6' for x²-5x+6=0): ").strip()
            
            if equation_input.lower() in ['quit', 'exit', 'q']:
                print("Exiting interactive demo...")
                break
            
            # Parse input
            try:
                parts = equation_input.split()
                if len(parts) != 3:
                    print("Please enter exactly 3 numbers: a b c")
                    continue
                
                a, b, c = float(parts[0]), float(parts[1]), float(parts[2])
                
                if a == 0:
                    print("Error: Coefficient 'a' cannot be zero for a quadratic equation.")
                    continue
                
                # Create and analyze equation
                equation = QuadraticEquation(a, b, c)
                print_analysis(equation)
                
                # Ask about plotting
                show_plot = input("\nWould you like to see the graph? (y/n): ").lower().strip()
                if show_plot in ['y', 'yes']:
                    plot_quadratic(equation)
                
            except ValueError:
                print("Error: Please enter valid numbers separated by spaces.")
                continue
                
        except KeyboardInterrupt:
            print("\nDemo interrupted by user.")
            break

def main():
    """Main demo function."""
    print("Welcome to the Quadratic Equation Solver Demo!")
    print("\nChoose a demo mode:")
    print("1. Guided examples (recommended for first-time users)")
    print("2. Interactive mode (try your own equations)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                demo_equations()
                break
            elif choice == '2':
                interactive_demo()
                break
            elif choice == '3':
                print("Goodbye! 👋")
                break
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\nDemo interrupted by user. Goodbye! 👋")
            break

if __name__ == "__main__":
    main()
