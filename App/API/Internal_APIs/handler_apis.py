# --- Default Imports ---
import os
from dotenv import load_dotenv

# --- OpenAI internal API Imports ---
from API.External_APIs.open_ai_apis import (
    ask_openai_for_title_and_resume,
    ask_openai_for_ref_schema,
    ask_openai_for_acts,
    ask_openai_for_chapters,
    ask_openai_for_beats,
    ask_openai_for_final_block,
)

# --- To generate Title and Resume ---
def ask_LLM(params: dict) -> list[str]:
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    ## For GPT Model
    if model.startswith("gpt"):
        return ask_openai_for_title_and_resume(params)
    
    ## For other models
    return [f"Sorry, model '{model}' not supported yet."]

# --- To generate Refference Board Schema ---
def ask_LLM_for_schema(book_title: str, book_resume: str) -> list[str]:
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    ## For GPT Model
    if model.startswith("gpt"):
        return ask_openai_for_ref_schema(book_title, book_resume)
    
    ## For other models
    return [
        f"Sorry, model '{model}' not supported yet.",
        f"Sorry, model '{model}' not supported yet.",
        f"Sorry, model '{model}' not supported yet."
        ]

# --- To generate Acts for the Sugest Acts Window ---
def ask_LLM_for_acts(book_title: str, book_resume: str, Places_Objects: str, Characters: str, Happenings: str) -> list[str]:
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    ## For GPT Model
    if model.startswith("gpt"):
        return ask_openai_for_acts(book_title, book_resume, Places_Objects, Characters, Happenings)
    
    ## For other models
    return [
        f"Sorry, model '{model}' not supported yet.",
        f"Sorry, model '{model}' not supported yet.",
        f"Sorry, model '{model}' not supported yet."
        ]

# --- To generate Chapters from Acts ---
def ask_LLM_for_chapters(book_title: str,
                         book_resume: str,
                         Places_Objects: str,
                         Characters: str,
                         Happenings: str,
                         act1: str, act2: str, act3: str) -> dict:    
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    ## For GPT Model
    if model.startswith("gpt"):
        return ask_openai_for_chapters(book_title, book_resume, Places_Objects, Characters, Happenings, act1, act2, act3)

    ## For other models:
    return {"Chapters": [
        ["Sorry, model not supported yet.", "", [f"CAP1-BEAT{j}-CONTENT{j}" for j in range(1, 13)]]
    ]}

# --- To generate Beats for each Chapter ---
def ask_LLM_for_beats(book_json: dict) -> dict:
    """
    Encaminha o JSON completo do projeto para a API externa,
    devolvendo {"Chapters": [...]} com os beats atualizados.
    """
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    # For GPT model
    if model.startswith("gpt"):
        return ask_openai_for_beats(book_json)

    # For other models with generic fallback:
    chapters_in = book_json.get("Chapters", [])
    chapters_out = []
    for i, ch in enumerate(chapters_in, start=1):
        title  = ch[0] if len(ch) > 0 else f"Capítulo {i}"
        resume = ch[1] if len(ch) > 1 else ""
        beats  = [f"CAP{i}-BEAT{j}-CONTENT{j}-ATUALIZADO" for j in range(1, 13)]
        chapters_out.append([title, resume, beats])
    return {"Chapters": chapters_out}

# --- To generate block from a pair of beats in order to complete the final text ---
def ask_LLM_for_final_block(book_title: str,
                            book_resume: str,
                            Places_Objects: str,
                            Characters: str,
                            Happenings: str,
                            chapter_number: int,
                            chap_title: str,
                            chap_resume: str,
                            beats_pair: list[str]) -> str:
    load_dotenv(dotenv_path="./config/.env", override=True)
    model = os.getenv("LLM_MODEL", "").strip().lower()

    # For GPT model
    if model.startswith("gpt"):
        return ask_openai_for_final_block(
            book_title, book_resume, Places_Objects, Characters, Happenings,
            chapter_number, chap_title, chap_resume, beats_pair
        )

    # For other model with a warning fallback
    return "THE BOOK IS GENERATED HERE FROM 2 CHAPTER STORY BEATS\n[Error: Model is not yet avaiable."

