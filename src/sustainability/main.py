#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def save_business_toolkit(result, session_id):
    """Save a business toolkit report - Web environment compatible"""
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
        txt_file = f'{outputs_dir}/business_toolkit_{timestamp}.txt'
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Sustainability Business Toolkit\n")
                f.write(f"Session: {session_id}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                f.write(str(result))
            print(f"📄 Business toolkit saved: {txt_file}")
        except (OSError, PermissionError) as e:
            print(f"⚠️ Could not save toolkit file: {e}")
        
        # Try to save structured data if available
        try:
            if hasattr(result, 'tasks_output') and result.tasks_output:
                last_task = result.tasks_output[-1]
                if hasattr(last_task, 'pydantic') and last_task.pydantic:
                    json_file = f'{outputs_dir}/structured_data_{timestamp}.json'
                    with open(json_file, 'w', encoding='utf-8') as f:
                        # Updated to use model_dump() instead of deprecated dict()
                        json.dump(last_task.pydantic.model_dump(), f, indent=2, ensure_ascii=False)
                    print(f"📊 Structured data saved: {json_file}")
                    
                    # Show toolkit summary
                    data = last_task.pydantic.model_dump()
                    toolkit_counts = {
                        'quick_reference_tools': len(data.get('quick_reference_tools', [])),
                        'market_intelligence': len(data.get('market_intelligence', [])),
                        'communication_templates': len(data.get('communication_templates', [])),
                        'role_specific_guides': len(data.get('role_specific_guides', []))
                    }
                    
                    total_toolkit = sum(toolkit_counts.values())
                    assessment_count = len(data.get('assessment_questions', []))
                    
                    print(f"🛠️ Toolkit Summary:")
                    for component, count in toolkit_counts.items():
                        status = '✅' if count > 0 else '⚠️'
                        print(f"   {status} {component}: {count} items")
                    
                    print(f"📈 Total business tools: {total_toolkit}")
                    print(f"📝 Legacy assessment questions: {assessment_count}")
                    
                    if total_toolkit > 0:
                        print("🎉 Business toolkit generation successful!")
                    else:
                        print("⚠️ No toolkit components generated - check configuration")
                        
        except Exception as e:
            print(f"⚠️ Could not save structured data: {e}")
    
    return True

def run():
    """Run the business toolkit generation crew - Web environment compatible"""
    session_id = f"TOOLKIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    inputs = {
        'user_industry': 'Marketing Agency',
        'regional_regulations': 'EU Green Claims Directive, CSRD',
        'current_year': str(datetime.now().year),
        'session_id': session_id
    }
    
    try:
        print("🛠️ Starting Sustainability Business Toolkit Generation...")
        print(f"Session: {session_id}")
        print("📋 Creating: Quick reference tools, templates, guides, and market intelligence")
        print("-" * 60)
        
        # Import here to avoid issues if running in web environment
        from sustainability.crew import Sustainability
        
        result = Sustainability().crew().kickoff(inputs=inputs)
        
        print("-" * 60)
        print("✅ Business toolkit generation completed!")
        save_business_toolkit(result, session_id)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        raise Exception(f"An error occurred while generating the business toolkit: {e}")

def train():
    """Business toolkit generation mode entry point"""
    return run()

def replay():
    """Replay mode entry point"""
    print("⚠️ Replay mode not implemented for web environment")
    return None

def test():
    """Test mode entry point"""
    print("🧪 Running business toolkit generation test...")
    try:
        from sustainability.crew import Sustainability
        
        # Simple test inputs
        test_inputs = {
            'user_industry': 'Technology',
            'regional_regulations': 'EU Green Claims Directive',
            'current_year': '2025',
            'session_id': 'TEST_TOOLKIT_SESSION'
        }
        
        print("✅ Sustainability crew imported successfully")
        print("✅ Test inputs created successfully")
        print("🎯 Test completed - ready for business toolkit generation")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    run()