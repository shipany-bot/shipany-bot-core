from .command import CommandActivation as CommandActivation
from .event import EventActivation as EventActivation
from .webhook import WebhookActivation as WebhookActivation

Activation = CommandActivation | EventActivation | WebhookActivation
Activations = list[Activation]
