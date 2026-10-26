"""Check that the shipped eval runner works with the anthropic SDK version pinned by eval-gate.yml.

Never touches the network. The SDK's HTTP layer is replaced with an httpx MockTransport, and the
judge call path (argument acceptance and request serialization) runs without stubs, so a change
in the SDK's argument contract fails here. CI (validate.yml) installs the pinned SDK and runs with
HOTL_REQUIRE_SDK=1. Locally the test is skipped when the SDK is not installed.
"""

import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

try:
    import anthropic
    # anthropic SDK 1.17 and later use httpx2 for HTTP; older versions use httpx
    try:
        import httpx2 as httpx
    except ImportError:
        import httpx
except ImportError:
    anthropic = None


ASSETS = Path(__file__).resolve().parents[2] / "plugins/hotl-engineering/skills/hotl-engineering/assets"
SDK_REQUIRED = os.environ.get("HOTL_REQUIRE_SDK") == "1"


def load_runner_with_real_sdk():
    spec = importlib.util.spec_from_file_location("hotl_evals_real_sdk", ASSETS / "evals/run_evals.py")
    runner = importlib.util.module_from_spec(spec)
    # dataclass looks up the defining module in sys.modules, so register it only while loading
    with patch.dict(sys.modules, {"hotl_evals_real_sdk": runner}):
        spec.loader.exec_module(runner)
    return runner


@unittest.skipIf(anthropic is None and not SDK_REQUIRED, "anthropic SDK not installed (required in CI via HOTL_REQUIRE_SDK=1)")
class JudgeSdkContractTests(unittest.TestCase):
    def setUp(self):
        if anthropic is None:
            self.fail("HOTL_REQUIRE_SDK=1 but the anthropic SDK cannot be imported")
        self.runner = load_runner_with_real_sdk()

    def test_default_judge_config_is_accepted_by_the_pinned_sdk(self):
        cfg = json.loads((ASSETS / "evals/thresholds.json").read_text())["judge"]
        vote = json.dumps({axis: {"score": 5, "reason": "fixture"} for axis in self.runner.AXES})
        requests = []

        def handler(request):
            requests.append(json.loads(request.content))
            return httpx.Response(200, json={
                "id": "msg_fixture", "type": "message", "role": "assistant",
                "model": self.runner.JUDGE_MODEL,
                "content": [{"type": "text", "text": vote}],
                "stop_reason": "end_turn", "stop_sequence": None,
                "usage": {"input_tokens": 1, "output_tokens": 1},
            })

        client = anthropic.AnthropicBedrock(
            aws_region="ap-northeast-1", aws_access_key="fixture", aws_secret_key="fixture",
            http_client=httpx.Client(transport=httpx.MockTransport(handler)))
        case = {"id": "fixture", "category": "answer", "query": "fixture"}

        result = self.runner.eval_l2(client, case, {}, "rubric", cfg)

        self.assertEqual(len(requests), cfg["votes"])
        self.assertEqual({axis: result[axis]["score"] for axis in self.runner.AXES},
                         {axis: 5 for axis in self.runner.AXES})
        # The default (previous-generation) judge does not support API version 2026-10-21 on
        # Bedrock (Bedrock legacy page). SDK 2.x sends that version, so keep the SDK major
        # until the judge moves to Claude 4.7 or later
        self.assertEqual({request.get("anthropic_version") for request in requests}, {"bedrock-2023-05-31"})


if __name__ == "__main__":
    unittest.main()
