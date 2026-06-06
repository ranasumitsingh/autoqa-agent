import logging

from agents.llm import llm

from models.schemas import (
    RootCauseResult,
    ClassificationResult,
    EvaluationResult
)

from utils.prompt_loader import load_prompt


logger = logging.getLogger(__name__)


ROOT_CAUSE_PROMPT = load_prompt(
    "root_cause.txt"
)

CLASSIFICATION_PROMPT = load_prompt(
    "classification.txt"
)

EVALUATION_PROMPT = load_prompt(
    "evaluation.txt"
)


ROOT_CAUSE_LLM = llm.with_structured_output(
    RootCauseResult
)

CLASSIFICATION_LLM = llm.with_structured_output(
    ClassificationResult
)

EVALUATION_LLM = llm.with_structured_output(
    EvaluationResult
)


CONFIDENCE_THRESHOLD = 0.70


def investigate_failure(
    failure: dict
) -> dict:

    test_name = failure.get(
        "test_name",
        "unknown_test"
    )

    error = failure.get(
        "error",
        ""
    )

    logger.info(
        f"Starting investigation: {test_name}"
    )

    try:

        # --------------------------------
        # Root Cause Analysis
        # --------------------------------

        root_prompt = ROOT_CAUSE_PROMPT.format(
            error=error
        )

        root_result = ROOT_CAUSE_LLM.invoke(
            root_prompt
        )

        logger.info(
            f"Root cause identified for {test_name}"
        )

        # --------------------------------
        # Classification
        # --------------------------------

        classification_prompt = (
            CLASSIFICATION_PROMPT.format(
                error=error,
                root_cause=root_result.root_cause
            )
        )

        classification_result = (
            CLASSIFICATION_LLM.invoke(
                classification_prompt
            )
        )

        logger.info(
            f"Failure classified as "
            f"{classification_result.category}"
        )

        # --------------------------------
        # Confidence Evaluation
        # --------------------------------

        evaluation_prompt = (
            EVALUATION_PROMPT.format(
                error=error,
                root_cause=root_result.root_cause
            )
        )

        evaluation_result = (
            EVALUATION_LLM.invoke(
                evaluation_prompt
            )
        )

        needs_human_review = (
            evaluation_result.confidence
            < CONFIDENCE_THRESHOLD
        )

        logger.info(
            f"Confidence={evaluation_result.confidence}"
        )

        return {
            "test_name": test_name,
            "category": classification_result.category,
            "root_cause": root_result.root_cause,
            "confidence": evaluation_result.confidence,
            "reasoning": evaluation_result.reasoning,
            "needs_human_review": (
                needs_human_review
            )
        }

    except Exception as e:

        logger.exception(
            f"Investigation failed "
            f"for {test_name}"
        )

        return {
            "test_name": test_name,
            "category": "Unknown",
            "root_cause": "Investigation Failed",
            "confidence": 0.0,
            "reasoning": str(e),
            "needs_human_review": True
        }