# import numpy as np
# import spacy
# from skillNer.cleaner import Cleaner
# # load default skills data base
# from skillNer.general_params import SKILL_DB
# # import skill extractor
# from skillNer.skill_extractor_class import SkillExtractor
# from spacy.matcher import PhraseMatcher
#
# # init params of skill extractor
# nlp = spacy.load('en_core_web_md')
# # init skill extractor
# skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
# cleaner = Cleaner(
#     to_lowercase=True,
#     include_cleaning_functions=["remove_punctuation", "remove_extra_space"]
# )
#
#
# def process_skill(skill_string):
#     global skill_extractor
#     # extract skills from job_description
#     annotations = skill_extractor.annotate(skill_string)
#     return annotations
#
#
# def handler(event, context):
#     try:
#         result = process_skill(event['job_description'])
#         print(result)
#         body = []
#         for skill in result['results']['full_matches']:
#             item = dict()
#             item['doc_node_value'] = skill['doc_node_value']
#             item['score'] = skill['score']
#             body.append(item)
#         for ngram in result['results']['ngram_scored']:
#             item = dict()
#             item['doc_node_value'] = ngram['doc_node_value']
#             if type(ngram['score']).__module__ == np.__name__:
#                 item['score'] = ngram['score'].item()
#             else:
#                 item['score'] = ngram['score']
#             body.append(item)
#         print(body)
#         return {
#             'statusCode': 200,
#             'body': body
#         }
#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'body': e.__class__
#         }
