SENSITIVE_LOG_FIELDS = {
    "authorization",
    "access_token",
    "refresh_token",
    "session_token",
    "otp",
    "phone",
    "address",
    "card_number",
    "payment_credential",
}


def redact_sensitive_fields(payload: dict) -> dict:
    redacted = {}
    for key, value in payload.items():
        if key.lower() in SENSITIVE_LOG_FIELDS:
            redacted[key] = "[REDACTED]"
        else:
            redacted[key] = value
    return redacted
