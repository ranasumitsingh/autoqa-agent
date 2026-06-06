from typing import TypedDict, List


class AgentState(TypedDict):

    log_text: str

    failures: List[dict]

    results: List[dict]