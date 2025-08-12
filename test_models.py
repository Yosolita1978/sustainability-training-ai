#!/usr/bin/env python
"""
Test script to validate new data models work correctly
"""
import sys
import os
sys.path.append('src')

def test_new_models():
    """Test that new models can be created"""
    try:
        from sustainability.crew import (
            QuickReferenceItem, 
            TrendingIntelligence, 
            TrendItem,
            CommunicationTemplate, 
            RoleSpecificGuide,
            WorkflowStep,
            ComprehensiveTrainingReport
        )
        
        # Test QuickReferenceItem
        ref_item = QuickReferenceItem(
        category="red_flags",
        title="Test Reference",
        display_format="checklist",
        content=["Item 1", "Item 2"],
        priority="high",
        industry_specific=True,
    )
        print("✅ QuickReferenceItem created successfully")
        
        # Test TrendItem
        trend_item = TrendItem(
            name="Test Trend",
            status="rising",
            description="Test description",
            example="Test example",
            risk_level="medium",
            recommendation="Test recommendation"
        )
        print("✅ TrendItem created successfully")
        
        # Test TrendingIntelligence
        trending = TrendingIntelligence(
            trend_type="rising_claims",
            industry_specific=False,
            items=[trend_item],
            last_updated="2025-01-01",
            confidence_level="high",
            geographic_scope="global"
        )
        print("✅ TrendingIntelligence created successfully")
        
        # Test CommunicationTemplate
        template = CommunicationTemplate(
            template_type="email_legal_review",
            recipient_role="legal_team",
            subject_line="Test Subject",
            body_template="Test body with [placeholder]",
            required_attachments=["doc1.pdf"],
            urgency_level="routine",
            customization_notes="Test notes"
        )
        print("✅ CommunicationTemplate created successfully")
        
        # Test WorkflowStep
        workflow_step = WorkflowStep(
            step_name="Legal Review",
            when_required="All external communications",
            estimated_time="2-3 days",
            required_information=["Evidence", "Claims"],
            responsible_role="Legal Team"
        )
        print("✅ WorkflowStep created successfully")
        
        # Test RoleSpecificGuide
        role_guide = RoleSpecificGuide(
            role="content_creator",
            daily_checklist=["Check 1", "Check 2"],
            approval_workflow=[workflow_step],
            common_mistakes=["Mistake 1"],
            escalation_triggers=["Trigger 1"],
            success_metrics=["Metric 1"],
            tools_and_resources=["Tool 1"]
        )
        print("✅ RoleSpecificGuide created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing new models: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_legacy_compatibility():
    """Test that legacy models still work"""
    try:
        from sustainability.crew import AssessmentQuestion, ComprehensiveTrainingReport
        
        # Test legacy AssessmentQuestion
        question = AssessmentQuestion(
            id="test_1",
            type="multiple_choice",
            question="Test question?",
            options=["A", "B", "C"],
            correct_answer="A",
            explanation="Test explanation",
            difficulty_level="intermediate",
            learning_objective="Test objective"
        )
        print("✅ Legacy AssessmentQuestion created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing legacy models: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_crew_initialization():
    """Test that the Sustainability crew can still be initialized"""
    try:
        from sustainability.crew import Sustainability
        
        # Just test that we can create the class (don't run it)
        crew_instance = Sustainability()
        print("✅ Sustainability crew class initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing Sustainability crew: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("🧪 Testing New Data Models")
    print("=" * 50)
    
    success = True
    
    print("\n1. Testing new model creation...")
    if not test_new_models():
        success = False
    
    print("\n2. Testing legacy compatibility...")
    if not test_legacy_compatibility():
        success = False
        
    print("\n3. Testing crew initialization...")
    if not test_crew_initialization():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Your models are working correctly.")
        print("Ready to proceed to Phase 2: Update tasks.yaml")
    else:
        print("❌ SOME TESTS FAILED! Check the errors above.")