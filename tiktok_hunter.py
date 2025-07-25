import requests
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
import random
import string

# إعدادات التليجرام
api_id = '21913360'
api_hash = '8aa8c90fd90d1c959e64a2071e617f1f'
bot_token =" 7571493494:AAEHYaE5lykHbUEGm7_fx-0f4kLODlshHj8"
phone_number = "+9647885888788"

# وقت الانتظار بين الطلبات (بالثواني)
REQUEST_DELAY = 3  # يمكنك تغيير هذه القيمة

# دالة التحقق من اليوزر مع إضافة تأخير
def check_username_availability(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # إضافة تأخير قبل كل طلب
    time.sleep(REQUEST_DELAY)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 404
    except Exception as e:
        print(f"Error checking @{username}: {str(e)}")
        return False

# دالة توليد اليوزرات مع تحسين الأداء
def generate_4char_usernames(limit=50):
    usernames = []
    chars = string.ascii_lowercase + string.digits + '_'
    
    print(f"جاري البحث عن {limit} يوزر متاح...")
    
    while len(usernames) < limit:
        username = ''.join(random.choice(chars) for _ in range(4))
        if check_username_availability(username):
            usernames.append(username)
            print(f"✅ وجدنا يوزر متاح: @{username} (عدد اليوزرات المتبقية: {limit-len(usernames)})")
    
    return usernames

# إرسال النتائج مع تأخير بين الرسائل
def send_to_telegram(usernames):
    with TelegramClient('session_name', api_id, api_hash) as client:
        client.start(phone=phone_number)
        
        for i, username in enumerate(usernames, 1):
            message = f"🎯 يوزر تيك توك متاح:\n@{username}\nرابط الحساب: https://www.tiktok.com/@{username}"
            
            try:
                client(SendMessageRequest(
                    peer='YOUR_BOT_USERNAME',
                    message=message
                ))
                print(f"تم إرسال اليوزر {i}/{len(usernames)} إلى البوت")
                
                # تأخير بين إرسال كل يوزر
                if i < len(usernames):
                    time.sleep(2)
                    
            except Exception as e:
                print(f"فشل إرسال اليوزر @{username}: {str(e)}")

# التنفيذ الرئيسي
if __name__ == '__main__':
    try:
        print("بدء عملية البحث عن يوزرات متاحة...")
        available_usernames = generate_4char_usernames(limit=20)
        
        if available_usernames:
            print("\nتم العثور على اليوزرات التالية:")
            for uname in available_usernames:
                print(f"@{uname}")
                
            print("\nجاري إرسال النتائج إلى البوت...")
            send_to_telegram(available_usernames)
            print("تم الانتهاء بنجاح!")
        else:
            print("لم يتم العثور على أي يوزرات متاحة")
            
    except KeyboardInterrupt:
        print("\nتم إيقاف البرنامج بواسطة المستخدم")
    except Exception as e:
        print(f"حدث خطأ غير متوقع: {str(e)}")