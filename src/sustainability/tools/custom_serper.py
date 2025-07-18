"""
Custom Serper Search Tool - Compatible with Web Deployment
This replaces crewai-tools SerperDevTool to avoid dependency conflicts
"""

from crewai.tools import BaseTool
from typing import Type, Any, Dict
from pydantic import BaseModel, Field
import os
import requests
import json

class SerperSearchInput(BaseModel):
    """Input schema for Serper search tool."""
    query: str = Field(..., description="Search query to execute")

class CustomSerperTool(BaseTool):
    """Custom Serper search tool that avoids crewai-tools dependency conflicts"""
    
    name: str = "SerperDevTool"
    description: str = (
        "A search tool that uses Serper API to search the web for information. "
        "Useful for finding current information, market trends, regulatory updates, "
        "company examples, and sustainability best practices."
    )
    args_schema: Type[BaseModel] = SerperSearchInput
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.getenv("SERPER_API_KEY")
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
            return self._format_results(data)
            
        except requests.exceptions.RequestException as e:
            return f"Search request failed: {str(e)}"
        except Exception as e:
            return f"Search error: {str(e)}"
    
    def _format_results(self, data: Dict[str, Any]) -> str:
        """Format search results into readable text"""
        
        results = []
        
        # Add organic results
        if "organic" in data:
            results.append("=== Search Results ===\n")
            
            for i, result in enumerate(data["organic"][:5], 1):  # Top 5 results
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
            return "No relevant search results found for this query."
        
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