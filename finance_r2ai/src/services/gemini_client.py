import os
import time
import logging
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load env
load_dotenv()


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Không tìm thấy GEMINI_API_KEY. Vui lòng cấu hình trong biến môi trường hoặc .env")

        # Sử dụng SDK mới google-genai
        self.client = genai.Client(api_key=self.api_key)

    def generate_content(self, prompt: str, model: str = "gemini-3.5-flash-lite", system_instruction: Optional[str] = None,
                         temperature: float = 0.0, response_schema: Optional[Dict[str, Any]] = None, retries: int = 3, delay: int = 2) -> str:
        """
        Gọi API Gemini với cơ chế Retry tự động.
        Sử dụng model mặc định là gemini-2.5-flash (tương đương với Flash Lite/Flash hiện tại)
        """
        config_params = {"temperature": temperature}

        if system_instruction:
            config_params["system_instruction"] = system_instruction

        if response_schema:
            config_params["response_mime_type"] = "application/json"
            config_params["response_schema"] = response_schema

        config = types.GenerateContentConfig(**config_params)

        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                logger.warning(f"Lỗi gọi Gemini API (lần {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    # Nếu lỗi 429 (Too Many Requests), đợi 60 giây để reset quota của Free Tier
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        logger.info("Phát hiện lỗi 429 Quota Exceeded. Tạm dừng 60 giây trước khi thử lại...")
                        time.sleep(60)
                    else:
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                else:
                    logger.error("Đã hết số lần thử lại. Thất bại.")
                    raise e
