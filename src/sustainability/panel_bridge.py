#!/usr/bin/env python
"""
Sustainability Training Panel Web Application - Enhanced with Modern CSS
"""

import panel as pn
import param
import asyncio
import threading
import traceback
import base64
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os

# Minimal Panel configuration for web deployment
pn.extension()

# Modern CSS Styling
MODERN_CSS = """
<style>
/* ===== DESIGN SYSTEM VARIABLES ===== */
:root {
  /* Colors - Modern Green Tech Theme */
  --primary-color: #10b981;
  --primary-dark: #059669;
  --primary-light: #34d399;
  --secondary-color: #3b82f6;
  --accent-color: #8b5cf6;
  
  /* Neutrals */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #e2e8f0;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --border-color: #e2e8f0;
  --border-hover: #cbd5e1;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  
  /* Border Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  
  /* Typography */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Courier New', monospace;
}

/* ===== GLOBAL RESET & BASE STYLES ===== */
* {
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  color: var(--text-primary);
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

/* ===== MAIN LAYOUT CONTAINER ===== */
.bk-root {
  background: transparent !important;
}

/* Panel Row - Main Layout */
.bk-Row {
  background: transparent;
  gap: var(--space-lg);
  padding: var(--space-lg);
  min-height: 100vh;
}

/* ===== SIDEBAR STYLING ===== */
.bk-Column:first-child {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--space-xl);
  border: 1px solid var(--border-color);
  position: sticky;
  top: var(--space-lg);
  max-height: calc(100vh - 2rem);
  overflow-y: auto;
}

/* Sidebar Headers */
.bk-Column:first-child .bk-Markdown h2 {
  color: var(--primary-color);
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 var(--space-lg) 0;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.bk-Column:first-child .bk-Markdown h2:before {
  content: "⚙️";
  font-size: 1.1em;
}

/* ===== MAIN CONTENT AREA ===== */
.bk-Column:last-child {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  overflow: hidden;
  flex: 1;
  min-height: 600px;
}

/* ===== FORM CONTROLS STYLING ===== */
/* Select Widgets */
.bk-input-group {
  margin-bottom: var(--space-lg);
}

.bk-input-group label {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
  display: block;
  font-size: 0.95rem;
}

select.bk-input {
  width: 100%;
  padding: var(--space-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-position: right var(--space-md) center;
  background-repeat: no-repeat;
  background-size: 1em;
  padding-right: 2.5rem;
}

select.bk-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgb(16 185 129 / 0.1);
}

select.bk-input:hover {
  border-color: var(--border-hover);
}

/* ===== BUTTON STYLING ===== */
.bk-btn {
  font-weight: 600;
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  font-size: 0.95rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

/* Primary Button (Start Training) */
.bk-btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  box-shadow: var(--shadow-md);
  font-size: 1.1rem;
  padding: var(--space-lg) var(--space-xl);
  font-weight: 700;
}

.bk-btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  background: linear-gradient(135deg, var(--primary-dark), #047857);
}

.bk-btn-primary:active {
  transform: translateY(0);
}

.bk-btn-primary:disabled {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
  cursor: not-allowed;
  transform: none;
  opacity: 0.7;
}

/* Default Buttons */
.bk-btn-default {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.bk-btn-default:hover:not(:disabled) {
  background: var(--bg-tertiary);
  border-color: var(--border-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.bk-btn-default:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Button Loading State */
.bk-btn-primary:disabled:after {
  content: "";
  position: absolute;
  width: 16px;
  height: 16px;
  margin: auto;
  border: 2px solid transparent;
  border-top-color: white;
  border-radius: 50%;
  animation: button-loading-spinner 1s ease infinite;
  left: var(--space-lg);
}

@keyframes button-loading-spinner {
  from { transform: rotate(0turn); }
  to { transform: rotate(1turn); }
}

/* ===== DIVIDER STYLING ===== */
.bk-Divider {
  border-color: var(--border-color);
  margin: var(--space-xl) 0;
  opacity: 0.6;
}

/* ===== CHAT INTERFACE STYLING ===== */
.chat-interface {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Chat Header */
.bk-ChatInterface .bk-header {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
  color: white;
  padding: var(--space-lg);
  font-weight: 700;
  font-size: 1.1rem;
  border-bottom: none;
}

/* Chat Messages Area */
.bk-ChatInterface .bk-chat-feed {
  background: var(--bg-secondary);
  padding: var(--space-lg);
  flex: 1;
  overflow-y: auto;
}

/* Individual Chat Messages */
.bk-ChatMessage {
  margin-bottom: var(--space-lg);
  animation: message-slide-in 0.3s ease-out;
}

@keyframes message-slide-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Chat Message Content */
.bk-ChatMessage .bk-msg-content {
  background: white;
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  position: relative;
}

/* System Messages */
.bk-ChatMessage[data-user="System"] .bk-msg-content,
.bk-ChatMessage[data-user="Results"] .bk-msg-content,
.bk-ChatMessage[data-user="PDF Help"] .bk-msg-content {
  background: linear-gradient(135deg, #ddd6fe, #e0e7ff);
  border-left: 4px solid var(--accent-color);
}

/* Agent Messages */
.bk-ChatMessage[data-user*="Agent"] .bk-msg-content {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-left: 4px solid var(--primary-color);
}

/* Download Messages */
.bk-ChatMessage[data-user="Download"] .bk-msg-content {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border-left: 4px solid #f59e0b;
}

/* Chat Input Area */
.bk-ChatInterface .bk-input-group {
  background: white;
  border-top: 1px solid var(--border-color);
  padding: var(--space-lg);
}

/* ===== MARKDOWN CONTENT STYLING ===== */
.bk-Markdown {
  line-height: 1.7;
}

.bk-Markdown h1 {
  color: var(--primary-color);
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: var(--space-lg);
  line-height: 1.2;
}

.bk-Markdown h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 700;
  margin: var(--space-xl) 0 var(--space-lg) 0;
  line-height: 1.3;
}

.bk-Markdown h3 {
  color: var(--text-primary);
  font-size: 1.25rem;
  font-weight: 600;
  margin: var(--space-lg) 0 var(--space-md) 0;
}

.bk-Markdown p {
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
  font-size: 1rem;
}

.bk-Markdown ul, .bk-Markdown ol {
  color: var(--text-secondary);
  padding-left: var(--space-xl);
  margin-bottom: var(--space-md);
}

.bk-Markdown li {
  margin-bottom: var(--space-sm);
}

.bk-Markdown code {
  background: var(--bg-tertiary);
  padding: 0.2em 0.4em;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--accent-color);
}

.bk-Markdown strong {
  color: var(--text-primary);
  font-weight: 700;
}

/* ===== PROGRESS INDICATORS ===== */
.progress-indicator {
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin: var(--space-lg) 0;
  border: 1px solid var(--border-color);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
  margin: var(--space-md) 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
  border-radius: 4px;
  transition: width 0.3s ease;
  animation: progress-shimmer 2s infinite;
}

@keyframes progress-shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

/* ===== MOBILE RESPONSIVENESS ===== */
@media (max-width: 768px) {
  .bk-Row {
    flex-direction: column;
    padding: var(--space-md);
    gap: var(--space-md);
  }
  
  .bk-Column:first-child {
    position: static;
    max-height: none;
    order: 2;
    margin-top: var(--space-md);
  }
  
  .bk-Column:last-child {
    order: 1;
    min-height: 400px;
  }
  
  /* Stack form controls */
  .bk-input-group {
    margin-bottom: var(--space-md);
  }
  
  /* Larger touch targets */
  .bk-btn {
    min-height: 48px;
    font-size: 1rem;
  }
  
  select.bk-input {
    min-height: 48px;
    font-size: 16px; /* Prevents zoom on iOS */
  }
  
  /* Chat interface mobile optimization */
  .bk-ChatInterface .bk-chat-feed {
    padding: var(--space-md);
  }
  
  .bk-ChatMessage .bk-msg-content {
    padding: var(--space-md);
  }
}

@media (max-width: 480px) {
  .bk-Row {
    padding: var(--space-sm);
  }
  
  .bk-Column:first-child,
  .bk-Column:last-child {
    border-radius: var(--radius-md);
    padding: var(--space-lg);
  }
  
  .bk-Markdown h1 {
    font-size: 1.75rem;
  }
  
  .bk-Markdown h2 {
    font-size: 1.25rem;
  }
}

/* ===== ACCESSIBILITY IMPROVEMENTS ===== */
.bk-btn:focus,
select.bk-input:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ===== HIGH CONTRAST MODE ===== */
@media (prefers-contrast: high) {
  :root {
    --border-color: #000000;
    --border-hover: #333333;
    --text-secondary: #000000;
  }
}

/* ===== DOWNLOAD WIDGET ENHANCEMENTS ===== */
.download-widget {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
  overflow: hidden;
  margin: var(--space-lg) 0;
}

.download-widget button {
  background: linear-gradient(135deg, #059669, #047857);
  color: white;
  border: none;
  padding: var(--space-lg) var(--space-xl);
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
}

.download-widget button:hover {
  background: linear-gradient(135deg, #047857, #065f46);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* ===== SCROLLBAR STYLING ===== */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--text-muted);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
}

/* ===== LOADING STATES ===== */
.loading-shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading-shimmer 1.5s infinite;
}

@keyframes loading-shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* ===== ENHANCED VISUAL FEEDBACK ===== */
.success-state {
  border-left: 4px solid #10b981;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
}

.warning-state {
  border-left: 4px solid #f59e0b;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
}

.error-state {
  border-left: 4px solid #ef4444;
  background: linear-gradient(135deg, #fee2e2, #fecaca);
}

.info-state {
  border-left: 4px solid #3b82f6;
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
}

/* ===== PRINT STYLES ===== */
@media print {
  .bk-Column:first-child {
    display: none;
  }
  
  .bk-Row {
    flex-direction: column;
  }
  
  .bk-ChatInterface {
    box-shadow: none;
    border: 1px solid #ccc;
  }
}
</style>
"""

class SustainabilityPanelApp(param.Parameterized):
    """
    Panel-based web interface for the Sustainability Training System - Enhanced Design
    """
    
    def __init__(self):
        super().__init__()
        
        # Web environment detection
        self.is_web_env = self.is_web_environment()
        
        # Configure Panel for deployment environment
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
        # Inject CSS styles first
        css_pane = pn.pane.HTML(MODERN_CSS, width=0, height=0, margin=0)
        
        # Sidebar with controls
        self.sidebar = pn.Column(
            pn.pane.Markdown("## Training Configuration"),
            self.user_industry,
            self.regional_regulations, 
            self.difficulty_level,
            pn.layout.Divider(),
            self.start_button,
            pn.layout.Divider(),
            pn.pane.Markdown("## Export Results"),
            self.download_md_button,
            self.download_pdf_button,
            pn.layout.Divider(),
            self.reset_button,
            pn.Spacer(),
            pn.pane.Markdown("""
            ---
            **Need Help?**
            
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
        
        # Complete layout with CSS
        self.layout = pn.Column(
            css_pane,  # CSS injection
            pn.Row(
                self.sidebar,
                self.main_content,
                sizing_mode="stretch_width",
                height=700
            ),
            sizing_mode="stretch_width"
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
            
            # Schedule UI updates on main thread using simpler approach
            import time
            time.sleep(0.1)  # Small delay to ensure completion
            self.on_training_complete(result)
            
        except Exception as e:
            error_msg = f"Training failed: {str(e)}"
            print(f"❌ Training error: {error_msg}")
            print(f"Full traceback: {traceback.format_exc()}")
            
            # Schedule error handling on main thread
            import time
            time.sleep(0.1)  # Small delay
            self.on_training_error(error_msg)
    
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
        """Download the training report as markdown - Web optimized with better encoding"""
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
                    
                    # Safer encoding approach for web deployment
                    try:
                        # Encode content as base64 to avoid URL encoding issues
                        content_bytes = markdown_content.encode('utf-8')
                        content_b64 = base64.b64encode(content_bytes).decode('ascii')
                        
                        download_html = f"""
                        <div class="download-widget" style="margin: 20px 0; padding: 25px; border: 2px solid #10b981; border-radius: 12px; background: linear-gradient(135deg, #f0fdfa, #ecfdf5); text-align: center; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
                            <h3 style="color: #047857; margin-bottom: 15px; font-size: 1.25rem; font-weight: 700;">📄 Training Report Ready!</h3>
                            <p style="margin-bottom: 20px; color: #374151; line-height: 1.6;">Click the button below to download your comprehensive sustainability training report.</p>
                            <button onclick="downloadReportSafe()" 
                                    style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 15px 30px; 
                                           border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600;
                                           box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 8px;">
                                📄 Download {filename}
                            </button>
                            <p style="margin-top: 15px; font-size: 14px; color: #6b7280; font-weight: 500;">
                                File size: ~{len(markdown_content):,} characters | Format: Markdown (.md)
                            </p>
                        </div>
                        <script>
                        function downloadReportSafe() {{
                            try {{
                                // Decode from base64
                                const contentB64 = '{content_b64}';
                                const contentBytes = Uint8Array.from(atob(contentB64), c => c.charCodeAt(0));
                                const blob = new Blob([contentBytes], {{ type: 'text/markdown;charset=utf-8' }});
                                
                                const url = window.URL.createObjectURL(blob);
                                const link = document.createElement('a');
                                link.href = url;
                                link.download = '{filename}';
                                link.style.display = 'none';
                                document.body.appendChild(link);
                                link.click();
                                document.body.removeChild(link);
                                window.URL.revokeObjectURL(url);
                                
                                console.log('✅ Download completed successfully');
                                
                                // Show success feedback
                                const button = document.querySelector('button[onclick="downloadReportSafe()"]');
                                if (button) {{
                                    const originalText = button.innerHTML;
                                    button.innerHTML = '✅ Downloaded!';
                                    button.style.background = 'linear-gradient(135deg, #059669, #047857)';
                                    setTimeout(() => {{
                                        button.innerHTML = originalText;
                                        button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                                    }}, 2000);
                                }}
                            }} catch (error) {{
                                console.error('Download error:', error);
                                // Fallback method
                                try {{
                                    const fallbackContent = atob('{content_b64}');
                                    const fallbackBlob = new Blob([fallbackContent], {{ type: 'text/plain;charset=utf-8' }});
                                    const fallbackUrl = window.URL.createObjectURL(fallbackBlob);
                                    const fallbackLink = document.createElement('a');
                                    fallbackLink.href = fallbackUrl;
                                    fallbackLink.download = '{filename}';
                                    fallbackLink.click();
                                    window.URL.revokeObjectURL(fallbackUrl);
                                    alert('✅ Download started (fallback method)');
                                }} catch (fallbackError) {{
                                    console.error('Fallback download failed:', fallbackError);
                                    alert('❌ Download failed. Please try refreshing the page or contact support.');
                                }}
                            }}
                        }}
                        </script>
                        """
                        
                    except Exception as encoding_error:
                        print(f"Encoding error: {encoding_error}")
                        # Ultra-safe fallback - just show the content
                        download_html = f"""
                        <div style="margin: 20px 0; padding: 20px; border: 2px solid #dc3545; border-radius: 10px; background-color: #f8f9fa;">
                            <h3 style="color: #dc3545;">Download Issue</h3>
                            <p>There was an encoding issue with the download. Please copy the content below:</p>
                            <textarea style="width: 100%; height: 200px; font-family: monospace; font-size: 12px;" readonly>
{markdown_content[:1000]}...
                            </textarea>
                            <p><small>Content truncated for display. Please refresh and try again for full report.</small></p>
                        </div>
                        """
                    
                    download_widget = pn.pane.HTML(download_html, sizing_mode="stretch_width")
                    
                    self.chat_interface.send("📄 **Training Report Generated Successfully!**", user="System", respond=False)
                    self.chat_interface.send(download_widget, user="Download", respond=False)
                    
        except Exception as e:
            error_msg = f"Error preparing download: {str(e)}"
            print(f"Download error: {error_msg}")
            print(f"Traceback: {traceback.format_exc()}")
            self.chat_interface.send(error_msg, user="System", respond=False)
    
    def download_pdf_report(self, event):
        """Download instructions for PDF conversion - Web optimized"""
        self.chat_interface.send(
            """📑 **PDF Conversion Instructions:**

**Step 1:** First download the Markdown report using the button above

**Step 2:** Convert to PDF:
• Go to **https://www.pdfforge.org/online/en/markdown-to-pdf**
• Upload your .md file or paste the content
• Click "Convert to PDF"
• Download your professionally formatted PDF report


Your report contains professional formatting that will look great as a PDF! 🎯""", 
            user="PDF Help", 
            respond=False
        )
    
    def format_results_as_markdown(self, data: Dict[str, Any]) -> str:
        """Format training results as markdown report with safe encoding - PDF-friendly without emojis"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract data sections with safe fallbacks
        scenario = data.get('scenario', {})
        problematic_analysis = data.get('problematic_analysis', {})
        best_practices = data.get('best_practices', {})
        assessment_questions = data.get('assessment_questions', [])
        personalized_feedback = data.get('personalized_feedback', {})
        key_takeaways = data.get('key_takeaways', [])
        
        # Helper function to safely format lists
        def safe_format_list(items, prefix="- "):
            if not items:
                return "- None specified\n"
            result = ""
            for item in items:
                # Clean any problematic characters
                clean_item = str(item).replace('\n', ' ').replace('\r', ' ')
                result += f"{prefix}{clean_item}\n"
            return result
        
        # Helper function to safely format text
        def safe_format_text(text, default="N/A"):
            if not text:
                return default
            return str(text).replace('\n', ' ').replace('\r', ' ')
        
        markdown = f"""# Sustainability Training Report

**Generated:** {timestamp}
**Session ID:** {safe_format_text(data.get('session_id', 'N/A'))}
**Learner Profile:** {safe_format_text(data.get('learner_profile', 'Marketing Professional'))}

---

## Executive Summary

This comprehensive sustainability training session was designed to enhance understanding of compliant sustainability messaging and prevent greenwashing violations. The training covers industry-specific scenarios, regulatory compliance requirements, and practical application strategies.

## Business Scenario

**Company:** {safe_format_text(scenario.get('company_name', 'N/A'))}
**Industry:** {safe_format_text(scenario.get('industry', 'N/A'))}
**Location:** {safe_format_text(scenario.get('location', 'N/A'))}
**Size:** {safe_format_text(scenario.get('company_size', 'N/A'))}

### Company Overview
**Product/Service:** {safe_format_text(scenario.get('product_service', 'N/A'))}
**Target Audience:** {safe_format_text(scenario.get('target_audience', 'N/A'))}

### Marketing Objectives
{safe_format_list(scenario.get('marketing_objectives', []))}

### Sustainability Context
{safe_format_text(scenario.get('sustainability_context', 'N/A'))}

### Regulatory Framework
{safe_format_text(scenario.get('regulatory_context', 'N/A'))}

---

## Problematic Messaging Analysis

"""
        
        # Add problematic messages with safe formatting
        for i, msg in enumerate(problematic_analysis.get('problematic_messages', []), 1):
            markdown += f"""### Example {i}: {safe_format_text(msg.get('id', f'Message {i}'))}

**Problematic Message:**
> {safe_format_text(msg.get('message', 'N/A'))}

**Problems Identified:**
{safe_format_list(msg.get('problems_identified', []))}

**Regulatory Violations:**
{safe_format_list(msg.get('regulatory_violations', []))}

**Why This Is Problematic:**
{safe_format_text(msg.get('why_problematic', 'N/A'))}

**Potential Consequences:**
{safe_format_list(msg.get('potential_consequences', []))}

---

"""
        
        markdown += """## Best Practice Corrections

"""
        
        # Add corrected messages with safe formatting
        for i, correction in enumerate(best_practices.get('corrected_messages', []), 1):
            markdown += f"""### Correction {i}

**Original Message ID:** {safe_format_text(correction.get('original_message_id', 'N/A'))}

**Improved Message:**
> {safe_format_text(correction.get('corrected_message', 'N/A'))}

**Changes Made:**
{safe_format_list(correction.get('changes_made', []))}

**Compliance Notes:**
{safe_format_text(correction.get('compliance_notes', 'N/A'))}

**Best Practices Applied:**
{safe_format_list(correction.get('best_practices_applied', []))}

---

"""
        
        markdown += """## Knowledge Assessment

"""
        
        # Add assessment questions with safe formatting
        for i, question in enumerate(assessment_questions, 1):
            markdown += f"""### Question {i}

**Type:** {safe_format_text(question.get('type', 'N/A'))} | **Difficulty:** {safe_format_text(question.get('difficulty_level', 'N/A'))}

**Question:** {safe_format_text(question.get('question', 'N/A'))}

"""
            if question.get('options'):
                markdown += "**Options:**\n"
                markdown += safe_format_list(question.get('options', []))
                markdown += "\n"
            
            markdown += f"""**Correct Answer:** {safe_format_text(question.get('correct_answer', 'N/A'))}

**Explanation:** {safe_format_text(question.get('explanation', 'N/A'))}

**Learning Objective:** {safe_format_text(question.get('learning_objective', 'N/A'))}

---

"""
        
        markdown += """## Personalized Feedback

### Role-Specific Tips
"""
        markdown += safe_format_list(personalized_feedback.get('role_specific_tips', []))
        
        markdown += """
### Team Training Recommendations
"""
        markdown += safe_format_list(personalized_feedback.get('team_training_recommendations', []))
        
        markdown += """
### Implementation Strategies
"""
        markdown += safe_format_list(personalized_feedback.get('implementation_strategies', []))
        
        markdown += """
### Next Steps
"""
        markdown += safe_format_list(personalized_feedback.get('next_steps', []))
        
        markdown += """
---

## Key Takeaways

"""
        markdown += safe_format_list(key_takeaways)
        
        markdown += """
---

## Compliance Checklist

"""
        markdown += safe_format_list(data.get('compliance_checklist', []), "- [ ] ")
        
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