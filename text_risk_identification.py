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

def text_risk_identify(client, system_prompt):
    try:
        # Read content from the text file
        with open('scraped_content.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        user_prompt = f"""
        Analyze the following text for potential risks and threats. Consider:
        1. Violence or harmful content
        2. Hate speech or discriminatory language
        3. Potential security threats
        4. Misinformation or fake news
        5. Any other concerning elements

        Text to analyze:
        {file_content}

        Please provide:
        1. Risk Classification (Safe/Suspicious/Risky/Dangerous)
        2. Specific concerns identified (if any)
        """

        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt},
                     {"role": "user", "content": user_prompt}],
            model="llama3-70b-8192",
            temperature=0.7
        )
        result = response.choices[0].message.content
        print(f"Threat Analysis: {result}")
    except FileNotFoundError:
        print("Error: scraped_content.txt file not found")
        return
    except Exception as e:
        print(f"Error generating the next question: {e}")
        return


if __name__ == "__main__":
    client=initialize_groq_client(api_key=api_key)
    text_risk_identify(client=client, system_prompt=system_prompt)