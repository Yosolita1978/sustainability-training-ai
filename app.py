#!/usr/bin/env python
"""
Sustainability Training Panel Web Application - Production Entry Point

This is the web-optimized entry point for deployment to Render.
It imports and configures your existing Panel app for production use.
"""

import os
import sys
import warnings
from datetime import datetime

# Load environment variables (for API keys)
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load from .env file if present (local development)
except ImportError:
    pass  # dotenv not required in production

# Suppress warnings for cleaner production logs
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", message=".*Accessing the 'model_fields' attribute.*")

# Add src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Import Panel and configure for web deployment
import panel as pn

# Production Panel configuration
pn.config.allow_websocket_origin = ["*"]  # Allow connections from Render domain
pn.extension('tabulator')  # Only load essential extensions

def check_environment():
    """Check that required environment variables are available"""
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Make sure to set these in your Render dashboard environment variables.")
        return False
    else:
        print("✅ All required environment variables found")
        return True

def create_app():
    """Create and configure the Panel application"""
    try:
        print("🚀 Starting Sustainability Training Application...")
        
        # Import your existing Panel app
        from sustainability.panel_bridge import create_sustainability_app
        
        print("✅ Panel bridge imported successfully")
        
        # Create the app instance
        app = create_sustainability_app()
        
        print("✅ Sustainability app created successfully")
        
        return app.layout
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure your src/sustainability modules are properly configured")
        
        # Create a simple error page
        error_app = pn.pane.Markdown(f"""
        # ⚠️ Configuration Error
        
        **Error:** {str(e)}
        
        **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        The application could not start due to a configuration issue.
        Please check the server logs for more details.
        """)
        return error_app
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
        # Create a generic error page
        error_app = pn.pane.Markdown(f"""
        # 🔧 Application Error
        
        **Error:** {str(e)}
        
        **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        The application encountered an error during startup.
        Please try again in a few moments.
        """)
        return error_app

def main():
    """Main entry point for the web application"""
    
    print("=" * 60)
    print("🌱 SUSTAINABILITY TRAINING AI - WEB APP")
    print("=" * 60)
    
    # Check environment configuration
    env_ok = check_environment()
    if not env_ok:
        print("⚠️  Application starting with missing environment variables")
    
    # Get port configuration
    PORT = int(os.environ.get('PORT', 5007))
    HOST = '0.0.0.0'  # Required for web deployment
    
    print(f"🌐 Server configuration:")
    print(f"   Host: {HOST}")
    print(f"   Port: {PORT}")
    print(f"   Environment: {'Production' if os.getenv('PORT') else 'Development'}")
    
    try:
        # Create the Panel application
        app = create_app()
        
        print("✅ Application ready to serve")
        print(f"🔗 Access at: http://{HOST}:{PORT}")
        print("=" * 60)
        
        return app
        
    except Exception as e:
        print(f"❌ Failed to create application: {e}")
        return pn.pane.Markdown("# Application Failed to Start\nPlease check server logs.")

# Create the application instance
app_instance = main()

# Make the app servable (required by Panel)
app_instance.servable()

# For development testing
if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5007))
    HOST = '0.0.0.0'
    
    print(f"\n🧪 Development mode - starting server...")
    print(f"🔗 Open: http://localhost:{PORT}")
    
    try:
        # Start the Panel server
        app_instance.show(
            port=PORT,
            host=HOST,
            show=False,  # Don't try to open browser in production
            allow_websocket_origin=["*"],
            autoreload=False  # Disable autoreload in production
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)