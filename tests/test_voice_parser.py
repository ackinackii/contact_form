from voice_assistant import VoiceCommandParser


def test_parse_send_email_command():
    parser = VoiceCommandParser()
    parsed = parser.parse("send email to user@example.com subject Greetings body Hello there")

    assert parsed is not None
    assert parsed.intent == "send"
    assert parsed.args["to"] == "user@example.com"
    assert parsed.args["subject"] == "Greetings"
    assert parsed.args["body"] == "Hello there"


def test_parse_read_inbox_command():
    parser = VoiceCommandParser()
    parsed = parser.parse("read inbox")

    assert parsed is not None
    assert parsed.intent == "read_inbox"
