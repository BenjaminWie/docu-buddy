#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import CodeExplainBuddy

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with code text and user prompt inputs.
    """
    # Replace these example inputs with your actual code and prompts
    inputs = {
        'code_text': """
        # Paste your source code here as a string
        def multiply(x, y):
            return x * y

        class Calculator:
            def add(self, a, b):
                return a + b
        """,
        'user_prompt': """
        Explain the functionality and relevance of this code.
        """,
        'topic': 'Code Understanding',
        'current_year': str(datetime.now().year),
    }
    
    try:
        CodeExplainBuddy().crew().kickoff(inputs=inputs)
        print("Crew execution completed successfully.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'code_text': '',  # Customize or parameterize as needed
        'user_prompt': '',
        'topic': 'Code Understanding',
        'current_year': str(datetime.now().year),
    }
    try:
        CodeExplainBuddy().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CodeExplainBuddy().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        'code_text': '',  # Add appropriate test code text here
        'user_prompt': '',
        'topic': 'Code Understanding',
        'current_year': str(datetime.now().year),
    }
    
    try:
        CodeExplainBuddy().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    elif sys.argv[1] == "train":
        train()
    elif sys.argv[1] == "replay":
        replay()
    elif sys.argv[1] == "test":
        test()
    else:
        print("Unknown command. Use no args to run, or 'train', 'replay', or 'test'.")
