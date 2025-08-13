#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime

# SMART PATH DETECTION: Find the actual src directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# If we're in src/sustainability/, go up two levels to find src/
if current_dir.endswith('src/sustainability'):
    src_path = os.path.dirname(current_dir)  # Go up one level to src/
elif current_dir.endswith('sustainability'):
    src_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'src')  # Project root + src
else:
    # Assume we're in project root
    src_path = os.path.join(current_dir, 'src')

# Clear old imports
for module_name in list(sys.modules.keys()):
    if module_name.startswith('sustainability'):
        del sys.modules[module_name]

sys.path.insert(0, src_path)
print(f"🔍 Debug: Using src path: {src_path}")

# Rest of your imports...
from sustainability.crew import SustainabilityCrew

print(f"🔍 Debug: Imported crew from: {SustainabilityCrew.__module__}")

def save_business_toolkit(result, session_id):
    """Save a comprehensive business toolkit report - Web environment compatible"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create outputs directory
    try:
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        outputs_dir = 'outputs'
    except (OSError, PermissionError):
        outputs_dir = None
        print("⚠️ Warning: Cannot create outputs directory in web environment")

    # Save TXT version
    if outputs_dir:
        txt_file = f'{outputs_dir}/business_toolkit_{timestamp}.txt'
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Sustainability Business Toolkit Report\n")
                f.write(f"Session: {session_id}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(str(result))
            print(f"📄 Business toolkit report saved: {txt_file}")
        except (OSError, PermissionError) as e:
            print(f"⚠️ Could not save toolkit file: {e}")

        # Save JSON structured version
        try:
            if hasattr(result, 'tasks_output') and result.tasks_output:
                final_task = result.tasks_output[-1]
                if hasattr(final_task, 'pydantic') and final_task.pydantic:
                    json_file = f'{outputs_dir}/business_toolkit_data_{timestamp}.json'
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(final_task.pydantic.model_dump(), f, indent=2, ensure_ascii=False)
                    print(f"📊 Business toolkit data saved: {json_file}")

                    data = final_task.pydantic.model_dump()
                    toolkit_metrics = {
                        'quick_reference_tools': len(data.get('quick_reference_tools', [])),
                        'market_intelligence': len(data.get('market_intelligence', [])),
                        'communication_templates': len(data.get('communication_templates', [])),
                        'role_specific_guides': len(data.get('role_specific_guides', []))
                    }
                    total_tools = sum(toolkit_metrics.values())
                    sources_count = len(data.get('sources_used', []))
                    scenario_created = bool(data.get('scenario', {}).get('company_name'))
                    compliance_analysis = len(data.get('problematic_analysis', {}).get('problematic_messages', []))
                    best_practices = len(data.get('best_practices', {}).get('corrected_messages', []))

                    print("\n🛠️  BUSINESS TOOLKIT GENERATION SUMMARY")
                    print("=" * 50)
                    print(f"📋 Business Toolkit Components:")
                    for component, count in toolkit_metrics.items():
                        status = '✅' if count > 0 else '❌'
                        component_name = component.replace('_', ' ').title()
                        print(f"   {status} {component_name}: {count} items")

                    print(f"\n📊 Business Analysis Completed:")
                    print(f"   ✅ Business Scenario: {'Created' if scenario_created else 'Missing'}")
                    print(f"   ✅ Compliance Issues Identified: {compliance_analysis}")
                    print(f"   ✅ Best Practice Solutions: {best_practices}")
                    print(f"   ✅ Market Research Sources: {sources_count}")

                    print(f"\n🎯 Business Value Delivered:")
                    print(f"   📈 Total Business Tools: {total_tools}")
                    print(f"   🔍 Market Intelligence Items: {toolkit_metrics['market_intelligence']}")
                    print(f"   📧 Communication Templates: {toolkit_metrics['communication_templates']}")
                    print(f"   👥 Role-Specific Guides: {toolkit_metrics['role_specific_guides']}")
                    print(f"   🚨 Quick Reference Tools: {toolkit_metrics['quick_reference_tools']}")

                    if total_tools >= 10:
                        print(f"\n🎉 BUSINESS TOOLKIT GENERATION SUCCESSFUL!")
                    elif total_tools >= 5:
                        print(f"\n⚠️  PARTIAL BUSINESS TOOLKIT GENERATED")
                    else:
                        print(f"\n❌ INSUFFICIENT BUSINESS TOOLKIT")
                        print(f"   📊 Only {total_tools} tools generated")
        except Exception as e:
            print(f"⚠️ Could not save structured business data: {e}")

    return True


def run():
    """Run the comprehensive business toolkit generation system"""
    session_id = f"BIZKIT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    inputs = {
        'company_profile': {"name": "Example Company", "description": "Sample description"},
        'industry_sector': 'Marketing Agency',
        'operations_data': {"facilities": ["HQ"], "energy_sources": ["solar"]},
        'jurisdiction': "US"
    }

    try:
        print("🛠️  SUSTAINABILITY BUSINESS TOOLKIT GENERATOR")
        print("=" * 60)
        print(f"Session: {session_id}")
        result = SustainabilityCrew().run_business_analysis(
            company_profile=inputs['company_profile'],
            industry_sector=inputs['industry_sector'],
            operations_data=inputs['operations_data'],
            jurisdiction=inputs['jurisdiction']
        )
        print("-" * 60)
        print("✅ BUSINESS TOOLKIT GENERATION COMPLETED!")
        save_business_toolkit(result, session_id)
        return result

    except Exception as e:
        print(f"❌ Business Toolkit Generation Error: {e}")
        import traceback
        print(f"Full diagnostic: {traceback.format_exc()}")
        raise


def train():
    """Business toolkit generation mode entry point"""
    print("🛠️  Starting Business Toolkit Generation Mode...")
    return run()


def replay():
    """Replay mode entry point"""
    print("⚠️ Replay mode not implemented for web environment")
    print("💡 Use 'run()' or 'train()' to generate fresh business toolkit")
    return None


def test():
    """Test business toolkit generation system"""
    print("🧪 BUSINESS TOOLKIT GENERATION SYSTEM TEST")
    print("=" * 50)
    try:
        _ = SustainabilityCrew()
        print("✅ Sustainability business toolkit system imported successfully")
        print("✅ Ready for business toolkit generation")
        return True
    except Exception as e:
        print(f"❌ System test failed: {e}")
        import traceback
        print(f"Full diagnostic: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    run()