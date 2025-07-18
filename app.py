#!/usr/bin/env python
"""
Sustainability Training Panel Web Application - Production Entry Point

This is the web-optimized entry point for deployment to Render.
"""

import os
import sys
import warnings
import traceback
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
pn.extension()  # Minimal extensions for faster startup

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

def create_simple_health_check():
    """Create a simple health check page if main app fails"""
    health_content = f"""
    # 🌱 Sustainability Training AI
    
    **Status:** Server is running
    **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    **Environment:** Production
    
    The application is starting up. Please refresh in a moment.
    
    If you continue to see this message, there may be a configuration issue.
    """
    
    return pn.pane.Markdown(health_content, sizing_mode="stretch_width")

def create_error_page(error_msg: str):
    """Create an error page with debugging information"""
    error_content = f"""
    # ⚠️ Application Error
    
    **Error:** {error_msg}
    **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    **Environment:** {'Production' if os.getenv('PORT') else 'Development'}
    
    ## Troubleshooting
    
    1. **Check Environment Variables:** Ensure OPENAI_API_KEY and SERPER_API_KEY are set
    2. **Check Dependencies:** Verify all required packages are installed
    3. **Check Logs:** Review the server logs for more detailed error information
    
    ## Support
    
    If this issue persists, please contact the administrator with the error details above.
    """
    
    return pn.pane.Markdown(error_content, sizing_mode="stretch_width")

def create_app():
    """Create and configure the Panel application"""
    try:
        print("🚀 Starting Sustainability Training Application...")
        print(f"🔧 Python path: {sys.path}")
        print(f"📁 Current directory: {current_dir}")
        print(f"📂 Source path: {src_path}")
        
        # Check if source path exists
        if not os.path.exists(src_path):
            raise ImportError(f"Source directory not found: {src_path}")
        
        # Check if sustainability module exists
        sustainability_path = os.path.join(src_path, 'sustainability')
        if not os.path.exists(sustainability_path):
            raise ImportError(f"Sustainability module not found: {sustainability_path}")
        
        # Try to import the panel bridge
        print("📦 Importing sustainability panel bridge...")
        from sustainability.panel_bridge import create_sustainability_app
        
        print("✅ Panel bridge imported successfully")
        
        # Create the app instance
        print("🔨 Creating app instance...")
        app = create_sustainability_app()
        
        print("✅ Sustainability app created successfully")
        
        return app.servable()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"📊 Full traceback:\n{traceback.format_exc()}")
        
        # List available modules for debugging
        try:
            import sustainability
            print(f"✅ Sustainability module found at: {sustainability.__file__}")
            
            # List sustainability submodules
            sustainability_dir = os.path.dirname(sustainability.__file__)
            files = os.listdir(sustainability_dir)
            print(f"📁 Sustainability module contents: {files}")
            
        except ImportError as ie:
            print(f"❌ Could not import sustainability module: {ie}")
        
        return create_error_page(f"Import Error: {str(e)}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"📊 Full traceback:\n{traceback.format_exc()}")
        
        return create_error_page(f"Application Error: {str(e)}")

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
    
    print(f"🌐 Server configuration:")
    print(f"   Port: {PORT}")
    print(f"   Environment: {'Production' if os.getenv('PORT') else 'Development'}")
    print(f"   Panel version: {pn.__version__}")
    
    try:
        # Create the Panel application
        print("🔨 Creating Panel application...")
        app = create_app()
        
        print("✅ Application ready to serve")
        print("=" * 60)
        
        return app
        
    except Exception as e:
        print(f"❌ Failed to create application: {e}")
        print(f"📊 Full traceback:\n{traceback.format_exc()}")
        return create_simple_health_check()

# Create the application instance for Panel CLI serving
print("🔄 Initializing application...")
app_instance = main()
print("✅ Application instance created")

# Make the app servable (required by Panel CLI)
app_instance.servable()
print("✅ Application is servable")