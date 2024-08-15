#!/usr/bin/env python3
"""
Sample quadratic equations for testing and demonstration purposes.
This file contains various types of quadratic equations with their expected solutions.
"""

from main import QuadraticEquation, print_analysis, plot_quadratic

# Sample equations organized by type
SAMPLE_EQUATIONS = {
    "two_real_roots": [
        {
            "name": "Basic quadratic",
            "equation": "x² - 5x + 6 = 0",
            "coefficients": (1, -5, 6),
            "expected_roots": (3.0, 2.0),
            "description": "Standard quadratic with two real roots"
        },
        {
            "name": "Perfect square trinomial",
            "equation": "x² - 6x + 9 = 0", 
            "coefficients": (1, -6, 9),
            "expected_roots": (3.0, 3.0),
            "description": "Actually has one repeated root (discriminant = 0)"
        },
        {
            "name": "Difference of squares",
            "equation": "x² - 4 = 0",
            "coefficients": (1, 0, -4),
            "expected_roots": (2.0, -2.0),
            "description": "No middle term, roots are opposites"
        }
    ],
    
    "one_repeated_root": [
        {
            "name": "Perfect square",
            "equation": "x² - 4x + 4 = 0",
            "coefficients": (1, -4, 4),
            "expected_roots": (2.0, 2.0),
            "description": "Discriminant = 0, one repeated root"
        },
        {
            "name": "Vertex at origin",
            "equation": "x² = 0",
            "coefficients": (1, 0, 0),
            "expected_roots": (0.0, 0.0),
            "description": "Simplest case, root at x = 0"
        }
    ],
    
    "complex_roots": [
        {
            "name": "No real roots",
            "equation": "x² + 1 = 0",
            "coefficients": (1, 0, 1),
            "expected_roots": "complex",
            "description": "Classic case with no real solutions"
        },
        {
            "name": "Complex with real part",
            "equation": "x² + 2x + 5 = 0",
            "coefficients": (1, 2, 5),
            "expected_roots": "complex",
            "description": "Complex roots with non-zero real part"
        }
    ],
    
    "downward_parabolas": [
        {
            "name": "Negative leading coefficient",
            "equation": "-x² + 3x - 2 = 0",
            "coefficients": (-1, 3, -2),
            "expected_roots": (2.0, 1.0),
            "description": "Opens downward, has real roots"
        },
        {
            "name": "Maximum at vertex",
            "equation": "-x² + 4x - 3 = 0",
            "coefficients": (-1, 4, -3),
            "expected_roots": (3.0, 1.0),
            "description": "Downward parabola with maximum point"
        }
    ],
    
    "special_cases": [
        {
            "name": "Linear term only",
            "equation": "x² - 9 = 0",
            "coefficients": (1, 0, -9),
            "expected_roots": (3.0, -3.0),
            "description": "No linear term, pure quadratic"
        },
        {
            "name": "Constant term only",
            "equation": "x² - 2x = 0",
            "coefficients": (1, -2, 0),
            "expected_roots": (2.0, 0.0),
            "description": "No constant term, one root at zero"
        },
        {
            "name": "Large coefficients",
            "equation": "2x² - 7x + 3 = 0",
            "coefficients": (2, -7, 3),
            "expected_roots": (3.0, 0.5),
            "description": "Non-unit leading coefficient"
        }
    ]
}

def run_sample_equation(equation_data, show_plot=False):
    """Run analysis on a sample equation."""
    print(f"\n{'='*60}")
    print(f"EQUATION: {equation_data['name']}")
    print(f"Form: {equation_data['equation']}")
    print(f"Description: {equation_data['description']}")
    print('='*60)
    
    # Create equation object
    a, b, c = equation_data['coefficients']
    equation = QuadraticEquation(a, b, c)
    
    # Print analysis
    print_analysis(equation)
    
    # Show plot if requested
    if show_plot:
        plot_quadratic(equation)
    
    return equation

def run_all_samples(category=None, show_plots=False):
    """Run all sample equations or a specific category."""
    
    if category and category in SAMPLE_EQUATIONS:
        categories = {category: SAMPLE_EQUATIONS[category]}
    else:
        categories = SAMPLE_EQUATIONS
    
    print("🧮 RUNNING SAMPLE QUADRATIC EQUATIONS")
    print("=" * 50)
    
    for cat_name, equations in categories.items():
        print(f"\n📂 CATEGORY: {cat_name.replace('_', ' ').title()}")
        print("-" * 40)
        
        for equation_data in equations:
            try:
                run_sample_equation(equation_data, show_plots)
                
                # Ask user if they want to continue
                if not show_plots:  # Only ask if not showing all plots
                    continue_choice = input("\nContinue to next equation? (y/n/q to quit): ").lower().strip()
                    if continue_choice in ['n', 'no']:
                        print("Stopping sample run.")
                        return
                    elif continue_choice in ['q', 'quit']:
                        print("Exiting sample run.")
                        return
                        
            except KeyboardInterrupt:
                print("\nSample run interrupted by user.")
                return
    
    print(f"\n{'='*60}")
    print("✅ ALL SAMPLE EQUATIONS COMPLETED!")
    print("="*60)

def list_available_equations():
    """List all available sample equations."""
    print("📋 AVAILABLE SAMPLE EQUATIONS")
    print("=" * 40)
    
    for category, equations in SAMPLE_EQUATIONS.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        for i, eq in enumerate(equations, 1):
            print(f"  {i}. {eq['name']}: {eq['equation']}")

def main():
    """Main function for running sample equations."""
    print("🧮 SAMPLE QUADRATIC EQUATIONS")
    print("=" * 35)
    print("This script contains various sample quadratic equations for testing.")
    print("\nOptions:")
    print("1. List all available equations")
    print("2. Run all sample equations")
    print("3. Run equations from a specific category")
    print("4. Run a specific equation")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                list_available_equations()
                
            elif choice == '2':
                show_plots = input("Show plots for all equations? (y/n): ").lower().strip() in ['y', 'yes']
                run_all_samples(show_plots=show_plots)
                
            elif choice == '3':
                print("\nAvailable categories:")
                for i, category in enumerate(SAMPLE_EQUATIONS.keys(), 1):
                    print(f"  {i}. {category.replace('_', ' ').title()}")
                
                try:
                    cat_choice = int(input("Enter category number: ")) - 1
                    categories = list(SAMPLE_EQUATIONS.keys())
                    if 0 <= cat_choice < len(categories):
                        selected_category = categories[cat_choice]
                        show_plots = input("Show plots? (y/n): ").lower().strip() in ['y', 'yes']
                        run_all_samples(category=selected_category, show_plots=show_plots)
                    else:
                        print("Invalid category number.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '4':
                list_available_equations()
                print("\nTo run a specific equation, modify the script or use the main program.")
                
            elif choice == '5':
                print("Goodbye! 👋")
                break
                
            else:
                print("Please enter a number between 1 and 5.")
                
        except KeyboardInterrupt:
            print("\nSample runner interrupted by user. Goodbye! 👋")
            break

if __name__ == "__main__":
    main()
