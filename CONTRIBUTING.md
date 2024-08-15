# Contributing to Quadratic Equation Solver

Thank you for your interest in contributing to the Quadratic Equation Solver! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/yourusername/quadratic-equations/issues) page
2. If not, create a new issue with:
   - Clear title describing the problem/request
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version)

### Making Changes

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the coding standards below
4. **Test your changes** thoroughly
5. **Commit your changes**: `git commit -m 'Add: brief description of changes'`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## 📋 Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and reasonably sized
- Use type hints where appropriate

### Code Structure

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
    """
    # Implementation here
    pass
```

### Testing

- Add tests for new functionality
- Ensure existing tests still pass
- Test edge cases and error conditions
- Use descriptive test names

## 🚀 Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- git

### Setup Steps

1. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/quadratic-equations.git
   cd quadratic-equations
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies** (if any):
   ```bash
   pip install pytest black flake8 mypy
   ```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=main

# Run specific test file
python -m pytest tests/test_main.py
```

### Code Quality Checks

```bash
# Format code
black main.py demo.py examples/

# Lint code
flake8 main.py demo.py examples/

# Type checking
mypy main.py
```

## 📁 Project Structure

```
quadratic-equations/
├── main.py                 # Main application
├── demo.py                 # Demo script
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # This file
├── .gitignore            # Git ignore rules
├── examples/             # Example equations
│   ├── __init__.py
│   └── sample_equations.py
└── tests/                # Test files (to be added)
    ├── __init__.py
    ├── test_main.py
    └── test_quadratic.py
```

## 🎯 Areas for Contribution

### High Priority

- [ ] Add unit tests
- [ ] Create GUI interface (tkinter/PyQt)
- [ ] Add web interface (Flask/Django)
- [ ] Improve error handling
- [ ] Add more visualization options

### Medium Priority

- [ ] Add support for higher-degree polynomials
- [ ] Create mobile app version
- [ ] Add equation history
- [ ] Export functionality (PDF, images)
- [ ] Internationalization support

### Low Priority

- [ ] Performance optimizations
- [ ] Additional mathematical analysis
- [ ] Plugin system
- [ ] Command-line interface improvements

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment**:
   - Operating System
   - Python version
   - Package versions

2. **Steps to reproduce**:
   - Exact commands or inputs
   - Expected behavior
   - Actual behavior

3. **Error messages**:
   - Full traceback (if any)
   - Screenshots (if applicable)

4. **Additional context**:
   - Any workarounds you've found
   - Related issues or discussions

## 💡 Feature Requests

For feature requests, please provide:

1. **Clear description** of the feature
2. **Use case** - why is this feature needed?
3. **Proposed implementation** (if you have ideas)
4. **Alternatives considered**
5. **Additional context** or examples

## 📝 Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] Commit messages are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings introduced
```

## 🏷️ Commit Message Format

Use clear, descriptive commit messages:

```
Add: feature description
Fix: bug description  
Update: change description
Remove: removal description
Docs: documentation update
Test: test addition/update
```

Examples:
- `Add: support for complex roots visualization`
- `Fix: vertex calculation for negative coefficients`
- `Update: improve error messages for invalid input`
- `Docs: add installation instructions for Windows`

## 📞 Getting Help

If you need help:

1. Check the [Issues](https://github.com/yourusername/quadratic-equations/issues) page
2. Search existing discussions
3. Create a new issue with the "question" label
4. Join our community discussions (if available)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to make mathematics education more accessible! 🎓
