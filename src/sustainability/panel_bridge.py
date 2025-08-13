"""
panel_bridge.py — Interface layer between sustainability backend agents and frontend/UI.
Updated for Phase 1 & 2:
- Removed all references to educational or testing assessments
- Handles only business-focused sustainability analysis, compliance review, strategy, and report compilation
"""

import logging
from typing import Dict, Any

from .crew import SustainabilityCrew

logger = logging.getLogger(__name__)


class PanelBridge:
    """
    Acts as the communication bridge between the agent orchestration layer
    (SustainabilityCrew) and the UI / API layer.
    """

    def __init__(self):
        self.crew = SustainabilityCrew()

    def run_full_business_workflow(
        self,
        company_profile: Dict[str, Any],
        industry_sector: str,
        operations_data: Dict[str, Any],
        jurisdiction: str
    ) -> Dict[str, Any]:
        """
        Runs the complete business sustainability workflow.

        This replaces the old 'create_business_risk_assessment' call with
        a fully business-oriented 'create_business_risk_analysis'.
        """

        logger.info("Starting complete business sustainability workflow via PanelBridge...")

        report_data = self.crew.run_business_analysis(
            company_profile=company_profile,
            industry_sector=industry_sector,
            operations_data=operations_data,
            jurisdiction=jurisdiction
        )

        # Ensure we NEVER return any 'assessment' keys from this layer
        if "assessment" in report_data:
            logger.debug("Removing legacy assessment key from bridge output")
            report_data.pop("assessment", None)

        logger.info("Business sustainability workflow completed successfully.")
        return report_data

    def run_partial_analysis(
        self,
        company_profile: Dict[str, Any],
        industry_sector: str,
        operations_data: Dict[str, Any],
        jurisdiction: str,
        step: str
    ) -> Dict[str, Any]:
        """
        Runs only a specific step in the sustainability analysis process.
        Steps can be: 'business_analysis', 'compliance_review', 'strategy', 'report'
        """

        logger.info(f"Running partial business workflow step: {step}")

        step_outputs = {}

        if step == "business_analysis":
            step_outputs = self.crew.runner.run_task(
                task_config=self.crew.tasks_config['business_analysis_task'],
                agent_config=self.crew.agents_config['business_toolkit_agent'],
                inputs={
                    "company_profile": company_profile,
                    "industry_sector": industry_sector,
                    "operations_data": operations_data
                }
            )

        elif step == "compliance_review":
            step_outputs = self.crew.runner.run_task(
                task_config=self.crew.tasks_config['compliance_review_task'],
                agent_config=self.crew.agents_config['compliance_analysis_agent'],
                inputs={
                    "company_profile": company_profile,
                    "jurisdiction": {"country": jurisdiction},
                    "operations_data": operations_data
                }
            )

        elif step == "strategy":
            step_outputs = self.crew.runner.run_task(
                task_config=self.crew.tasks_config['strategy_development_task'],
                agent_config=self.crew.agents_config['strategy_recommendation_agent'],
                inputs={
                    # In reality you'd pass in prior step results here
                    "business_benchmark": None,
                    "compliance_summary": None,
                    "opportunity_list": None
                }
            )

        elif step == "report":
            step_outputs = self.crew.runner.run_task(
                task_config=self.crew.tasks_config['report_compilation_task'],
                agent_config=self.crew.agents_config['report_generator_agent'],
                inputs={
                    # In reality you'd gather all prior step outputs here
                    "business_benchmark": None,
                    "opportunity_list": None,
                    "compliance_summary": None,
                    "strategic_initiatives": None
                }
            )

        else:
            logger.warning(f"Unknown workflow step requested: {step}")

        # Remove any leftover assessment keys (safety net)
        if isinstance(step_outputs, dict) and "assessment" in step_outputs:
            logger.debug("Removing legacy assessment key from partial step output")
            step_outputs.pop("assessment", None)

        logger.info(f"Workflow step '{step}' completed.")
        return step_outputs
