from pydantic import BaseModel
from typing import List


class Failure(BaseModel):
    test_name: str
    error: str


class FailureList(BaseModel):
    failures: List[Failure]


class RootCauseResult(BaseModel):
    root_cause: str
    evidence: str


class ClassificationResult(BaseModel):
    category: str
    severity: str


class EvaluationResult(BaseModel):
    confidence: float
    reasoning: str


class FailureAnalysis(BaseModel):
    test_name: str
    category: str
    root_cause: str
    confidence: float


class InvestigationReport(BaseModel):
    failures: List[FailureAnalysis]