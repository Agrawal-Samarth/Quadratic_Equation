from django.contrib import admin
from .models import QuadraticEquation

@admin.register(QuadraticEquation)
class QuadraticEquationAdmin(admin.ModelAdmin):
    list_display = ['get_equation_string', 'discriminant', 'get_roots_type', 'get_direction', 'created_at']
    list_filter = ['created_at', 'a']
    search_fields = ['a', 'b', 'c']
    readonly_fields = ['discriminant', 'vertex_x', 'vertex_y', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Equation', {
            'fields': ('a', 'b', 'c')
        }),
        ('Results', {
            'fields': ('discriminant', 'root1', 'root2', 'root1_imag', 'root2_imag')
        }),
        ('Vertex', {
            'fields': ('vertex_x', 'vertex_y')
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
    
    def get_equation_string(self, obj):
        return obj.get_equation_string()
    get_equation_string.short_description = 'Equation'
    
    def get_roots_type(self, obj):
        return obj.get_roots_type()
    get_roots_type.short_description = 'Roots Type'
    
    def get_direction(self, obj):
        return obj.get_direction()
    get_direction.short_description = 'Direction'
