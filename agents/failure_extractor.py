import logging

from agents.llm import llm
from models.schemas import FailureList
from models.state import AgentState
from utils.prompt_loader import load_prompt

logger = logging.getLogger(__name__)

FAILURE_EXTRACTION_PROMPT = load_prompt(
    "failure_extraction.txt"
)


def failure_extractor_agent(
    state: AgentState
):

    try:

        logger.info(
            "Extracting failed test cases"
        )

        prompt = FAILURE_EXTRACTION_PROMPT.format(
            log_text=state["log_text"]
        )

        structured_llm = llm.with_structured_output(
            FailureList
        )

        result = structured_llm.invoke(
            prompt
        )

        logger.info(
            f"Found {len(result.failures)} failures"
        )

        return {
            "failures": [
                failure.model_dump()
                for failure in result.failures
            ]
        }

    except Exception:

        logger.exception(
            "Failure extraction failed"
        )

        return {
            "failures": []
        }