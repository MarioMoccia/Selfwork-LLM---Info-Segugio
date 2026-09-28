import chainlit as cl

from web_search import WebSearch
from utils import LLMHelper


@cl.on_chat_start
async def start():
    await cl.Message(
        content=(
            "Ciao! Sono Info Segugio 🐕‍🦺, faccio ricerche sul web e ti do una risposta "
            "con le fonti citate. Chiedimi qualcosa!"
        )
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content

    searching_msg = cl.Message(content="🔍 Sto cercando sul web...")
    await searching_msg.send()

    results = WebSearch.search(query)

    if not results:
        searching_msg.content = "❌ Nessun risultato trovato. Prova a riformulare la domanda."
        await searching_msg.update()
        return

    context = LLMHelper.build_context(results)

    searching_msg.content = f"✅ Trovate {len(results)} fonti. Sto elaborando la risposta..."
    await searching_msg.update()

    response_message = cl.Message(content="")
    await response_message.send()

    try:
        stream = LLMHelper.answer_stream(query, context, len(results))

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            await response_message.stream_token(token)

        # Aggiunge l'elenco delle fonti come link cliccabili alla fine della risposta
        sources_text = "\n\n**Fonti:**\n" + "\n".join(
            f"[{i}] [{r['title']}]({r['url']})" for i, r in enumerate(results, start=1)
        )
        response_message.content += sources_text
        await response_message.update()

    except Exception as e:
        error_message = f"❌ Si è verificato un errore: {str(e)}"
        await cl.Message(content=error_message).send()
        print(error_message)
