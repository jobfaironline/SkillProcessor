import json
import logging
import math

import spacy
from skillNer.cleaner import Cleaner
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher

from models import MatchingPointRequest
from utils import timeit

# init params of skill extractor
nlp = spacy.load('en_core_web_lg')
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
cleaner = Cleaner(
    to_lowercase=True,
    include_cleaning_functions=["remove_punctuation", "remove_extra_space"]
)

f = open('weights.json')
weights = json.load(f)

logger = logging.getLogger(__name__)


def logistic_sigmoid(x):
    return 1 / (1 + math.exp(-x))


def extract_keyword_service(text):
    text = cleaner(text)
    annotations = skill_extractor.annotate(text)
    return annotations


def get_max_similarity_score(word_vector, keyword_vectors):
    scores = [word_vector.similarity(keyword_vector) for keyword_vector in keyword_vectors]
    logger.info(scores)
    return max(scores)


def calculate_attendant_category_score(request: MatchingPointRequest, category_keyword_vectors):
    job_requirement_scores = [get_max_similarity_score(keyword, request.requirementKeyWords) for keyword in
                              category_keyword_vectors]
    job_description_scores = [get_max_similarity_score(keyword, request.descriptionKeyWords) for keyword in
                              category_keyword_vectors]
    job_skill_scores = [get_max_similarity_score(keyword, request.jobSkills) for keyword in category_keyword_vectors]
    job_other_scores = [get_max_similarity_score(keyword, request.otherRequireKeywords) for keyword in
                        category_keyword_vectors]
    requirement_score = 0
    description_score = 0
    skill_score = 0
    other_score = 0
    if len(job_requirement_scores) != 0:
        requirement_score = (sum(job_requirement_scores) / len(job_requirement_scores)) * weights['job_requirement']
    if len(job_description_scores) != 0:
        description_score = (sum(job_description_scores) / len(job_description_scores)) * weights['job_description']
    if len(job_skill_scores) != 0:
        skill_score = (sum(job_skill_scores) / len(job_skill_scores)) * weights['job_skill']
    if len(job_other_scores) != 0:
        other_score = (sum(job_other_scores) / len(job_other_scores)) * weights['job_other']
    score = sum([requirement_score, description_score, skill_score, other_score]) / sum(
        [weights['job_requirement'], weights['job_description'], weights['job_skill'], weights['job_other']])
    return score


def calculate_matching_point(request: MatchingPointRequest):
    request.requirementKeyWords = [nlp(word) for word in request.requirementKeyWords]
    request.descriptionKeyWords = [nlp(word) for word in request.descriptionKeyWords]
    request.jobSkills = [nlp(word) for word in request.jobSkills]
    request.otherRequireKeywords = [nlp(word) for word in request.otherRequireKeywords]

    request.attendantSkills = [nlp(word) for word in request.attendantSkills]
    request.attendantEducationKeyWords = [nlp(word) for word in request.attendantEducationKeyWords]
    request.attendantWorkHistoryKeyWords = [nlp(word) for word in request.attendantWorkHistoryKeyWords]
    request.attendantCertificationKeyWords = [nlp(word) for word in request.attendantCertificationKeyWords]
    request.attendantActivityKeyWords = [nlp(word) for word in request.attendantActivityKeyWords]

    attendant_skill_score = calculate_attendant_category_score(request, request.attendantSkills) * weights['attendant_skill']
    attendant_education_score = calculate_attendant_category_score(request, request.attendantEducationKeyWords) * weights['attendant_education']
    attendant_work_history_score = calculate_attendant_category_score(request, request.attendantWorkHistoryKeyWords) * weights['attendant_work_history']
    attendant_certification_score = calculate_attendant_category_score(request, request.attendantCertificationKeyWords) * weights['attendant_certification']
    attendant_activity_score = calculate_attendant_category_score(request, request.attendantActivityKeyWords) * weights['attendant_activity']

    logger.info(f"Application {request.applicationId} has attendant skill score: {attendant_skill_score} with weight: {weights['attendant_skill']}")
    logger.info(f"Application {request.applicationId} has attendant education score: {attendant_education_score} with weight: {weights['attendant_education']}")
    logger.info(f"Application {request.applicationId} has attendant work history score: {attendant_work_history_score} with weight: {weights['attendant_work_history']}")
    logger.info(f"Application {request.applicationId} has attendant certification score: {attendant_certification_score} with weight: {weights['attendant_certification']}")
    logger.info(f"Application {request.applicationId} has attendant activity score: {attendant_activity_score} with weight: {weights['attendant_activity']}")

    return sum([attendant_skill_score, attendant_education_score, attendant_work_history_score, attendant_certification_score, attendant_activity_score]) / \
           sum([weights['attendant_skill'], weights['attendant_education'], weights['attendant_work_history'], weights['attendant_certification'], weights['attendant_activity']])


@timeit
def similarity(a, b):
    doc1 = nlp(a)
    doc2 = nlp(b)
    return doc1.similarity(doc2)


if __name__ == "__main__":
    text1 = 'quality products'
    text2 = 'design'
    print(similarity(text1, text2))
