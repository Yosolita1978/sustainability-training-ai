"""
Custom Serper Search Tool - Compatible with Web Deployment
This replaces crewai-tools SerperDevTool to avoid dependency conflicts
Enhanced with better source tracking for sustainability training reports
"""

from crewai.tools import BaseTool
from typing import Type, Any, Dict, Optional, List, Tuple
from pydantic import BaseModel, Field
import os
import requests
import json
from datetime import datetime

class SerperSearchInput(BaseModel):
    """Input schema for Serper search tool."""
    query: str = Field(..., description="Search query to execute")

class CustomSerperTool(BaseTool):
    """Custom Serper search tool that avoids crewai-tools dependency conflicts"""
    
    name: str = "SerperDevTool"
    description: str = (
        "A search tool that uses Serper API to search the web for information. "
        "Useful for finding current information, market trends, regulatory updates, "
        "company examples, and sustainability best practices. "
        "Returns both formatted results and source references for citation."
    )
    args_schema: Type[BaseModel] = SerperSearchInput
    
    # Properly declare api_key as a class field with default factory
    api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("SERPER_API_KEY"),
        description="Serper API key for authentication"
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check if API key is available and warn if not
        if not self.api_key:
            print("⚠️ Warning: SERPER_API_KEY not found in environment variables")
    
    def _run(self, query: str) -> str:
        """Execute search using Serper API"""
        
        if not self.api_key:
            return "Error: Serper API key not configured. Please set SERPER_API_KEY environment variable."
        
        try:
            # Serper API endpoint
            url = "https://google.serper.dev/search"
            
            # Request payload
            payload = {
                "q": query,
                "num": 10,  # Number of results
                "gl": "us",  # Geographic location
                "hl": "en"   # Language
            }
            
            # Headers
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Make the request
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            # Parse results
            data = response.json()
            formatted_results, sources = self._format_results_with_sources(data, query)
            
            # Return formatted results with embedded source information
            return self._combine_results_and_sources(formatted_results, sources, query)
            
        except requests.exceptions.RequestException as e:
            return f"Search request failed: {str(e)}"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _extract_sources_from_data(self, data: Dict[str, Any], query: str) -> List[Dict[str, str]]:
        """Extract clean source data from search results"""
        sources = []
        access_date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract from organic results
        if "organic" in data:
            for result in data["organic"][:8]:  # Top 8 results
                source = {
                    "title": result.get("title", "").strip(),
                    "url": result.get("link", "").strip(),
                    "description": result.get("snippet", "").strip()[:200],  # Limit description length
                    "type": "web_search",
                    "query": query,
                    "access_date": access_date
                }
                
                # Only add if we have both title and URL
                if source["title"] and source["url"]:
                    sources.append(source)
        
        # Extract from knowledge panel
        if "knowledgeGraph" in data:
            kg = data["knowledgeGraph"]
            if "title" in kg and "url" in kg:
                source = {
                    "title": kg["title"].strip(),
                    "url": kg["url"].strip(),
                    "description": kg.get("description", "").strip()[:200],
                    "type": "knowledge_panel",
                    "query": query,
                    "access_date": access_date
                }
                sources.append(source)
        
        # Extract from news results
        if "news" in data:
            for news in data["news"][:3]:  # Top 3 news
                source = {
                    "title": news.get("title", "").strip(),
                    "url": news.get("link", "").strip(),
                    "description": news.get("snippet", "").strip()[:200],
                    "type": "news",
                    "query": query,
                    "access_date": access_date,
                    "date": news.get("date", "")
                }
                
                # Only add if we have both title and URL
                if source["title"] and source["url"]:
                    sources.append(source)
        
        return sources
    
    def _format_results_with_sources(self, data: Dict[str, Any], query: str) -> Tuple[str, List[Dict[str, str]]]:
        """Format search results into readable text and extract sources"""
        
        results = []
        sources = self._extract_sources_from_data(data, query)
        
        # Add organic results
        if "organic" in data:
            results.append("=== Search Results ===\n")
            
            for i, result in enumerate(data["organic"][:5], 1):  # Top 5 results for display
                title = result.get("title", "No title")
                snippet = result.get("snippet", "No description")
                link = result.get("link", "No URL")
                
                results.append(f"{i}. **{title}**")
                results.append(f"   {snippet}")
                results.append(f"   Source: {link}\n")
        
        # Add knowledge panel if available
        if "knowledgeGraph" in data:
            kg = data["knowledgeGraph"]
            results.append("=== Knowledge Panel ===")
            
            if "title" in kg:
                results.append(f"**{kg['title']}**")
            
            if "description" in kg:
                results.append(f"{kg['description']}")
            
            if "attributes" in kg:
                for attr_name, attr_value in kg["attributes"].items():
                    results.append(f"{attr_name}: {attr_value}")
            
            results.append("")
        
        # Add news results if available
        if "news" in data:
            results.append("=== Recent News ===")
            
            for news in data["news"][:3]:  # Top 3 news items
                title = news.get("title", "No title")
                snippet = news.get("snippet", "No description")
                date = news.get("date", "No date")
                
                results.append(f"• **{title}** ({date})")
                results.append(f"  {snippet}\n")
        
        # Join all results
        formatted_results = "\n".join(results)
        
        if not formatted_results.strip():
            formatted_results = "No relevant search results found for this query."
        
        return formatted_results, sources
    
    def _combine_results_and_sources(self, formatted_results: str, sources: List[Dict[str, str]], query: str) -> str:
        """Combine formatted results with source information for agent consumption"""
        
        # Start with the formatted results
        combined_output = formatted_results
        
        # Add source information in a structured way that agents can easily parse
        if sources:
            combined_output += "\n\n=== SOURCES FOR CITATION ===\n"
            combined_output += f"Query: {query}\n"
            combined_output += f"Sources found: {len(sources)}\n\n"
            
            for i, source in enumerate(sources[:10], 1):  # Limit to top 10 sources
                combined_output += f"[{i}] {source['title']}\n"
                combined_output += f"    URL: {source['url']}\n"
                combined_output += f"    Type: {source['type']}\n"
                if source.get('date'):
                    combined_output += f"    Date: {source['date']}\n"
                combined_output += f"    Access Date: {source['access_date']}\n"
                if source['description']:
                    combined_output += f"    Description: {source['description']}\n"
                combined_output += "\n"
            
            # Add instruction for agents
            combined_output += "AGENT INSTRUCTION: When referencing information from this search, "
            combined_output += "please include the source URL and title in your research_sources field. "
            combined_output += "Use the format: [Title] - [URL] (accessed [Access Date])\n\n"
        
        return combined_output
    
    def _format_results(self, data: Dict[str, Any]) -> str:
        """Legacy method - kept for backward compatibility"""
        formatted_results, _ = self._format_results_with_sources(data, "legacy_query")
        return formatted_results
    
    async def _arun(self, query: str) -> str:
        """Async version of the search"""
        return self._run(query)


# Factory function to create the tool
def create_serper_tool():
    """Create a Serper search tool instance"""
    return CustomSerperTool()


# Backward compatibility alias
SerperDevTool = CustomSerperTool