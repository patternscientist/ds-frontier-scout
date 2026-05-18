"""Run a fixed-stub OpenAI-compatible transport check for Milestone 3z.

This is a fallback plumbing test only. It serves one deterministic local HTTP
response that looks like an OpenAI chat-completions response. It performs no
model inference, no autonomous mutation, and no policy discovery.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
ZERO_RUNNER = REPO_ROOT / "scripts" / "run_list_update_openevolve_zero_money_milestone3.py"
SOURCE_CONFIG = (
    REPO_ROOT
    / "examples"
    / "list_update_openevolve"
    / "config_tiny_milestone3_ollama.yaml"
)
DEFAULT_RUN_DIR = REPO_ROOT / "runs" / "list_update_openevolve_milestone3z_fixed_stub"
STUB_MODEL = "fixed-stub-list-update-v0"
STUB_DIFF = """<<<<<<< SEARCH
    target_index = 0
=======
    target_index = len(state) - 1
>>>>>>> REPLACE"""


class FixedStubHandler(BaseHTTPRequestHandler):
    server_version = "ListUpdateFixedStub/0.1"

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/v1/models":
            self._send_json(
                {
                    "object": "list",
                    "data": [
                        {
                            "id": STUB_MODEL,
                            "object": "model",
                            "created": int(time.time()),
                            "owned_by": "local-fixed-stub",
                        }
                    ],
                }
            )
            return
        self._send_json({"error": {"message": "not found"}}, status=404)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length:
            self.rfile.read(length)
        path = self.path.rstrip("/")
        if path == "/v1/chat/completions":
            self._send_json(
                {
                    "id": "chatcmpl-fixed-stub",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": STUB_MODEL,
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": STUB_DIFF,
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                    },
                }
            )
            return
        if path == "/v1/completions":
            self._send_json(
                {
                    "id": "cmpl-fixed-stub",
                    "object": "text_completion",
                    "created": int(time.time()),
                    "model": STUB_MODEL,
                    "choices": [
                        {
                            "index": 0,
                            "text": STUB_DIFF,
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                    },
                }
            )
            return
        self._send_json({"error": {"message": "not found"}}, status=404)

    def log_message(self, _format: str, *args: Any) -> None:
        return

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main(argv: list[str] | None = None) -> int:
    if argv:
        print("This fixed-stub runner does not accept arguments.", file=sys.stderr)
        return 2

    zero_runner = _load_zero_runner()
    DEFAULT_RUN_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), FixedStubHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    api_base = f"http://127.0.0.1:{server.server_port}/v1"
    stub_config = DEFAULT_RUN_DIR / "config_tiny_milestone3_fixed_stub.yaml"
    _write_stub_config(SOURCE_CONFIG, stub_config, api_base)

    try:
        return zero_runner.main(
            [
                "--config",
                str(stub_config),
                "--run-dir",
                str(DEFAULT_RUN_DIR),
                "--api-base",
                api_base,
                "--model",
                STUB_MODEL,
                "--process-timeout-seconds",
                "180",
                "--stubbed-transport-label",
                zero_runner.STUB_LABEL,
            ]
        )
    finally:
        server.shutdown()
        server.server_close()


def _load_zero_runner():
    spec = importlib.util.spec_from_file_location(
        "run_list_update_openevolve_zero_money_milestone3",
        ZERO_RUNNER,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_stub_config(source: Path, destination: Path, api_base: str) -> None:
    text = source.read_text(encoding="utf-8")
    text = text.replace(
        "# Milestone 3z zero-money local-model OpenEvolve/list-update integration test.",
        "# Milestone 3z fixed-stub OpenAI-compatible transport test.",
    )
    text = text.replace(
        "This config points OpenEvolve at a local OpenAI-compatible endpoint, intended\n"
        "# first for Ollama:",
        "This generated config points OpenEvolve at a local fixed-response HTTP\n"
        "# stub. It performs no model inference and is not autonomous discovery:",
    )
    text = text.replace(
        "runs/list_update_openevolve_milestone3z_zero_money",
        "runs/list_update_openevolve_milestone3z_fixed_stub",
    )
    replacements = {
        "  api_base: http://localhost:11434/v1": f"  api_base: {api_base}",
        "  api_key: ollama": "  api_key: fixed-stub",
        "  primary_model: qwen2.5-coder:1.5b": f"  primary_model: {STUB_MODEL}",
        "  max_tokens: 512": "  max_tokens: 256",
        "  timeout: 120": "  timeout: 30",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text += (
        "\n# Stubbed OpenAI-compatible transport test; fixed response, no model\n"
        "# inference, no autonomous mutation, no policy discovery.\n"
    )
    destination.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
