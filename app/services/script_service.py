import json
import asyncio
from typing import AsyncGenerator, Dict, Any, List
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "aladdin_scene_dialogue.json"


class ScriptService:
    def __init__(self, data_path: Path = DATA_PATH):
        self.data_path = data_path
        self._script_data: List[Dict[str, Any]] = self._load_script()

    def _load_script(self) -> List[Dict[str, Any]]:
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def stream_script(self, language: str, interval: float = 2.0) -> AsyncGenerator[str, None]:
        """
        Yields script lines formatted as Server-Sent Events (SSE).
        Map language selection ('es' or 'zh') to the underlying target translations.
        """
        lang_key_map = {
            "spanish": "spanish_translation",
            "es": "spanish_translation",
            "chinese": "chinese_translation",
            "zh": "chinese_translation"
        }

        target_field = lang_key_map.get(language.lower(), "english")

        for line in self._script_data:
            payload = {
                "line_id": line.get("line_id"),
                "scene_id": line.get("scene_id"),
                "actor": line.get("actor"),
                "text": line.get(target_field, line.get("english"))
            }
            # SSE framing format requires standard `data: <string>\n\n` syntax
            yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
            await asyncio.sleep(interval)