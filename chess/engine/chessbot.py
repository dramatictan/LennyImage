from google import genai
from sympy.simplify.hyperexpand import try_lerchphi

import pygame
import requests
from io import BytesIO
import chess
import chess.engine
import asyncio

# ---------------------------- UI ---------------------------------
client = genai.Client(api_key = "AQ.Ab8RN6K6twL06xW4uRWR_7BStcGPgAURrh9VGO8LKAnzq9M1AA")
models_pool = [
    "gemini-2.5-flash", "gemini-2.5-flash-lite"
]

# Interact with Stockfish engine
async def main() -> None:
    engine_path = "stockfish-windows-x86-64-avx2.exe"




