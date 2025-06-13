from groq import Groq

api_key="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"

def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None

system_prompt = """
                    You are an AI-powered threat detection chatbot. Your role is to analyze the user's input and determine whether it contains any potentially risky, dangerous, or harmful content. 

                    Instructions:
                    - Classify the input into one of the following categories: "Safe", "Suspicious", "Risky", or "Dangerous".
                    - If the input is dangerous or risky, suggest a safer alternative if possible.
                    - Keep responses concise and to the point.

                    Your primary goal is to help users understand the risk level of their text while maintaining a responsible and unbiased approach.
                """



def threat_detection_chatbot(client, system_prompt):
    while True:
        input_string = input("Enter a message (or type 'exit' to quit): ")
        if input_string.lower() == 'exit':
            print("Exiting chatbot...")
            break
        
        user_prompt = f"""
                        Analyze the following text and determine whether it contains any threats, dangerous content, or suspicious elements. Provide the final output analysis result in one single line as a conclusion.

                        Keep the output format as:
                        final conclusion of the analysis in a single line

                        Input Text: {input_string}
                    """

        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt},
                          {"role": "user", "content": user_prompt}],
                model="llama3-70b-8192",
                temperature=0.7
            )
            result = response.choices[0].message.content
            print(f"Threat Analysis: {result}")
        except Exception as e:
            print(f"Error generating the next question: {e}")
            return


if __name__ == "__main__":
    client=initialize_groq_client(api_key=api_key)
    threat_detection_chatbot(client=client, system_prompt=system_prompt)