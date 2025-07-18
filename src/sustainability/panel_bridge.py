#!/usr/bin/env python
"""
Complete Panel Bridge for Sustainability Training Application
"""

import panel as pn
import param
import asyncio
import threading
import traceback
import urllib.parse
from datetime import datetime
from typing import Optional, Dict, Any
import os
import json

# Minimal Panel configuration for web deployment
pn.extension()

class SustainabilityPanelApp(param.Parameterized):
    """
    Panel-based web interface for the Sustainability Training System
    """
    
    def __init__(self):
        super().__init__()
        
        # Web environment detection
        self.is_web_env = self.is_web_environment()
        
        # Configure Panel for deployment environment - removed deprecated config
        if self.is_web_env:
            pn.config.autoreload = False
        else:
            pn.config.autoreload = True
        
        # Initialize components
        self.setup_chat_interface()
        self.setup_controls()
        self.setup_layout()
        
        # Training state
        self.latest_results = None
        self.is_training_active = False
        self.current_thread = None
        
        # Register callback handler
        from .callbacks import get_panel_callback_handler
        self.callback_handler = get_panel_callback_handler()
        self.callback_handler.register_chat_interface(self.chat_interface)
    
    def is_web_environment(self):
        """Detect if running in web deployment vs local development"""
        return bool(os.environ.get('PORT'))
    
    def setup_chat_interface(self):
        """Initialize the chat interface"""
        self.chat_interface = pn.chat.ChatInterface(
            callback=self.chat_callback,
            callback_user="Assistant",
            height=500,
            sizing_mode="stretch_width",
            header="🌱 Sustainability Training AI Assistant",
            help_text="Your AI training session is in progress. Messages from the training agents will appear here.",
            placeholder_text="Training messages will appear here...",
            visible=False  # Hide initially
        )
        
        # Don't send welcome message initially
    
    def setup_controls(self):
        """Initialize control widgets"""
        # User inputs
        self.user_industry = pn.widgets.Select(
            name="🏢 Industry Focus",
            value="Marketing Agency",
            options=[
                "Marketing Agency", "Consumer Goods", "Fashion & Apparel", 
                "Food & Beverage", "Technology", "Finance", "Healthcare",
                "Energy", "Automotive", "Real Estate", "Other"
            ],
            sizing_mode="stretch_width"
        )
        
        self.regional_regulations = pn.widgets.Select(
            name="🌍 Regulatory Framework",
            value="EU (Green Claims Directive, CSRD)",
            options=[
                "EU (Green Claims Directive, CSRD)",
                "US (FTC Green Guides)",
                "UK (CMA Guidelines)", 
                "Canada (Competition Bureau)",
                "Australia (ACCC Guidelines)",
                "Global Best Practices"
            ],
            sizing_mode="stretch_width"
        )
        
        self.difficulty_level = pn.widgets.Select(
            name="📊 Difficulty Level",
            value="Intermediate",
            options=["Beginner", "Intermediate", "Advanced"],
            sizing_mode="stretch_width"
        )
        
        # Action buttons
        self.start_button = pn.widgets.Button(
            name="🚀 Start Training",
            button_type="primary",
            sizing_mode="stretch_width",
            margin=(20, 5)
        )
        
        self.download_md_button = pn.widgets.Button(
            name="📄 Download Report (MD)",
            button_type="default",
            sizing_mode="stretch_width",
            disabled=True
        )
        
        self.download_pdf_button = pn.widgets.Button(
            name="📑 PDF Instructions",
            button_type="default", 
            sizing_mode="stretch_width",
            disabled=True
        )
        
        self.reset_button = pn.widgets.Button(
            name="🔄 Reset Session",
            button_type="default",
            sizing_mode="stretch_width"
        )
        
        # Bind button events
        self.start_button.on_click(self.start_training)
        self.download_md_button.on_click(self.download_markdown_report)
        self.download_pdf_button.on_click(self.download_pdf_report) 
        self.reset_button.on_click(self.reset_session)
    
    def setup_layout(self):
        """Create the main application layout"""
        # Sidebar with controls
        self.sidebar = pn.Column(
            pn.pane.Markdown("## 🎯 Training Configuration"),
            self.user_industry,
            self.regional_regulations, 
            self.difficulty_level,
            pn.layout.Divider(),
            self.start_button,
            pn.layout.Divider(),
            pn.pane.Markdown("## 📥 Export Results"),
            self.download_md_button,
            self.download_pdf_button,
            pn.layout.Divider(),
            self.reset_button,
            pn.Spacer(),
            pn.pane.Markdown("""
            ---
            **🔧 Need Help?**
            
            This AI trainer creates personalized sustainability messaging courses using:
            - Real market research
            - Current regulations  
            - Industry best practices
            - Interactive scenarios
            
            **Training includes:**
            - Business scenarios
            - Problem identification
            - Compliant alternatives
            - Knowledge assessment
            """, sizing_mode="stretch_width"),
            width=350,
            sizing_mode="stretch_height"
        )
        
        # Main content area
        self.initial_instructions = pn.pane.Markdown("""
        # 🌱 AI-Powered Sustainability Training
        
        **Get personalized training on compliant sustainability messaging**
        
        Our AI agents will research current market trends and regulations to create 
        a customized training experience tailored to your industry and role.
        
        ## 🚀 How it works:
        
        1. **Configure** your training preferences on the left sidebar
        2. **Click "Start Training"** to begin your personalized session
        3. **Watch** as our AI agents work together to create your content:
           - 🏢 Business scenario creation
           - ⚠️ Problem identification  
           - ✅ Best practice solutions
           - 📝 Knowledge assessment
        4. **Download** your comprehensive training report
        
        ## 🎯 What you'll learn:
        
        - **Regulatory compliance** - Stay up-to-date with current laws
        - **Greenwashing avoidance** - Identify and fix problematic messaging
        - **Best practices** - Learn from successful sustainability communications
        - **Industry-specific guidance** - Tailored to your sector and role
        
        **Ready to begin?** Configure your preferences and click "Start Training"!
        """, sizing_mode="stretch_both")
        
        self.main_content = pn.Column(
            self.initial_instructions,
            self.chat_interface,
            sizing_mode="stretch_both"
        )
        
        # Complete layout
        self.layout = pn.Row(
            self.sidebar,
            self.main_content,
            sizing_mode="stretch_width",
            height=700
        )
    
    def chat_callback(self, contents: str, user: str, instance):
        """Handle chat messages from user"""
        # For now, just acknowledge user messages
        if contents.strip():
            response = "Thanks for your message! Use the training controls on the left to start your session."
            return response
        return None
    
    def start_training(self, event):
        """Start the sustainability training process"""
        if self.is_training_active:
            self.chat_interface.send("⚠️ Training is already in progress. Please wait for it to complete.", user="System", respond=False)
            return
        
        # Show chat interface and hide instructions
        self.initial_instructions.visible = False
        self.chat_interface.visible = True
        
        # Disable start button
        self.start_button.disabled = True
        self.start_button.name = "🔄 Training in Progress..."
        self.is_training_active = True
        
        # Prepare training inputs
        session_id = f"TRAIN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        training_inputs = {
            'user_industry': self.user_industry.value,
            'regional_regulations': self.regional_regulations.value,
            'difficulty_level': self.difficulty_level.value,
            'current_year': str(datetime.now().year),
            'session_id': session_id
        }
        
        # Send session start notification
        self.callback_handler.on_session_start({
            'session_id': session_id,
            'user_industry': self.user_industry.value,
            'regional_regulations': self.regional_regulations.value,
            'difficulty_level': self.difficulty_level.value
        })
        
        # Start training in background thread
        self.current_thread = threading.Thread(
            target=self.run_training_crew,
            args=(training_inputs,),
            daemon=True
        )
        self.current_thread.start()
    
    def run_training_crew(self, inputs: Dict[str, Any]):
        """Run the CrewAI training process in background"""
        try:
            from .crew import Sustainability
            
            # Create and run the crew
            sustainability_crew = Sustainability()
            result = sustainability_crew.crew().kickoff(inputs=inputs)
            
            # Store results
            self.latest_results = result
            
            # Schedule UI updates on main thread
            pn.io.add_periodic_callback(
                lambda: self.on_training_complete(result),
                period=100,
                count=1
            )
            
        except Exception as e:
            error_msg = f"Training failed: {str(e)}"
            print(f"❌ Training error: {error_msg}")
            print(f"Full traceback: {traceback.format_exc()}")
            
            # Schedule error handling on main thread
            pn.io.add_periodic_callback(
                lambda: self.on_training_error(error_msg),
                period=100,
                count=1
            )
    
    def on_training_complete(self, result):
        """Handle training completion"""
        try:
            # Reset button state
            self.start_button.disabled = False
            self.start_button.name = "🚀 Start Training"
            self.is_training_active = False
            
            # Enable download buttons
            self.download_md_button.disabled = False
            self.download_pdf_button.disabled = False
            
            # Send completion notification
            self.callback_handler.on_session_complete(result)
            
            # Show results summary
            self.show_results_summary(result)
            
        except Exception as e:
            print(f"Error in training completion: {e}")
            self.on_training_error(f"Error processing results: {str(e)}")
    
    def on_training_error(self, error_msg: str):
        """Handle training errors"""
        # Reset button state
        self.start_button.disabled = False
        self.start_button.name = "🚀 Start Training"
        self.is_training_active = False
        
        # Send error message
        self.chat_interface.send(f"❌ **Training Error**\n{error_msg}\n\nPlease try again or contact support if the issue persists.", user="System", respond=False)
    
    def show_results_summary(self, result):
        """Show a summary of training results"""
        try:
            if hasattr(result, 'tasks_output') and result.tasks_output:
                final_task = result.tasks_output[-1]
                if hasattr(final_task, 'pydantic') and final_task.pydantic:
                    data = final_task.pydantic.model_dump()
                    
                    # Extract key metrics
                    scenario = data.get('scenario', {})
                    problematic_analysis = data.get('problematic_analysis', {})
                    assessment_questions = data.get('assessment_questions', [])
                    
                    company_name = scenario.get('company_name', 'Example Company')
                    problem_count = len(problematic_analysis.get('problematic_messages', []))
                    question_count = len(assessment_questions)
                    
                    summary = f"""📊 **Training Results Summary**

**Scenario Created:** {company_name}
**Industry:** {scenario.get('industry', 'N/A')}
**Problems Identified:** {problem_count} messaging issues
**Assessment Questions:** {question_count} knowledge checks
**Training Duration:** Complete 4-module course

**Next Steps:**
1. ⬇️ Download your detailed report using the buttons on the left
2. 📚 Review the assessment questions and explanations
3. 🎯 Implement the compliance recommendations
4. 👥 Share insights with your team"""
                    
                    self.chat_interface.send(summary, user="Results", respond=False)
                    
        except Exception as e:
            print(f"Error showing results summary: {e}")
            self.chat_interface.send("✅ Training completed! Use the download buttons to access your results.", user="System", respond=False)
    
    def download_markdown_report(self, event):
        """Download the training report as markdown - Web optimized"""
        if not self.latest_results:
            self.chat_interface.send("No results available for download.", user="System", respond=False)
            return
        
        try:
            # Get the structured data
            if hasattr(self.latest_results, 'tasks_output') and self.latest_results.tasks_output:
                final_task = self.latest_results.tasks_output[-1]
                if hasattr(final_task, 'pydantic') and final_task.pydantic:
                    data = final_task.pydantic.model_dump()
                    markdown_content = self.format_results_as_markdown(data)
                    
                    # Create download filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"sustainability_training_report_{timestamp}.md"
                    
                    # Web-only download using JavaScript
                    encoded_content = urllib.parse.quote(markdown_content)
                    
                    download_html = f"""
                    <div style="margin: 20px 0; padding: 20px; border: 2px solid #28a745; border-radius: 10px; background-color: #f8f9fa; text-align: center;">
                        <h3 style="color: #28a745; margin-bottom: 15px;">📄 Training Report Ready!</h3>
                        <p style="margin-bottom: 20px;">Click the button below to download your comprehensive sustainability training report.</p>
                        <button onclick="downloadReport()" 
                                style="background-color: #28a745; color: white; padding: 15px 30px; 
                                       border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;
                                       box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: background-color 0.3s;">
                            📄 Download {filename}
                        </button>
                        <p style="margin-top: 15px; font-size: 14px; color: #666;">
                            File size: ~{len(markdown_content):,} characters | Format: Markdown (.md)
                        </p>
                    </div>
                    <script>
                    function downloadReport() {{
                        try {{
                            const content = decodeURIComponent(`{encoded_content}`);
                            const blob = new Blob([content], {{ type: 'text/markdown;charset=utf-8' }});
                            const url = window.URL.createObjectURL(blob);
                            const link = document.createElement('a');
                            link.href = url;
                            link.download = '{filename}';
                            link.style.display = 'none';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            window.URL.revokeObjectURL(url);
                            
                            alert('✅ Download started! Check your Downloads folder for {filename}');
                        }} catch (error) {{
                            console.error('Download error:', error);
                            alert('❌ Download failed. Please try again or contact support.');
                        }}
                    }}
                    </script>
                    """
                    
                    download_widget = pn.pane.HTML(download_html, sizing_mode="stretch_width")
                    
                    self.chat_interface.send("📄 **Training Report Generated Successfully!**", user="System", respond=False)
                    self.chat_interface.send(download_widget, user="Download", respond=False)
                    
        except Exception as e:
            self.chat_interface.send(f"Error preparing download: {str(e)}", user="System", respond=False)
    
    def download_pdf_report(self, event):
        """Download instructions for PDF conversion - Web optimized"""
        self.chat_interface.send(
            """📑 **PDF Conversion Instructions:**

**Step 1:** First download the Markdown report using the button above

**Step 2:** Convert to PDF using any of these methods:

🌐 **Online Conversion (Easiest):**
• Go to **pandoc.org/try**
• Upload your .md file  
• Select "PDF" as output format
• Download the converted PDF

💻 **Local Conversion:**
• Install Pandoc: `brew install pandoc` (Mac) or `apt install pandoc` (Linux)
• Run: `pandoc your_report.md -o report.pdf`

📝 **Alternative Tools:**
• **Typora** - Markdown editor with PDF export
• **Mark Text** - Free markdown editor  
• **VS Code** - With "Markdown PDF" extension

Your report contains professional formatting that will look great as a PDF! 🎯""", 
            user="PDF Help", 
            respond=False
        )
    
    def format_results_as_markdown(self, data: Dict[str, Any]) -> str:
        """Format training results as markdown report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract data sections
        scenario = data.get('scenario', {})
        problematic_analysis = data.get('problematic_analysis', {})
        best_practices = data.get('best_practices', {})
        assessment_questions = data.get('assessment_questions', [])
        personalized_feedback = data.get('personalized_feedback', {})
        key_takeaways = data.get('key_takeaways', [])
        
        markdown = f"""# Sustainability Training Report

**Generated:** {timestamp}
**Session ID:** {data.get('session_id', 'N/A')}
**Learner Profile:** {data.get('learner_profile', 'Marketing Professional')}

---

## 📋 Executive Summary

This comprehensive sustainability training session was designed to enhance understanding of compliant sustainability messaging and prevent greenwashing violations. The training covers industry-specific scenarios, regulatory compliance requirements, and practical application strategies.

## 🏢 Business Scenario

**Company:** {scenario.get('company_name', 'N/A')}
**Industry:** {scenario.get('industry', 'N/A')}
**Location:** {scenario.get('location', 'N/A')}
**Size:** {scenario.get('company_size', 'N/A')}

### Company Overview
**Product/Service:** {scenario.get('product_service', 'N/A')}
**Target Audience:** {scenario.get('target_audience', 'N/A')}

### Marketing Objectives
"""
        
        # Add marketing objectives
        for objective in scenario.get('marketing_objectives', []):
            markdown += f"- {objective}\n"
        
        markdown += f"""
### Sustainability Context
{scenario.get('sustainability_context', 'N/A')}

### Regulatory Framework
{scenario.get('regulatory_context', 'N/A')}

---

## ⚠️ Problematic Messaging Analysis

"""
        
        # Add problematic messages
        for i, msg in enumerate(problematic_analysis.get('problematic_messages', []), 1):
            markdown += f"""### Example {i}: {msg.get('id', f'Message {i}')}

**Problematic Message:**
> {msg.get('message', 'N/A')}

**Problems Identified:**
"""
            for problem in msg.get('problems_identified', []):
                markdown += f"- {problem}\n"
            
            markdown += f"""
**Regulatory Violations:**
"""
            for violation in msg.get('regulatory_violations', []):
                markdown += f"- {violation}\n"
            
            markdown += f"""
**Why This Is Problematic:**
{msg.get('why_problematic', 'N/A')}

**Potential Consequences:**
"""
            for consequence in msg.get('potential_consequences', []):
                markdown += f"- {consequence}\n"
            
            markdown += "\n---\n\n"
        
        markdown += """## ✅ Best Practice Corrections

"""
        
        # Add corrected messages
        for i, correction in enumerate(best_practices.get('corrected_messages', []), 1):
            markdown += f"""### Correction {i}

**Original Message ID:** {correction.get('original_message_id', 'N/A')}

**Improved Message:**
> {correction.get('corrected_message', 'N/A')}

**Changes Made:**
"""
            for change in correction.get('changes_made', []):
                markdown += f"- {change}\n"
            
            markdown += f"""
**Compliance Notes:**
{correction.get('compliance_notes', 'N/A')}

**Best Practices Applied:**
"""
            for practice in correction.get('best_practices_applied', []):
                markdown += f"- {practice}\n"
            
            markdown += "\n---\n\n"
        
        markdown += """## 📝 Knowledge Assessment

"""
        
        # Add assessment questions
        for i, question in enumerate(assessment_questions, 1):
            markdown += f"""### Question {i}

**Type:** {question.get('type', 'N/A')} | **Difficulty:** {question.get('difficulty_level', 'N/A')}

**Question:** {question.get('question', 'N/A')}

"""
            if question.get('options'):
                markdown += "**Options:**\n"
                for option in question.get('options', []):
                    markdown += f"- {option}\n"
                markdown += "\n"
            
            markdown += f"""**Correct Answer:** {question.get('correct_answer', 'N/A')}

**Explanation:** {question.get('explanation', 'N/A')}

**Learning Objective:** {question.get('learning_objective', 'N/A')}

---

"""
        
        markdown += """## 🎯 Personalized Feedback

### Role-Specific Tips
"""
        for tip in personalized_feedback.get('role_specific_tips', []):
            markdown += f"- {tip}\n"
        
        markdown += """
### Team Training Recommendations
"""
        for rec in personalized_feedback.get('team_training_recommendations', []):
            markdown += f"- {rec}\n"
        
        markdown += """
### Implementation Strategies
"""
        for strategy in personalized_feedback.get('implementation_strategies', []):
            markdown += f"- {strategy}\n"
        
        markdown += """
### Next Steps
"""
        for step in personalized_feedback.get('next_steps', []):
            markdown += f"- {step}\n"
        
        markdown += """
---

## 🎓 Key Takeaways

"""
        for takeaway in key_takeaways:
            markdown += f"- {takeaway}\n"
        
        markdown += """
---

## 📋 Compliance Checklist

"""
        for item in data.get('compliance_checklist', []):
            markdown += f"- [ ] {item}\n"
        
        markdown += f"""
---

*This report was generated by AI-powered sustainability training system on {timestamp}*
*For questions or support, please contact your training administrator*
"""
        
        return markdown
    
    def reset_session(self, event):
        """Reset the training session"""
        # Reset state
        self.latest_results = None
        self.is_training_active = False
        
        # Reset UI
        self.start_button.disabled = False
        self.start_button.name = "🚀 Start Training"
        self.download_md_button.disabled = True
        self.download_pdf_button.disabled = True
        
        # Show instructions and hide chat
        self.initial_instructions.visible = True
        self.chat_interface.visible = False
        
        # Clear chat
        self.chat_interface.clear()
    
    def servable(self):
        """Return the servable Panel application"""
        return self.layout


def create_sustainability_app():
    """Factory function to create the sustainability training app"""
    try:
        app = SustainabilityPanelApp()
        print("✅ Sustainability Panel App created successfully")
        return app
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        print(f"Full traceback: {traceback.format_exc()}")
        raise e


# For direct testing
if __name__ == "__main__":
    app = create_sustainability_app()
    app.layout.servable()
    
    # Local development server
    if not os.environ.get('PORT'):
        pn.serve(
            app.layout,
            port=5007,
            show=True,
            autoreload=True
        )