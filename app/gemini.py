import pathlib
import textwrap
from app_constants import appConstants
import google.generativeai as gemini



# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY = appConstants.GOOGLE_API_KEY
gemini.configure(api_key=GOOGLE_API_KEY)


def query_gemini(company_name):
    try:
        model = gemini.GenerativeModel('gemini-pro')
        response = model.generate_content(("provide information about a bike company called {} in less than 50 words.").format(company_name))
        return response.text
    except Exception as e:
        return ""

