# utils.py
from config import Config
from openai import OpenAI

client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)


class LLMHelper:

    @staticmethod
    def build_context(results: list[dict]) -> str:
        """Costruisce il contesto numerato da passare al modello, una fonte per blocco."""
        blocks = []
        for i, r in enumerate(results, start=1):
            blocks.append(
                f"[{i}] {r['title']}\nURL: {r['url']}\nEstratto: {r['snippet']}"
            )
        return "\n\n".join(blocks)

    @staticmethod
    def build_prompt(query: str, context: str, num_sources: int) -> str:
        return f"""
Sei un assistente di ricerca. Rispondi alla domanda dell'utente usando ESCLUSIVAMENTE le
informazioni contenute nei risultati di ricerca qui sotto, numerati da [1] a [{num_sources}].

Domanda dell'utente: {query}

Risultati di ricerca:
{context}

Istruzioni:
- Scrivi una risposta chiara e sintetica in italiano.
- Ogni affermazione deve citare la fonte da cui proviene, con il numero tra parentesi quadre, es. [1].
- Se i risultati non contengono una risposta sufficiente, dillo esplicitamente invece di inventare.
- Non aggiungere fonti che non siano tra quelle elencate sopra.
"""

    @staticmethod
    def answer_stream(query: str, context: str, num_sources: int):
        """Ritorna lo stream di risposta del modello, con citazioni alle fonti."""
        prompt = LLMHelper.build_prompt(query, context, num_sources)
        return client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
