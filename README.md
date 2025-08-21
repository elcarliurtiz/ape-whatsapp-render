# APE WhatsApp (Render)

Bot de WhatsApp para docentes que conecta Twilio ⇄ OpenAI (APE). Listo para desplegar en **Render**.

## 1) Preparar el repo
1. Cloná este proyecto o descomprimí el ZIP.
2. Creá un repo en GitHub y subí estos archivos.
3. **NO subas** tu `.env` al repo. Usá el `.env.example` como guía.

## 2) Variables de entorno (en Render)
En Render → *Environment* agregá:
- `OPENAI_API_KEY` = tu API key de OpenAI
- (Opcional) `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` si más adelante querés enviar mensajes salientes con la API de Twilio (acá respondemos con **TwiML**, no hace falta).

> No necesitás `TWILIO_WHATSAPP_FROM` mientras respondas con TwiML.

## 3) Desplegar en Render
1. Crear cuenta en https://render.com
2. **New + Web Service** → conectá tu repo de GitHub.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Elegí una región cercana y el plan gratuito para empezar.
6. Al finalizar, Render te dará una URL pública. Ej: `https://ape-whatsapp.onrender.com`

## 4) Conectar con Twilio (Sandbox de WhatsApp)
1. En Twilio Console → **Messaging → Try it out → WhatsApp Sandbox**.
2. Pegá en **"When a message comes in"** la URL:
   ```
   https://ape-whatsapp.onrender.com/whatsapp
   ```
3. Guardá.
4. En tu teléfono, uní el sandbox (enviá el código que muestra Twilio al número que te dan).
5. Enviá un WhatsApp al número de Twilio y APE te responderá.

## 5) Producción con número real
1. Pedí alta de WhatsApp Business API para tu número en Twilio.
2. Configurá el **Sender** (número) y reemplazá el webhook del sandbox por el del **sender real**.
3. Si en algún momento preferís enviar mensajes salientes con la API de Twilio, agregá `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` y usá `client.messages.create` en vez de TwiML.

## 6) Personalizar el comportamiento
- Editá `SYSTEM_PROMPT` en `app.py` para ajustar estilo y reglas.
- Cambiá `maxlen` de la memoria si querés más contexto por usuario.
- Ajustá `model`, `temperature` y `max_tokens` según costo y calidad.

## 7) Seguridad
- Para producción, validá la firma `X-Twilio-Signature` del request.
- Nunca expongas tu `OPENAI_API_KEY`.
- Activá HTTPS (Render ya te da HTTPS).

## 8) Prueba rápida (curl)
```bash
curl -X POST https://TU-URL-RENDER/whatsapp \
  -d "From=whatsapp:+5492317XXXXXX" \
  -d "Body=Matemática 3°: proporcionalidad. Dame idea de actividad breve."
```

¡Listo!
