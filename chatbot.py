import os
import json
import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

# Load enviroment
load_dotenv()

# check if there is a key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Please put your API key in .env")

class InterviewBot:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        
        # Load the questions into memory immediately
        self.questions = self.load_questions()
        self.current_question = None

    def load_questions(self):
        try:
            with open('interview_data.json', 'r') as f: 
                return json.load(f)
        except FileNotFoundError:
            print('Error: interview_data.json not found')
            return[]
        
    def select_question(self):
        if self.questions:
            # Randonly pick a questions from our dataset
            q_data = random.choice(self.questions)
            self.current_question = q_data
            return f"Let's practice. {q_data['question']}"
        return "I couldn't find any questions loaded."
    
    def get_feedback(self, user_answer):
        """Generates feedback based on the user's answer and the specific question tip."""
        
        # 1. The Persona (System Prompt)
        system_template = """
        You are a supportive but strict Job Interview Coach.
        
        Context:
        The user was asked: "{question}"
        The known tip for this question is: "{tip}"
        
        Your Task:
        1. Analyze the user's answer below.
        2. Check if they used the STAR method (Situation, Task, Action, Result).
        3. Provide 2 sentences of constructive feedback.
        """
        
        # 2. Combining the Persona with User Input
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("user", "{answer}")
        ])

        # 3. The Chain: Prompt -> Model -> Text Cleaner
        chain = prompt | self.model | StrOutputParser()

        # 4. Execution: Sending the data to OpenAI
        response = chain.invoke({
            "question": self.current_question['question'],
            "tip": self.current_question['tip'],
            "answer": user_answer
        })
        
        return response
    
    # Main class
def main():
    bot = InterviewBot()
    print("Hello, this is your friendly AI Interview Coach.")
    print("Type 'q' to exit")
    print("------------------------------------------------")

    # Bot will ask the first question
    first_q = bot.select_question()    
    print(f"Your first question: {first_q}")

    while True:
        user_input = input("You: ")

        # See if they want to exit or not
        if user_input.lower() == 'q':
            print("Good luck with your interviews!")
            break

        feedback = bot.get_feedback(user_input)
        print(f"Here are some feedbacks: {feedback}")

        # ask the next question
        next_q = bot.select_question()
        print("Do you want to practice another question? (yes or no answer only)")
        if user_input.lower() == 'yes':
            print(f"Your next question is: {next_q}")
        else:
            print("Good luck with your interviews!")
            break
    
if __name__ == "__main__":
    main()