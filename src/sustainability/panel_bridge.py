#!/usr/bin/env python
"""
Panel Bridge for Sustainability Training Application
"""

import panel as pn
import asyncio
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Configure Panel
pn.extension()

def is_web_environment():
    """Detect if running in web deployment vs local development"""
    return bool(os.environ.get('PORT'))

class SustainabilityPanelApp:
    """Panel application wrapper for Sustainability Training"""
    
    def __init__(self):
        self.setup_components()
        self.latest_results = None
        self.training_in_progress = False
        
    def setup_components(self):
        """Setup Panel components"""
        
        # Header
        self.header = pn.pane.Markdown("""
        # 🌱 Sustainability Training AI
        
        **AI-Powered Training for Compliant Sustainability Communications**
        
        Get personalized training scenarios, identify greenwashing risks, and learn best practices 
        for creating compliant sustainability messages that meet current EU regulations.
        """, sizing_mode="stretch_width")
        
        # Chat interface for real-time feedback
        self.chat_interface = pn.chat.ChatInterface(
            callback=self.handle_chat_message,
            height=400,
            sizing_mode="stretch_width",
            placeholder_text="Ask questions about sustainability messaging or start a training session..."
        )
        
        # Industry selection
        self.industry_select = pn.widgets.Select(
            name="Industry Focus",
            value="Marketing Agency",
            options=[
                "Marketing Agency", 
                "Fashion & Retail", 
                "Food & Beverage", 
                "Technology", 
                "Financial Services",
                "Real Estate",
                "Manufacturing",
                "Other"
            ],
            sizing_mode="stretch_width"
        )
        
        # Difficulty level
        self.difficulty_select = pn.widgets.Select(
            name="Training Level",
            value="Intermediate",
            options=["Beginner", "Intermediate", "Advanced"],
            sizing_mode="stretch_width"
        )
        
        # Start training button
        self.start_button = pn.widgets.Button(
            name="🚀 Start Training Session",
            button_type="primary",
            sizing_mode="stretch_width",
            height=50
        )
        self.start_button.on_click(self.start_training)
        
        # Download buttons (initially disabled) - FIXED: using valid button types
        self.download_md_button = pn.widgets.Button(
            name="📄 Download Report (Markdown)",
            button_type="default",  # FIXED: changed from "outline" to "default"
            sizing_mode="stretch_width",
            disabled=True
        )
        self.download_md_button.on_click(self.download_markdown_report)
        
        self.download_pdf_button = pn.widgets.Button(
            name="📑 PDF Instructions",
            button_type="default",  # FIXED: changed from "outline" to "default" 
            sizing_mode="stretch_width",
            disabled=True
        )
        self.download_pdf_button.on_click(self.download_pdf_report)
        
        # Status indicator
        self.status_indicator = pn.pane.Markdown(
            "**Status:** Ready to start training 🟢",
            sizing_mode="stretch_width"
        )
        
        # Progress indicator
        self.progress_bar = pn.indicators.Progress(
            name="Training Progress",
            value=0,
            max=100,
            sizing_mode="stretch_width",
            visible=False
        )
    
    def handle_chat_message(self, contents: str, user: str, instance):
        """Handle chat messages from user"""
        if not self.training_in_progress:
            # Provide helpful responses when not training
            if "start" in contents.lower() or "training" in contents.lower():
                return "Click the '🚀 Start Training Session' button to begin your personalized sustainability training!"
            elif "help" in contents.lower():
                return """**Available Actions:**
                
🚀 **Start Training** - Click the button to begin
🏢 **Select Industry** - Choose your industry focus
📊 **Set Level** - Pick your difficulty level
❓ **Ask Questions** - I can help with sustainability messaging topics

**What you'll get:**
- Realistic business scenarios
- Problematic messaging examples  
- Best practice corrections
- Comprehensive assessment
- Downloadable reports"""
            else:
                return "I'm here to help with sustainability training! Click 'Start Training Session' to begin, or ask me about sustainability messaging best practices."
        else:
            return "Training session in progress... Please wait for completion before asking questions."
    
    def start_training(self, event):
        """Start the training session"""
        if self.training_in_progress:
            self.chat_interface.send("⚠️ Training already in progress. Please wait for completion.", user="System", respond=False)
            return
        
        # Set up training session
        self.training_in_progress = True
        self.progress_bar.visible = True
        self.progress_bar.value = 0
        self.start_button.disabled = True
        self.start_button.name = "🔄 Training in Progress..."
        self.status_indicator.object = "**Status:** Training session starting... 🟡"
        
        # Send welcome message
        session_info = {
            'session_id': f"TRAIN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'user_industry': self.industry_select.value,
            'regional_regulations': 'EU Green Claims Directive, CSRD',
            'difficulty_level': self.difficulty_select.value
        }
        
        self.chat_interface.send(f"""🌱 **Sustainability Training Session Started**

**Session ID:** {session_info['session_id']}
**Industry Focus:** {session_info['user_industry']}
**Regulatory Framework:** {session_info['regional_regulations']}
**Difficulty Level:** {session_info['difficulty_level']}

**Training Plan:**
1. 🏢 Create realistic business scenario
2. ⚠️ Identify problematic messaging patterns  
3. ✅ Develop compliant alternatives
4. 📝 Generate assessment and feedback

Please wait while our AI agents work together to create your personalized training content...""", user="System", respond=False)
        
        # Start the actual training asynchronously
        asyncio.create_task(self.run_training_async(session_info))
    
    async def run_training_async(self, session_info: Dict[str, Any]):
        """Run the training session asynchronously"""
        try:
            # Import crew
            from .crew import Sustainability
            
            # Update progress
            self.progress_bar.value = 10
            self.status_indicator.object = "**Status:** Initializing AI agents... 🟡"
            
            # Create and run crew
            crew = Sustainability().crew()
            
            inputs = {
                'user_industry': session_info['user_industry'],
                'regional_regulations': session_info['regional_regulations'],
                'current_year': str(datetime.now().year),
                'session_id': session_info['session_id']
            }
            
            self.progress_bar.value = 25
            self.status_indicator.object = "**Status:** AI agents working together... 🟡"
            
            self.chat_interface.send("🤖 **AI Agents Starting Work:**", user="System", respond=False)
            self.chat_interface.send("📋 Scenario Builder is researching your industry...", user="Agent 1", respond=False)
            
            # Run the training
            result = crew.kickoff(inputs=inputs)
            
            self.progress_bar.value = 100
            self.status_indicator.object = "**Status:** Training completed successfully! 🟢"
            
            # Store results
            self.latest_results = result
            
            # Enable download buttons
            self.download_md_button.disabled = False
            self.download_pdf_button.disabled = False
            
            # Send completion message
            self.chat_interface.send(f"""🎉 **Training Session Completed Successfully!**

📊 **Session Summary:**
- ✅ All 4 training modules completed
- 📋 Comprehensive report generated
- 🎯 Personalized feedback provided
- 📚 Assessment questions created

**Next Steps:**
1. Review the detailed training results
2. Use the download buttons to save your results
3. Share insights with your team
4. Implement the compliance recommendations

Thank you for using our AI-powered sustainability training system! 🌱""", user="System", respond=False)
            
        except Exception as e:
            self.progress_bar.value = 0
            self.status_indicator.object = f"**Status:** Training failed ❌"
            self.chat_interface.send(f"❌ **Training Error:** {str(e)}\n\nPlease check your API keys and try again.", user="System", respond=False)
            
        finally:
            # Reset UI state
            self.training_in_progress = False
            self.start_button.disabled = False
            self.start_button.name = "🚀 Start Training Session"
            self.progress_bar.visible = False
    
    def download_markdown_report(self, event):
        """Download the training report as markdown"""
        if not self.latest_results:
            self.chat_interface.send("No results available for download.", user="System", respond=False)
            return
        
        self.chat_interface.send("📄 **Report Download Feature**\n\nIn a full deployment, this would generate and download a comprehensive training report. For now, check the outputs/ directory for generated files.", user="System", respond=False)
    
    def download_pdf_report(self, event):
        """Download instructions for PDF conversion"""
        self.chat_interface.send(
            """📑 **PDF Conversion Instructions:**

**Step 1:** Files are saved in the outputs/ directory

**Step 2:** Convert to PDF using:
• **Pandoc**: `pandoc report.md -o report.pdf`
• **Online tools**: pandoc.org/try
• **VS Code**: Markdown PDF extension

Your report will contain professional formatting! 🎯""", 
            user="PDF Help", 
            respond=False
        )
    
    @property
    def layout(self):
        """Create the main layout"""
        
        # Sidebar with controls
        sidebar = pn.Column(
            "## ⚙️ Training Setup",
            self.industry_select,
            self.difficulty_select,
            "---",
            self.start_button,
            "---", 
            "## 📄 Downloads",
            self.download_md_button,
            self.download_pdf_button,
            "---",
            self.status_indicator,
            self.progress_bar,
            width=350,
            height=800,
            scroll=True
        )
        
        # Main content area
        main_content = pn.Column(
            self.header,
            self.chat_interface,
            sizing_mode="stretch_both"
        )
        
        # Complete layout
        layout = pn.Row(
            sidebar,
            main_content,
            sizing_mode="stretch_width",
            height=800
        )
        
        return layout

def create_sustainability_app():
    """Factory function to create the sustainability app"""
    return SustainabilityPanelApp()