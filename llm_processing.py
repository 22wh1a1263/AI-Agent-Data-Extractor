import openai
import logging
import time

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_openai_api(api_key):
    """
    Initialize OpenAI API with the provided API key.
    """
    openai.api_key = api_key
    if openai_api_key:
    # Initialize OpenAI API client
        openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract the email from the following text."},
                {"role": "user", "content": f"Text: {simulated_search_results['snippets'][0]}"},
            ],
        )
        extracted_info = response['choices'][0]['message']['content']
    except openai.error.RateLimitError:
        st.error("Rate limit exceeded. Please try again later.")
        return
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
    else:
        extracted_info = "No API key found!"



def truncate_text(text, max_length=2000):
    """
    Truncate text to avoid exceeding maximum GPT input length.
    """
    return text[:max_length] if len(text) > max_length else text


def format_search_results(search_results):
    """
    Format search results into a readable text for GPT prompt.
    Args:
        search_results (list): List of dictionaries containing search results.
    Returns:
        str: Formatted string for GPT.
    """
    if not search_results:
        logging.warning("No search results to format.")
        return "No search results available."

    formatted_text = ""
    for result in search_results:
        formatted_text += f"Title: {result.get('title', 'N/A')}\n"
        formatted_text += f"Snippet: {result.get('snippet', 'N/A')}\n"
        formatted_text += f"URL: {result.get('link', 'N/A')}\n\n"

    return truncate_text(formatted_text)


def query_gpt(prompt, engine="text-davinci-003", max_tokens=150, temperature=0.7, retries=3):
    """
    Send a query to OpenAI's GPT API and handle retries.
    Args:
        prompt (str): Input prompt for GPT.
        engine (str): OpenAI engine to use.
        max_tokens (int): Maximum tokens for the output.
        temperature (float): Creativity control.
        retries (int): Number of retries for handling rate limits or errors.
    Returns:
        str: GPT's response text.
    """
    for attempt in range(retries):
        try:
            logging.info("Sending prompt to OpenAI API...")
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            logging.info("OpenAI API response received.")
            return response.choices[0].text.strip()
        except openai.error.RateLimitError:
            logging.warning("Rate limit hit. Retrying in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Error while querying GPT: {e}")
            if attempt == retries - 1:
                raise e


def extract_information_from_search_results(search_results, openai_api_key, query_template):
    """
    Process search results using GPT to extract required information.
    Args:
        search_results (list): List of search results to analyze.
        openai_api_key (str): OpenAI API key for authentication.
        query_template (str): Template to construct GPT prompt with {entity} placeholder.
    Returns:
        str: Extracted information or error message.
    """
    if not search_results:
        logging.error("Empty search results. Nothing to process.")
        return "No search results provided."

    # Initialize OpenAI API
    initialize_openai_api(openai_api_key)

    # Format search results
    search_text = format_search_results(search_results)

    # Replace placeholder in query template with search results
    prompt = query_template.replace("{entity}", search_text)

    # Call GPT API to process the query
    try:
        return query_gpt(prompt)
    except Exception as e:
        logging.error(f"Error during GPT query: {e}")
        return "An error occurred while processing the search results."
