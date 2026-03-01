"""
Supply Chain Risk Mitigation Module
Integrated with FMEA Generator for real-time transport optimization
"""

from .network_config import ROUTE_MAP, SUPPLY_CAPACITY, DEMAND_REQ, route_map
from .mitigation_solver import generate_impact_report, solve_mitigation_plan, solve_guardian_plan
from .disruption_extractor import DisruptionExtractor
from .report_generator import (
    generate_impact_report as generate_impact_report_v1,
    format_for_streamlit,
    get_route_change_summary
)
from .risk_monitor import scan_news_for_risk
from .input_handler import extract_shipment_plan

__version__ = "2.0.0"
__all__ = [
    'ROUTE_MAP',
    'route_map',
    'SUPPLY_CAPACITY', 
    'DEMAND_REQ',
    'DisruptionExtractor',
    'generate_impact_report',
    'solve_mitigation_plan',
    'solve_guardian_plan',
    'generate_impact_report_v1',
    'format_for_streamlit',
    'get_route_change_summary',
    'scan_news_for_risk',
    'extract_shipment_plan'
]
