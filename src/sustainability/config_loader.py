"""
config_loader.py — Configuration loader for YAML agent and task definitions
Loads agents.yaml and tasks.yaml from the config directory
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_config_path() -> Path:
    """Get the path to the config directory"""
    current_file = Path(__file__)
    config_dir = current_file.parent / "config"
    return config_dir


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file)
            return content or {}
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading {file_path}: {e}")
        raise


def load_agents_config() -> Dict[str, Any]:
    """
    Load the agents configuration from agents.yaml
    
    Returns:
        Dict containing agent configurations
    """
    config_dir = get_config_path()
    agents_file = config_dir / "agents.yaml"
    
    logger.debug(f"Loading agents config from: {agents_file}")
    
    if not agents_file.exists():
        logger.error(f"Agents configuration file not found: {agents_file}")
        raise FileNotFoundError(f"agents.yaml not found at {agents_file}")
    
    agents_config = load_yaml_file(agents_file)
    
    # Validate that we have the expected agents
    expected_agents = [
        'business_toolkit_agent',
        'compliance_analysis_agent', 
        'strategy_recommendation_agent',
        'report_generator_agent'
    ]
    
    missing_agents = [agent for agent in expected_agents if agent not in agents_config]
    if missing_agents:
        logger.warning(f"Missing expected agents in config: {missing_agents}")
    
    logger.info(f"Loaded {len(agents_config)} agent configurations")
    return agents_config


def load_tasks_config() -> Dict[str, Any]:
    """
    Load the tasks configuration from tasks.yaml
    
    Returns:
        Dict containing task configurations
    """
    config_dir = get_config_path()
    tasks_file = config_dir / "tasks.yaml"
    
    logger.debug(f"Loading tasks config from: {tasks_file}")
    
    if not tasks_file.exists():
        logger.error(f"Tasks configuration file not found: {tasks_file}")
        raise FileNotFoundError(f"tasks.yaml not found at {tasks_file}")
    
    tasks_config = load_yaml_file(tasks_file)
    
    # Validate that we have the expected tasks
    expected_tasks = [
        'business_analysis_task',
        'compliance_review_task',
        'strategy_development_task', 
        'report_compilation_task'
    ]
    
    missing_tasks = [task for task in expected_tasks if task not in tasks_config]
    if missing_tasks:
        logger.warning(f"Missing expected tasks in config: {missing_tasks}")
    
    logger.info(f"Loaded {len(tasks_config)} task configurations")
    return tasks_config


def validate_config_structure(agents_config: Dict[str, Any], tasks_config: Dict[str, Any]) -> bool:
    """
    Validate that the loaded configurations have the expected structure
    
    Args:
        agents_config: Loaded agents configuration
        tasks_config: Loaded tasks configuration
        
    Returns:
        True if valid, raises exception if invalid
    """
    # Check that each agent has required fields
    required_agent_fields = ['description', 'goals', 'tools', 'output_format', 'tone']
    
    for agent_name, agent_config in agents_config.items():
        for field in required_agent_fields:
            if field not in agent_config:
                logger.warning(f"Agent {agent_name} missing required field: {field}")
    
    # Check that each task has required fields  
    required_task_fields = ['description', 'agent', 'input', 'output', 'priority']
    
    for task_name, task_config in tasks_config.items():
        for field in required_task_fields:
            if field not in task_config:
                logger.warning(f"Task {task_name} missing required field: {field}")
        
        # Check that the agent referenced in the task exists
        agent_name = task_config.get('agent')
        if agent_name and agent_name not in agents_config:
            logger.error(f"Task {task_name} references unknown agent: {agent_name}")
            raise ValueError(f"Task {task_name} references unknown agent: {agent_name}")
    
    logger.info("Configuration structure validation completed")
    return True


def load_and_validate_configs() -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Load both configuration files and validate their structure
    
    Returns:
        Tuple of (agents_config, tasks_config)
    """
    agents_config = load_agents_config()
    tasks_config = load_tasks_config()
    
    validate_config_structure(agents_config, tasks_config)
    
    return agents_config, tasks_config


if __name__ == "__main__":
    # Test loading configurations
    logging.basicConfig(level=logging.DEBUG)
    
    try:
        agents, tasks = load_and_validate_configs()
        print(f"✅ Successfully loaded {len(agents)} agents and {len(tasks)} tasks")
        print(f"Agents: {list(agents.keys())}")
        print(f"Tasks: {list(tasks.keys())}")
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        raise