import codecs


def quote_identifier(s, errors="strict"):
    encodable = s.encode("utf-8", errors).decode("utf-8")
    return "\"" + encodable.replace("\"", "\"\"") + "\""
