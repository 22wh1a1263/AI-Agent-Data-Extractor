import openai

# Function to process search results using OpenAI API
def process_with_llm(search_results, openai_api_key):
    openai.api_key = openai_api_key

    # Example prompt to extract emails from search result snippets
    prompt = f"Extract the email address from the following search result snippets:\n\n"
    for result in search_results:
        prompt += f"Snippet: {result.get('snippet')}\n"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # or you can use another engine like GPT-4
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Assuming OpenAI returns the extracted data in a usable format
    extracted_data = response.choices[0].text.strip()
    return {"entity": search_results[0].get('title'), "extracted_data": extracted_data}
