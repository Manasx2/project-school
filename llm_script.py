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

def generate_response(prompt):
    # Initialize the text generation pipeline with GPT-Neo
    generator = pipeline("text-generation", model="distilgpt2")
    
    # Generate text based on the prompt
    result = generator(prompt, max_length=150, num_return_sequences=1)
    response = result[0]["generated_text"]
    
    print("Generated response:", response)
    return response

def save_response_to_file(response, filename="generated_output.txt"):
    with open(filename, "w") as f:
        f.write(response)
    print(f"Response saved to", filename)

def main():
    # Load the prompt
    prompt = load_prompt_from_file()
    if prompt:
        # Generate a response based on the prompt
        response = generate_response(prompt)
        
        # Save the response to a file
        save_response_to_file(response)

if __name__ == "__main__":
    main()