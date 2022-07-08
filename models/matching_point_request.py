from pydantic import BaseModel


class MatchingPointRequest(BaseModel):
    applicationId: str = ""
    requirementKeyWords: list = []
    descriptionKeyWords: list = []
    jobSkills: list = []
    otherRequireKeywords: list = []

    attendantSkills: list = []
    attendantEducationKeyWords: list = []
    attendantWorkHistoryKeyWords: list = []
    attendantCertificationKeyWords: list = []
    attendantActivityKeyWords: list = []
