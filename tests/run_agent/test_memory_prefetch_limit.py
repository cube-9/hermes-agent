from agent.memory_manager import limit_memory_prefetch_context


def test_limit_memory_prefetch_context_truncates_when_limit_is_positive():
    context = "a" * 20

    limited = limit_memory_prefetch_context(context, 8)

    assert limited == "a" * 8


def test_limit_memory_prefetch_context_keeps_context_when_limit_is_none_or_zero():
    context = "memory context"

    assert limit_memory_prefetch_context(context, None) == context
    assert limit_memory_prefetch_context(context, 0) == context
