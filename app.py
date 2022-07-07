import concurrent
import time
from functools import wraps

import numpy as np
import spacy
from skillNer.cleaner import Cleaner
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher

# init params of skill extractor
nlp = spacy.load('en_core_web_sm')
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
cleaner = Cleaner(
    to_lowercase=True,
    include_cleaning_functions=["remove_punctuation", "remove_extra_space"]
)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def process_skill(skill_string):
    global skill_extractor
    # extract skills from job_description
    annotations = skill_extractor.annotate(skill_string)
    return annotations


def data_partitioning(text):
    global cleaner
    text = cleaner(text)
    chunks, chunk_size = len(text), len(text) // 10
    result = [text[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
    return result


def handler(event, context):
    try:
        result = process_skill(event['job_description'])
        print(result)
        body = []
        for skill in result['results']['full_matches']:
            item = dict()
            item['doc_node_value'] = skill['doc_node_value']
            item['score'] = skill['score']
            body.append(item)
        for ngram in result['results']['ngram_scored']:
            item = dict()
            item['doc_node_value'] = ngram['doc_node_value']
            if type(ngram['score']).__module__ == np.__name__:
                item['score'] = ngram['score'].item()
            else:
                item['score'] = ngram['score']
            body.append(item)
        print(body)
        return {
            'statusCode': 200,
            'body': body
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': e.__class__
        }


@timeit
def multiprocessing_main(text):
    result = data_partitioning(text)
    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(process_skill, item) for item in result]
    concurrent.futures.wait(futures)
    # print([future.result() for future in futures])


@timeit
def sequential_main(text):
    text = cleaner(text)
    result = process_skill(text)
    return result


def main():
    text = """
        You have a passion for paving the road for crypto-based gaming economies and have experience with the traditional F2P economies. You will use economics, behavioral psychology, and business intelligence methodologies to design an healthy play-to-earn game economy. The Economic Designer will be responsible to design and managing all systems that will encourage the player to invest in a game to enhance his experience.

Your main responsibilities will be to:

    Design, prototype, balance, and champion the economic systems to increase our main game KPIs – Retention, Engagement, Monetization, Virality, on game & platform level.
    Recommend rewards and monetization game features to create an economic system to fulfill player needs
    Contribute to game features/systems design that compels and re-engage players
    Collaborate with game designers on new game features to maximize short and long-term player engagement, and provide for monetization opportunities
    Manage the economy and pricing of virtual goods; balance free content vs. paid currency in the game economy
    Balance player experience and progression, both in skills, in-game progression, and content release pacing.
    Request detailed data analysis from the games we operate to validate design choices & drive the development of the upcoming feature/balancing
    Produce reports highlighting through data the problematics of the games & recommend next steps/adjustments/new features to further improve KPIs
    Knowledge of macro, microeconomics, pricing theory, and statistics, especially in the mobile gaming industry and/or live service-oriented products, with the ability to model problems into quantitative systems, formulate ratios and indexes specific to each game
    Keep up to date with market trends and do proactive analysis of economy tuning in relevant competitive products
    Ability to model and simulate planned changes, overall sinks, and sources while anticipating downstream effects with post-launch analysis to ensure expected outcomes are reached

Qualifications

    An avid gamer with a strong understanding of mobile games (online, multiplayer, social, F2P), while a solid knowledge about the endless possibilities of blockchain and NFT
    Extremely robust logical and analytical thinking with the ability to abstract and decompose complex systems and identify key relationships and levers that influence the outputs
    Detail-oriented and capable of providing specific solutions at each step of the process
    Advanced understanding of Excel, SQL, and/or Python
    Design by data approach
    Strong problem-solving skills
    Strong communication skills (oral and written)

Additional Information

Why it's great to work at Ubisoft Danang:

    An international, professional, collaborative, modern, and creative environment
    Attractive remuneration package
    Performance rewards
    Creative & endless fun projects
    Unlimited access to Ubisoft games on Uplay
    Flexible working time
    Premium healthcare insurance
    UBIVERSARY for your working milestones
    Team building, Lunar New year Celebration, Projects celebration
    Beers and treats every Friday (yay!)
    Staff clubs
    Free in-house entertainment facilities (PS5…), coffee, tea, and fresh fruits
    """
    sequential_main(text)


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
