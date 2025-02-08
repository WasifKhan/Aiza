from data_loader.data_loader import DataLoader


class Aiza:
    """
    A chatbot system that interacts with users through
    learning their personal information.

    Attributes:
        chatbot: AI used for chat interactions
        sources: Sources used for learning
    """

    def __init__(self, config):
        """
        Initializes the Chatbot with API details.

        Args:
            config(dict): Dictionary containing configuration for various runs
        """
        self.user = config['user']
        self.sources = config['sources']
        if config['model'] == 'GPT':
            from models.gpt.gpt import GPT
            self.chatbot = GPT(self.user)

    def generate_data(self):
        """
        Generates the 'training_data.jsonl' file from all provided sources.
        Requires permissions from user.
        """
        data_loader = DataLoader(self.user, self.sources)
        data_loader.authenticate_sources()
        data_loader.process_sources()

    def learn_user(self):
        """
        Learns the user from data stored in the 'training_data.jsonl' file
        """
        learning_parameters = {'n_epochs': 5, 'batch_size': 4, 'LR_mult': 0.2}
        self.chatbot.learn_user(learning_parameters)

    def run(self):
        """
        Runs the AI for chat interactions.
        """
        self.chatbot.run()
