class Aiza:
    """
    A chatbot system that interacts with users through 
    learning their personal information.

    Attributes:
        ai: AI used for chat interactions
        sources: Sources used for learning
    """

    def __init__(self, config):
        """
        Initializes the Chatbot with API details.

        Args:
            config(dict): Dictionary containing configuration for various runs
        """
        if config['model'] == 'GPT':
            from models.gpt.gpt import GPT
            self.ai = GPT()
        self.sources = config['sources']

    def generate_data(self):
        """
        Generates the 'training_data.jsonl' file from all provided sources.
        Requires permissions from user.
        """
        self.ai.generate_data()

    def learn_user(self):
        """
        Learns the user from data stored in the 'training_data.jsonl' file
        """
        self.ai.learn_user()

    def run(self):
        """
        Runs the AI for chat interactions.
        """
        self.ai.run()
