import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """
    Multi-Provider LLM Engine for NyayaAI.
    
    Primary: Google Gemini (gemini-1.5-flash) - high accuracy, generous free tier.
    Fallback: Groq (llama-3.3-70b-versatile) - ultra-fast open-source fallback.
    """

    def __init__(self):
        self._gemini_client = None
        self._groq_client = None
        self._setup_clients()

    def _setup_clients(self):
        # 1. Initialize Gemini
        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._gemini_client = genai
                logger.info("Google Gemini client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")

        # 2. Initialize Groq
        if settings.GROQ_API_KEY:
            try:
                from groq import AsyncGroq
                self._groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq client initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")

    async def generate_completion(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generates text completion with automatic fallback:
        Gemini -> Groq -> Local Mock Error
        """
        # Attempt 1: Google Gemini
        if self._gemini_client and settings.GEMINI_API_KEY:
            try:
                logger.info(f"Generating completion via Gemini ({settings.GEMINI_MODEL})...")
                model = self._gemini_client.GenerativeModel(
                    model_name=settings.GEMINI_MODEL,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini generation failed ({e}). Falling back to Groq...")

        # Attempt 2: Groq Fallback
        if self._groq_client and settings.GROQ_API_KEY:
            try:
                logger.info(f"Generating completion via Groq ({settings.GROQ_MODEL})...")
                messages = []
                if system_instruction:
                    messages.append({"role": "system", "content": system_instruction})
                messages.append({"role": "user", "content": prompt})

                chat_completion = await self._groq_client.chat.completions.create(
                    messages=messages,
                    model=settings.GROQ_MODEL,
                    temperature=0.2,
                )
                return chat_completion.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"Groq fallback failed: {e}")

        # Attempt 3: Graceful fallback if no keys configured or both failed
        logger.warning("No LLM API keys provided or both providers failed. Returning mock guidance.")
        return (
            "[SYSTEM NOTICE: Real LLM generation requires GEMINI_API_KEY or GROQ_API_KEY in backend/.env]\n\n"
            f"Drafting generated based on provided facts:\n{prompt[:300]}..."
        )

# Global singleton instance
llm_service = LLMService()
