from telethon import TelegramClient, events
import os

# Telegram hisobingiz uchun ma'lumotlar
api_id = 'YOUR_API_ID'  # my.telegram.org saytidan olingan API ID
api_hash = 'YOUR_API_HASH'  # my.telegram.org saytidan olingan API Hash
phone_number = 'YOUR_PHONE_NUMBER'  # Telefon raqamingiz, masalan: '+123456789'

# Kalit so'zlar faylining nomi
keyword_file = 'keyWord.txt'

# Xabarni yuborish kerak bo'lgan guruh ID'si
target_group_id = -10012345678  # Xabar yuboriladigan guruh ID

# Kalit so'zlar ro'yxatini yuklash funksiyasi
def load_keywords():
    if not os.path.exists(keyword_file):
        return []
    with open(keyword_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]

# Yangi kalit so'zlarni faylga qo'shish funksiyasi
def add_keyword(new_keyword):
    with open(keyword_file, 'a', encoding='utf-8') as f:
        f.write(f'{new_keyword}\n')

# Telegram mijozini yaratish
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Kirish uchun raqamingizni ko'rsating
    await client.start(phone=phone_number)

    # Guruhlardagi barcha xabarlarni tinglash
    @client.on(events.NewMessage)
    async def handler(event):
        # Xabar matni
        message_text = event.raw_text

        # Kalit so'zlarni yuklash
        keywords = load_keywords()

        # Xabar ovozli bo'lsa (voice message)
        if event.message.voice:
            # Ovozli xabarni boshqa guruhga yuborish
            await client.send_message(target_group_id, "Yangi ovozli xabar!")
            await client.send_file(target_group_id, event.message.voice)
            print(f"Ovozli xabar yuborildi! Guruh ID: {event.chat_id}")

        # Agar kalit so'zlardan biri xabar matnida mavjud bo'lsa
        elif any(keyword.lower() in message_text.lower() for keyword in keywords):
            # Xabarni qaysi guruhdan kelganini chiqarish (guruh ID)
            group_id = event.chat_id
            print(f"Kalit so'z topildi! Guruh ID: {group_id}")
            
            # Xabarni boshqa guruhga yuborish
            await client.send_message(target_group_id, f"Yangi xabar: {message_text}")

        # Yangi kalit so'z qo'shish buyrug'i (masalan: /addword yangi_soz)
        if message_text.startswith('/addword'):
            # Buyruqdan so'nggi so'zni ajratib olish
            new_word = message_text.split(' ', 1)[1]
            add_keyword(new_word)
            await event.respond(f'Yangi kalit soʻz "{new_word}" qoʻshildi!')

    # Mijozni ishlatish
    await client.run_until_disconnected()

# Mijozni ishga tushirish
with client:
    client.loop.run_until_complete(main())
