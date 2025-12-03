import os
import json
import random
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load enviroment
load_dotenv()

# check if there is a key
if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    raise ValueError("CRITICAL: HUGGINGFACEHUB_API_TOKEN is missing from .env file")

class InterviewBot:
    def __init__(self):
        print("Connecting to Hugging Face Cloud... (This might take 5-10 seconds)")
        self.client = InferenceClient(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
        
        # We use a specific model that is great for chat
        self.model_id = "HuggingFaceH4/zephyr-7b-beta"
        # Load the questions into memory immediately
        self.questions = self.load_questions()
        self.current_question = None

    def load_questions(self):
        try:
            with open('interview_data.json', 'r') as f: 
                return json.load(f)
        except FileNotFoundError:
            print('Error: interview_data.json not found')
            return []
        
    def select_question(self):
        if self.questions:
            # Randonly pick a questions from our dataset
            q_data = random.choice(self.questions)
            self.current_question = q_data
            return f"Let's practice. {q_data['question']}"
        return "I couldn't find any questions loaded."
    
    def get_feedback(self, user_answer):
        """Generates feedback based on the user's answer and the specific question tip."""
        
        system_instruction = (
            "You are a Job Interview Coach. Your task is to EVALUATE the candidate's answer. "
            "RULES:\n"
            "1. Do NOT generate a sample answer.\n"
            "2. Do NOT pretend to be the candidate.\n"
            "3. If the answer is too short (like 'yes', 'no', or empty), strictly say: 'That is too short. Please provide a full sentence.'\n"
            "4. Provide 2 sentences of constructive feedback only."
        )

        messages = [
            {
                "role": "system", 
                "content": system_instruction
            },
            {
                "role": "user", 
                "content": (
                    f"INTERVIEW QUESTION: {self.current_question['question']}\n"
                    f"TIP: {self.current_question.get('tip')}\n"
                    f"CANDIDATE ANSWER: \"{user_answer}\"\n\n"
                    "Evaluate the answer above. Do not rewrite it."
                )
            }
        ]

        try:
            # 4. Call the API
            response = self.client.chat_completion(
                model=self.model_id,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract the text from the response object
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {e}"

# Main function
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
        
        if len(user_input) < 10:
            print("⚠️  That answer is too short for an interview question.")
            print("   Please type a full sentence explaining your experience.")
            continue
        
        print("\n... Analyzing (via Mistral) ...")
        feedback = bot.get_feedback(user_input)
        print(f"Here are some feedbacks: {feedback}")

        # ask the next question
        print("Do you want to practice another question? (yes or no answer only)")
        continue_choice = input("You: ").lower()
        
        if continue_choice == 'yes':
            next_q = bot.select_question()
            print(f"Your next question is: {next_q}")
        else:
            print("Good luck with your interviews!")
            break
    
if __name__ == "__main__":
    main()