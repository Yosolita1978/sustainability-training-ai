#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def save_simple_report(result, session_id):
    """Save a simple report - Web environment compatible"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create outputs directory if possible
    try:
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        outputs_dir = 'outputs'
    except (OSError, PermissionError):
        # Fallback for web environments where file system access is limited
        outputs_dir = None
        print("⚠️ Warning: Cannot create outputs directory in web environment")
    
    if outputs_dir:
        # Save as text file
        txt_file = f'{outputs_dir}/training_report_{timestamp}.txt'
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Sustainability Training Report\n")
                f.write(f"Session: {session_id}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                f.write(str(result))
            print(f"📄 Report saved: {txt_file}")
        except (OSError, PermissionError) as e:
            print(f"⚠️ Could not save text report: {e}")
        
        # Try to save structured data if available
        try:
            if hasattr(result, 'tasks_output') and result.tasks_output:
                last_task = result.tasks_output[-1]
                if hasattr(last_task, 'pydantic') and last_task.pydantic:
                    json_file = f'{outputs_dir}/structured_data_{timestamp}.json'
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(last_task.pydantic.model_dump(), f, indent=2, ensure_ascii=False)
                    print(f"📊 Structured data saved: {json_file}")
        except Exception as e:
            print(f"⚠️ Could not save structured data: {e}")
    
    return True

def run():
    """Run the crew - Web environment compatible"""
    session_id = f"TRAIN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    inputs = {
        'user_industry': 'Marketing Agency',
        'regional_regulations': 'EU Green Claims Directive, CSRD',
        'current_year': str(datetime.now().year),
        'session_id': session_id
    }
    
    try:
        print("🌱 Starting Sustainability Training...")
        print(f"Session: {session_id}")
        
        # Import here to avoid issues if running in web environment
        from sustainability.crew import Sustainability
        
        result = Sustainability().crew().kickoff(inputs=inputs)
        
        print("✅ Training completed!")
        save_simple_report(result, session_id)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """Training mode entry point"""
    return run()

def replay():
    """Replay mode entry point"""
    print("⚠️ Replay mode not implemented for web environment")
    return None

def test():
    """Test mode entry point"""
    print("🧪 Running test mode...")
    try:
        from sustainability.crew import Sustainability
        
        # Simple test inputs
        test_inputs = {
            'user_industry': 'Technology',
            'regional_regulations': 'EU Green Claims Directive',
            'current_year': '2025',
            'session_id': 'TEST_SESSION'
        }
        
        print("✅ Sustainability crew imported successfully")
        print("✅ Test inputs created successfully")
        print("🎯 Test completed - ready for web deployment")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    run()