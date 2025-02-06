"""
Chatbot System - Main Entry Point

This script initializes and runs the chatbot system, processing user queries 
and fetching responses from a fine-tuned model trained on user information.

Usage:
    Run the script from the command line with a mode argument:
    
        python main.py train
        python main.py test_train
        python main.py test_run
        python main.py run

Modes:
    - train:       Train the chatbot model.
    - test_train:  Run tests related to model training.
    - test_run:    Run tests for the chatbot runtime.
    - run:         Deploy the chatbot and handle queries in production.

Dependencies:
    - Python 3.x
    - Requests (for API calls)
    - googlemaps (for google maps data)
    - googleapiclient (for all other google data)

Installation:
    Install required dependencies using pip:

        pip install requests googlemaps googleapiclient

Author:
    Your Name <wasif.k1112@gmail.com>
"""


from aiza import Aiza
from argparse import ArgumentParser


def main(mode: str):
    """
    Main function to execute the chatbot system in different modes.
    Generates a configuration based on the mode provided.

    Args:
        mode (str): The mode in which the chatbot will run.

    Raises:
        ValueError: If an invalid mode is provided.
    """
    config = {'model': 'GPT'}
    if mode == "generate_data":
        config['sources'] = []
        aiza = Aiza(config)
        aiza.generate_data()
    elif mode == "learn_user":
        config['sources'] = ['google']
        aiza = Aiza(config)
        aiza.learn_user()
    elif mode == "run":
        config['sources'] = ['google drive']
        aiza = Aiza(config)
        aiza.run()
    else:
        raise ValueError(f"Invalid mode: {mode}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Run the chatbot system.")
    parser.add_argument(
        "mode",
        choices=["generate_data", "learn_user", "run"],
        help="Mode of operation: 'generate_data', 'learn_user', or 'run'."
    )
    args = parser.parse_args()
    main(args.mode)
