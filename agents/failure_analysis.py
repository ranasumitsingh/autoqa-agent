import logging

from agents.investigator import investigate_failure

logger = logging.getLogger(__name__)


def failure_analysis_agent(state):

    analyses = []

    for failure in state.get("failures", []):

        try:

            result = investigate_failure(
                failure
            )

            analyses.append(result)

        except Exception as e:

            logger.exception(
                f"Investigation failed for "
                f"{failure.get('test_name')}"
            )

    return {
        "results": analyses
    }