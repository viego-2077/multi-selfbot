name = "thelp"

async def run(message, args):
    langs = [
        ("af", "Afrikaans"), ("ar", "Arabic"), ("bn", "Bengali"),
        ("zh-cn", "Chinese (Simplified)"), ("zh-tw", "Chinese (Traditional)"), ("cs", "Czech"),
        ("da", "Danish"), ("nl", "Dutch"), ("en", "English"),
        ("fi", "Finnish"), ("fr", "French"), ("de", "German"),
        ("el", "Greek"), ("he", "Hebrew"), ("hi", "Hindi"),
        ("hu", "Hungarian"), ("id", "Indonesian"), ("it", "Italian"),
        ("ja", "Japanese"), ("ko", "Korean"), ("la", "Latin"),
        ("ms", "Malay"), ("no", "Norwegian"), ("pl", "Polish"),
        ("pt", "Portuguese"), ("ro", "Romanian"), ("ru", "Russian"),
        ("es", "Spanish"), ("sv", "Swedish"), ("th", "Thai"),
        ("tr", "Turkish"), ("uk", "Ukrainian"), ("ur", "Urdu"),
        ("vi", "Vietnamese")
    ]

    
    lines = []
    for i in range(0, len(langs), 3):
        group = " | ".join([f"{code} → {name}" for code, name in langs[i:i+3]])
        lines.append(group)

    formatted = "\n".join(lines)
    await message.channel.send(f"**Danh sách mã ngôn ngữ phổ biến:**\n{formatted}")
