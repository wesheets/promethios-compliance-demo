"""
Regulatory Frameworks Package for Promethios Compliance Demo.

This package contains the implementation of the Dynamic Regulatory Mapping System,
which maps trust factors to specific regulatory requirements for different frameworks.
"""

from .base_framework import RegulatoryFramework
from .eu_ai_act_framework import EUAIActFramework
from .finra_framework import FINRAFramework

__all__ = [
    'RegulatoryFramework',
    'EUAIActFramework',
    'FINRAFramework',
]
