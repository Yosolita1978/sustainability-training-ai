"""
marketing_tools.py — Marketing-specific analysis tools for sustainability compliance
Focused on brand awareness campaigns, email/content marketing, and detailed compliance analysis.
"""

from crewai.tools import BaseTool
from typing import Type, List, Dict, Any
from pydantic import BaseModel, Field
import json
import re
from datetime import datetime

from sustainability.models import (
    MarketingChannel, SustainabilityClaimType, ComplianceRiskLevel, 
    ComplianceStatus, ClaimVerificationResult, ChannelComplianceAnalysis,
    RiskAssessmentResult, MarketingRecommendation
)


# ----------------------
# INPUT SCHEMAS
# ----------------------

class BrandAwarenessInput(BaseModel):
    """Input schema for brand awareness compliance scanning."""
    campaign_content: str = Field(..., description="Campaign content to analyze for brand awareness compliance")
    target_audience: str = Field(..., description="Target audience for the brand awareness campaign")
    channels: List[str] = Field(..., description="Marketing channels being used")
    sustainability_claims: List[str] = Field(..., description="Sustainability claims being made")


class EmailMarketingInput(BaseModel):
    """Input schema for email marketing claim verification."""
    email_subject: str = Field(..., description="Email subject line")
    email_content: str = Field(..., description="Email body content")
    call_to_action: str = Field(..., description="Email call to action")
    recipient_segment: str = Field(..., description="Target recipient segment")


class ContentMarketingInput(BaseModel):
    """Input schema for content marketing analysis."""
    content_type: str = Field(..., description="Type of content (blog post, article, whitepaper, etc.)")
    content_title: str = Field(..., description="Content title or headline")
    content_body: str = Field(..., description="Full content body")
    publication_channel: str = Field(..., description="Where content will be published")


class ClaimValidationInput(BaseModel):
    """Input schema for sustainability claim validation."""
    claims: List[str] = Field(..., description="List of sustainability claims to validate")
    evidence_provided: List[str] = Field(..., description="Evidence supporting the claims")
    target_markets: List[str] = Field(..., description="Geographic markets where claims will be used")
    industry_sector: str = Field(..., description="Company industry sector")


class RiskAssessmentInput(BaseModel):
    """Input schema for marketing risk assessment."""
    campaign_name: str = Field(..., description="Campaign name")
    marketing_channels: List[str] = Field(..., description="Marketing channels to be used")
    sustainability_claims: List[str] = Field(..., description="Sustainability claims in campaign")
    target_markets: List[str] = Field(..., description="Target geographic markets")
    budget_tier: str = Field(..., description="Campaign budget tier (small, medium, large)")


# ----------------------
# MARKETING ANALYSIS TOOLS
# ----------------------

class BrandAwarenessComplianceScanner(BaseTool):
    """Analyzes brand awareness campaign messaging for sustainability compliance"""
    
    name: str = "brand_awareness_compliance_scanner"
    description: str = (
        "Analyzes brand awareness campaign content for sustainability compliance issues. "
        "Identifies potential greenwashing risks, regulatory violations, and provides "
        "specific recommendations for brand messaging compliance across marketing channels."
    )
    args_schema: Type[BaseModel] = BrandAwarenessInput
    
    def _run(self, campaign_content: str, target_audience: str, channels: List[str], sustainability_claims: List[str]) -> str:
        """Analyze brand awareness campaign for compliance"""
        
        # Analyze content for compliance issues
        analysis_results = {
            "campaign_analysis": {
                "content_length": len(campaign_content),
                "channels_analyzed": len(channels),
                "claims_detected": len(sustainability_claims),
                "target_audience": target_audience
            },
            "compliance_findings": [],
            "risk_assessment": "medium",
            "channel_specific_issues": {},
            "recommendations": []
        }
        
        # Check for common greenwashing terms
        greenwashing_terms = [
            "eco-friendly", "green", "natural", "sustainable", "environmentally friendly",
            "earth-friendly", "carbon neutral", "100% renewable", "zero waste", "clean energy"
        ]
        
        detected_terms = []
        for term in greenwashing_terms:
            if term.lower() in campaign_content.lower():
                detected_terms.append(term)
        
        if detected_terms:
            analysis_results["compliance_findings"].append(
                f"Detected potentially problematic terms requiring substantiation: {', '.join(detected_terms)}"
            )
        
        # Channel-specific analysis
        for channel in channels:
            channel_lower = channel.lower()
            if "email" in channel_lower:
                analysis_results["channel_specific_issues"]["email_marketing"] = [
                    "Ensure CAN-SPAM compliance with sustainability claims",
                    "Verify all claims can be substantiated in linked content",
                    "Consider disclaimer requirements for environmental claims"
                ]
            elif "content" in channel_lower or "blog" in channel_lower:
                analysis_results["channel_specific_issues"]["content_marketing"] = [
                    "Ensure long-form content provides adequate substantiation",
                    "Include citations for environmental data and claims",
                    "Consider SEO implications of sustainability terminology"
                ]
        
        # Risk level assessment
        risk_factors = 0
        if len(detected_terms) > 3:
            risk_factors += 2
        if any("100%" in claim or "zero" in claim for claim in sustainability_claims):
            risk_factors += 2
        if len(channels) > 3:
            risk_factors += 1
        
        if risk_factors >= 4:
            analysis_results["risk_assessment"] = "high"
        elif risk_factors >= 2:
            analysis_results["risk_assessment"] = "medium"
        else:
            analysis_results["risk_assessment"] = "low"
        
        # Generate recommendations
        analysis_results["recommendations"] = [
            "Conduct substantiation review for all environmental claims",
            "Develop channel-specific compliance guidelines",
            "Implement pre-publication legal review process",
            "Create approved sustainability messaging framework",
            "Establish ongoing monitoring for competitor practices"
        ]
        
        return json.dumps(analysis_results, indent=2)


class EmailMarketingClaimVerifier(BaseTool):
    """Verifies email marketing content for sustainability claim compliance"""
    
    name: str = "email_marketing_claim_verifier"
    description: str = (
        "Analyzes email marketing content for sustainability claim compliance. "
        "Checks subject lines, body content, and calls-to-action for regulatory "
        "compliance and provides specific recommendations for email campaigns."
    )
    args_schema: Type[BaseModel] = EmailMarketingInput
    
    def _run(self, email_subject: str, email_content: str, call_to_action: str, recipient_segment: str) -> str:
        """Verify email marketing claims for compliance"""
        
        verification_results = {
            "email_analysis": {
                "subject_line_length": len(email_subject),
                "content_length": len(email_content),
                "cta_present": bool(call_to_action),
                "recipient_segment": recipient_segment
            },
            "claim_verification": [],
            "compliance_status": "requires_review",
            "risk_level": "medium",
            "specific_issues": [],
            "recommendations": []
        }
        
        # Analyze subject line for claims
        subject_claims = []
        sustainability_keywords = [
            "sustainable", "eco", "green", "carbon neutral", "renewable", 
            "organic", "natural", "environmentally friendly", "zero waste"
        ]
        
        for keyword in sustainability_keywords:
            if keyword.lower() in email_subject.lower():
                subject_claims.append(keyword)
        
        if subject_claims:
            verification_results["claim_verification"].append({
                "location": "subject_line",
                "claims_detected": subject_claims,
                "substantiation_required": True,
                "risk_level": "high" if len(subject_claims) > 2 else "medium"
            })
        
        # Analyze email body content
        body_claims = []
        absolute_terms = ["100%", "completely", "totally", "zero", "never", "always", "all"]
        
        for term in absolute_terms:
            if term in email_content:
                body_claims.append(f"Absolute claim: '{term}'")
        
        if body_claims:
            verification_results["claim_verification"].append({
                "location": "email_body",
                "claims_detected": body_claims,
                "substantiation_required": True,
                "risk_level": "high"
            })
        
        # Analyze call-to-action
        if call_to_action:
            cta_issues = []
            if any(keyword in call_to_action.lower() for keyword in sustainability_keywords):
                cta_issues.append("Sustainability claims in CTA require substantiation")
            
            if cta_issues:
                verification_results["claim_verification"].append({
                    "location": "call_to_action",
                    "issues": cta_issues,
                    "risk_level": "medium"
                })
        
        # Determine overall compliance status
        high_risk_claims = sum(1 for claim in verification_results["claim_verification"] 
                              if claim.get("risk_level") == "high")
        
        if high_risk_claims > 0:
            verification_results["compliance_status"] = "non_compliant"
            verification_results["risk_level"] = "high"
        elif len(verification_results["claim_verification"]) > 0:
            verification_results["compliance_status"] = "requires_review"
            verification_results["risk_level"] = "medium"
        else:
            verification_results["compliance_status"] = "compliant"
            verification_results["risk_level"] = "low"
        
        # Generate specific recommendations
        verification_results["recommendations"] = [
            "Add disclaimers for all environmental claims",
            "Include links to substantiation evidence",
            "Review subject line claims for FTC compliance",
            "Implement A/B testing for compliant alternatives",
            "Establish legal review process for sustainability emails"
        ]
        
        return json.dumps(verification_results, indent=2)


class ContentMarketingAnalyzer(BaseTool):
    """Analyzes content marketing materials for sustainability compliance"""
    
    name: str = "content_marketing_analyzer"
    description: str = (
        "Analyzes blog posts, articles, whitepapers, and other content marketing "
        "materials for sustainability claim compliance. Provides detailed analysis "
        "of content structure, claim substantiation, and regulatory requirements."
    )
    args_schema: Type[BaseModel] = ContentMarketingInput
    
    def _run(self, content_type: str, content_title: str, content_body: str, publication_channel: str) -> str:
        """Analyze content marketing for sustainability compliance"""
        
        content_analysis = {
            "content_metadata": {
                "type": content_type,
                "title": content_title,
                "word_count": len(content_body.split()),
                "publication_channel": publication_channel
            },
            "sustainability_analysis": {
                "claims_identified": [],
                "evidence_assessment": {},
                "citation_analysis": {},
                "regulatory_considerations": []
            },
            "compliance_score": 0,
            "risk_assessment": {},
            "improvement_recommendations": []
        }
        
        # Identify sustainability claims in content
        sustainability_patterns = [
            r"carbon.{0,10}neutral",
            r"100%.{0,20}renewable",
            r"zero.{0,10}waste",
            r"environmentally.{0,10}friendly",
            r"sustainable.{0,20}sourcing",
            r"eco.{0,10}friendly",
            r"green.{0,10}technology"
        ]
        
        claims_found = []
        for pattern in sustainability_patterns:
            matches = re.findall(pattern, content_body, re.IGNORECASE)
            claims_found.extend(matches)
        
        content_analysis["sustainability_analysis"]["claims_identified"] = claims_found
        
        # Assess evidence and citations
        citation_indicators = ["according to", "study shows", "research indicates", "data from", "source:"]
        citations_count = sum(1 for indicator in citation_indicators 
                             if indicator.lower() in content_body.lower())
        
        content_analysis["sustainability_analysis"]["citation_analysis"] = {
            "citations_found": citations_count,
            "claims_to_citations_ratio": citations_count / max(len(claims_found), 1),
            "adequately_cited": citations_count >= len(claims_found)
        }
        
        # Compliance scoring
        base_score = 50
        if content_analysis["sustainability_analysis"]["citation_analysis"]["adequately_cited"]:
            base_score += 30
        if len(claims_found) <= 5:  # Reasonable number of claims
            base_score += 15
        if content_type.lower() in ["whitepaper", "case_study", "research_report"]:
            base_score += 5  # Higher standard expected
        
        content_analysis["compliance_score"] = min(base_score, 100)
        
        # Risk assessment
        risk_factors = []
        if len(claims_found) > 5:
            risk_factors.append("High number of sustainability claims")
        if citations_count < len(claims_found):
            risk_factors.append("Insufficient citation support")
        if any("100%" in claim for claim in claims_found):
            risk_factors.append("Absolute claims requiring strong substantiation")
        
        content_analysis["risk_assessment"] = {
            "risk_factors": risk_factors,
            "risk_level": "high" if len(risk_factors) >= 3 else "medium" if len(risk_factors) >= 1 else "low"
        }
        
        # Generate recommendations
        recommendations = [
            "Add citations for all sustainability claims",
            "Include methodology explanations for data claims",
            "Consider adding sustainability disclaimer section"
        ]
        
        if content_analysis["compliance_score"] < 70:
            recommendations.extend([
                "Reduce number of unsubstantiated claims",
                "Implement fact-checking review process",
                "Consider legal review before publication"
            ])
        
        content_analysis["improvement_recommendations"] = recommendations
        
        return json.dumps(content_analysis, indent=2)


class SustainabilityClaimValidator(BaseTool):
    """Validates specific sustainability claims against evidence and regulations"""
    
    name: str = "sustainability_claim_validator"
    description: str = (
        "Validates sustainability claims against provided evidence and regulatory "
        "requirements. Analyzes claim types, substantiation requirements, and "
        "provides specific compliance recommendations for each claim."
    )
    args_schema: Type[BaseModel] = ClaimValidationInput
    
    def _run(self, claims: List[str], evidence_provided: List[str], target_markets: List[str], industry_sector: str) -> str:
        """Validate sustainability claims against evidence and regulations"""
        
        validation_results = {
            "validation_summary": {
                "total_claims": len(claims),
                "evidence_items": len(evidence_provided),
                "target_markets": target_markets,
                "industry_sector": industry_sector
            },
            "individual_claim_analysis": [],
            "evidence_adequacy": {},
            "regulatory_compliance": {},
            "overall_assessment": {}
        }
        
        # Analyze each claim individually
        for i, claim in enumerate(claims):
            claim_analysis = {
                "claim_id": f"claim_{i+1}",
                "claim_text": claim,
                "claim_type": self._categorize_claim(claim),
                "risk_level": self._assess_claim_risk(claim),
                "substantiation_requirements": self._get_substantiation_requirements(claim),
                "regulatory_considerations": self._get_regulatory_considerations(claim, target_markets),
                "evidence_match": self._match_evidence_to_claim(claim, evidence_provided)
            }
            validation_results["individual_claim_analysis"].append(claim_analysis)
        
        # Overall evidence adequacy assessment
        evidence_score = min((len(evidence_provided) / max(len(claims), 1)) * 100, 100)
        validation_results["evidence_adequacy"] = {
            "adequacy_score": evidence_score,
            "sufficient_evidence": evidence_score >= 80,
            "evidence_gaps": self._identify_evidence_gaps(claims, evidence_provided),
            "recommended_additional_evidence": self._recommend_additional_evidence(claims, evidence_provided)
        }
        
        # Regulatory compliance assessment
        high_risk_claims = sum(1 for analysis in validation_results["individual_claim_analysis"] 
                              if analysis["risk_level"] == "high")
        
        validation_results["regulatory_compliance"] = {
            "overall_compliance_risk": "high" if high_risk_claims > 2 else "medium" if high_risk_claims > 0 else "low",
            "market_specific_requirements": self._get_market_requirements(target_markets),
            "industry_specific_considerations": self._get_industry_considerations(industry_sector)
        }
        
        # Overall assessment
        overall_risk = "low"
        if high_risk_claims > 2 or evidence_score < 60:
            overall_risk = "high"
        elif high_risk_claims > 0 or evidence_score < 80:
            overall_risk = "medium"
        
        validation_results["overall_assessment"] = {
            "validation_status": "approved" if overall_risk == "low" else "requires_modification" if overall_risk == "medium" else "not_approved",
            "confidence_level": max(evidence_score - (high_risk_claims * 20), 0),
            "recommended_actions": self._generate_recommended_actions(overall_risk, evidence_score, high_risk_claims)
        }
        
        return json.dumps(validation_results, indent=2)
    
    def _categorize_claim(self, claim: str) -> str:
        """Categorize sustainability claim type"""
        claim_lower = claim.lower()
        if "carbon" in claim_lower and "neutral" in claim_lower:
            return "carbon_neutral"
        elif "renewable" in claim_lower:
            return "renewable_energy"
        elif "organic" in claim_lower:
            return "organic"
        elif "sustainable" in claim_lower:
            return "sustainable_sourcing"
        elif "eco" in claim_lower or "green" in claim_lower:
            return "eco_friendly"
        else:
            return "general_environmental"
    
    def _assess_claim_risk(self, claim: str) -> str:
        """Assess risk level of individual claim"""
        high_risk_terms = ["100%", "zero", "completely", "never", "always", "carbon neutral"]
        medium_risk_terms = ["eco-friendly", "green", "sustainable", "environmentally friendly"]
        
        claim_lower = claim.lower()
        if any(term in claim_lower for term in high_risk_terms):
            return "high"
        elif any(term in claim_lower for term in medium_risk_terms):
            return "medium"
        else:
            return "low"
    
    def _get_substantiation_requirements(self, claim: str) -> List[str]:
        """Get substantiation requirements for claim"""
        claim_lower = claim.lower()
        if "carbon neutral" in claim_lower:
            return ["Carbon footprint calculation", "Offset verification", "Third-party audit"]
        elif "renewable" in claim_lower:
            return ["Energy source documentation", "Renewable energy certificates", "Usage percentage verification"]
        elif "organic" in claim_lower:
            return ["Organic certification", "Supply chain documentation", "Regular testing results"]
        else:
            return ["General environmental impact assessment", "Supporting documentation", "Third-party verification"]
    
    def _get_regulatory_considerations(self, claim: str, target_markets: List[str]) -> List[str]:
        """Get regulatory considerations for claim and markets"""
        considerations = []
        for market in target_markets:
            if market.upper() in ["US", "USA", "UNITED STATES"]:
                considerations.append("FTC Green Guides compliance required")
            elif market.upper() in ["EU", "EUROPE", "EUROPEAN UNION"]:
                considerations.append("EU Green Claims Directive compliance required")
            elif market.upper() in ["UK", "UNITED KINGDOM"]:
                considerations.append("ASA Green Claims Guidelines compliance required")
        return considerations
    
    def _match_evidence_to_claim(self, claim: str, evidence_provided: List[str]) -> Dict[str, Any]:
        """Match provided evidence to claim requirements"""
        return {
            "evidence_relevance": "medium",  # Simplified for mock
            "evidence_strength": "adequate",
            "gaps_identified": ["Additional third-party verification recommended"]
        }
    
    def _identify_evidence_gaps(self, claims: List[str], evidence: List[str]) -> List[str]:
        """Identify gaps in evidence coverage"""
        return ["Third-party verification documents", "Quantitative impact measurements", "Compliance certifications"]
    
    def _recommend_additional_evidence(self, claims: List[str], evidence: List[str]) -> List[str]:
        """Recommend additional evidence needed"""
        return ["Industry-standard certifications", "Independent audit reports", "Peer-reviewed research citations"]
    
    def _get_market_requirements(self, markets: List[str]) -> Dict[str, List[str]]:
        """Get market-specific requirements"""
        requirements = {}
        for market in markets:
            if market.upper() in ["US", "USA"]:
                requirements[market] = ["FTC substantiation standards", "CAN-SPAM compliance for email"]
            elif market.upper() in ["EU", "EUROPE"]:
                requirements[market] = ["Green Claims Directive", "GDPR for email marketing"]
        return requirements
    
    def _get_industry_considerations(self, industry: str) -> List[str]:
        """Get industry-specific considerations"""
        return [
            f"Industry standards for {industry} sector",
            "Sector-specific sustainability frameworks",
            "Peer benchmarking requirements"
        ]
    
    def _generate_recommended_actions(self, risk_level: str, evidence_score: float, high_risk_claims: int) -> List[str]:
        """Generate recommended actions based on assessment"""
        actions = []
        if risk_level == "high":
            actions.extend([
                "Immediate legal review required",
                "Modify or remove high-risk claims",
                "Gather additional substantiation evidence"
            ])
        elif risk_level == "medium":
            actions.extend([
                "Additional evidence gathering recommended",
                "Consider adding disclaimers",
                "Implement ongoing monitoring"
            ])
        else:
            actions.extend([
                "Proceed with current approach",
                "Maintain evidence documentation",
                "Regular compliance monitoring"
            ])
        return actions


class RiskAssessmentTool(BaseTool):
    """Comprehensive risk assessment for marketing campaigns"""
    
    name: str = "marketing_risk_assessment_tool"
    description: str = (
        "Performs comprehensive risk assessment for marketing campaigns including "
        "regulatory, reputational, and operational risks. Provides risk scoring "
        "and detailed mitigation strategies for sustainability marketing."
    )
    args_schema: Type[BaseModel] = RiskAssessmentInput
    
    def _run(self, campaign_name: str, marketing_channels: List[str], sustainability_claims: List[str], 
             target_markets: List[str], budget_tier: str) -> str:
        """Perform comprehensive marketing risk assessment"""
        
        risk_assessment = {
            "campaign_overview": {
                "campaign_name": campaign_name,
                "channels_count": len(marketing_channels),
                "claims_count": len(sustainability_claims),
                "markets_count": len(target_markets),
                "budget_tier": budget_tier
            },
            "risk_scoring": {
                "overall_risk_score": 0,
                "risk_level": "low",
                "risk_breakdown": {}
            },
            "risk_categories": {
                "regulatory_risks": {},
                "reputational_risks": {},
                "operational_risks": {},
                "financial_risks": {}
            },
            "mitigation_strategies": {
                "immediate_actions": [],
                "short_term_strategies": [],
                "long_term_monitoring": []
            },
            "recommendations": []
        }
        
        # Calculate risk scores
        regulatory_risk = self._assess_regulatory_risk(sustainability_claims, target_markets, marketing_channels)
        reputational_risk = self._assess_reputational_risk(sustainability_claims, budget_tier)
        operational_risk = self._assess_operational_risk(marketing_channels, budget_tier)
        financial_risk = self._assess_financial_risk(budget_tier, target_markets)
        
        # Overall risk calculation
        total_risk_score = (regulatory_risk + reputational_risk + operational_risk + financial_risk) / 4
        
        risk_assessment["risk_scoring"] = {
            "overall_risk_score": round(total_risk_score, 2),
            "risk_level": "high" if total_risk_score >= 7 else "medium" if total_risk_score >= 4 else "low",
            "risk_breakdown": {
                "regulatory_risk": regulatory_risk,
                "reputational_risk": reputational_risk,
                "operational_risk": operational_risk,
                "financial_risk": financial_risk
            }
        }
        
        # Detailed risk category analysis
        risk_assessment["risk_categories"]["regulatory_risks"] = {
            "risk_score": regulatory_risk,
            "primary_concerns": self._get_regulatory_concerns(sustainability_claims, target_markets),
            "compliance_requirements": self._get_compliance_requirements(target_markets),
            "penalty_potential": "high" if regulatory_risk >= 7 else "medium" if regulatory_risk >= 4 else "low"
        }
        
        risk_assessment["risk_categories"]["reputational_risks"] = {
            "risk_score": reputational_risk,
            "greenwashing_potential": "high" if len(sustainability_claims) > 5 else "medium",
            "social_media_exposure": "high" if "social_media_content" in marketing_channels else "medium",
            "brand_impact_assessment": self._assess_brand_impact(sustainability_claims)
        }
        
        risk_assessment["risk_categories"]["operational_risks"] = {
            "risk_score": operational_risk,
            "implementation_complexity": self._assess_implementation_complexity(marketing_channels),
            "resource_requirements": self._assess_resource_requirements(budget_tier, marketing_channels),
            "timeline_risks": self._assess_timeline_risks(marketing_channels)
        }
        
        risk_assessment["risk_categories"]["financial_risks"] = {
            "risk_score": financial_risk,
            "potential_penalties": self._estimate_penalty_range(target_markets, budget_tier),
            "campaign_cost_exposure": budget_tier,
            "roi_impact_potential": self._assess_roi_impact(total_risk_score)
        }
        
        # Generate mitigation strategies
        risk_assessment["mitigation_strategies"] = self._generate_mitigation_strategies(
            total_risk_score, regulatory_risk, reputational_risk, sustainability_claims
        )
        
        # Final recommendations
        risk_assessment["recommendations"] = self._generate_final_recommendations(
            total_risk_score, marketing_channels, sustainability_claims, target_markets
        )
        
        return json.dumps(risk_assessment, indent=2)
    
    def _assess_regulatory_risk(self, claims: List[str], markets: List[str], channels: List[str]) -> float:
        """Assess regulatory compliance risk"""
        base_risk = 3.0
        
        # Risk factors
        if len(claims) > 5:
            base_risk += 1.5
        if any("100%" in claim or "zero" in claim for claim in claims):
            base_risk += 2.0
        if len(markets) > 3:
            base_risk += 1.0
        if "email_marketing" in channels:
            base_risk += 0.5  # Additional email regulations
        
        return min(base_risk, 10.0)
    
    def _assess_reputational_risk(self, claims: List[str], budget_tier: str) -> float:
        """Assess reputational risk"""
        base_risk = 2.0
        
        if len(claims) > 3:
            base_risk += 1.0
        if budget_tier == "large":
            base_risk += 1.5  # Higher visibility
        if any("eco" in claim.lower() or "green" in claim.lower() for claim in claims):
            base_risk += 1.0  # Common greenwashing terms
        
        return min(base_risk, 10.0)
    
    def _assess_operational_risk(self, channels: List[str], budget_tier: str) -> float:
        """Assess operational implementation risk"""
        base_risk = 2.0
        
        if len(channels) > 4:
            base_risk += 1.5  # Complexity
        if budget_tier == "small":
            base_risk += 1.0  # Resource constraints
        
        return min(base_risk, 10.0)
    
    def _assess_financial_risk(self, budget_tier: str, markets: List[str]) -> float:
        """Assess financial risk exposure"""
        base_risk = 1.0
        
        if budget_tier == "large":
            base_risk += 2.0
        if len(markets) > 2:
            base_risk += 1.0
        
        return min(base_risk, 10.0)
    
    def _get_regulatory_concerns(self, claims: List[str], markets: List[str]) -> List[str]:
        """Get specific regulatory concerns"""
        concerns = []
        if any("carbon neutral" in claim.lower() for claim in claims):
            concerns.append("Carbon neutrality claims require rigorous substantiation")
        if "US" in markets or "USA" in markets:
            concerns.append("FTC Green Guides compliance required")
        if "EU" in markets or "Europe" in markets:
            concerns.append("EU Green Claims Directive compliance required")
        return concerns
    
    def _get_compliance_requirements(self, markets: List[str]) -> List[str]:
        """Get compliance requirements by market"""
        requirements = []
        for market in markets:
            if market.upper() in ["US", "USA"]:
                requirements.append("FTC substantiation standards")
            elif market.upper() in ["EU", "EUROPE"]:
                requirements.append("Green Claims Directive requirements")
        return requirements
    
    def _assess_brand_impact(self, claims: List[str]) -> str:
        """Assess potential brand impact"""
        if len(claims) > 5:
            return "High potential for greenwashing accusations"
        elif len(claims) > 2:
            return "Moderate brand risk if claims unsubstantiated"
        else:
            return "Low brand risk with proper substantiation"
    
    def _assess_implementation_complexity(self, channels: List[str]) -> str:
        """Assess implementation complexity"""
        if len(channels) > 4:
            return "High complexity - multiple channel coordination required"
        elif len(channels) > 2:
            return "Medium complexity - coordinated approach needed"
        else:
            return "Low complexity - focused channel strategy"
    
    def _assess_resource_requirements(self, budget_tier: str, channels: List[str]) -> str:
        """Assess resource requirements"""
        if budget_tier == "large" and len(channels) > 3:
            return "High resource requirements - dedicated compliance team recommended"
        elif budget_tier == "medium":
            return "Medium resource requirements - part-time compliance focus needed"
        else:
            return "Low resource requirements - basic compliance processes sufficient"
    
    def _assess_timeline_risks(self, channels: List[str]) -> str:
        """Assess timeline-related risks"""
        if len(channels) > 4:
            return "High timeline risk - staggered launch recommended"
        else:
            return "Low timeline risk - coordinated launch feasible"
    
    def _estimate_penalty_range(self, markets: List[str], budget_tier: str) -> str:
        """Estimate potential penalty range"""
        if "US" in markets and budget_tier == "large":
            return "Potential FTC penalties: $10,000 - $1,000,000+"
        elif budget_tier == "medium":
            return "Potential penalties: $5,000 - $100,000"
        else:
            return "Potential penalties: $1,000 - $50,000"
    
    def _assess_roi_impact(self, risk_score: float) -> str:
        """Assess potential ROI impact"""
        if risk_score >= 7:
            return "High negative ROI potential if compliance issues arise"
        elif risk_score >= 4:
            return "Medium ROI impact - mitigation costs may affect returns"
        else:
            return "Low ROI impact - compliance costs manageable"
    
    def _generate_mitigation_strategies(self, total_risk: float, regulatory_risk: float, 
                                      reputational_risk: float, claims: List[str]) -> Dict[str, List[str]]:
        """Generate risk mitigation strategies"""
        strategies = {
            "immediate_actions": [],
            "short_term_strategies": [],
            "long_term_monitoring": []
        }
        
        if total_risk >= 7:
            strategies["immediate_actions"] = [
                "Conduct legal review before campaign launch",
                "Gather comprehensive substantiation evidence",
                "Consider reducing number of sustainability claims"
            ]
        
        if regulatory_risk >= 6:
            strategies["short_term_strategies"] = [
                "Establish compliance monitoring process",
                "Develop substantiation documentation library",
                "Implement pre-publication review workflow"
            ]
        
        strategies["long_term_monitoring"] = [
            "Regular compliance audits",
            "Competitor monitoring for industry standards",
            "Ongoing regulatory update tracking"
        ]
        
        return strategies
    
    def _generate_final_recommendations(self, total_risk: float, channels: List[str], 
                                      claims: List[str], markets: List[str]) -> List[str]:
        """Generate final recommendations based on assessment"""
        recommendations = []
        
        if total_risk >= 7:
            recommendations = [
                "High risk campaign - recommend postponing launch until compliance gaps addressed",
                "Engage legal counsel for comprehensive review",
                "Reduce scope of sustainability claims to lower risk"
            ]
        elif total_risk >= 4:
            recommendations = [
                "Medium risk campaign - proceed with enhanced compliance measures",
                "Implement robust substantiation process",
                "Consider phased rollout to test compliance approach"
            ]
        else:
            recommendations = [
                "Low risk campaign - proceed with standard compliance measures",
                "Maintain documentation for all claims",
                "Implement routine monitoring processes"
            ]
        
        # Add channel-specific recommendations
        if "email_marketing" in channels:
            recommendations.append("Ensure CAN-SPAM and GDPR compliance for email campaigns")
        
        if len(markets) > 2:
            recommendations.append("Develop market-specific compliance guidelines")
        
        return recommendations


# ----------------------
# TOOL FACTORY FUNCTIONS
# ----------------------

def create_marketing_tools() -> Dict[str, BaseTool]:
    """Create all marketing analysis tools"""
    return {
        "brand_awareness_compliance_scanner": BrandAwarenessComplianceScanner(),
        "email_marketing_claim_verifier": EmailMarketingClaimVerifier(),
        "content_marketing_analyzer": ContentMarketingAnalyzer(),
        "sustainability_claim_validator": SustainabilityClaimValidator(),
        "marketing_risk_assessment_tool": RiskAssessmentTool()
    }