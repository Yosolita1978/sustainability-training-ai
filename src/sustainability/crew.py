from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from .tools.custom_serper import CustomSerperTool
from pydantic import BaseModel, Field
from typing import List
import os
from datetime import datetime

# Add Panel callback imports
from .callbacks import print_task_output, get_panel_callback_handler

# ===== CORE TRAINING MODELS ===== #

class SustainabilityScenario(BaseModel):
    """A realistic business scenario for sustainability messaging training"""
    company_name: str = Field(description="Company name")
    industry: str = Field(description="Industry sector")
    company_size: str = Field(description="Company size (startup, SME, large corporation)")
    location: str = Field(description="Company location/market")
    product_service: str = Field(description="Main product or service offered")
    target_audience: str = Field(description="Primary target audience for marketing")
    marketing_objectives: List[str] = Field(description="Key marketing objectives")
    sustainability_context: str = Field(description="Current sustainability challenges and context")
    preliminary_claims: List[str] = Field(description="Initial sustainability claims the company wants to make")
    regulatory_context: str = Field(description="Relevant regulatory requirements (EU directives, etc.)")
    market_research_sources: List[str] = Field(description="Sources used to create this scenario")

class ProblematicMessage(BaseModel):
    """A problematic sustainability message with detailed analysis"""
    id: str = Field(description="Unique identifier for this message")
    message: str = Field(description="The problematic sustainability message")
    problems_identified: List[str] = Field(description="Specific problems with this message")
    regulatory_violations: List[str] = Field(description="Specific regulations this violates")
    greenwashing_patterns: List[str] = Field(description="Greenwashing patterns demonstrated")
    real_world_examples: List[str] = Field(description="Real companies/cases that made similar mistakes")
    why_problematic: str = Field(description="Detailed explanation of why this message is problematic")
    potential_consequences: List[str] = Field(description="Potential legal/reputational consequences")

class ProblematicMessageAnalysis(BaseModel):
    """Complete analysis of problematic sustainability messages"""
    scenario_reference: str = Field(description="Reference to the business scenario")
    problematic_messages: List[ProblematicMessage] = Field(description="List of problematic messages with analysis")
    general_patterns_found: List[str] = Field(description="Common greenwashing patterns identified")
    regulatory_landscape: str = Field(description="Current regulatory landscape overview")
    research_sources: List[str] = Field(description="Sources used for real-world examples")

class CorrectedMessage(BaseModel):
    """A corrected sustainability message with best practices"""
    original_message_id: str = Field(description="Reference to the original problematic message")
    corrected_message: str = Field(description="The improved, compliant message")
    changes_made: List[str] = Field(description="Specific changes made to fix the problems")
    compliance_notes: str = Field(description="How this message ensures regulatory compliance")
    best_practices_applied: List[str] = Field(description="Best practices applied in the correction")
    real_world_examples: List[str] = Field(description="Companies that use similar effective messaging")
    effectiveness_rationale: str = Field(description="Why this corrected message is effective")

class BestPracticeGuidance(BaseModel):
    """Complete best practice guidance for sustainability messaging"""
    scenario_reference: str = Field(description="Reference to the business scenario")
    corrected_messages: List[CorrectedMessage] = Field(description="List of corrected messages")
    general_guidelines: List[str] = Field(description="General guidelines for compliant messaging")
    key_principles: List[str] = Field(description="Key principles for effective sustainability communication")
    regulatory_compliance_tips: List[str] = Field(description="Tips for ensuring regulatory compliance")
    industry_specific_advice: str = Field(description="Advice specific to the industry in the scenario")
    research_sources: List[str] = Field(description="Sources for best practices and examples")

class SourceReference(BaseModel):
    """A source reference used in the training"""
    title: str = Field(description="Title of the source")
    url: str = Field(description="URL of the source")
    type: str = Field(description="Type of source (web_search, news, knowledge_panel, regulatory)")
    description: str = Field(description="Brief description of the source content")
    access_date: str = Field(description="Date when the source was accessed")
    used_by_agent: str = Field(description="Which agent used this source")
    query: str = Field(description="Search query that found this source")

# ===== BUSINESS TOOLKIT MODELS ===== #

class QuickReferenceItem(BaseModel):
    """Quick reference tool for marketing teams"""
    id: str = Field(description="Unique identifier for reference item")
    title: str = Field(description="Tool title")
    category: str = Field(description="red_flags/safe_alternatives/approval_checklist/risk_assessment")
    description: str = Field(description="Brief description of the tool")
    content: List[str] = Field(description="Tool content items")
    display_format: str = Field(description="checklist/comparison_table/flowchart/guide")
    priority: str = Field(description="high/medium/low priority level")
    last_updated: str = Field(description="Last update date")
    usage_context: str = Field(description="When and how to use this tool")

class TrendingIntelligence(BaseModel):
    """Market intelligence about sustainability trends"""
    trend_id: str = Field(description="Unique trend identifier")
    trend_name: str = Field(description="Name of the trend")
    trend_type: str = Field(description="rising_claims/declining_claims/regulatory_changes")
    description: str = Field(description="Detailed trend description")
    industry_impact: str = Field(description="Impact on the specific industry")
    industry_specific: bool = Field(description="Whether trend is industry-specific")
    examples: List[str] = Field(description="Real market examples")
    implications: List[str] = Field(description="Business implications")
    recommended_actions: List[str] = Field(description="Recommended actions for marketing teams")
    source_references: List[str] = Field(description="Sources for this intelligence")

class CommunicationTemplate(BaseModel):
    """Communication template for business processes"""
    template_id: str = Field(description="Unique template identifier")
    template_name: str = Field(description="Template name")
    template_type: str = Field(description="email_legal_review/vendor_brief/internal_approval/crisis_response")
    recipient_role: str = Field(description="legal_team/agency_partner/c_suite/media")
    urgency_level: str = Field(description="routine/urgent/crisis")
    subject_line: str = Field(description="Email subject line or document title")
    template_content: str = Field(description="Full template content with placeholders")
    usage_instructions: List[str] = Field(description="How to use this template")
    customization_notes: List[str] = Field(description="What to customize for each use")
    approval_required: bool = Field(description="Whether approval is required before use")

class RoleSpecificGuide(BaseModel):
    """Role-specific guidance for different team members"""
    guide_id: str = Field(description="Unique guide identifier")
    role: str = Field(description="content_creator/campaign_manager/brand_manager")
    role_title: str = Field(description="Human-readable role title")
    responsibilities: List[str] = Field(description="Key responsibilities for this role")
    daily_checklist: List[str] = Field(description="Daily compliance checklist")
    escalation_triggers: List[str] = Field(description="When to escalate issues")
    tools_and_resources: List[str] = Field(description="Tools and resources for this role")
    common_mistakes: List[str] = Field(description="Common mistakes to avoid")
    best_practices: List[str] = Field(description="Role-specific best practices")
    success_metrics: List[str] = Field(description="How success is measured in this role")

class PersonalizedFeedback(BaseModel):
    """Personalized feedback for the learner"""
    role_specific_tips: List[str] = Field(description="Tips specific to role")
    team_training_recommendations: List[str] = Field(description="Recommendations for training the team")
    implementation_strategies: List[str] = Field(description="Strategies for implementing learnings")
    next_steps: List[str] = Field(description="Recommended next steps for continued learning")
    additional_resources: List[str] = Field(description="Additional resources for further learning")

# ===== COMPREHENSIVE TRAINING REPORT (TOOLKIT ONLY) ===== #

class ComprehensiveTrainingReport(BaseModel):
    """Complete sustainability training toolkit - No assessments/tests"""
    session_id: str = Field(description="Training session identifier")
    timestamp: str = Field(description="Session timestamp")
    learner_profile: str = Field(description="Learner profile summary")
    
    # Core Training Components
    scenario: SustainabilityScenario = Field(description="Business scenario used in training")
    problematic_analysis: ProblematicMessageAnalysis = Field(description="Analysis of problematic messages")
    best_practices: BestPracticeGuidance = Field(description="Best practice guidance and corrections")
    
    # Business Toolkit Components
    quick_reference_tools: List[QuickReferenceItem] = Field(description="Quick reference tools for daily use")
    market_intelligence: List[TrendingIntelligence] = Field(description="Current market intelligence")
    communication_templates: List[CommunicationTemplate] = Field(description="Business communication templates")
    role_specific_guides: List[RoleSpecificGuide] = Field(description="Role-specific guidance")
    
    # Additional Components (NO TESTS/ASSESSMENTS)
    personalized_feedback: PersonalizedFeedback = Field(description="Personalized feedback and recommendations")
    key_takeaways: List[str] = Field(description="Key takeaways from the training session")
    compliance_checklist: List[str] = Field(description="Checklist for ensuring message compliance")
    sources_used: List[SourceReference] = Field(
        default_factory=list,
        description="All sources referenced during the training session"
    )

@CrewBase
class Sustainability():
    """Sustainability Messaging Training Crew - Toolkit Focus"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self) -> None:
        self.user_preferences = self._load_user_preferences()
        self._ensure_output_directory()
        self.search_tool = CustomSerperTool()
        
    def _load_user_preferences(self):
        """Load user preferences from knowledge folder"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            preferences_path = os.path.join(project_root, 'knowledge', 'user_preference.txt')
            
            possible_paths = [
                preferences_path,
                os.path.join(current_dir, '..', '..', 'knowledge', 'user_preference.txt'),
                'knowledge/user_preference.txt'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as file:
                        return file.read()
            
            print("⚠️ Warning: user_preference.txt not found, using defaults")
            return self._get_default_preferences()
            
        except Exception as e:
            print(f"⚠️ Warning: Error loading user preferences: {e}")
            return self._get_default_preferences()
    
    def _get_default_preferences(self):
        """Return default user preferences"""
        return """USER_PROFILE:
Name: Marketing Professional
Role: Marketing Director
Company_Type: Marketing/Communications Agency
Location: Global
Industry_Focus: Multi-client agency serving various industries

SUSTAINABILITY_TRAINING_PREFERENCES:
Experience_Level: Intermediate
Primary_Interest: Building team capability in sustainability communications
Company_Size: Small to medium agency
Target_Audience_for_Messages: Diverse client base across industries
Training_Goal: Capacitate team members on sustainability messaging compliance"""
    
    def _ensure_output_directory(self):
        """Create outputs directory if it doesn't exist"""
        try:
            if not os.path.exists('outputs'):
                os.makedirs('outputs')
        except Exception as e:
            print(f"⚠️ Warning: Could not create outputs directory: {e}")
    
    @agent
    def scenario_builder(self) -> Agent:
        return Agent(
            config=self.agents_config['scenario_builder'],
            tools=[self.search_tool],
            verbose=True
        )
    
    @agent
    def mistake_illustrator(self) -> Agent:
        return Agent(
            config=self.agents_config['mistake_illustrator'],
            tools=[self.search_tool],
            verbose=True
        )
    
    @agent
    def best_practice_coach(self) -> Agent:
        return Agent(
            config=self.agents_config['best_practice_coach'],
            tools=[self.search_tool],
            verbose=True
        )
    
    @agent
    def assessment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['assessment_agent'],
            tools=[self.search_tool],
            verbose=True
        )
    
    @task
    def scenario_creation_task(self) -> Task:
        task_config = self.tasks_config['scenario_creation_task'].copy()
        task_config['description'] = f"""
        {task_config['description']}
        
        User Preferences Context:
        {self.user_preferences}
        """
        
        return Task(
            config=task_config,
            agent=self.scenario_builder(),
            output_pydantic=SustainabilityScenario,
            callback=print_task_output
        )
    
    @task
    def mistake_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['mistake_generation_task'],
            agent=self.mistake_illustrator(),
            output_pydantic=ProblematicMessageAnalysis,
            callback=print_task_output
        )
    
    @task
    def best_practice_transformation_task(self) -> Task:
        return Task(
            config=self.tasks_config['best_practice_transformation_task'],
            agent=self.best_practice_coach(),
            output_pydantic=BestPracticeGuidance,
            callback=print_task_output
        )
    
    @task
    def assessment_and_feedback_task(self) -> Task:
        """Generate business toolkit (no assessments/tests)"""
        output_file = None
        try:
            if os.path.exists('outputs') or os.makedirs('outputs', exist_ok=True):
                output_file = 'outputs/sustainability_toolkit.json'
        except:
            pass
        
        return Task(
            config=self.tasks_config['assessment_and_feedback_task'],
            agent=self.assessment_agent(),
            output_pydantic=ComprehensiveTrainingReport,
            output_file=output_file,
            callback=print_task_output
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Sustainability Training crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
            output_log_file=None
        )