# 🎯 Quadratic Equation Solver and Visualizer

A comprehensive Python tool for solving quadratic equations and visualizing their graphs with detailed mathematical analysis.

> **Built during Class 10** - This project was created as a learning exercise while studying quadratic equations in high school mathematics.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

## ✨ Features

- **🔢 Complete Root Calculation**: Handles real, repeated, and complex roots
- **📊 Beautiful Visualizations**: Professional-quality graphs with matplotlib
- **🎯 Vertex Analysis**: Calculates and displays parabola vertices
- **📈 Interactive Interface**: User-friendly input system with validation
- **🔍 Detailed Analysis**: Comprehensive mathematical breakdown
- **🎨 Modern Styling**: Clean, professional visual design
- **⚡ Error Handling**: Robust input validation and error management
- **🔄 Multiple Equations**: Solve multiple equations in one session

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quadratic-equations.git
cd quadratic-equations
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the program:
```bash
python main.py
```

## 📖 Usage

### Basic Usage

Simply run the program and follow the prompts:

```bash
python main.py
```

The program will ask you to enter the coefficients for your quadratic equation in the form `ax² + bx + c = 0`.

### Example Session

```
🎯 Quadratic Equation Solver and Visualizer
==================================================
Enter the coefficients for the quadratic equation ax² + bx + c = 0
Enter coefficient 'a' (cannot be 0): 1
Enter coefficient 'b': -5
Enter coefficient 'c': 6

============================================================
QUADRATIC EQUATION ANALYSIS
============================================================
Equation: x² - 5x + 6 = 0
Discriminant: 1.000000
Nature of roots: Two distinct real roots
Direction: Opens upward
Vertex: (2.500000, -0.250000)
Axis of symmetry: x = 2.500000

Roots:
  Root 1: 3.000000
  Root 2: 2.000000
============================================================
```

## 🧮 Mathematical Features

### Root Types Handled

1. **Two Real Roots** (D > 0): `x² - 5x + 6 = 0`
2. **One Repeated Root** (D = 0): `x² - 4x + 4 = 0`
3. **Complex Roots** (D < 0): `x² + 1 = 0`

### Analysis Provided

- **Discriminant**: `b² - 4ac`
- **Vertex**: Maximum/minimum point of the parabola
- **Axis of Symmetry**: `x = -b/(2a)`
- **Direction**: Whether the parabola opens upward or downward
- **Root Nature**: Real, repeated, or complex

## 📊 Visualization Features

- **Function Graph**: Smooth curve plotting
- **Root Markers**: Red dots showing real roots
- **Vertex Marker**: Green triangle showing the vertex
- **Axis Lines**: Reference lines for x and y axes
- **Information Box**: Key properties displayed on the graph
- **Professional Styling**: Clean, modern appearance

## 🛠️ Technical Details

### Dependencies

- `matplotlib >= 3.5.0`: For graph visualization
- `numpy >= 1.21.0`: For numerical computations

### Code Structure

```
quadratic-equations/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── .gitignore          # Git ignore rules
├── examples/           # Example equations
│   └── sample_equations.py
└── demo.py             # Demo script
```

### Key Classes

- **`QuadraticEquation`**: Main class handling equation analysis
  - `get_roots()`: Calculate equation roots
  - `get_vertex()`: Find parabola vertex
  - `get_discriminant_info()`: Analyze root nature
  - `format_equation()`: Pretty-print equation

## 📁 Project Structure

```
Quadratic_Equations/
├── main.py                    # Main application
├── requirements.txt           # Dependencies
├── README.md                 # Documentation
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore file
├── demo.py                  # Demo script
└── examples/                # Example equations
    └── sample_equations.py  # Sample equations
```

## 🎯 Example Equations

Try these example equations to see the solver in action:

1. **Two Real Roots**: `x² - 5x + 6 = 0` (Roots: 2, 3)
2. **One Root**: `x² - 4x + 4 = 0` (Root: 2)
3. **Complex Roots**: `x² + 2x + 5 = 0` (Complex roots)
4. **Downward Parabola**: `-x² + 3x - 2 = 0` (Roots: 1, 2)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and matplotlib during Class 10 studies
- Inspired by mathematical education and visualization needs
- Thanks to the open-source community for the amazing tools
- Special thanks to my mathematics teachers for inspiring this project

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [Issues](https://github.com/yourusername/quadratic-equations/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your problem

## 🔮 Future Enhancements

- [ ] GUI interface with tkinter
- [ ] Multiple equation comparison
- [ ] Export graphs as images
- [ ] Web interface with Flask
- [ ] Mobile app version
- [ ] Integration with symbolic math libraries

---

**Made with ❤️ for mathematics education**  
*Built by a Class 10 student passionate about making math more visual and interactive*
