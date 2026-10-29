def process_download_and_send(message, query):
    chat_id = message.chat.id
    status_msg = bot.reply_to(message, f"🔍 **جاري البحث والتحميل عن:** `{query}` ...", parse_mode="Markdown")
    
    # روابط مباشرة لكبار القراء للتلاوات المباشرة (Mp3Quran)
    reciter_servers = {
        "ماهر المعيقلي": "https://server12.mp3quran.net/maher/",
        "عبد الباسط": "https://server7.mp3quran.net/basit/",
        "السديس": "https://server11.mp3quran.net/sds/",
        "ياسر الدوسري": "https://server11.mp3quran.net/yasser/",
        "العفاسي": "https://server8.mp3quran.net/afs/",
        "المنشاوي": "https://server10.mp3quran.net/minsh/"
    }

    # رابط مباشر لأداة yt-dlp في حال أرسل المستخدم رابط يوتيوب
    if query.startswith("http://") or query.startswith("https://"):
        file_prefix = f"islamic_{chat_id}_{random.randint(1000, 9999)}"
        output_template = f"{file_prefix}.%(ext)s"
        cmd = [
            "yt-dlp", "-f", "ba", "-o", output_template, query
        ]
        try:
            res = subprocess.run(cmd, timeout=60)
            files = [f for f in os.listdir('.') if f.startswith(file_prefix)]
            if files:
                audio_file = files[0]
                bot.edit_message_text("⬆️ **جاري رفع التسجيل الصوتي...**", chat_id, status_msg.message_id, parse_mode="Markdown")
                with open(audio_file, 'rb') as audio:
                    bot.send_audio(chat_id, audio, title="تسجيل إسلامي")
                os.remove(audio_file)
                bot.delete_message(chat_id, status_msg.message_id)
                return
        except Exception as e:
            pass

    # بحث عن اسم السورة للتحميل المباشر MP3
    surah_dict = {
        "الفاتحة": "001", "البقرة": "002", "آل عمران": "003", "النساء": "004", "المائدة": "005",
        "الأنعام": "006", "الأعراف": "007", "الأنفال": "008", "التوبة": "009", "يونس": "010",
        "هود": "011", "يوسف": "012", "الرعد": "013", "إبراهيم": "014", "الحجر": "015",
        "النحل": "016", "الإسراء": "017", "الكهف": "018", "مريم": "019", "طه": "020",
        "الأنبياء": "021", "الحج": "022", "المؤمنون": "023", "النور": "024", "الفرقان": "025",
        "الشعراء": "026", "النمل": "027", "القصص": "028", "العنكبوت": "029", "الروم": "030",
        "يس": "036", "الواقعة": "056", "الملك": "067", "النبأ": "078", "الإخلاص": "112",
        "الفلق": "113", "الناس": "114"
    }

    found_surah = None
    for name, num in surah_dict.items():
        if name in query:
            found_surah = num
            break

    found_server = "https://server12.mp3quran.net/maher/" # الافتراضي ماهر المعيقلي
    for r_name, r_url in reciter_servers.items():
        if r_name in query:
            found_server = r_url
            break

    if found_surah:
        audio_url = f"{found_server}{found_surah}.mp3"
        try:
            bot.edit_message_text("⬆️ **جاري جلب الملف الصوتي المباشر...**", chat_id, status_msg.message_id, parse_mode="Markdown")
            bot.send_audio(chat_id, audio_url, title=f"سورة {query}")
            bot.delete_message(chat_id, status_msg.message_id)
            return
        except Exception as e:
            pass

    bot.edit_message_text("⚠️ **لم يتم العثور على التلاوة.**\n💡 أرسل رابط يوتيوب مباشر أو اكتب اسم السورة والقارئ (مثال: `سورة الملك ماهر المعيقلي` أو `سورة الكهف السديس`).", chat_id, status_msg.message_id, parse_mode="Markdown")
