"""
Voice Module - Handles speech input and output for the AI Fitness Assistant
"""

from voice.speech_input import SpeechInput, speech_input
from voice.speech_output import (
    SpeechOutput, speech_output,
    get_random_quote, FITNESS_RESPONSES, MOTIVATIONAL_QUOTES
)

__all__ = [
    'SpeechInput',
    'speech_input',
    'SpeechOutput',
    'speech_output',
    'get_random_quote',
    'FITNESS_RESPONSES',
    'MOTIVATIONAL_QUOTES'
]
