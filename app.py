from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from config import settings
from email_client import EmailClient, MailCredentials
from voice_assistant import VoiceCommandParser

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.secret_key

email_client = EmailClient(
    smtp_server=settings.smtp_server,
    smtp_port=settings.smtp_port,
    imap_server=settings.imap_server,
    imap_port=settings.imap_port,
)
parser = VoiceCommandParser()


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/command")
def handle_command():
    data = request.get_json(silent=True) or {}
    command = data.get("command", "")
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    parsed = parser.parse(command)
    if not parsed:
        return jsonify({"response": "I did not hear a command. Please try again."}), 400

    if parsed.intent == "help":
        return jsonify(
            {
                "response": (
                    "Available commands: read inbox, send email to <address> subject <text> body <text>, "
                    "reply to <address> subject <text> body <text>, and delete email <number>."
                )
            }
        )

    if not email or not password:
        return jsonify({"response": "Please provide your email and app password first."}), 400

    creds = MailCredentials(address=email, password=password)

    try:
        if parsed.intent == "read_inbox":
            messages = email_client.fetch_inbox(creds)
            if not messages:
                return jsonify({"response": "Your inbox is empty."})

            readout = [
                f"Email {index + 1} from {msg.sender}, subject {msg.subject}."
                for index, msg in enumerate(messages)
            ]
            return jsonify({"response": " ".join(readout)})

        if parsed.intent == "send":
            email_client.send_email(
                creds,
                to=parsed.args["to"],
                subject=parsed.args["subject"],
                body=parsed.args["body"],
            )
            return jsonify({"response": "Email sent successfully."})

        if parsed.intent == "reply":
            email_client.reply_email(
                creds,
                to=parsed.args["to"],
                subject=parsed.args["subject"],
                body=parsed.args["body"],
            )
            return jsonify({"response": "Reply sent successfully."})

        if parsed.intent == "delete":
            messages = email_client.fetch_inbox(creds)
            requested = int(parsed.args["index"])
            if requested < 1 or requested > len(messages):
                return jsonify({"response": f"Email number {requested} does not exist."}), 400

            uid = messages[requested - 1].uid
            email_client.delete_email(creds, uid)
            return jsonify({"response": f"Email {requested} deleted successfully."})

        return jsonify(
            {
                "response": (
                    "Sorry, I could not understand that command. Say help to hear valid commands."
                )
            }
        ), 400

    except Exception as exc:
        return jsonify({"response": f"I hit an error while processing email: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
