"""
Advanced Analytics Engine for Quadratic Equation Solver
Provides comprehensive data analysis, reporting, and insights
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
import pandas as pd
from django.db.models import Count, Avg, Min, Max, Q
from django.core.cache import cache
from .models import QuadraticEquation
from .performance_optimizer import performance_monitor, data_analyzer
from .advanced_equation_solver import pattern_analyzer

logger = logging.getLogger(__name__)


class AdvancedAnalyticsEngine:
    """Comprehensive analytics engine for equation data"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour
        self.performance_monitor = performance_monitor
    
    @performance_monitor.time_function('generate_comprehensive_analytics')
    def generate_comprehensive_analytics(self) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        cache_key = 'comprehensive_analytics'
        cached_result = cache.get(cache_key)
        
        if cached_result:
            logger.info("Returning cached analytics")
            return cached_result
        
        analytics = {
            'overview': self._get_overview_stats(),
            'temporal_analysis': self._get_temporal_analysis(),
            'coefficient_analysis': self._get_coefficient_analysis(),
            'geometric_analysis': self._get_geometric_analysis(),
            'pattern_analysis': self._get_pattern_analysis(),
            'performance_metrics': self._get_performance_metrics(),
            'user_behavior': self._get_user_behavior_analysis(),
            'mathematical_insights': self._get_mathematical_insights(),
            'predictive_analysis': self._get_predictive_analysis()
        }
        
        cache.set(cache_key, analytics, self.cache_timeout)
        return analytics
    
    def _get_overview_stats(self) -> Dict[str, Any]:
        """Get overview statistics"""
        total_equations = QuadraticEquation.objects.count()
        
        if total_equations == 0:
            return {'total_equations': 0, 'message': 'No equations found'}
        
        # Basic statistics
        real_roots = QuadraticEquation.objects.filter(discriminant__gte=0).count()
        complex_roots = QuadraticEquation.objects.filter(discriminant__lt=0).count()
        perfect_squares = QuadraticEquation.objects.filter(discriminant=0).count()
        
        # Coefficient statistics
        coeff_stats = QuadraticEquation.objects.aggregate(
            avg_a=Avg('a'), avg_b=Avg('b'), avg_c=Avg('c'),
            min_a=Min('a'), max_a=Max('a'),
            min_b=Min('b'), max_b=Max('b'),
            min_c=Min('c'), max_c=Max('c')
        )
        
        return {
            'total_equations': total_equations,
            'real_roots_count': real_roots,
            'complex_roots_count': complex_roots,
            'perfect_squares_count': perfect_squares,
            'real_roots_percentage': (real_roots / total_equations) * 100,
            'complex_roots_percentage': (complex_roots / total_equations) * 100,
            'perfect_squares_percentage': (perfect_squares / total_equations) * 100,
            'coefficient_statistics': coeff_stats
        }
    
    def _get_temporal_analysis(self) -> Dict[str, Any]:
        """Analyze usage patterns over time"""
        # Get equations from the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_equations = QuadraticEquation.objects.filter(
            created_at__gte=thirty_days_ago
        ).order_by('created_at')
        
        if not recent_equations.exists():
            return {'message': 'No recent data available'}
        
        # Daily usage
        daily_usage = {}
        for equation in recent_equations:
            date = equation.created_at.date()
            daily_usage[date] = daily_usage.get(date, 0) + 1
        
        # Hourly usage patterns
        hourly_usage = {}
        for equation in recent_equations:
            hour = equation.created_at.hour
            hourly_usage[hour] = hourly_usage.get(hour, 0) + 1
        
        # Weekly patterns
        weekly_usage = {}
        for equation in recent_equations:
            weekday = equation.created_at.weekday()
            weekly_usage[weekday] = weekly_usage.get(weekday, 0) + 1
        
        return {
            'daily_usage': daily_usage,
            'hourly_usage': hourly_usage,
            'weekly_usage': weekly_usage,
            'peak_hour': max(hourly_usage.items(), key=lambda x: x[1])[0] if hourly_usage else None,
            'peak_day': max(weekly_usage.items(), key=lambda x: x[1])[0] if weekly_usage else None,
            'total_recent_equations': recent_equations.count()
        }
    
    def _get_coefficient_analysis(self) -> Dict[str, Any]:
        """Analyze coefficient patterns"""
        equations = list(QuadraticEquation.objects.all())
        
        if not equations:
            return {'message': 'No equations available for analysis'}
        
        # Convert to DataFrame for analysis
        data = []
        for eq in equations:
            data.append({
                'a': eq.a, 'b': eq.b, 'c': eq.c,
                'discriminant': eq.discriminant,
                'vertex_x': eq.vertex_x, 'vertex_y': eq.vertex_y
            })
        
        df = pd.DataFrame(data)
        
        # Coefficient distribution analysis
        coefficient_analysis = {
            'a_distribution': {
                'positive': (df['a'] > 0).sum(),
                'negative': (df['a'] < 0).sum(),
                'integer': df['a'].apply(lambda x: x.is_integer()).sum(),
                'decimal': (~df['a'].apply(lambda x: x.is_integer())).sum()
            },
            'b_distribution': {
                'positive': (df['b'] > 0).sum(),
                'negative': (df['b'] < 0).sum(),
                'zero': (df['b'] == 0).sum(),
                'integer': df['b'].apply(lambda x: x.is_integer()).sum()
            },
            'c_distribution': {
                'positive': (df['c'] > 0).sum(),
                'negative': (df['c'] < 0).sum(),
                'zero': (df['c'] == 0).sum(),
                'integer': df['c'].apply(lambda x: x.is_integer()).sum()
            }
        }
        
        # Correlation analysis
        correlation_matrix = df[['a', 'b', 'c', 'discriminant']].corr()
        
        return {
            'coefficient_distributions': coefficient_analysis,
            'correlation_matrix': correlation_matrix.to_dict(),
            'statistical_summary': df.describe().to_dict()
        }
    
    def _get_geometric_analysis(self) -> Dict[str, Any]:
        """Analyze geometric properties of equations"""
        equations = list(QuadraticEquation.objects.all())
        
        if not equations:
            return {'message': 'No equations available for analysis'}
        
        # Direction analysis
        upward_count = sum(1 for eq in equations if eq.get_direction() == 'upward')
        downward_count = len(equations) - upward_count
        
        # Vertex analysis
        vertices = [(eq.vertex_x, eq.vertex_y) for eq in equations]
        vertex_x_values = [v[0] for v in vertices]
        vertex_y_values = [v[1] for v in vertices]
        
        # Quadrant analysis
        quadrants = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'axes': 0}
        for x, y in vertices:
            if x == 0 or y == 0:
                quadrants['axes'] += 1
            elif x > 0 and y > 0:
                quadrants['I'] += 1
            elif x < 0 and y > 0:
                quadrants['II'] += 1
            elif x < 0 and y < 0:
                quadrants['III'] += 1
            else:
                quadrants['IV'] += 1
        
        return {
            'direction_analysis': {
                'upward_parabolas': upward_count,
                'downward_parabolas': downward_count,
                'upward_percentage': (upward_count / len(equations)) * 100
            },
            'vertex_analysis': {
                'vertex_range_x': [min(vertex_x_values), max(vertex_x_values)],
                'vertex_range_y': [min(vertex_y_values), max(vertex_y_values)],
                'quadrant_distribution': quadrants,
                'average_vertex_x': np.mean(vertex_x_values),
                'average_vertex_y': np.mean(vertex_y_values)
            }
        }
    
    def _get_pattern_analysis(self) -> Dict[str, Any]:
        """Analyze mathematical patterns"""
        equations = list(QuadraticEquation.objects.all())
        
        if not equations:
            return {'message': 'No equations available for analysis'}
        
        # Convert to format expected by pattern analyzer
        equation_data = []
        for eq in equations:
            equation_data.append({
                'coefficients': {'a': eq.a, 'b': eq.b, 'c': eq.c},
                'discriminant': eq.discriminant,
                'roots_type': eq.get_roots_type(),
                'direction': eq.get_direction(),
                'vertex': [eq.vertex_x, eq.vertex_y]
            })
        
        return pattern_analyzer.analyze_equation_patterns(equation_data)
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            'database_queries': len(connection.queries),
            'query_time': sum(float(q['time']) for q in connection.queries),
            'cache_stats': self._get_cache_stats(),
            'performance_report': performance_monitor.get_performance_report()
        }
    
    def _get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        # This would need to be implemented based on your cache backend
        return {
            'cache_backend': 'redis',
            'cache_timeout': self.cache_timeout,
            'cache_keys': len(cache.keys('*'))
        }
    
    def _get_user_behavior_analysis(self) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        # IP-based analysis
        ip_counts = QuadraticEquation.objects.values('ip_address').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Session analysis (based on IP and time proximity)
        sessions = self._identify_user_sessions()
        
        return {
            'top_ips': list(ip_counts),
            'user_sessions': sessions,
            'average_equations_per_session': np.mean([s['equation_count'] for s in sessions]) if sessions else 0
        }
    
    def _identify_user_sessions(self) -> List[Dict[str, Any]]:
        """Identify user sessions based on IP and time proximity"""
        sessions = []
        equations = QuadraticEquation.objects.order_by('ip_address', 'created_at')
        
        current_session = None
        for eq in equations:
            if (current_session is None or 
                current_session['ip'] != eq.ip_address or 
                (eq.created_at - current_session['last_activity']).seconds > 3600):  # 1 hour gap
                
                if current_session:
                    sessions.append(current_session)
                
                current_session = {
                    'ip': eq.ip_address,
                    'start_time': eq.created_at,
                    'last_activity': eq.created_at,
                    'equation_count': 1,
                    'equations': [eq.id]
                }
            else:
                current_session['last_activity'] = eq.created_at
                current_session['equation_count'] += 1
                current_session['equations'].append(eq.id)
        
        if current_session:
            sessions.append(current_session)
        
        return sessions
    
    def _get_mathematical_insights(self) -> Dict[str, Any]:
        """Generate mathematical insights"""
        equations = list(QuadraticEquation.objects.all())
        
        if not equations:
            return {'message': 'No equations available for analysis'}
        
        insights = {
            'common_patterns': self._find_common_patterns(equations),
            'unusual_cases': self._find_unusual_cases(equations),
            'educational_opportunities': self._identify_educational_opportunities(equations)
        }
        
        return insights
    
    def _find_common_patterns(self, equations: List[QuadraticEquation]) -> List[Dict[str, Any]]:
        """Find common mathematical patterns"""
        patterns = []
        
        # Perfect squares
        perfect_squares = [eq for eq in equations if eq.discriminant == 0]
        if perfect_squares:
            patterns.append({
                'type': 'perfect_squares',
                'count': len(perfect_squares),
                'description': 'Equations with discriminant = 0 (perfect squares)',
                'examples': [eq.get_equation_string() for eq in perfect_squares[:3]]
            })
        
        # Factorable equations
        factorable = []
        for eq in equations:
            if (eq.root1 is not None and eq.root1_imag == 0 and 
                eq.root2 is not None and eq.root2_imag == 0):
                if eq.root1.is_integer() and eq.root2.is_integer():
                    factorable.append(eq)
        
        if factorable:
            patterns.append({
                'type': 'factorable_equations',
                'count': len(factorable),
                'description': 'Equations with integer roots (factorable)',
                'examples': [eq.get_equation_string() for eq in factorable[:3]]
            })
        
        return patterns
    
    def _find_unusual_cases(self, equations: List[QuadraticEquation]) -> List[Dict[str, Any]]:
        """Find unusual or interesting cases"""
        unusual = []
        
        # Very large coefficients
        large_coeff = [eq for eq in equations if abs(eq.a) > 100 or abs(eq.b) > 100 or abs(eq.c) > 100]
        if large_coeff:
            unusual.append({
                'type': 'large_coefficients',
                'count': len(large_coeff),
                'description': 'Equations with very large coefficients',
                'examples': [eq.get_equation_string() for eq in large_coeff[:3]]
            })
        
        # Very small coefficients
        small_coeff = [eq for eq in equations if 0 < abs(eq.a) < 0.01 or 0 < abs(eq.b) < 0.01 or 0 < abs(eq.c) < 0.01]
        if small_coeff:
            unusual.append({
                'type': 'small_coefficients',
                'count': len(small_coeff),
                'description': 'Equations with very small coefficients',
                'examples': [eq.get_equation_string() for eq in small_coeff[:3]]
            })
        
        return unusual
    
    def _identify_educational_opportunities(self, equations: List[QuadraticEquation]) -> List[Dict[str, Any]]:
        """Identify educational opportunities"""
        opportunities = []
        
        # Complex roots for advanced students
        complex_roots = [eq for eq in equations if eq.get_roots_type() == 'complex']
        if complex_roots:
            opportunities.append({
                'type': 'complex_roots',
                'count': len(complex_roots),
                'description': 'Equations with complex roots for advanced study',
                'difficulty': 'advanced'
            })
        
        # Perfect squares for factoring practice
        perfect_squares = [eq for eq in equations if eq.discriminant == 0]
        if perfect_squares:
            opportunities.append({
                'type': 'perfect_squares',
                'count': len(perfect_squares),
                'description': 'Perfect square equations for factoring practice',
                'difficulty': 'intermediate'
            })
        
        return opportunities
    
    def _get_predictive_analysis(self) -> Dict[str, Any]:
        """Generate predictive analysis"""
        equations = list(QuadraticEquation.objects.all())
        
        if len(equations) < 10:
            return {'message': 'Insufficient data for predictive analysis'}
        
        # Simple trend analysis
        recent_equations = equations[-10:]  # Last 10 equations
        older_equations = equations[:-10] if len(equations) > 10 else []
        
        if older_equations:
            recent_avg_discriminant = np.mean([eq.discriminant for eq in recent_equations])
            older_avg_discriminant = np.mean([eq.discriminant for eq in older_equations])
            
            trend = 'increasing' if recent_avg_discriminant > older_avg_discriminant else 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend_analysis': {
                'discriminant_trend': trend,
                'recent_equations_count': len(recent_equations),
                'older_equations_count': len(older_equations)
            },
            'predictions': {
                'next_equation_type': self._predict_next_equation_type(equations),
                'usage_forecast': self._forecast_usage(equations)
            }
        }
    
    def _predict_next_equation_type(self, equations: List[QuadraticEquation]) -> str:
        """Predict the type of the next equation"""
        if not equations:
            return 'unknown'
        
        recent_types = [eq.get_roots_type() for eq in equations[-5:]]
        type_counts = {}
        for eq_type in recent_types:
            type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
        
        return max(type_counts.items(), key=lambda x: x[1])[0]
    
    def _forecast_usage(self, equations: List[QuadraticEquation]) -> Dict[str, Any]:
        """Forecast future usage patterns"""
        if len(equations) < 7:
            return {'message': 'Insufficient data for forecasting'}
        
        # Simple linear trend
        daily_counts = {}
        for eq in equations:
            date = eq.created_at.date()
            daily_counts[date] = daily_counts.get(date, 0) + 1
        
        dates = sorted(daily_counts.keys())
        counts = [daily_counts[date] for date in dates]
        
        if len(counts) >= 2:
            # Simple linear regression
            x = np.arange(len(counts))
            slope = np.polyfit(x, counts, 1)[0]
            
            return {
                'trend_slope': slope,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                'forecast_next_week': max(0, counts[-1] + slope * 7)
            }
        
        return {'message': 'Insufficient data for forecasting'}


class ReportGenerator:
    """Generate various types of reports"""
    
    def __init__(self):
        self.analytics_engine = AdvancedAnalyticsEngine()
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary report"""
        analytics = self.analytics_engine.generate_comprehensive_analytics()
        
        return {
            'report_type': 'executive_summary',
            'generated_at': datetime.now().isoformat(),
            'key_metrics': {
                'total_equations': analytics['overview']['total_equations'],
                'real_roots_percentage': analytics['overview']['real_roots_percentage'],
                'complex_roots_percentage': analytics['overview']['complex_roots_percentage'],
                'perfect_squares_percentage': analytics['overview']['perfect_squares_percentage']
            },
            'insights': analytics['mathematical_insights'],
            'recommendations': self._generate_recommendations(analytics)
        }
    
    def _generate_recommendations(self, analytics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        if analytics['overview']['total_equations'] > 0:
            if analytics['overview']['complex_roots_percentage'] < 10:
                recommendations.append("Consider adding more complex root examples for advanced students")
            
            if analytics['overview']['perfect_squares_percentage'] > 30:
                recommendations.append("High percentage of perfect squares - good for factoring practice")
            
            if analytics['temporal_analysis'].get('peak_hour'):
                recommendations.append(f"Peak usage at hour {analytics['temporal_analysis']['peak_hour']} - consider server scaling")
        
        return recommendations


# Global instances
analytics_engine = AdvancedAnalyticsEngine()
report_generator = ReportGenerator()
