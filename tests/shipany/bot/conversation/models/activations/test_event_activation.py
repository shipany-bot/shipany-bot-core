import pytest

from shipany.bot.conversation.models.activations.event import EventActivation


@pytest.mark.parametrize(
  "event",
  [
    "onsomething",
    "test",
    "test-event",
    "test_event",
    "testEvent",
    "testEvent123",
    "test-event-123",
    "test_event_123",
  ],
)
def test_event_incorrent_names(event: str) -> None:
  with pytest.raises(ValueError, match="on-"):
    EventActivation.model_validate({"event": event, "next-step": "test"})
