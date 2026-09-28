# web_search.py
from ddgs import DDGS

from config import Config


class WebSearch:
    """Wrapper minimale sopra DDGS: cerca sul web e restituisce risultati puliti."""

    @staticmethod
    def search(query: str, max_results: int = None) -> list[dict]:
        """Esegue una ricerca web e restituisce una lista di risultati.

        Ogni risultato è un dizionario con "title", "url" e "snippet".
        Nessuna chiave API richiesta: usa il motore DuckDuckGo tramite la libreria ddgs.
        """
        max_results = max_results or Config.MAX_RESULTS

        try:
            raw_results = DDGS().text(query, max_results=max_results)
        except Exception as e:
            print(f"Errore durante la ricerca web: {e}")
            return []

        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            }
            for r in raw_results
        ]
