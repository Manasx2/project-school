import time
import os
from transformers import pipeline

def load_prompt_from_file(filename="recognized_text.txt"):
    try:
        with open(filename, "r") as f:
            prompt = f.read().strip()
            print("Prompt loaded:", prompt)
            return prompt
    except FileNotFoundError:
        print("Prompt file not found.")
        return None

def generate_response(prompt, conversation_history):
    # Initialize the text generation pipeline with BlenderBot
    generator = pipeline("text-generation", model="facebook/blenderbot-400M-distill")
    
    # Combine the conversation history with the new prompt
    full_prompt = "\n".join(conversation_history + [prompt])
    
    # Generate conversational response with truncation
    result = generator(full_prompt, max_length=150, truncation=True, temperature=0.7, top_k=50)
    response = result[0]["generated_text"].strip()
    
    print("Generated response:", response)
    return response

def save_response_to_file(response, filename="generated_output.txt"):
    with open(filename, "w") as f:
        f.write(response)
    print(f"Response saved to {filename}")

def main():
    # Store the last modified time of the prompt file
    last_modified_time = 0
    previous_prompt = ""  # To keep track of the last prompt
    conversation_history = []  # List to store conversation history

    while True:
        # Check for file modification
        current_modified_time = os.path.getmtime("recognized_text.txt")
        
        if current_modified_time != last_modified_time:
            # Update the last modified time
            last_modified_time = current_modified_time
            
            # Load the prompt
            prompt = load_prompt_from_file()
            if prompt and prompt != previous_prompt:
                previous_prompt = prompt  # Update the previous prompt
                conversation_history.append(prompt)  # Append new prompt to conversation history
                # Generate a response based on the new prompt
                response = generate_response(prompt, conversation_history)
                
                # Save the response to a file
                save_response_to_file(response)

        # Sleep for a while before checking again
        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()