"""
callbacks.py — Real-time progress and message handling for Sustainability Business Toolkit
Updated for Phase 1 & 2:
- Removed all traces of "assessment" workflow and language
- Uses business-focused phrasing and logic only
"""

import logging

logger = logging.getLogger(__name__)


def handle_agent_progress(agent_name: str, msg_count: int):
    """
    Called whenever an agent sends a progress update.
    Transforms raw agent_name + msg_count into a human-readable status message.
    """
    agent_name_lower = agent_name.lower()

    # Business toolkit core agent
    if "toolkit" in agent_name_lower:
        progress_message = (
            f"📊 Business toolkit analysis in progress — {msg_count} insights gathered so far"
        )

    # Compliance review agent
    elif "compliance" in agent_name_lower:
        progress_message = (
            f"⚖️ Compliance analysis in progress — {msg_count} regulatory items reviewed"
        )

    # Strategy development agent
    elif "strategy" in agent_name_lower:
        progress_message = (
            f"🚀 Strategy development underway — {msg_count} strategic options formulated"
        )

    # Report generator agent
    elif "report" in agent_name_lower:
        progress_message = (
            f"📝 Compiling executive report — {msg_count} sections completed"
        )

    else:
        progress_message = f"🔍 Processing data — {msg_count} updates so far"

    logger.debug(f"Progress update: {progress_message}")
    return progress_message


def handle_agent_completion(agent_name: str, output_data: dict):
    """
    Called when an agent finishes its task.
    Generates a short business-focused completion summary for UI/log consumption.
    """
    agent_name_lower = agent_name.lower()

    if "toolkit" in agent_name_lower:
        output_summary = (
            f"📊 Business analysis completed — {len(output_data or {})} key findings identified"
        )

    elif "compliance" in agent_name_lower:
        output_summary = (
            f"⚖️ Compliance analysis completed — {len(output_data or {})} regulatory areas processed"
        )

    elif "strategy" in agent_name_lower:
        output_summary = (
            f"🚀 Strategy development completed — {len(output_data or {})} initiatives proposed"
        )

    elif "report" in agent_name_lower:
        output_summary = (
            f"📝 Executive report compiled — {len(output_data or {})} outputs generated"
        )

    else:
        output_summary = f"✅ Task completed — {len(output_data or {})} result items processed"

    logger.debug(f"Completion: {output_summary}")
    return output_summary


def handle_error(agent_name: str, error_message: str):
    """
    Called when an error occurs during agent execution.
    """
    logger.error(f"❌ Error in agent {agent_name}: {error_message}")
    return f"❌ Error in {agent_name}: {error_message}"
