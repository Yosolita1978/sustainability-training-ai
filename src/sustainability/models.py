"""
models.py — Pydantic data models for Sustainability Business Toolkit
Defines validated structures for inputs and outputs to preserve functionality.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ----------------------
# INPUT MODELS
# ----------------------

class CompanyProfile(BaseModel):
    name: str = Field(..., description="Company name")
    description: Optional[str] = Field(None, description="Brief description of the company")
    size: Optional[str] = Field(None, description="Size category: SME, Mid, Large")
    location: Optional[str] = Field(None, description="Headquarters location")
    industry: Optional[str] = Field(None, description="Main industry sector")
    founded_year: Optional[int] = Field(None, description="Year company was founded")
    sustainability_goals: Optional[List[str]] = Field(None, description="High-level sustainability objectives")


class OperationsData(BaseModel):
    facilities: Optional[List[str]] = Field(None, description="List of facilities / sites operated")
    energy_sources: Optional[List[str]] = Field(None, description="Types of energy sources used")
    annual_emissions_tonnes: Optional[float] = Field(None, description="Annual CO₂ equivalent emissions")
    supply_chain_notes: Optional[str] = Field(None, description="Additional supply chain details")


class JurisdictionInfo(BaseModel):
    country: str
    region: Optional[str] = None


# ----------------------
# OUTPUT MODELS
# ----------------------

class BusinessBenchmark(BaseModel):
    comparative_rank: Optional[str] = Field(None, description="Industry percentile or ranking")
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class OpportunityItem(BaseModel):
    opportunity_name: str
    description: Optional[str] = None
    potential_roi: Optional[str] = None


class ComplianceSummary(BaseModel):
    compliant_areas: Optional[List[str]] = None
    non_compliant_areas: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None


class StrategicInitiative(BaseModel):
    name: str
    description: Optional[str] = None
    expected_roi: Optional[str] = None


class FinalReport(BaseModel):
    formatted_markdown: str
    pdf_export: Optional[bytes] = None
    json_export: Optional[dict] = None


# ----------------------
# AGGREGATE RESULT MODELS
# ----------------------

class BusinessAnalysisResult(BaseModel):
    business_benchmark: Optional[BusinessBenchmark] = None
    opportunity_list: Optional[List[OpportunityItem]] = None
    operational_risk_list: Optional[List[str]] = None
    quick_reference_tools: Optional[List[Dict[str, Any]]] = None
    market_intelligence: Optional[List[Dict[str, Any]]] = None
    communication_templates: Optional[List[Dict[str, Any]]] = None
    role_specific_guides: Optional[List[Dict[str, Any]]] = None


class StrategyResult(BaseModel):
    strategic_initiatives: Optional[List[StrategicInitiative]]
    roi_analysis: Optional[dict] = None
    market_positioning: Optional[str] = None