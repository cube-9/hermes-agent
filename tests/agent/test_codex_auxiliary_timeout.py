from types import SimpleNamespace

from agent.auxiliary_client import _CodexCompletionsAdapter


class _FakeResponses:
    def __init__(self):
        self.stream_kwargs = None

    def stream(self, **kwargs):
        self.stream_kwargs = kwargs
        return _FakeStream()


class _FakeStream:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def __iter__(self):
        return iter(())

    def get_final_response(self):
        return SimpleNamespace(output=[], usage=None)


def test_codex_completions_adapter_forwards_timeout_to_responses_stream():
    responses = _FakeResponses()
    client = SimpleNamespace(responses=responses)
    adapter = _CodexCompletionsAdapter(client, "gpt-5.2-codex")

    adapter.create(
        messages=[{"role": "user", "content": "hello"}],
        timeout=12.5,
    )

    assert responses.stream_kwargs["timeout"] == 12.5
