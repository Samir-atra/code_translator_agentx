from pydantic import BaseModel
from typing import Literal

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)


class TranslatorScore(BaseModel):
    execution_correctness: float
    style_and_comments: float
    conciseness: float
    logic_and_structure: float
    total_score: float

class TranslatorEval(BaseModel):
    researcher_translator: TranslatorScore
    developer_translator: TranslatorScore
    winner: Literal["researcher_translator", "developer_translator"]
    reason: str

def translator_judge_agent_card(agent_name: str, card_url: str) -> AgentCard:
    skill = AgentSkill(
        id='moderate_and_judge_translations',
        name='Orchestrates and judges programming languages translations',
        description='Orchestrate and judge a translations between two agents on a given topic.',
        tags=['translation'],
#         examples=["""
# {
#   "participants": {
#     "creative_pitcher": "https://creative-pitcher.example.com:443",
#     "factual_pitcher": "https://factual-pitcher.example.org:8443"
#   },
#   "config": {
#     "topic": "Should artificial intelligence be regulated?",
#     "num_rounds": 3
#   }
# }
# """]
    )
    agent_card = AgentCard(
        name=agent_name,
        description='Orchestrate and judge a structured programming languages translation and choose between two translators.',
        url=card_url,
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )
    return agent_card
