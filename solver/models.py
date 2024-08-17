from django.db import models
from django.utils import timezone
import json

class QuadraticEquation(models.Model):
    """Model to store quadratic equation solving history."""
    
    # Coefficients
    a = models.FloatField(help_text="Coefficient of x²")
    b = models.FloatField(help_text="Coefficient of x")
    c = models.FloatField(help_text="Constant term")
    
    # Results
    discriminant = models.FloatField(help_text="Discriminant value")
    root1 = models.FloatField(null=True, blank=True, help_text="First root")
    root2 = models.FloatField(null=True, blank=True, help_text="Second root")
    root1_imag = models.FloatField(default=0, help_text="Imaginary part of first root")
    root2_imag = models.FloatField(default=0, help_text="Imaginary part of second root")
    
    # Vertex
    vertex_x = models.FloatField(help_text="X-coordinate of vertex")
    vertex_y = models.FloatField(help_text="Y-coordinate of vertex")
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quadratic Equation"
        verbose_name_plural = "Quadratic Equations"
    
    def __str__(self):
        return f"{self.a}x² + {self.b}x + {self.c} = 0"
    
    def get_equation_string(self):
        """Return formatted equation string."""
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
    
    def get_roots_type(self):
        """Return the type of roots."""
        if self.discriminant > 0:
            return "Two distinct real roots"
        elif self.discriminant == 0:
            return "One repeated real root"
        else:
            return "Two complex roots"
    
    def get_direction(self):
        """Return if parabola opens upward or downward."""
        return "upward" if self.a > 0 else "downward"
