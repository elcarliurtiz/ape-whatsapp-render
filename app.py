import os
from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from openai import OpenAI
from collections import deque

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memoria simple en RAM por usuario (teléfono)
SESSIONS = {}  # { phone: deque([...], maxlen=12) }

SYSTEM_PROMPT = (
    "Sos APE, asistente pedagógico institucional de una escuela de la "
    "Tecnicatura en Producción Agropecuaria (Provincia de Buenos Aires).\n\n"
    "MODO DE RESPUESTA:\n"
    "- Respondé siempre BREVE, claro y directo.\n"
    "- NO nombres leyes/documentos salvo que el docente lo pida explícitamente "
    "con frases tipo 'citá', 'norma', 'página', 'ampliá'.\n"
    "- Si piden ampliar, podés extender y citar documentos (sin inventar nada).\n"
    "- Si algo NO está en las fuentes institucionales cargadas, decí: "
    "'No está en las fuentes institucionales cargadas'.\n"
    "Estilo: rioplatense, práctico, sin tecnicismos innecesarios."
)

def get_session(phone: str):
    if phone not in SESSIONS:
        SESSIONS[phone] = deque(maxlen=12)
    return SESSIONS[phone]

def build_messages(session_deque, user_text):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for role, content in session_deque:
        msgs.append({"role": role, "content": content})
    msgs.append({"role": "user", "content": user_text})
    return msgs

@app.post("/whatsapp")
def whatsapp_webhook():
    from_phone = request.form.get("From")
    body = request.form.get("Body", "").strip()

    if not from_phone or not body:
        abort(400, "Bad request")

    session = get_session(from_phone)
    messages = build_messages(session, body)

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2,
            max_tokens=350,
        )
        reply = (resp.choices[0].message.content or "").strip()
        if not reply:
            reply = "No pude generar respuesta. Probá reformular en una línea."
    except Exception as e:
        reply = f"Ups, hubo un error procesando tu consulta. Probá de nuevo. ({e})"

    session.append(("user", body))
    session.append(("assistant", reply))

    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
