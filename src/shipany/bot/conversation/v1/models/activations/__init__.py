from .command import CommandActivation as CommandActivation
from .event import EventActivation as EventActivation

Activation = CommandActivation | EventActivation
Activations = list[Activation]
