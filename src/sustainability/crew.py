"""
crew.py — Sustainability Business Toolkit Orchestrator
Business-only workflow with full deliverables:
- quick_reference_tools
- market_intelligence
- communication_templates
- role_specific_guides

Uses Pydantic models for input/output validation.
"""

import logging
from pathlib import Path
import json

# Use absolute imports so the file works in both `python -m` and direct runs
from sustainability.config_loader import load_agents_config, load_tasks_config
from sustainability.agent_runner import AgentRunner
from sustainability.models import (
    CompanyProfile,
    OperationsData,
    JurisdictionInfo,
    BusinessAnalysisResult,
    ComplianceSummary,
    StrategyResult,
    FinalReport
)

logger = logging.getLogger(__name__)


class SustainabilityCrew:
    """
    Orchestrates all business-focused sustainability analysis tasks
    using the configured AI agents and tasks.
    """

    def __init__(self):
        self.agents_config = load_agents_config()
        self.tasks_config = load_tasks_config()
        self.runner = AgentRunner()
        logger.info("Loaded business-only configuration")

    def run_business_analysis(self, company_profile, industry_sector, operations_data, jurisdiction):
        """
        Full Sustainability Business Toolkit workflow.
        """
        logger.info("Starting full business sustainability analysis")

        # Validate inputs
        company = CompanyProfile(**company_profile)
        operations = OperationsData(**operations_data)
        jurisdiction_info = JurisdictionInfo(country=jurisdiction)

        # 1️⃣ Business Analysis
        ba_raw = self.runner.run_task(
            task_config=self.tasks_config['business_analysis_task'],
            agent_config=self.agents_config['business_toolkit_agent'],
            inputs={
                "company_profile": company.dict(),
                "industry_sector": industry_sector,
                "operations_data": operations.dict()
            }
        )
        business_analysis_result = BusinessAnalysisResult(**ba_raw)

        # Capture toolkit deliverables
        quick_tools = business_analysis_result.quick_reference_tools or []
        market_info = business_analysis_result.market_intelligence or []
        comm_templates = business_analysis_result.communication_templates or []
        role_guides = business_analysis_result.role_specific_guides or []

        # 2️⃣ Compliance Review
        cr_raw = self.runner.run_task(
            task_config=self.tasks_config['compliance_review_task'],
            agent_config=self.agents_config['compliance_analysis_agent'],
            inputs={
                "company_profile": company.dict(),
                "jurisdiction": jurisdiction_info.dict(),
                "operations_data": operations.dict()
            }
        )
        compliance_review_result = ComplianceSummary(**cr_raw)

        # 3️⃣ Strategy Development
        sd_raw = self.runner.run_task(
            task_config=self.tasks_config['strategy_development_task'],
            agent_config=self.agents_config['strategy_recommendation_agent'],
            inputs={
                "business_benchmark": business_analysis_result.business_benchmark.dict()
                if business_analysis_result.business_benchmark else None,
                "compliance_summary": compliance_review_result.dict(),
                "opportunity_list": [o.dict() for o in (business_analysis_result.opportunity_list or [])]
            }
        )
        strategy_result = StrategyResult(**sd_raw)

        # 4️⃣ Final Report Compilation (includes toolkit components)
        fr_raw = self.runner.run_task(
            task_config=self.tasks_config['report_compilation_task'],
            agent_config=self.agents_config['report_generator_agent'],
            inputs={
                "business_benchmark": business_analysis_result.business_benchmark.dict()
                if business_analysis_result.business_benchmark else None,
                "opportunity_list": [o.dict() for o in (business_analysis_result.opportunity_list or [])],
                "compliance_summary": compliance_review_result.dict(),
                "strategic_initiatives": [i.dict() for i in (strategy_result.strategic_initiatives or [])],
                "quick_reference_tools": [
                    qt.dict() if hasattr(qt, "dict") else qt for qt in quick_tools
                ],
                "market_intelligence": [
                    mi.dict() if hasattr(mi, "dict") else mi for mi in market_info
                ],
                "communication_templates": [
                    ct.dict() if hasattr(ct, "dict") else ct for ct in comm_templates
                ],
                "role_specific_guides": [
                    rg.dict() if hasattr(rg, "dict") else rg for rg in role_guides
                ]
            }
        )
        final_report = FinalReport(**fr_raw)

        logger.info("Business analysis completed successfully")
        return final_report.dict()


def run_full_analysis(company_profile_path, industry, operations_path, jurisdiction):
    """
    CLI/Test convenience function.
    """
    with open(company_profile_path, 'r', encoding='utf-8') as f:
        company_profile = json.load(f)
    with open(operations_path, 'r', encoding='utf-8') as f:
        operations_data = json.load(f)

    crew = SustainabilityCrew()
    return crew.run_business_analysis(company_profile, industry, operations_data, jurisdiction)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    example_company_profile = Path("examples/company_profile.json")
    example_operations = Path("examples/operations.json")
    jurisdiction = "US"
    industry_sector = "Manufacturing"

    if example_company_profile.exists() and example_operations.exists():
        report = run_full_analysis(
            example_company_profile,
            industry_sector,
            example_operations,
            jurisdiction
        )
        print(json.dumps(report, indent=2))
    else:
        logger.warning("Example files not found — skipping")
