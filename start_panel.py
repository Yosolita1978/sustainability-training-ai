#!/usr/bin/env python
"""
Simple Panel Test for Sustainability Training

This is a minimal test version for debugging and development.
"""

import warnings
import panel as pn
import sys
import os

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", message=".*Accessing the 'model_fields' attribute.*")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

pn.extension()

def create_simple_app():
    """Create a simple test app"""
    
    # Chat interface
    chat = pn.chat.ChatInterface(
        callback=lambda contents, user, instance: None,
        height=400,
        sizing_mode="stretch_width"
    )
    
    # Start button
    start_btn = pn.widgets.Button(
        name="🚀 Start Test", 
        button_type="primary",
        sizing_mode="stretch_width"
    )
    
    # Industry input for testing
    industry_input = pn.widgets.TextInput(
        name="Industry", 
        value="Marketing Agency",
        placeholder="Enter industry"
    )
    
    def start_test(event):
        """Test function"""
        chat.send("🌱 Test message from Panel!", user="System", respond=False)
        chat.send(f"Industry set to: {industry_input.value}", user="System", respond=False)
    
    start_btn.on_click(start_test)
    
    # Layout
    sidebar = pn.Column(
        "## 🧪 Panel Test",
        industry_input,
        start_btn,
        width=300
    )
    
    main_content = pn.Column(
        "# Sustainability Training Test",
        "This is a simple test interface to verify Panel is working correctly.",
        chat,
        sizing_mode="stretch_both"
    )
    
    layout = pn.Row(
        sidebar,
        main_content,
        sizing_mode="stretch_width",
        height=600
    )
    
    return layout

# Create the app
app = create_simple_app()

# Make it servable for panel serve command
app.servable()

# If running directly, start the server
if __name__ == "__main__":
    print("🚀 Starting Panel Test Server...")
    print("🌐 Open your browser to: http://localhost:5007")
    
    try:
        app.show(port=5007, show=True, autoreload=False)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try using: panel serve start_panel.py --show --port=5007")