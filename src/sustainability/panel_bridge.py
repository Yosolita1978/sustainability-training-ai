#!/usr/bin/env python
"""
Sustainability Training API Toolkit - Backend Services
Replaces Panel interface with REST API endpoints for Next.js frontend
"""

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import asyncio
import json
import uuid
import os
from datetime import datetime
import traceback
from pathlib import Path

# Background task management
import threading
from queue import Queue
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sustainability Training API",
    description="AI-powered sustainability messaging training toolkit",
    version="2.0.0"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app", "https://*.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== DATA MODELS ===== #

class TrainingRequest(BaseModel):
    """Request model for training session"""
    industry: str = Field(..., description="Target industry focus")
    regulations: str = Field(..., description="Regulatory framework")
    difficulty: str = Field(default="Intermediate", description="Training difficulty level")
    user_profile: Optional[Dict[str, Any]] = Field(default=None, description="Optional user profile data")

class TrainingSession(BaseModel):
    """Training session data model"""
    session_id: str = Field(..., description="Unique session identifier")
    status: str = Field(..., description="Session status: pending, running, completed, error")
    progress: float = Field(default=0.0, description="Completion percentage 0-100")
    current_agent: Optional[str] = Field(default=None, description="Currently active agent")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    results: Optional[Dict[str, Any]] = Field(default=None)

class AgentUpdate(BaseModel):
    """Real-time agent update model"""
    session_id: str
    agent_name: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: str = Field(default="info")  # info, progress, success, error
    progress: Optional[float] = Field(default=None)

class ReportRequest(BaseModel):
    """Report generation request"""
    session_id: str
    format: str = Field(default="markdown", description="Output format: markdown, json, pdf")
    include_sources: bool = Field(default=True, description="Include source citations")
    business_focus: bool = Field(default=True, description="Focus on business-relevant content")

# ===== GLOBAL STATE MANAGEMENT ===== #

class SessionManager:
    """Manages training sessions and real-time updates"""
    
    def __init__(self):
        self.sessions: Dict[str, TrainingSession] = {}
        self.websocket_connections: Dict[str, List[WebSocket]] = {}
        self.update_queue: Queue = Queue()
        
    def create_session(self, request: TrainingRequest) -> TrainingSession:
        """Create new training session"""
        session_id = f"train_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = TrainingSession(
            session_id=session_id,
            status="pending"
        )
        
        self.sessions[session_id] = session
        logger.info(f"Created session: {session_id}")
        return session
    
    def update_session(self, session_id: str, **updates):
        """Update session data"""
        if session_id in self.sessions:
            for key, value in updates.items():
                if hasattr(self.sessions[session_id], key):
                    setattr(self.sessions[session_id], key, value)
    
    def get_session(self, session_id: str) -> Optional[TrainingSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    async def broadcast_update(self, session_id: str, update: AgentUpdate):
        """Broadcast update to all connected WebSocket clients"""
        if session_id in self.websocket_connections:
            disconnected = []
            for websocket in self.websocket_connections[session_id]:
                try:
                    await websocket.send_text(update.model_dump_json())
                except Exception as e:
                    logger.warning(f"WebSocket send failed: {e}")
                    disconnected.append(websocket)
            
            # Remove disconnected clients
            for ws in disconnected:
                self.websocket_connections[session_id].remove(ws)
    
    def add_websocket(self, session_id: str, websocket: WebSocket):
        """Add WebSocket connection for session"""
        if session_id not in self.websocket_connections:
            self.websocket_connections[session_id] = []
        self.websocket_connections[session_id].append(websocket)
    
    def remove_websocket(self, session_id: str, websocket: WebSocket):
        """Remove WebSocket connection"""
        if session_id in self.websocket_connections:
            try:
                self.websocket_connections[session_id].remove(websocket)
            except ValueError:
                pass

# Global session manager instance
session_manager = SessionManager()

# ===== TRAINING ORCHESTRATION ===== #

class TrainingOrchestrator:
    """Orchestrates the AI training process with real-time updates"""
    
    @staticmethod
    async def run_training_session(session_id: str, request: TrainingRequest):
        """Run complete training session with real-time updates"""
        
        try:
            # Update session status
            session_manager.update_session(session_id, status="running", progress=5.0)
            
            # Send start notification
            await session_manager.broadcast_update(session_id, AgentUpdate(
                session_id=session_id,
                agent_name="System",
                message=f"🚀 Starting sustainability training session for {request.industry}",
                message_type="info",
                progress=5.0
            ))
            
            # Prepare training inputs
            training_inputs = {
                'user_industry': request.industry,
                'regional_regulations': request.regulations,
                'difficulty_level': request.difficulty,
                'current_year': str(datetime.now().year),
                'session_id': session_id,
                'business_focus': True,  # New: Focus on business-relevant content
                'report_format': 'toolkit'  # New: Toolkit-optimized format
            }
            
            # Import and run CrewAI system
            from sustainability.crew import Sustainability
            from sustainability.callbacks import get_panel_callback_handler
            
            # Set up callback handler for real-time updates
            callback_handler = get_panel_callback_handler()
            callback_handler.session_id = session_id
            callback_handler.websocket_broadcast = lambda update: asyncio.create_task(
                session_manager.broadcast_update(session_id, update)
            )
            
            # Progress tracking through agents
            agent_progress = {
                "scenario_builder": 25.0,
                "mistake_illustrator": 50.0, 
                "best_practice_coach": 75.0,
                "assessment_agent": 100.0
            }
            
            # Run the training crew
            logger.info(f"Starting CrewAI training for session {session_id}")
            sustainability_crew = Sustainability()
            result = sustainability_crew.crew().kickoff(inputs=training_inputs)
            
            # Process results for toolkit format
            processed_results = TrainingOrchestrator._process_results_for_toolkit(result)
            
            # Update session with results
            session_manager.update_session(
                session_id,
                status="completed",
                progress=100.0,
                completed_at=datetime.now(),
                results=processed_results
            )
            
            # Send completion notification
            await session_manager.broadcast_update(session_id, AgentUpdate(
                session_id=session_id,
                agent_name="System",
                message="✅ Training completed successfully! Results are ready for download.",
                message_type="success",
                progress=100.0
            ))
            
            logger.info(f"Training session {session_id} completed successfully")
            
        except Exception as e:
            error_message = f"Training failed: {str(e)}"
            logger.error(f"Session {session_id} error: {error_message}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            # Update session with error
            session_manager.update_session(
                session_id,
                status="error",
                error_message=error_message,
                completed_at=datetime.now()
            )
            
            # Send error notification
            await session_manager.broadcast_update(session_id, AgentUpdate(
                session_id=session_id,
                agent_name="System",
                message=f"❌ Training error: {error_message}",
                message_type="error"
            ))
    
    @staticmethod
    def _process_results_for_toolkit(result) -> Dict[str, Any]:
        """Process CrewAI results for toolkit format - streamlined for business use"""
        
        try:
            if hasattr(result, 'tasks_output') and result.tasks_output:
                final_task = result.tasks_output[-1]
                if hasattr(final_task, 'pydantic') and final_task.pydantic:
                    raw_data = final_task.pydantic.model_dump()
                    
                    # Extract and streamline for business toolkit
                    toolkit_data = {
                        "session_info": {
                            "session_id": raw_data.get('session_id', 'unknown'),
                            "generated_at": datetime.now().isoformat(),
                            "version": "2.0"
                        },
                        "executive_summary": TrainingOrchestrator._create_executive_summary(raw_data),
                        "business_scenario": TrainingOrchestrator._extract_business_scenario(raw_data),
                        "compliance_analysis": TrainingOrchestrator._extract_compliance_analysis(raw_data),
                        "actionable_recommendations": TrainingOrchestrator._extract_recommendations(raw_data),
                        "implementation_checklist": TrainingOrchestrator._create_implementation_checklist(raw_data),
                        "risk_assessment": TrainingOrchestrator._create_risk_assessment(raw_data),
                        "sources_and_references": TrainingOrchestrator._organize_sources(raw_data),
                        "raw_data": raw_data  # Keep original for detailed reports
                    }
                    
                    return toolkit_data
                    
        except Exception as e:
            logger.error(f"Error processing results: {e}")
            return {"error": "Failed to process training results", "raw_result": str(result)}
        
        return {"error": "No structured results available", "raw_result": str(result)}
    
    @staticmethod
    def _create_executive_summary(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary for business toolkit"""
        scenario = data.get('scenario', {})
        problems = data.get('problematic_analysis', {}).get('problematic_messages', [])
        corrections = data.get('best_practices', {}).get('corrected_messages', [])
        
        return {
            "company_focus": scenario.get('company_name', 'Example Company'),
            "industry": scenario.get('industry', 'Not specified'),
            "compliance_issues_found": len(problems),
            "solutions_provided": len(corrections),
            "risk_level": "High" if len(problems) > 3 else "Medium" if len(problems) > 1 else "Low",
            "implementation_priority": "Immediate action required" if len(problems) > 3 else "Review and implement",
            "estimated_implementation_time": "2-4 weeks" if len(problems) > 2 else "1-2 weeks"
        }
    
    @staticmethod
    def _extract_business_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business scenario in toolkit format"""
        scenario = data.get('scenario', {})
        return {
            "company_profile": {
                "name": scenario.get('company_name', ''),
                "industry": scenario.get('industry', ''),
                "size": scenario.get('company_size', ''),
                "location": scenario.get('location', ''),
                "target_market": scenario.get('target_audience', '')
            },
            "business_context": {
                "product_service": scenario.get('product_service', ''),
                "sustainability_goals": scenario.get('preliminary_claims', []),
                "market_position": scenario.get('marketing_objectives', []),
                "regulatory_environment": scenario.get('regulatory_context', '')
            }
        }
    
    @staticmethod
    def _extract_compliance_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract compliance analysis for business decision-making"""
        problems = data.get('problematic_analysis', {}).get('problematic_messages', [])
        corrections = data.get('best_practices', {}).get('corrected_messages', [])
        
        # Categorize issues by severity and regulatory risk
        high_risk_issues = []
        medium_risk_issues = []
        low_risk_issues = []
        
        for problem in problems:
            violations = problem.get('regulatory_violations', [])
            consequences = problem.get('potential_consequences', [])
            
            risk_score = len(violations) + len(consequences)
            
            issue_summary = {
                "message": problem.get('message', ''),
                "primary_violation": violations[0] if violations else 'Compliance concern',
                "business_impact": consequences[0] if consequences else 'Reputational risk',
                "recommended_action": "Immediate revision required"
            }
            
            if risk_score >= 4:
                high_risk_issues.append(issue_summary)
            elif risk_score >= 2:
                medium_risk_issues.append(issue_summary)
            else:
                low_risk_issues.append(issue_summary)
        
        return {
            "overall_compliance_score": max(0, 100 - (len(high_risk_issues) * 25 + len(medium_risk_issues) * 10)),
            "critical_issues": high_risk_issues,
            "moderate_issues": medium_risk_issues,
            "minor_issues": low_risk_issues,
            "regulatory_frameworks_analyzed": data.get('problematic_analysis', {}).get('regulatory_landscape', ''),
            "compliance_recommendations": [
                "Implement pre-publication compliance review process",
                "Train marketing team on current regulations",
                "Establish legal approval workflow for sustainability claims",
                "Regular compliance audits of marketing materials"
            ]
        }
    
    @staticmethod
    def _extract_recommendations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract actionable recommendations for business implementation"""
        corrections = data.get('best_practices', {}).get('corrected_messages', [])
        feedback = data.get('personalized_feedback', {})
        
        recommendations = []
        
        # Message-specific recommendations
        for correction in corrections:
            rec = {
                "category": "Message Improvement",
                "priority": "High",
                "action": "Replace problematic messaging",
                "original_issue": correction.get('original_message_id', ''),
                "recommended_solution": correction.get('corrected_message', ''),
                "business_rationale": correction.get('effectiveness_rationale', ''),
                "implementation_steps": correction.get('changes_made', []),
                "timeline": "Immediate",
                "responsible_team": "Marketing & Legal"
            }
            recommendations.append(rec)
        
        # Process-specific recommendations
        process_recs = [
            {
                "category": "Process Improvement",
                "priority": "High",
                "action": "Establish compliance review process",
                "description": "Create formal review process for all sustainability communications",
                "implementation_steps": [
                    "Draft compliance review checklist",
                    "Assign legal team review responsibilities", 
                    "Create approval workflow in marketing tools",
                    "Train team on new process"
                ],
                "timeline": "2-3 weeks",
                "responsible_team": "Marketing Operations & Legal"
            },
            {
                "category": "Team Training",
                "priority": "Medium",
                "action": "Conduct team compliance training",
                "description": "Educate marketing team on sustainability messaging best practices",
                "implementation_steps": feedback.get('team_training_recommendations', []),
                "timeline": "1 month",
                "responsible_team": "HR & Marketing Leadership"
            }
        ]
        
        recommendations.extend(process_recs)
        return recommendations
    
    @staticmethod
    def _create_implementation_checklist(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create actionable implementation checklist"""
        return [
            {
                "task": "Review and replace flagged messaging",
                "priority": "Critical",
                "timeline": "This week",
                "owner": "Marketing Team",
                "status": "pending",
                "dependencies": []
            },
            {
                "task": "Legal review of revised messages",
                "priority": "Critical", 
                "timeline": "This week",
                "owner": "Legal Team",
                "status": "pending",
                "dependencies": ["Review and replace flagged messaging"]
            },
            {
                "task": "Implement compliance review process",
                "priority": "High",
                "timeline": "2 weeks",
                "owner": "Marketing Operations",
                "status": "pending",
                "dependencies": []
            },
            {
                "task": "Train team on compliance requirements",
                "priority": "High",
                "timeline": "3 weeks",
                "owner": "Marketing Leadership",
                "status": "pending",
                "dependencies": ["Implement compliance review process"]
            },
            {
                "task": "Audit existing marketing materials",
                "priority": "Medium",
                "timeline": "1 month",
                "owner": "Marketing Team",
                "status": "pending",
                "dependencies": ["Train team on compliance requirements"]
            },
            {
                "task": "Establish ongoing monitoring process",
                "priority": "Medium",
                "timeline": "6 weeks",
                "owner": "Marketing Operations",
                "status": "pending",
                "dependencies": ["Audit existing marketing materials"]
            }
        ]
    
    @staticmethod
    def _create_risk_assessment(data: Dict[str, Any]) -> Dict[str, Any]:
        """Create business risk assessment"""
        problems = data.get('problematic_analysis', {}).get('problematic_messages', [])
        
        # Calculate risk metrics
        regulatory_risks = []
        reputational_risks = []
        financial_risks = []
        
        for problem in problems:
            violations = problem.get('regulatory_violations', [])
            consequences = problem.get('potential_consequences', [])
            
            for violation in violations:
                if any(keyword in violation.lower() for keyword in ['fine', 'penalty', 'enforcement']):
                    financial_risks.append(violation)
                else:
                    regulatory_risks.append(violation)
            
            for consequence in consequences:
                if any(keyword in consequence.lower() for keyword in ['reputation', 'brand', 'trust']):
                    reputational_risks.append(consequence)
                elif any(keyword in consequence.lower() for keyword in ['fine', 'lawsuit', 'penalty']):
                    financial_risks.append(consequence)
        
        # Calculate overall risk score
        total_risks = len(regulatory_risks) + len(reputational_risks) + len(financial_risks)
        risk_level = "High" if total_risks > 6 else "Medium" if total_risks > 3 else "Low"
        
        return {
            "overall_risk_level": risk_level,
            "risk_score": min(100, total_risks * 10),
            "regulatory_compliance_risks": regulatory_risks[:5],  # Top 5
            "reputational_risks": reputational_risks[:5],
            "financial_risks": financial_risks[:5],
            "mitigation_priority": "Immediate" if risk_level == "High" else "Within 30 days",
            "recommended_next_steps": [
                "Immediate legal review of flagged content",
                "Pause distribution of problematic messaging",
                "Implement enhanced compliance processes",
                "Consider external compliance audit"
            ] if risk_level == "High" else [
                "Schedule legal review within 1 week",
                "Revise flagged messaging",
                "Enhance review processes",
                "Monitor industry compliance trends"
            ]
        }
    
    @staticmethod
    def _organize_sources(data: Dict[str, Any]) -> Dict[str, Any]:
        """Organize sources for business reference"""
        sources = data.get('sources_used', [])
        
        organized = {
            "regulatory_sources": [],
            "industry_examples": [],
            "best_practice_guides": [],
            "news_and_updates": [],
            "total_sources": len(sources)
        }
        
        for source in sources:
            source_type = source.get('type', 'other')
            source_info = {
                "title": source.get('title', ''),
                "url": source.get('url', ''),
                "description": source.get('description', ''),
                "access_date": source.get('access_date', ''),
                "relevance": "High"  # Could be calculated based on usage
            }
            
            if source_type == 'regulatory':
                organized["regulatory_sources"].append(source_info)
            elif source_type in ['company_example', 'case_study']:
                organized["industry_examples"].append(source_info)
            elif source_type == 'best_practice':
                organized["best_practice_guides"].append(source_info)
            elif source_type == 'news':
                organized["news_and_updates"].append(source_info)
        
        return organized

# ===== API ENDPOINTS ===== #

@app.get("/")
async def root():
    """API health check"""
    return {
        "service": "Sustainability Training API Toolkit",
        "version": "2.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test CrewAI import
        from sustainability.crew import Sustainability
        crewai_status = "available"
    except Exception as e:
        crewai_status = f"error: {str(e)}"
    
    # Check API keys
    api_keys = {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "serper": bool(os.getenv("SERPER_API_KEY"))
    }
    
    return {
        "status": "healthy",
        "crewai": crewai_status,
        "api_keys": api_keys,
        "active_sessions": len(session_manager.sessions),
        "websocket_connections": sum(len(conns) for conns in session_manager.websocket_connections.values())
    }

@app.post("/training/start", response_model=TrainingSession)
async def start_training(request: TrainingRequest, background_tasks: BackgroundTasks):
    """Start new training session"""
    
    # Validate inputs
    if not request.industry or not request.regulations:
        raise HTTPException(status_code=400, detail="Industry and regulations are required")
    
    # Create session
    session = session_manager.create_session(request)
    
    # Start training in background
    background_tasks.add_task(
        TrainingOrchestrator.run_training_session,
        session.session_id,
        request
    )
    
    return session

@app.get("/training/{session_id}", response_model=TrainingSession)
async def get_training_status(session_id: str):
    """Get training session status"""
    
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@app.get("/training/{session_id}/results")
async def get_training_results(session_id: str):
    """Get training session results"""
    
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != "completed":
        raise HTTPException(status_code=400, detail="Training not completed")
    
    return session.results

@app.post("/reports/generate")
async def generate_report(request: ReportRequest):
    """Generate report in specified format"""
    
    session = session_manager.get_session(request.session_id)
    if not session or not session.results:
        raise HTTPException(status_code=404, detail="Session or results not found")
    
    if request.format == "markdown":
        report_content = ReportGenerator.generate_business_markdown(session.results, request)
        return {"content": report_content, "filename": f"sustainability_report_{request.session_id}.md"}
    
    elif request.format == "json":
        return {"content": session.results, "filename": f"sustainability_data_{request.session_id}.json"}
    
    elif request.format == "executive":
        executive_report = ReportGenerator.generate_executive_summary(session.results)
        return {"content": executive_report, "filename": f"executive_summary_{request.session_id}.md"}
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates"""
    
    await websocket.accept()
    session_manager.add_websocket(session_id, websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "session_id": session_id,
            "agent_name": "System", 
            "message": "Connected to real-time updates",
            "message_type": "info",
            "timestamp": datetime.now().isoformat()
        }))
        
        # Keep connection alive
        while True:
            # Receive any messages from client (ping/pong, etc.)
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.ping()
            
    except Exception as e:
        logger.info(f"WebSocket disconnected for session {session_id}: {e}")
    finally:
        session_manager.remove_websocket(session_id, websocket)

@app.get("/sessions")
async def list_sessions():
    """List all training sessions"""
    return [
        {
            "session_id": session.session_id,
            "status": session.status,
            "created_at": session.created_at.isoformat(),
            "progress": session.progress
        }
        for session in session_manager.sessions.values()
    ]

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete training session"""
    if session_id in session_manager.sessions:
        del session_manager.sessions[session_id]
        return {"message": "Session deleted"}
    raise HTTPException(status_code=404, detail="Session not found")

# ===== REPORT GENERATION ===== #

class ReportGenerator:
    """Generate business-focused reports for the toolkit"""
    
    @staticmethod
    def generate_business_markdown(results: Dict[str, Any], request: ReportRequest) -> str:
        """Generate business-focused markdown report"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_info = results.get('session_info', {})
        executive_summary = results.get('executive_summary', {})
        scenario = results.get('business_scenario', {})
        compliance = results.get('compliance_analysis', {})
        recommendations = results.get('actionable_recommendations', [])
        checklist = results.get('implementation_checklist', [])
        risk_assessment = results.get('risk_assessment', {})
        
        markdown = f"""# Sustainability Compliance Analysis Report

**Generated:** {timestamp}  
**Session ID:** {session_info.get('session_id', 'N/A')}  
**Analysis Version:** {session_info.get('version', '2.0')}

## Executive Summary

**Company:** {executive_summary.get('company_focus', 'N/A')}  
**Industry:** {executive_summary.get('industry', 'N/A')}  
**Risk Level:** {executive_summary.get('risk_level', 'Medium')}  
**Implementation Priority:** {executive_summary.get('implementation_priority', 'Review required')}  

**Key Findings:**
- {executive_summary.get('compliance_issues_found', 0)} compliance issues identified
- {executive_summary.get('solutions_provided', 0)} solutions provided
- Estimated implementation time: {executive_summary.get('estimated_implementation_time', '2-4 weeks')}

## Business Context

### Company Profile
- **Industry:** {scenario.get('company_profile', {}).get('industry', 'N/A')}
- **Size:** {scenario.get('company_profile', {}).get('size', 'N/A')}
- **Target Market:** {scenario.get('company_profile', {}).get('target_market', 'N/A')}

### Product/Service
{scenario.get('business_context', {}).get('product_service', 'No description available')}

## Compliance Analysis

**Overall Compliance Score:** {compliance.get('overall_compliance_score', 0)}/100

### Critical Issues Requiring Immediate Action
"""
        
        # Add critical issues
        for issue in compliance.get('critical_issues', []):
            markdown += f"""
#### {issue.get('primary_violation', 'Compliance Issue')}
- **Problematic Message:** {issue.get('message', 'N/A')}
- **Business Impact:** {issue.get('business_impact', 'Risk to reputation')}
- **Action Required:** {issue.get('recommended_action', 'Immediate review')}
"""
        
        markdown += f"""
## Risk Assessment

**Overall Risk Level:** {risk_assessment.get('overall_risk_level', 'Medium')}  
**Risk Score:** {risk_assessment.get('risk_score', 0)}/100  
**Mitigation Timeline:** {risk_assessment.get('mitigation_priority', 'Within 30 days')}

### Primary Risk Categories
- **Regulatory Risks:** {len(risk_assessment.get('regulatory_compliance_risks', []))} identified
- **Reputational Risks:** {len(risk_assessment.get('reputational_risks', []))} identified  
- **Financial Risks:** {len(risk_assessment.get('financial_risks', []))} identified

## Implementation Roadmap

### Immediate Actions (This Week)
"""
        
        # Add immediate actions from checklist
        immediate_tasks = [task for task in checklist if task.get('priority') == 'Critical']
        for task in immediate_tasks:
            markdown += f"- [ ] {task.get('task', '')} (Owner: {task.get('owner', 'TBD')})\n"
        
        markdown += """
### Short-term Actions (2-4 Weeks)
"""
        
        short_term_tasks = [task for task in checklist if task.get('priority') == 'High']
        for task in short_term_tasks:
            markdown += f"- [ ] {task.get('task', '')} (Owner: {task.get('owner', 'TBD')})\n"
        
        markdown += """
### Medium-term Actions (1-2 Months)
"""
        
        medium_term_tasks = [task for task in checklist if task.get('priority') == 'Medium']
        for task in medium_term_tasks:
            markdown += f"- [ ] {task.get('task', '')} (Owner: {task.get('owner', 'TBD')})\n"
        
        markdown += """
## Detailed Recommendations

### Process Improvements
"""
        
        # Add process recommendations
        process_recs = [rec for rec in recommendations if rec.get('category') == 'Process Improvement']
        for rec in process_recs:
            markdown += f"""
#### {rec.get('action', '')}
**Priority:** {rec.get('priority', 'Medium')}  
**Timeline:** {rec.get('timeline', 'TBD')}  
**Responsible Team:** {rec.get('responsible_team', 'TBD')}

{rec.get('description', '')}

**Implementation Steps:**
"""
            for step in rec.get('implementation_steps', []):
                markdown += f"- {step}\n"
        
        # Add sources if requested
        if request.include_sources:
            sources = results.get('sources_and_references', {})
            markdown += f"""
## Sources and References

**Total Sources:** {sources.get('total_sources', 0)}

### Regulatory Sources
"""
            for source in sources.get('regulatory_sources', [])[:5]:
                markdown += f"- [{source.get('title', 'Untitled')}]({source.get('url', '#')})\n"
            
            markdown += """
### Industry Examples
"""
            for source in sources.get('industry_examples', [])[:5]:
                markdown += f"- [{source.get('title', 'Untitled')}]({source.get('url', '#')})\n"
        
        markdown += f"""
---

*This report was generated by the Sustainability Training AI Toolkit v2.0*  
*Report ID: {session_info.get('session_id', 'N/A')} | Generated: {timestamp}*
"""
        
        return markdown
    
    @staticmethod
    def generate_executive_summary(results: Dict[str, Any]) -> str:
        """Generate executive summary for leadership"""
        
        executive_summary = results.get('executive_summary', {})
        risk_assessment = results.get('risk_assessment', {})
        compliance = results.get('compliance_analysis', {})
        
        return f"""# Executive Summary - Sustainability Compliance Analysis

## Key Findings

**Company:** {executive_summary.get('company_focus', 'N/A')}  
**Overall Risk Level:** {risk_assessment.get('overall_risk_level', 'Medium')}  
**Compliance Score:** {compliance.get('overall_compliance_score', 0)}/100

## Business Impact

- **Compliance Issues:** {executive_summary.get('compliance_issues_found', 0)} issues requiring attention
- **Implementation Time:** {executive_summary.get('estimated_implementation_time', '2-4 weeks')}
- **Risk Mitigation:** {risk_assessment.get('mitigation_priority', 'Within 30 days')}

## Recommended Actions

{', '.join(risk_assessment.get('recommended_next_steps', [])[:3])}

## Investment Required

- **Time:** {executive_summary.get('estimated_implementation_time', '2-4 weeks')} for full implementation
- **Resources:** Marketing, Legal, and Operations team coordination
- **Priority:** {executive_summary.get('implementation_priority', 'Review and implement')}

**Bottom Line:** Immediate action required to ensure regulatory compliance and protect brand reputation.
"""

# ===== APPLICATION FACTORY ===== #

def create_sustainability_toolkit():
    """Factory function to create the API toolkit"""
    return app

# For direct deployment
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "panel_bridge:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Set to True for development
        log_level="info"
    )