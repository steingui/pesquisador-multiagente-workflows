import re
import logging
import unicodedata

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"forget\s+(all\s+)?(previous|prior)\s+commands",
    r"you\s+are\s+now\s+a",
    r"system\s*prompt\s*:",
    r"override\s+(the\s+)?system",
    r"disregard\s+(all\s+)?above",
    r"jailbreak",
    r"dan\s+mode",
    r"ignore\s+.*instru[çc][õo]es",
    r"esque[çc]a\s+(tudo|todas?\s+regras?|instru[çc][õo]es)",
    r"agora\s+voc[êe]\s+[ée]\s+um",
    r"exec\s*\(",
    r"eval\s*\(",
    r"<script[\s>]",
]

COMPILED_INJECTION_REGEX = re.compile(
    "|".join(PROMPT_INJECTION_PATTERNS), re.IGNORECASE
)

def validate_and_sanitize_query(query: str) -> str:
    """Higieniza e valida a consulta do usuário contra injeção de prompt e exploits."""
    if not query or not query.strip():
        raise ValueError("A consulta não pode estar vazia.")

    cleaned_query = query.strip()
    if len(cleaned_query) > 1000:
        raise ValueError("A consulta excede o limite máximo de 1000 caracteres.")

    normalized_query = unicodedata.normalize("NFKC", cleaned_query)
    if COMPILED_INJECTION_REGEX.search(normalized_query):
        logging.warning(f"Prompt Injection bloqueado: {cleaned_query[:40]}...")
        raise ValueError("Consulta bloqueada por diretrizes de segurança anti-prompt injection.")

    return cleaned_query
