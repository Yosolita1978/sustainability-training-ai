"""
models.py — Pydantic data models for Marketing-Focused Sustainability Compliance Platform
Updated to support brand awareness campaigns, email/content marketing, and detailed compliance reporting.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime, date


# ----------------------
# ENUMS FOR MARKETING CONTEXT
# ----------------------

class MarketingChannel(str, Enum):
    EMAIL_MARKETING = "email_marketing"
    CONTENT_MARKETING = "content_marketing" 
    BLOG_POSTS = "blog_posts"
    WEBSITE_CONTENT = "website_content"
    SOCIAL_MEDIA_CONTENT = "social_media_content"
    NEWSLETTERS = "newsletters"
    WHITEPAPERS = "whitepapers"
    CASE_STUDIES = "case_studies"
    PRESS_RELEASES = "press_releases"


class CampaignType(str, Enum):
    BRAND_AWARENESS = "brand_awareness"
    PRODUCT_LAUNCH = "product_launch"
    THOUGHT_LEADERSHIP = "thought_leadership"
    CUSTOMER_EDUCATION = "customer_education"
    CORPORATE_MESSAGING = "corporate_messaging"


class SustainabilityClaimType(str, Enum):
    CARBON_NEUTRAL = "carbon_neutral"
    ECO_FRIENDLY = "eco_friendly"
    SUSTAINABLE_SOURCING = "sustainable_sourcing"
    RENEWABLE_ENERGY = "renewable_energy"
    CIRCULAR_ECONOMY = "circular_economy"
    ORGANIC = "organic"
    BIODEGRADABLE = "biodegradable"
    RECYCLABLE = "recyclable"
    ZERO_WASTE = "zero_waste"
    ENERGY_EFFICIENT = "energy_efficient"
    WATER_CONSERVATION = "water_conservation"
    ETHICAL_SOURCING = "ethical_sourcing"
    GREEN_TECHNOLOGY = "green_technology"
    SUSTAINABLE_PACKAGING = "sustainable_packaging"
    CARBON_NEGATIVE = "carbon_negative"


class ComplianceRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"


class BudgetTier(str, Enum):
    SMALL = "small"  # <$10K
    MEDIUM = "medium"  # $10K-$100K
    LARGE = "large"  # >$100K


class CampaignPhase(str, Enum):
    PRE_LAUNCH = "pre_launch"
    LAUNCH = "launch"
    POST_CAMPAIGN = "post_campaign"


class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


# ----------------------
# ORIGINAL INPUT MODELS (KEPT FOR COMPATIBILITY)
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
# NEW MARKETING INPUT MODELS
# ----------------------

class MarketingCampaignProfile(BaseModel):
    """Complete marketing campaign profile for compliance analysis"""
    
    # Campaign Basics
    campaign_name: str = Field(..., description="Name of the marketing campaign")
    campaign_type: CampaignType = Field(..., description="Type of marketing campaign")
    campaign_phase: CampaignPhase = Field(default=CampaignPhase.PRE_LAUNCH, description="Current phase of campaign")
    
    # Company Context
    company_name: str = Field(..., description="Company running the campaign")
    industry: str = Field(..., description="Company industry sector")
    company_size: Optional[str] = Field(None, description="Company size (SME, Mid, Large)")
    
    # Campaign Details
    target_audience: str = Field(..., description="Primary target audience description")
    campaign_duration: Optional[str] = Field(None, description="Expected campaign duration")
    budget_tier: BudgetTier = Field(..., description="Campaign budget category")
    
    # Marketing Channels
    primary_channels: List[MarketingChannel] = Field(..., description="Primary marketing channels to be used")
    secondary_channels: Optional[List[MarketingChannel]] = Field(None, description="Secondary marketing channels")
    
    # Content and Claims
    campaign_objectives: List[str] = Field(..., description="Main campaign objectives")
    sustainability_claims: List[str] = Field(..., description="Sustainability claims to be made")
    claim_types: List[SustainabilityClaimType] = Field(..., description="Types of sustainability claims")
    
    # Supporting Evidence
    evidence_available: Optional[List[str]] = Field(None, description="Evidence supporting sustainability claims")
    certifications: Optional[List[str]] = Field(None, description="Relevant certifications or third-party validations")
    
    # Regulatory Context
    target_markets: List[str] = Field(..., description="Geographic markets for campaign")
    regulatory_requirements: Optional[List[str]] = Field(None, description="Known regulatory requirements")
    
    # Risk Factors
    competitive_claims: Optional[List[str]] = Field(None, description="Competitor sustainability claims in market")
    potential_challenges: Optional[List[str]] = Field(None, description="Anticipated compliance challenges")


class CampaignContent(BaseModel):
    """Specific campaign content for analysis"""
    
    content_id: str = Field(..., description="Unique identifier for content piece")
    channel: MarketingChannel = Field(..., description="Marketing channel for this content")
    content_type: str = Field(..., description="Type of content (email, blog post, etc.)")
    
    # Content Details
    subject_line: Optional[str] = Field(None, description="Subject line or headline")
    body_content: str = Field(..., description="Main content body")
    call_to_action: Optional[str] = Field(None, description="Call to action text")
    
    # Claims Analysis
    explicit_claims: List[str] = Field(default=[], description="Explicit sustainability claims made")
    implicit_claims: List[str] = Field(default=[], description="Implied sustainability claims")
    visual_elements: Optional[List[str]] = Field(None, description="Visual elements with sustainability messaging")
    
    # Metadata
    target_audience_segment: Optional[str] = Field(None, description="Specific audience segment")
    publication_date: Optional[date] = Field(None, description="Planned or actual publication date")


# ----------------------
# MARKETING OUTPUT MODELS
# ----------------------

class ClaimVerificationResult(BaseModel):
    """Result of verifying a specific sustainability claim"""
    
    claim_text: str = Field(..., description="The exact claim being verified")
    claim_type: SustainabilityClaimType = Field(..., description="Category of sustainability claim")
    
    # Verification Results
    compliance_status: ComplianceStatus = Field(..., description="Overall compliance status")
    risk_level: ComplianceRiskLevel = Field(..., description="Risk level assessment")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence in assessment (0-1)")
    
    # Analysis Details
    supporting_evidence: List[str] = Field(default=[], description="Evidence supporting the claim")
    missing_evidence: List[str] = Field(default=[], description="Required evidence not provided")
    regulatory_requirements: List[str] = Field(default=[], description="Applicable regulatory requirements")
    
    # Recommendations
    compliance_issues: List[str] = Field(default=[], description="Identified compliance issues")
    recommended_modifications: List[str] = Field(default=[], description="Suggested claim modifications")
    additional_evidence_needed: List[str] = Field(default=[], description="Additional evidence required")


class ChannelComplianceAnalysis(BaseModel):
    """Compliance analysis for a specific marketing channel"""
    
    channel: MarketingChannel = Field(..., description="Marketing channel analyzed")
    overall_risk_level: ComplianceRiskLevel = Field(..., description="Overall risk level for this channel")
    
    # Channel-Specific Analysis
    channel_regulations: List[str] = Field(default=[], description="Regulations specific to this channel")
    common_violations: List[str] = Field(default=[], description="Common compliance violations for this channel")
    best_practices: List[str] = Field(default=[], description="Recommended best practices")
    
    # Content Analysis
    content_pieces_analyzed: int = Field(default=0, description="Number of content pieces analyzed")
    compliant_content: int = Field(default=0, description="Number of compliant content pieces")
    flagged_content: List[str] = Field(default=[], description="Content requiring attention")
    
    # Recommendations
    immediate_actions: List[str] = Field(default=[], description="Actions needed immediately")
    optimization_opportunities: List[str] = Field(default=[], description="Opportunities for improvement")
    monitoring_requirements: List[str] = Field(default=[], description="Ongoing monitoring needs")


class RiskAssessmentResult(BaseModel):
    """Comprehensive risk assessment for marketing campaign"""
    
    overall_risk_level: ComplianceRiskLevel = Field(..., description="Overall campaign risk level")
    risk_score: float = Field(..., ge=0, le=100, description="Numerical risk score (0-100)")
    
    # Risk Categories
    regulatory_risks: List[str] = Field(default=[], description="Regulatory compliance risks")
    reputational_risks: List[str] = Field(default=[], description="Brand reputation risks")
    market_risks: List[str] = Field(default=[], description="Market positioning risks")
    operational_risks: List[str] = Field(default=[], description="Operational implementation risks")
    
    # Risk Mitigation
    high_priority_mitigations: List[str] = Field(default=[], description="High priority risk mitigations")
    medium_priority_mitigations: List[str] = Field(default=[], description="Medium priority risk mitigations")
    monitoring_protocols: List[str] = Field(default=[], description="Risk monitoring protocols")
    
    # Impact Assessment
    potential_penalties: List[str] = Field(default=[], description="Potential regulatory penalties")
    brand_impact_assessment: str = Field(default="", description="Assessment of potential brand impact")
    financial_risk_estimate: Optional[str] = Field(None, description="Estimated financial risk range")


class MarketingRecommendation(BaseModel):
    """Specific recommendation for marketing compliance"""
    
    recommendation_id: str = Field(..., description="Unique identifier for recommendation")
    priority_level: ComplianceRiskLevel = Field(..., description="Priority level (using risk level enum)")
    category: str = Field(..., description="Category of recommendation")
    
    # Recommendation Details
    title: str = Field(..., description="Brief title of recommendation")
    description: str = Field(..., description="Detailed description of recommendation")
    rationale: str = Field(..., description="Explanation of why this is recommended")
    
    # Implementation
    implementation_steps: List[str] = Field(default=[], description="Steps to implement recommendation")
    required_resources: List[str] = Field(default=[], description="Resources needed for implementation")
    timeline: Optional[str] = Field(None, description="Recommended implementation timeline")
    
    # Impact
    expected_outcome: str = Field(..., description="Expected outcome of implementing recommendation")
    success_metrics: List[str] = Field(default=[], description="Metrics to measure success")
    dependencies: List[str] = Field(default=[], description="Dependencies for implementation")


class CompetitorAnalysis(BaseModel):
    """Analysis of competitor sustainability messaging"""
    
    competitor_name: Optional[str] = Field(None, description="Competitor company name")
    market_segment: str = Field(..., description="Market segment analysis")
    
    # Competitive Landscape
    common_claims: List[str] = Field(default=[], description="Common sustainability claims in market")
    differentiation_opportunities: List[str] = Field(default=[], description="Opportunities to differentiate")
    compliance_benchmarks: List[str] = Field(default=[], description="Industry compliance benchmarks")
    
    # Risk Analysis
    over_saturated_claims: List[str] = Field(default=[], description="Overused claims to avoid")
    emerging_trends: List[str] = Field(default=[], description="Emerging sustainability trends")
    regulatory_precedents: List[str] = Field(default=[], description="Relevant regulatory actions")


class MarketingComplianceReport(BaseModel):
    """Comprehensive marketing compliance report - main output model"""
    
    # Report Metadata
    report_id: str = Field(..., description="Unique report identifier")
    campaign_name: str = Field(..., description="Campaign name analyzed")
    company_name: str = Field(..., description="Company name")
    analysis_date: datetime = Field(default_factory=datetime.now, description="Date of analysis")
    report_version: str = Field(default="1.0", description="Report version")
    
    # Executive Summary
    overall_compliance_status: ComplianceStatus = Field(..., description="Overall compliance status")
    overall_risk_level: ComplianceRiskLevel = Field(..., description="Overall risk level")
    executive_summary: str = Field(..., description="Executive summary of findings")
    key_findings: List[str] = Field(default=[], description="Key findings from analysis")
    
    # Detailed Analysis
    claim_verification_results: List[ClaimVerificationResult] = Field(default=[], description="Individual claim verification results")
    channel_analysis: List[ChannelComplianceAnalysis] = Field(default=[], description="Channel-specific compliance analysis")
    risk_assessment: RiskAssessmentResult = Field(..., description="Comprehensive risk assessment")
    
    # Recommendations
    immediate_actions: List[MarketingRecommendation] = Field(default=[], description="Immediate actions required")
    strategic_recommendations: List[MarketingRecommendation] = Field(default=[], description="Strategic recommendations")
    ongoing_monitoring: List[str] = Field(default=[], description="Ongoing monitoring requirements")
    
    # Market Intelligence
    competitor_analysis: Optional[CompetitorAnalysis] = Field(None, description="Competitive landscape analysis")
    market_trends: List[str] = Field(default=[], description="Relevant market trends")
    regulatory_updates: List[str] = Field(default=[], description="Recent regulatory updates")
    
    # Supporting Information
    evidence_summary: List[str] = Field(default=[], description="Summary of supporting evidence")
    regulatory_framework: List[str] = Field(default=[], description="Applicable regulatory frameworks")
    industry_benchmarks: List[str] = Field(default=[], description="Industry compliance benchmarks")
    
    # Action Plan
    short_term_actions: List[str] = Field(default=[], description="Actions for next 30 days")
    medium_term_actions: List[str] = Field(default=[], description="Actions for next 90 days")
    long_term_strategy: List[str] = Field(default=[], description="Long-term compliance strategy")
    
    # Quality Assurance
    confidence_level: float = Field(..., ge=0, le=1, description="Overall confidence in analysis")
    limitations: List[str] = Field(default=[], description="Analysis limitations")
    assumptions: List[str] = Field(default=[], description="Assumptions made in analysis")
    
    # Sources and References
    sources_consulted: List[str] = Field(default=[], description="Sources consulted for analysis")
    regulatory_references: List[str] = Field(default=[], description="Regulatory references used")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ----------------------
# LEGACY COMPATIBILITY MODELS (KEPT FOR EXISTING FUNCTIONALITY)
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
# SUMMARY MODELS FOR SMART CONTEXT MANAGEMENT
# ----------------------

class AgentSummary(BaseModel):
    """Base summary model for condensed agent outputs"""
    agent_name: str = Field(..., description="Name of the agent that produced this summary")
    execution_timestamp: datetime = Field(default_factory=datetime.now, description="When the agent completed")
    overall_status: str = Field(..., description="Overall status from agent analysis")
    key_findings: List[str] = Field(default=[], description="Top 3-5 key findings")
    critical_issues: List[str] = Field(default=[], description="Issues requiring immediate attention")
    confidence_level: float = Field(default=0.8, ge=0, le=1, description="Agent confidence in analysis")


class ComplianceAnalysisSummary(AgentSummary):
    """Condensed summary of marketing compliance analysis"""
    compliance_status: ComplianceStatus = Field(..., description="Overall compliance status")
    risk_level: ComplianceRiskLevel = Field(..., description="Overall risk level")
    claims_analyzed: int = Field(default=0, description="Number of claims analyzed")
    high_risk_claims: int = Field(default=0, description="Number of high-risk claims")
    channels_with_issues: List[str] = Field(default=[], description="Channels requiring attention")
    immediate_actions_needed: List[str] = Field(default=[], description="Immediate actions required")
    evidence_gaps: List[str] = Field(default=[], description="Critical evidence gaps")


class RegulatoryReviewSummary(AgentSummary):
    """Condensed summary of regulatory compliance review"""
    enforcement_risk: ComplianceRiskLevel = Field(..., description="Regulatory enforcement risk level")
    applicable_regulations: List[str] = Field(default=[], description="Key applicable regulations")
    high_priority_obligations: List[str] = Field(default=[], description="High priority compliance obligations")
    penalty_exposure: str = Field(default="", description="Potential penalty exposure summary")
    regulatory_deadlines: List[str] = Field(default=[], description="Upcoming regulatory deadlines")


class StrategyAnalysisSummary(AgentSummary):
    """Condensed summary of brand positioning strategy analysis"""
    positioning_approach: str = Field(..., description="Core positioning strategy")
    competitive_advantage: str = Field(..., description="Primary competitive advantage")
    implementation_priority: ComplianceRiskLevel = Field(..., description="Implementation priority level")
    roi_outlook: str = Field(..., description="ROI outlook summary")
    strategic_recommendations: List[str] = Field(default=[], description="Top strategic recommendations")


class LightweightCampaignData(BaseModel):
    """Reduced campaign data for agent-to-agent communication"""
    campaign_name: str
    campaign_type: CampaignType
    company_name: str
    industry: str
    primary_channels: List[MarketingChannel]
    target_markets: List[str]
    budget_tier: BudgetTier
    claims_count: int = Field(default=0, description="Number of sustainability claims")
    high_risk_claims: List[str] = Field(default=[], description="High-risk claims requiring attention")
    evidence_available: bool = Field(default=False, description="Whether supporting evidence is available")


class AgentDataPackage(BaseModel):
    """Data package passed between agents with only essential information"""
    lightweight_campaign: LightweightCampaignData
    previous_summaries: List[AgentSummary] = Field(default=[], description="Summaries from previous agents")
    specific_inputs: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific input data")
    context_metadata: Dict[str, Any] = Field(default_factory=dict, description="Context and processing metadata")


# ----------------------
# AGGREGATE RESULT MODELS (UPDATED)
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


class MarketingAnalysisResult(BaseModel):
    """New primary output for marketing-focused analysis"""
    marketing_compliance_report: MarketingComplianceReport
    campaign_profile: MarketingCampaignProfile
    analysis_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Optional legacy compatibility
    legacy_business_analysis: Optional[BusinessAnalysisResult] = None


class MarketingWorkflowResult(BaseModel):
    """Complete workflow result with summaries and full details"""
    final_report: MarketingComplianceReport
    agent_summaries: List[AgentSummary] = Field(default=[], description="Summaries from each agent")
    workflow_metadata: Dict[str, Any] = Field(default_factory=dict, description="Workflow execution metadata")
    context_optimization: Dict[str, Any] = Field(default_factory=dict, description="Context management metrics")