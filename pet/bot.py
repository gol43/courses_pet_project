import os
import django
import uuid
from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          filters, ContextTypes, ConversationHandler)
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password
from api.models import User

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet.settings')
django.setup()

# Состояния разговора
EMAIL = range(1)


# Функции бота
async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Здравствуйте, введите свой email:')
    return EMAIL


async def handle_email(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    email = update.message.text

    # Генерация уникального пароля
    password = str(uuid.uuid4()).replace('-', '')

    # Хеширование пароля
    hashed_password = make_password(password)

    # Сохранение информации о пользователе в БД
    await sync_to_async(User.objects.create)(email=email,
                                             password=hashed_password)

    await update.message.reply_text(
        f'Вот ваш логин: {email}, и вот ваш пароль: {password}')
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(
        "6974658149:AAHQHnOCDBAGrQo6bXyh9_xF9j_7ovjjvsw").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   handle_email)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
