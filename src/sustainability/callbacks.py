from typing import Optional, Callable, Any, Dict
from crewai.tasks.task_output import TaskOutput
from datetime import datetime
import json

class PanelCallbackHandler:
    """Callback handler to bridge CrewAI outputs to Panel ChatInterface"""
    
    def __init__(self):
        self.chat_interface: Optional[Any] = None
        self.session_id: Optional[str] = None
        self.active_agent: Optional[str] = None
        self.task_count: int = 0
        self.completed_tasks: int = 0
        
    def register_chat_interface(self, chat_interface: Any):
        """Register the Panel ChatInterface to send messages to"""
        self.chat_interface = chat_interface
        
    def set_session_id(self, session_id: str):
        """Set the current business toolkit session ID"""
        self.session_id = session_id
        
    def send_message(self, message: str, user: str = "System", message_type: str = "info"):
        """Send a message to the Panel chat interface"""
        if self.chat_interface is None:
            print(f"[{user}] {message}")  # Fallback to console
            return
            
        # Format message with timestamp and type
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add emoji and formatting based on message type
        if message_type == "agent_start":
            formatted_message = f"🤖 **{user}** [{timestamp}]\n{message}"
        elif message_type == "agent_thinking":
            formatted_message = f"💭 **{user}** [{timestamp}]\n{message}"
        elif message_type == "tool_use":
            formatted_message = f"🛠️ **{user}** [{timestamp}]\n{message}"
        elif message_type == "task_complete":
            formatted_message = f"✅ **{user}** [{timestamp}]\n{message}"
        elif message_type == "error":
            formatted_message = f"❌ **{user}** [{timestamp}]\n{message}"
        elif message_type == "session":
            formatted_message = f"🚀 **Session** [{timestamp}]\n{message}"
        elif message_type == "progress":
            formatted_message = f"📊 **Progress** [{timestamp}]\n{message}"
        elif message_type == "search":
            formatted_message = f"🔍 **{user}** [{timestamp}]\n{message}"
        elif message_type == "business_insight":
            formatted_message = f"💡 **{user}** [{timestamp}]\n{message}"
        else:
            formatted_message = f"📝 **{user}** [{timestamp}]\n{message}"
            
        # Send to Panel chat
        try:
            self.chat_interface.send(formatted_message, user=user, respond=False)
        except Exception as e:
            print(f"Error sending to chat: {e}")
            print(f"[{user}] {message}")  # Fallback
    
    def on_agent_start(self, agent_name: str, task_description: str):
        """Called when an agent starts working on a business toolkit task"""
        self.active_agent = agent_name
        self.task_count += 1
        
        # Format task description nicely
        clean_description = task_description[:200] + "..." if len(task_description) > 200 else task_description
        message = f"Starting business analysis: {clean_description}"
        self.send_message(message, user=agent_name, message_type="agent_start")
        
        # Send progress update
        progress_msg = f"Business Component {self.task_count} of 4: {agent_name} is analyzing market data..."
        self.send_message(progress_msg, user="System", message_type="progress")
    
    def on_agent_thinking(self, agent_name: str, thought: str):
        """Called when an agent is analyzing business data"""
        # Only show brief thinking messages to avoid spam
        clean_thought = thought[:150] + "..." if len(thought) > 150 else thought
        message = f"Business Analysis: {clean_thought}"
        self.send_message(message, user=agent_name, message_type="agent_thinking")
    
    def on_tool_use(self, agent_name: str, tool_name: str, tool_input: str, tool_output: str):
        """Called when an agent uses a tool - Updated for business toolkit research"""
        # Handle our custom SerperDevTool for business research
        if tool_name in ["SerperDevTool", "CustomSerperTool"]:
            # Format search results nicely for business context
            clean_input = tool_input[:100] + "..." if len(tool_input) > 100 else tool_input
            
            # Check if we got results
            if "Search Results" in tool_output or "=== " in tool_output:
                # Count results for better feedback
                result_count = tool_output.count("**") // 2  # Approximate result count
                message = f"🔍 Market Research: {clean_input}\n📊 Found {result_count} business intelligence sources and industry insights"
            elif "Error:" in tool_output:
                message = f"🔍 Research attempted: {clean_input}\n⚠️ Using cached business intelligence and industry knowledge"
            else:
                message = f"🔍 Business Intelligence: {clean_input}\n📊 Gathering current market data and competitive insights"
            
            self.send_message(message, user=agent_name, message_type="search")
        else:
            # Other tools
            clean_input = tool_input[:100] + "..." if len(tool_input) > 100 else tool_input
            clean_output = tool_output[:200] + "..." if len(tool_output) > 200 else tool_output
            message = f"Using {tool_name}\n🔍 Input: {clean_input}\n📋 Business Data: {clean_output}"
            self.send_message(message, user=agent_name, message_type="tool_use")
    
    def on_task_complete(self, agent_name: str, task_output: str):
        """Called when a business toolkit task is completed"""
        self.completed_tasks += 1
        
        # Show brief completion message
        message = f"Business component delivered successfully! ✨\n📊 Progress: {self.completed_tasks}/4 business components completed"
        self.send_message(message, user=agent_name, message_type="task_complete")
        
        # Show business-focused task summary based on agent
        if "scenario" in agent_name.lower():
            summary = "✅ Business scenario analysis completed with market context and regulatory framework"
        elif "mistake" in agent_name.lower():
            summary = "✅ Compliance risk analysis completed with real-world violation examples and business impact"
        elif "practice" in agent_name.lower():
            summary = "✅ Best practice implementation strategies delivered with proven market solutions"
        elif "assessment" in agent_name.lower() or "toolkit" in agent_name.lower():
            summary = "✅ Comprehensive business toolkit generated with templates, guides, and operational resources"
        else:
            summary = "✅ Business analysis component completed successfully"
            
        self.send_message(summary, user="System", message_type="business_insight")
    
    def on_error(self, agent_name: str, error_message: str):
        """Called when an error occurs during business toolkit generation"""
        clean_error = error_message[:300] + "..." if len(error_message) > 300 else error_message
        message = f"⚠️ Business analysis issue: {clean_error}"
        self.send_message(message, user=agent_name, message_type="error")
    
    def on_session_start(self, session_info: Dict[str, Any]):
        """Called when a business toolkit generation session starts"""
        self.session_id = session_info.get('session_id', 'Unknown')
        self.task_count = 0
        self.completed_tasks = 0
        
        message = f"""🛠️ **Business Toolkit Generation Initiated**

**Session ID:** {self.session_id}
**Industry Focus:** {session_info.get('user_industry', 'Multi-Industry')}
**Regulatory Framework:** {session_info.get('regional_regulations', 'Global Best Practices')}
**Business Scope:** {session_info.get('difficulty_level', 'Professional')}

**Business Toolkit Components:**
1. 🏢 Market scenario analysis and competitive context
2. ⚠️ Compliance risk assessment with real violation cases  
3. ✅ Implementation strategies with proven market solutions
4. 🛠️ Operational toolkit with templates and resources

**Business Value Delivered:**
- 🔍 Quick reference tools for daily marketing operations
- 📊 Market intelligence and competitive analysis  
- 📧 Communication templates for business processes  
- 👥 Role-specific implementation guides
- ⚖️ Compliance frameworks and risk mitigation tools

Our business intelligence agents are now researching current market conditions, regulatory requirements, and industry best practices to create your comprehensive toolkit..."""
        
        self.send_message(message, user="System", message_type="session")
    
    def on_session_complete(self, results: Any):
        """Called when the business toolkit generation is complete"""
        message = f"""🎉 **Business Toolkit Generation Completed Successfully!**

📊 **Business Toolkit Summary:**
- ✅ All 4 business components delivered
- 🛠️ Comprehensive operational toolkit generated
- 🎯 Implementation guidance and templates provided
- 📧 Business communication workflows created

**Your Business Toolkit Includes:**
- 🔍 Daily-use compliance and safety tools
- 📊 Market intelligence and competitive insights
- 📧 Professional communication templates
- 👥 Role-specific implementation guides for marketing teams
- ⚖️ Risk assessment and compliance frameworks

**Immediate Business Value:**
1. Download your comprehensive business toolkit using the export options
2. Implement the quick reference tools for immediate compliance improvement
3. Use communication templates with your legal and marketing teams
4. Follow role-specific guides for daily marketing operations
5. Reference market intelligence for competitive positioning

**Next Steps for Business Implementation:**
- Review compliance tools and integrate into daily workflows
- Train marketing team using role-specific guides
- Implement communication templates in business processes
- Use market intelligence for strategic planning
- Establish ongoing compliance monitoring using provided frameworks

Your business toolkit is ready for immediate implementation! 🚀"""
        
        self.send_message(message, user="System", message_type="task_complete")

# Global instance that can be used across the application
panel_callback_handler = PanelCallbackHandler()

def print_task_output(task_output: TaskOutput) -> TaskOutput:
    """Callback function for CrewAI tasks - Business toolkit focused"""
    if task_output.agent and panel_callback_handler.chat_interface:
        agent_name = task_output.agent
        
        # Try to extract meaningful business output information
        if hasattr(task_output, 'pydantic') and task_output.pydantic:
            # For structured Pydantic outputs, show business-focused summary
            try:
                data = task_output.pydantic.model_dump()
                if 'company_name' in data:
                    # Business scenario task
                    output_summary = f"Market scenario created for {data.get('company_name', 'target company')} in {data.get('industry', 'focus industry')}"
                elif 'problematic_messages' in data:
                    # Compliance risk analysis task
                    msg_count = len(data.get('problematic_messages', []))
                    output_summary = f"Compliance analysis completed: {msg_count} risk patterns identified with business impact assessment"
                elif 'corrected_messages' in data:
                    # Business implementation strategy task
                    correction_count = len(data.get('corrected_messages', []))
                    output_summary = f"Implementation strategies delivered: {correction_count} proven solutions with market examples"
                elif 'quick_reference_tools' in data or 'communication_templates' in data:
                    # Business toolkit task
                    toolkit_counts = {
                        'quick_reference_tools': len(data.get('quick_reference_tools', [])),
                        'market_intelligence': len(data.get('market_intelligence', [])),
                        'communication_templates': len(data.get('communication_templates', [])),
                        'role_specific_guides': len(data.get('role_specific_guides', []))
                    }
                    total_items = sum(toolkit_counts.values())
                    output_summary = f"Comprehensive business toolkit delivered: {total_items} operational tools and templates ready for implementation"
                else:
                    output_summary = "Business component completed with structured deliverables"
                    
            except Exception:
                output_summary = "Business task completed successfully"
        else:
            # For text outputs, show a brief business-focused summary
            output_text = str(task_output.raw)
            output_summary = output_text[:200] + "..." if len(output_text) > 200 else output_text
        
        panel_callback_handler.on_task_complete(agent_name, output_summary)
    
    return task_output

def get_panel_callback_handler() -> PanelCallbackHandler:
    """Get the global callback handler instance"""
    return panel_callback_handler