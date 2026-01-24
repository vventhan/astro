"""Astrology agent module using Google Gemini."""

from google import genai
from google.genai import types

from .prompts import get_system_prompt, get_user_prompt

# Available models to try (in order of preference)
MODELS = [
    "gemini-3-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
]


class AstrologyAgent:
    """Agent for generating Vedic astrology readings using Gemini."""

    def __init__(self, api_key: str, model: str = None):
        """
        Initialize the agent with a Gemini API key.

        Args:
            api_key: Google Gemini API key
            model: Specific model to use (optional, will be auto-detected if not provided)
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model  # Use provided model or will be set during validation

    def validate_api_key(self) -> tuple[bool, str]:
        """
        Validate the API key by making a simple request.
        Tries multiple models to find one that works.

        Returns:
            Tuple of (is_valid, error_message)
        """
        last_error = None

        for model_name in MODELS:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents="Say 'ok' if you can read this."
                )
                # If we get here, the model works
                self.model = model_name
                return True, ""
            except Exception as e:
                last_error = str(e)
                continue

        # None of the models worked
        error_lower = last_error.lower() if last_error else ""

        if "invalid" in error_lower or "api_key" in error_lower or "api key" in error_lower:
            return False, "Invalid API key. Please check and try again."
        elif "permission" in error_lower or "denied" in error_lower:
            return False, "API key doesn't have permission. Please check your Gemini API settings."
        elif "quota" in error_lower or "limit" in error_lower or "resource" in error_lower:
            return False, "API quota exceeded. Please try again later or check your usage limits."
        else:
            return False, f"Could not connect to Gemini API: {last_error}"

    def get_reading(self, category: str, chart_content: str, year: int = None, dasha_lord: str = None) -> str:
        """
        Generate an astrology reading for the given category.

        Args:
            category: Type of reading (general, relationship, career, health, wealth, dasha, annual)
            chart_content: Extracted text from the birth chart PDF
            year: Year for annual predictions (required if category is 'annual')
            dasha_lord: Specific dasha lord to analyze (optional for 'dasha' category)

        Returns:
            Generated reading text

        Raises:
            ValueError: If required parameters are missing
            Exception: If API call fails
        """
        if category == "annual" and not year:
            raise ValueError("Year is required for annual predictions.")

        if not self.model:
            raise Exception("No model available. Please validate API key first.")

        system_prompt = get_system_prompt(category)
        user_prompt = get_user_prompt(category, chart_content, year, dasha_lord)

        # Combine prompts
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=1.0,
                    max_output_tokens=8192,
                )
            )
            return response.text

        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "limit" in error_str:
                raise Exception("API quota exceeded. Please try again later or check your Gemini usage limits.")
            elif "invalid" in error_str:
                raise Exception(f"Invalid request: {str(e)}")
            else:
                raise Exception(f"Error generating reading: {str(e)}")

    def stream_reading(self, category: str, chart_content: str, year: int = None, dasha_lord: str = None):
        """
        Stream an astrology reading for the given category.

        Yields:
            Text chunks as they are generated
        """
        if category == "annual" and not year:
            raise ValueError("Year is required for annual predictions.")

        if not self.model:
            raise Exception("No model available. Please validate API key first.")

        system_prompt = get_system_prompt(category)
        user_prompt = get_user_prompt(category, chart_content, year, dasha_lord)
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=1.0,
                    max_output_tokens=8192,
                )
            ):
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "limit" in error_str:
                raise Exception("API quota exceeded. Please try again later.")
            else:
                raise Exception(f"Error generating reading: {str(e)}")

    def stream_chat(self, prompt: str):
        """
        Stream a chat response.

        Yields:
            Text chunks as they are generated
        """
        if not self.model:
            raise Exception("No model available. Please validate API key first.")

        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=2048,
                )
            ):
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            raise Exception(f"Error: {str(e)}")
