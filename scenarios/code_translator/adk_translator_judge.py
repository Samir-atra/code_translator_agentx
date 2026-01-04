import argparse
import uvicorn
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agentbeats.tool_provider import ToolProvider
from translator_judge_common import TranslatorEval, translator_judge_agent_card


system_prompt = '''
you are an expert evaluation agent specialized in evaluating code and programming languages translation and 
how efficient it is to run without errors, and judging a successful translation requires the following
considerations:

    - it does not produce error when it runs.
    - it is styled and commented in the new language method.
    - it is consise and does not have extra non relevant code.
    - it is clear and relevant to the topic.

the format of the output translation is as follows, containing at least two points of them with requirement for the first one:

    1 - the translation: the translation of the code in the new language.
    2 - it keeps the same functionality of the original code.
    3 - it have the same structure and logic of the original code.

the translation needs to start eith a note about the current language and the new language.

in general the translation needs to be clear, clean and error free.

    '''


def main():
    parser = argparse.ArgumentParser(description="Run the A2A programming languages translation judge.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=9009, help="Port to bind the server")
    parser.add_argument("--card-url", type=str, help="External URL to provide in the agent card")
    args = parser.parse_args()

    tool_provider = ToolProvider()
    root_agent = Agent(
        name="translator_judge_adk",
        model="gemini-2.5-flash",
        description=(
            "assess the quality of the programming language translation given and which one is better meeting the criteria"
        ),
        instruction=system_prompt,
        tools=[FunctionTool(func=tool_provider.talk_to_agent)],
        output_schema=TranslatorEval,
        after_agent_callback=lambda callback_context: tool_provider.reset()
    )

    agent_card = translator_judge_agent_card("TranslatorJudgeADK", args.card_url or f"http://{args.host}:{args.port}/")
    a2a_app = to_a2a(root_agent, agent_card=agent_card)
    uvicorn.run(a2a_app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
