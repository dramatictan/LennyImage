from google import genai
from sympy.simplify.hyperexpand import try_lerchphi

# ---------------------------- UI ---------------------------------
client = genai.Client(api_key = "AQ.Ab8RN6K6twL06xW4uRWR_7BStcGPgAURrh9VGO8LKAnzq9M1AA")
models_pool = [
    "gemini-2.5-flash", "gemini-2.5-flash-lite"
]

def generate_output(user_text):
    for model in models_pool:
        try:
            selected_model = model
            response = client.models.generate_content(
                model=selected_model,
                contents=user_text  # send input to chatbot
            )
            return response.text

        except Exception as e:
            if "429" in str(e):
                print(f"{model} limit is up, switching to another model in sequence.")
                continue # continue to next model in array

    return "All models used up for today"


