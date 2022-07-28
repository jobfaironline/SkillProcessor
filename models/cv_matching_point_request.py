from pydantic import BaseModel


class CVMatchingPointRequest(BaseModel):
    jobPositionId: str = ""
    requirementKeyWords: list = []
    descriptionKeyWords: list = []
    jobSkills: list = []
    otherRequireKeywords: list = []

    attendantSkills: list = []
    attendantEducationKeyWords: list = []
    attendantWorkHistoryKeyWords: list = []
    attendantCertificationKeyWords: list = []
    attendantActivityKeyWords: list = []