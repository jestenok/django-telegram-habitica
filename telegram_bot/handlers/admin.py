import datetime
from django.utils.timezone import now

# Telegram imports
import telegram

# Local imports
from telegram_bot.handlers import static_text
from telegram_bot.models import User

def admin(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text('Недостаточно прав!')

    return update.message.reply_text(static_text.secret_admin_commands)
    

def stats(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text('Недостаточно прав!')

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(updated_at__gte=now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text, 
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )

