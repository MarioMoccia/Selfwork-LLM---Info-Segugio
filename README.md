# Selfwork LLM - Info Segugio

Assistente di ricerca in chat (Chainlit): fai una domanda, l'app cerca sul web in tempo reale
e un LLM sintetizza una risposta citando le fonti trovate, che restano cliccabili in fondo al
messaggio.

- **Ricerca web:** [`ddgs`](https://github.com/deedy5/ddgs) (motore DuckDuckGo), nessuna
  chiave richiesta.
- **Generazione della risposta:** OpenAI (`gpt-4o-mini`) di default, per usare un modello più
  performante di quelli locali. È comunque possibile passare a Ollama locale (vedi sotto),
  senza alcuna chiave API.

## Come funziona

1. L'utente scrive una domanda in chat.
2. `web_search.py` cerca sul web (di serie 5 risultati) e restituisce titolo, URL ed estratto
   di ogni pagina.
3. `utils.py` costruisce un prompt che numera le fonti trovate e chiede al modello di
   rispondere **solo** in base a quelle, citando il numero della fonte tra parentesi quadre
   (es. `[1]`) per ogni affermazione. Se le fonti non bastano, il modello lo dichiara invece di
   inventare.
4. La risposta viene mostrata in streaming, seguita dall'elenco delle fonti come link
   cliccabili.

## Setup

```bash
poetry install
```

### Versione con OpenAI (default)

```bash
cp .env.example .env   # e inserisci la tua OPENAI_API_KEY
```

### Versione locale con Ollama (alternativa, nessuna chiave richiesta)

In `info_segugio/config.py`, commenta il blocco OpenAI e scommenta quello Ollama, poi:

```bash
ollama pull llama3.2
ollama serve
```

## Per eseguire l'applicazione

```bash
eval $(poetry env activate)
chainlit run info_segugio/__init__.py -w
```

## Limiti di questa versione

- La ricerca usa i soli estratti (snippet) restituiti dal motore di ricerca, non il contenuto
  completo delle pagine: per risposte più approfondite si potrebbe scaricare e leggere le
  pagine più rilevanti prima di rispondere.
- `ddgs` interroga DuckDuckGo senza una API ufficiale: adatto per uso personale/didattico a
  basso volume, non per un traffico elevato o un uso in produzione.
- Nessuna memoria tra una domanda e l'altra: ogni messaggio è una ricerca indipendente.
