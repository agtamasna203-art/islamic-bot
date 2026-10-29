import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import subprocess
import random
import threading
import requests
import urllib.parse
import time

TOKEN = "9123171463:AAEcp4WbW4rzWkJ0pX5P1UgV7Y_pREJlEvQ"
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=16)

active_chats = set()

PRO_MAX_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Android 14; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0"
]

AUTO_AZKAR = [
    "🌅 **من أذكار الصباح:** «أَصْبَحْنَا وَأَصْبَحَ المُلْكُ للَّهِ، وَالحَمْدُ للَّهِ، لاَ إلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ»",
    "🏙️ **من أذكار المساء:** «أَمْسَيْنَا وَأَمْسَى المُلْكُ للَّهِ، وَالحَمْدُ للَّهِ، لاَ إلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ»",
    "💎 **فضل الذكر:** «سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ العَظِيمِ»",
    "🕊️ **الصلاة على النبي:** «اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى نَبِيِّنَا مُحَمَّدٍ»",
    "🤍 **الاستغفار:** «أَسْتَغْفِرُ اللَّهَ الْعَظِيمَ الَّذِي لاَ إِلَهَ إِلاَّ هُوَ الْحَيَّ الْقَيُّومَ وَأَتُوبُ إِلَيْهِ»",
    "🛡️ **من أذكار الوقاية:** «أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ»",
    "🌿 **الباقيات الصالحات:** «سُبْحَانَ اللَّهِ، وَالْحَمْدُ لِلَّهِ، وَلاَ إِلَهَ إِلاَّ اللَّهُ، وَاللَّهُ أَكْبَرُ»",
    "✨ **الحوقلة:** «لاَ حَوْلَ وَلاَ قُوَّةَ إِلاَّ بِاللَّهِ الْعَلِيِّ الْعَظِيمِ»"
]

def auto_azkar_loop():
    while True:
        time.sleep(300)
        if not active_chats:
            continue
        selected_zikr = random.choice(AUTO_AZKAR)
        reminder_text = (
            f"🔔 **تذكير دوري بالأذكار (كل 5 دقائق)** 🌿\n\n"
            f"{selected_zikr}\n\n"
            f"🤲 *اللهم اغفر لـ **فؤاد القريشي** ولوالديه وللمؤمنين والمؤمنات.*"
        )
        for chat_id in list(active_chats):
            try:
                bot.send_message(chat_id, reminder_text, parse_mode="Markdown")
            except Exception:
                pass

threading.Thread(target=auto_azkar_loop, daemon=True).start()

def main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("📖 القرآن الكريم", callback_data="quran_menu")
    b2 = InlineKeyboardButton("📜 الأحاديث النبوية", callback_data="hadith_menu")
    b3 = InlineKeyboardButton("🤲 الأذكار والأدعية", callback_data="azkar_menu")
    b4 = InlineKeyboardButton("🕌 قصص الأنبياء والسيرة", callback_data="stories_menu")
    b5 = InlineKeyboardButton("🔍 بحث وتحميل صوتي", callback_data="search_info")
    b6 = InlineKeyboardButton("🤍 صدقة جارية والدعاء", callback_data="sadaka_info")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b6)
    return markup

def quran_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("🎧 كبار القراء", callback_data="q_reciters")
    b2 = InlineKeyboardButton("📖 قراءة المصحف", callback_data="q_read")
    b3 = InlineKeyboardButton("💡 التفسير الميسر", callback_data="q_tafsir")
    b4 = InlineKeyboardButton("⬇️ تحميل سورة صوتياً", callback_data="q_download_info")
    back = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(back)
    return markup

def reciters_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("عبد الباسط عبد الصمد", callback_data="rec_basit")
    b2 = InlineKeyboardButton("عبد الرحمن السديس", callback_data="rec_sudais")
    b3 = InlineKeyboardButton("ماهر المعيقلي", callback_data="rec_maher")
    b4 = InlineKeyboardButton("ياسر الدوسري", callback_data="rec_yasser")
    b5 = InlineKeyboardButton("محمد صديق المنشاوي", callback_data="rec_minshawi")
    b6 = InlineKeyboardButton("مشاري العفاسي", callback_data="rec_afasy")
    back = InlineKeyboardButton("🔙 قائمة القرآن", callback_data="quran_menu")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5, b6)
    markup.add(back)
    return markup

def hadith_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton("✨ الأربعون النووية كاملة", callback_data="h_nawawi")
    b2 = InlineKeyboardButton("💎 جوامع كلم النبي ﷺ", callback_data="h_jawami")
    b3 = InlineKeyboardButton("📚 أحاديث في فضائل الأعمال", callback_data="h_fadail")
    back = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
    markup.add(b1, b2, b3, back)
    return markup

def azkar_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("🌅 أذكار الصباح", callback_data="az_sabah")
    b2 = InlineKeyboardButton("🏙️ أذكار المساء", callback_data="az_masaa")
    b3 = InlineKeyboardButton("🌙 أذكار النوم", callback_data="az_nowm")
    b4 = InlineKeyboardButton("🛡️ الرقية الشرعية", callback_data="az_roqya")
    back = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(back)
    return markup

def stories_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton("آدم عليه السلام", callback_data="s_adam")
    b2 = InlineKeyboardButton("نوح عليه السلام", callback_data="s_nuh")
    b3 = InlineKeyboardButton("إبراهيم عليه السلام", callback_data="s_ibrahim")
    b4 = InlineKeyboardButton("موسى عليه السلام", callback_data="s_musa")
    b5 = InlineKeyboardButton("عيسى عليه السلام", callback_data="s_isa")
    b6 = InlineKeyboardButton("محمد ﷺ (السيرة)", callback_data="s_muhammad")
    back = InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(back)
    return markup

def search_wikipedia_islamic(query):
    try:
        url = f"https://ar.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        res = requests.get(url, timeout=5).json()
        if 'extract' in res and res['extract']:
            return res['extract']
    except Exception:
        pass
    return None

def process_download_and_send(message, query):
    chat_id = message.chat.id
    status_msg = bot.reply_to(message, f"🔍 **جاري البحث في المكتبة الصوتية عن:** `{query}` ...", parse_mode="Markdown")
    
    info_text = search_wikipedia_islamic(query)
    if info_text:
        bot.send_message(chat_id, f"📖 **نبذة معرفية:**\n\n{info_text[:900]}")

    file_prefix = f"islamic_{chat_id}_{random.randint(1000, 9999)}"
    output_template = f"{file_prefix}.%(ext)s"

    if query.startswith("http://") or query.startswith("https://"):
        cmd = [
            "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--user-agent", random.choice(PRO_MAX_USER_AGENTS),
            "-o", output_template, query
        ]
    else:
        cmd = [
            "yt-dlp", "-x", "--audio-format", "mp3", "--audio-quality", "0",
            "--user-agent", random.choice(PRO_MAX_USER_AGENTS),
            "-o", output_template, f"ytsearch1:{query}"
        ]

    try:
        res = subprocess.run(cmd)
        expected_file = f"{file_prefix}.mp3"
        
        if res.returncode == 0 and os.path.exists(expected_file):
            bot.edit_message_text("⬆️ **جاري رفع التسجيل الصوتي إليك مباشرة...**", chat_id, status_msg.message_id, parse_mode="Markdown")
            with open(expected_file, 'rb') as audio:
                bot.send_audio(chat_id, audio, title=query[:40])
            os.remove(expected_file)
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("⚠️ تعذر جلب التسجيل الصوتي. يرجى كتابة اسم أكثر دقة.", chat_id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ أثناء المعالجة: {e}", chat_id, status_msg.message_id)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    active_chats.add(message.chat.id)
    welcome_text = (
        "✨ **أهلاً بك في البوت الإسلامي الشامل** 🌿\n\n"
        "قال رسول الله ﷺ: *«إِذَا مَاتَ الإِنْسَانُ انْقَطَعَ عَنْهُ عَمَلُهُ إِلاَّ مِنْ ثَلاَثٍ: إِلاَّ مِنْ صَدَقَةٍ جَارِيَةٍ، أَوْ عِلْمٍ يُنْتَفَعُ بِهِ، أَوْ وَلَدٍ صَالِحٍ يَدْعُو لَهُ»*\n\n"
        "🤲 **دعاء لصاحب البوت:**\n"
        "«اللهم اغفر لصاحب هذا العمل **فؤاد القريشي** ولوالديه، وبارك له في رزقه وعمره، واجعل هذا البوت صدقة جارية له في حياته وبعد مماته».\n\n"
        "⏰ *تم تفعيل التذكير التلقائي بالأذكار والدعاء كل 5 دقائق.*\n\n"
        "اختر من القوائم التالية للوصول للقرآن، الأحاديث، الأذكار، والقصص:"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    active_chats.add(chat_id)
    msg_id = call.message.message_id

    if call.data == "main_menu":
        bot.edit_message_text("اختر من القوائم التالية:", chat_id, msg_id, reply_markup=main_menu())
    elif call.data == "quran_menu":
        bot.edit_message_text("📖 **قسم القرآن الكريم:** اختر ما تريد الوصول إليه:", chat_id, msg_id, parse_mode="Markdown", reply_markup=quran_menu())
    elif call.data == "q_reciters":
        bot.edit_message_text("🎧 **اختر القارئ المفضّل لاستماع التلاوات:**", chat_id, msg_id, parse_mode="Markdown", reply_markup=reciters_menu())
    elif call.data.startswith("rec_"):
        reciter_names = {
            "rec_basit": "عبد الباسط عبد الصمد", "rec_sudais": "عبد الرحمن السديس",
            "rec_maher": "ماهر المعيقلي", "rec_yasser": "ياسر الدوسري",
            "rec_minshawi": "محمد صديق المنشاوي", "rec_afasy": "مشاري العفاسي"
        }
        name = reciter_names.get(call.data, "القارئ")
        bot.send_message(chat_id, f"🎧 **للاستماع للقارئ {name}:**\nاكتب في المحادثة اسم السورة مع اسم القارئ (مثال: `سورة الملك {name}`) وسيرسلها البوت كملف MP3 فوراً!")
    elif call.data == "q_read":
        bot.send_message(chat_id, "📖 **قراءة المصحف الشريف كاملاً برواية حفص:**\n• [مجمع الملك فهد لطباعة المصحف الشريف](https://qurancomplex.gov.sa)\n• [المصحف الإلكتروني بجامعة الملك سعود](https://quran.ksu.edu.sa)", parse_mode="Markdown")
    elif call.data == "q_tafsir":
        bot.send_message(chat_id, "💡 **التفسير الميسر وتفسير ابن كثير:**\nاكتب اسم الآية أو السورة متبوعة بكلمة تفسير (مثال: `تفسير سورة الإخلاص`) وسيجلب البوت الشرح لك.")
    elif call.data == "q_download_info":
        bot.send_message(chat_id, "⬇️ **تحميل السور والتلاوات:**\nأرسل اسم أي سورة أو قارئ مباشرة دون الحاجة لأزرار وسيقوم البوت بجلب الملف الصوتي وإرساله لك.")
    elif call.data == "hadith_menu":
        bot.edit_message_text("📜 **قسم الأحاديث النبوية والشريفة:**", chat_id, msg_id, parse_mode="Markdown", reply_markup=hadith_menu())
    elif call.data == "h_nawawi":
        txt = "✨ **الحديث الأول من الأربعين النووية:**\nعن أمير المؤمنين عمر بن الخطاب رضي الله عنه قال: سمعت رسول الله ﷺ يقول:\n«إنَّما الأَعْمالُ بالنِّيَّاتِ...» [متفق عليه]"
        bot.send_message(chat_id, txt)
    elif call.data == "h_jawami":
        txt = "💎 **من جوامع كلم النبي ﷺ:**\nقال رسول الله ﷺ:\n«اتَّقِ اللَّهِ حَيْثُمَا كُنْتَ، وَأَتْبِعِ السَّيِّئَةَ الْحَسَنَةَ تَمْحُهَا، وَخَالِقِ النَّاسَ بِخُلُقٍ حَسَنٍ» [رواه الترمذي]"
        bot.send_message(chat_id, txt)
    elif call.data == "h_fadail":
        txt = "📚 **في فضل الذكر والدعاء:**\nقال رسول الله ﷺ:\n«كَلِمَتَانِ خَفِيفَتَانِ عَلَى اللِّسَانِ، ثَقِيلَتَانِ فِي المِيزَانِ، حَبِيبَتَانِ إِلَى الرَّحْمَنِ: سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ العَظِيمِ» [متفق عليه]"
        bot.send_message(chat_id, txt)
    elif call.data == "azkar_menu":
        bot.edit_message_text("🤲 **قسم الأذكار والرقية الشرعية:**", chat_id, msg_id, parse_mode="Markdown", reply_markup=azkar_menu())
    elif call.data == "az_sabah":
        txt = "🌅 **من أذكار الصباح:**\n• «أَصْبَحْنَا وَأَصْبَحَ المُلْكُ للَّهِ، وَالحَمْدُ للَّهِ، لاَ إلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ»\n• «اللَّهُمَّ بكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ»"
        bot.send_message(chat_id, txt)
    elif call.data == "az_masaa":
        txt = "🏙️ **من أذكار المساء:**\n• «أَمْسَيْنَا وَأَمْسَى المُلْكُ للَّهِ، وَالحَمْدُ للَّهِ، لاَ إلَهَ إلاَّ اللَّهُ وَحْدَهُ لاَ شَرِيكَ لَهُ»\n• «أَعُوذُ بِكَلِمَاتِ اللهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ» (3 مرات)"
        bot.send_message(chat_id, txt)
    elif call.data == "az_nowm":
        txt = "🌙 **أذكار النوم:**\n• قراءة آية الكرسي والمعوذتين.\n• «بِاسْمِكَ رَبِّي وَضَعْتُ جَنْبِي، وَبِكَ أَرْفَعُهُ، إنْ أَمْسَكْتَ نَفْسِي فَارْحَمْهَا، وَإنْ أَرْسَلْتَهَا فَاحْفَظْهَا بِمَا تَحْفَظُ بِهِ عِبَادَكَ الصَّالِحِينَ»"
        bot.send_message(chat_id, txt)
    elif call.data == "az_roqya":
        txt = "🛡️ **الرقية الشرعية من الكتاب والسنة:**\n• قراءة سورة الفاتحة وآية الكرسي وخواتيم سورة البقرة.\n• «أَذْهِبِ البَاسَ رَبَّ النَّاسِ، واشْفِ أَنْتَ الشَّافِي، لاَ شِفَاءَ إِلاَّ شِفَاؤُكَ»"
        bot.send_message(chat_id, txt)
    elif call.data == "stories_menu":
        bot.edit_message_text("🕌 **قصص الأنبياء عليهم السلام:**", chat_id, msg_id, parse_mode="Markdown", reply_markup=stories_menu())
    elif call.data == "s_adam":
        bot.send_message(chat_id, "📖 **قصة آدم عليه السلام:** أول الأنبياء وخلق البشرية.")
    elif call.data == "s_nuh":
        bot.send_message(chat_id, "📖 **قصة نوح عليه السلام:** شيخ الأنبياء وصاحب السفينة.")
    elif call.data == "s_ibrahim":
        bot.send_message(chat_id, "📖 **قصة إبراهيم عليه السلام:** خليل الرحمن وباني البيت الحرام.")
    elif call.data == "s_musa":
        bot.send_message(chat_id, "📖 **قصة موسى عليه السلام:** كليم الله ومواجه فرعون.")
    elif call.data == "s_isa":
        bot.send_message(chat_id, "📖 **قصة عيسى عليه السلام:** كلمة الله ورسوله.")
    elif call.data == "s_muhammad":
        bot.send_message(chat_id, "📖 **السيرة النبوية:** نبينا محمد ﷺ خاتم الأنبياء والمرسلين.")
    elif call.data == "search_info":
        bot.send_message(chat_id, "🔍 **البحث والتحميل:** أرسل اسم أي شيخ، سورة، أو خطبة في المحادثة مباشرة وسأقوم برفعها لك كملف MP3.")
    elif call.data == "sadaka_info":
        txt = (
            "🤍 **هذا البوت صدقة جارية** 🤍\n\n"
            "تم إنشاء هذا البوت ليكون خادماً لكتاب الله وسنة نبيه المصطفى ﷺ وصدقة جارية عن الأخ الكريم **فؤاد القريشي** وعن والديه وأهله وكل من استخدمه وساهم في نشره.\n\n"
            "🤲 **دعاء للصاحب والقائمين على البوت:**\n"
            "«اللهم اغفر لـ **فؤاد القريشي** ولوالديه، واجعل هذا العمل في ميزان حسناته، وبارك له في رزقه وعمره وصحته، واجعله نوراً له في الدنيا والآخرة» 🌿"
        )
        bot.send_message(chat_id, txt, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    active_chats.add(message.chat.id)
    threading.Thread(target=process_download_and_send, args=(message, message.text.strip())).start()

bot.infinity_polling(timeout=10, long_polling_timeout=5)
