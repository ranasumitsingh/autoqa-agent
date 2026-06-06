from langgraph.graph import StateGraph
from langgraph.graph import END

from models.state import AgentState

from agents.failure_extractor import (
    failure_extractor_agent
)

from agents.failure_analysis import (
    failure_analysis_agent
)


builder = StateGraph(AgentState)

builder.add_node(
    "extract_failures",
    failure_extractor_agent
)

builder.add_node(
    "analyze_failures",
    failure_analysis_agent
)

builder.set_entry_point(
    "extract_failures"
)

builder.add_edge(
    "extract_failures",
    "analyze_failures"
)

builder.add_edge(
    "analyze_failures",
    END
)

graph = builder.compile()