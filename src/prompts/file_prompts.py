user = 'Wasif'

# Goal, Return Format, Warnings, Content Dump
perfect_prompt = "I want a list of the best medium-length hikes within two hours of San Francisco." \
        "Each hike should provide a cool and unique adventure, and be lesser known." \
        "For each hike, return the name of the hike as I'd find it on AllTrails, then provide the starting address of the hike, the ending address of the hike, distance, drive time, hike duration, and what makes it a cool and unique adventure." \
        "Return the top 3." \
        "Be careful to make sure that the name of trail is correct, that it actually exists, and that the time is correct." \
        "For context: my girlfriend and I hike a ton! We've done pretty much all of the local SF hikes, whether that's Presidio or Golden Gate Park. We definitely want to get out of town -- we did Mount Tam pretty recently, the whole thing from the beginning of the stairs to Stinson -- it was really long and we are definitely in the mood for something different this weekend! Ocean views would still be nice. We love delicious food. One thing I loved about the Mt Tam hike is that it ends with a celebration (Arriving in town to breakfast!) The old missile silos and stuff near Discovery Point is cool but I've just done that hike probably 20x at this point. We won't be seeing each other for a few weeks (she has to stay in LA for work) so the uniqueness here really counts. "

check_duplicate = "You are to determine if a given file name is similar " \
        "to any file name in a list of files. The user input will " \
        "contain a file name followed by a list of file names in " \
        "enclosed in brackets separated by commas. Output True if " \
        "the file name is similar to a file name in the list and " \
        "False otherwise. " \
        "For example: " \
        "input: 'Resume (cover letter, timeline, paper)' and " \
        "output: False. Another example: " \
        "input: 'Cover Letter (resume, edu-cover letter, research)' " \
        "and " \
        "output: True. Another example: " \
        "input: 'Timeline (timeline-long, resume, cover letter)' and " \
        "output: True."

valid_data = "You are a personal document classifier. You will " \
        "be provided the name of the file followed by some contents " \
        "of the file and you need to determine " \
        "if the contents of a file contains valuable information or " \
        "if it is code/AI generated/junk. This can be anything from " \
        "a diary, resume, transcript, exercise info, nutritional " \
        "information, among other things one would consider valuable " \
        "information. Documents containing dates/times are " \
        "considered valuable. " \
        "Provide your response with just one word 'True' or 'False' " \
        "where True means the file contains personal information " \
        "and False otherwise. If you are unsure, assume False." \
        "For example: " \
        "input: 'Resume:\nWasif Khan Resume 5 years experience' and " \
        "output: True. Another example: " \
        "input: 'research-12-paper:\nThis paper discusses the side " \
        "effects of model distillation.' and " \
        "output: False. Another example: " \
        "input: 'Timeline:\n1992-2001 School\n2000 Lost " \
        "virginity. 2003-2007 Worked.' and " \
        "output: True."

generate_facts = "You are a fact generator. " \
            "The user will provide long unstructured text " \
            f"documents. Assume the text is about {user}. " \
            "Generate facts about {user}, one fact per " \
            "line. Focus on providing facts that includes names of friends, " \
            "family, work companies, job titles, dynamics of relationships, " \
            "locations and times of events. Provide facts in third person " \
            "as opposed to first person. Ie. 'He is 32 years old', not " \
            f"'{user} is 32 years old.'. If the text contains no " \
            f"facts about {user}, output 'False'."


generate_datapoints = "You are a teacher. The user will provide long " \
            "unstructured text documents. Generate questions that could be " \
            "asked about the text the user provided alongside the " \
            "associated correct answer. Only include questions that test " \
            f"for personal information about {user}. Try to include " \
            f"dates, and names of other family and friends in {user}'s " \
            "life as part of the questions and answers where possible. " \
            "The " \
            "questions should be easy and phrased in first-tense such as " \
            "'How old am I?' not 'How old is Wasif'. The answers should be " \
            "concise. Spend time to think about the answer. " \
            "Provide your response in the exact format: " \
            "'question: <question> answer: <answer>'. If " \
            "personal information cannot be found, respond with 'False'. " \
            f"For example: input: '{user} is 32 years old, attends " \
            "university and enjoys working out.' output: " \
            "'question: How old am I? " \
            "answer: 32 years old. question: Am I enrolled in school? " \
            "answer: yes. question: what activity do I enjoy? answer: " \
            "working out'"

input_msg = 'Aiza is a personal assistant cuztomized for '\
        f'providing personal information about me ({user}).'

