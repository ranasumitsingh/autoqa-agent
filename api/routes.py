def confidence_router(state):

    if state["confidence"] >= 0.80:
        return "bug_report"

    return "human_review"