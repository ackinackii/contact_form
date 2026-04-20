# Voice-Based Email System (Flask + Python)

This project implements a **voice-first email interface** intended to improve accessibility for visually impaired users.

## Objective coverage

1. **Analyse user challenges**
   - Conventional email clients depend heavily on visual scanning, mouse navigation, and dense layouts.
   - Keyboard-only flows still require memorizing many shortcuts and reading large text blocks.
   - Common pain points include identifying sender/subject quickly and avoiding accidental actions.

2. **Design intuitive voice interface (STT + TTS)**
   - **Speech-to-text**: browser Web Speech API captures command text.
   - **Text-to-speech**: browser SpeechSynthesis announces responses and inbox summaries.
   - UI is simple, high-contrast, keyboard-friendly, and exposes live regions for assistive tech.

3. **Implement core email functions by voice**
   - Compose/send
   - Read inbox summary
   - Reply
   - Delete

4. **Integrate secure authentication + SMTP/IMAP**
   - Uses SMTP (send/reply) and IMAP (read/delete).
   - Requires user email + app password (recommended by major providers).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Voice command examples

- `read inbox`
- `send email to friend@example.com subject Meeting update body We can meet tomorrow at 10`
- `reply to friend@example.com subject Re: Meeting update body Thanks, confirmed`
- `delete email 2`
- `help`

## Security notes

- Prefer app-specific passwords instead of your primary mailbox password.
- Avoid logging credentials.
- In production, move secrets to environment variables and deploy behind HTTPS.
