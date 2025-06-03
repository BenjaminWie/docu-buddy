#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import DocubuddyAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with code text and compliance info inputs.
    """
    # Replace these example inputs with your actual code and compliance data
    inputs = {
        'code_text': """
        # Paste your source code here as a string
        def example_function(x):
            return x * 2
        """
        }
    
    try:
        #DocubuddyAi().crew().kickoff(inputs=inputs)
        docubuddy = DocubuddyAi()
        code_explainer = docubuddy.developer_explainer()
        code_explainer_task = docubuddy.explain_code_developer_task()
        code_explainer_task.agent = code_explainer
        result = code_explainer_task.run(inputs=inputs)
        
        print("Crew execution completed successfully.")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'code_text': '',  # You may want to customize or parameterize this
        'compliance_info': '',
        'topic': 'AI LLMs'
        }
    try:
        DocubuddyAi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DocubuddyAi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'code_text': '',  # Add appropriate test code text here
        'compliance_info': '',
        'topic': 'AI LLMs'
    }
    
    try:
        DocubuddyAi().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

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
