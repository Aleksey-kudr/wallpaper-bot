from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
KeyboardButton, ReplyKeyboardMarkup

inline_btn_start = InlineKeyboardButton('ПРОДОЛЖИТЬ', callback_data='start')
inline_start = InlineKeyboardMarkup().add(inline_btn_start)

inline_btn_money_KZT = InlineKeyboardButton('Тенге (KZT)', callback_data='mon_KZT')
inline_btn_money_UAH = InlineKeyboardButton('Гривна (UAH)', callback_data='mon_UAH')
inline_btn_money_RUB = InlineKeyboardButton('Рубль (RUB)', callback_data='mon_RUB')
inline_btn_money_BYN = InlineKeyboardButton('Белорусский рубль (BYN)', callback_data='mon_BYN')
inline_btn_money_EUR = InlineKeyboardButton('Евро (EUR)', callback_data='mon_EUR')
inline_select_money = InlineKeyboardMarkup(row_width=1).add(inline_btn_money_KZT, inline_btn_money_UAH, inline_btn_money_RUB, inline_btn_money_BYN, inline_btn_money_EUR)

inline_btn_get = InlineKeyboardButton('ПОЛУЧИТЬ', callback_data='get')
inline_get = InlineKeyboardMarkup().add(inline_btn_get)

inline_btn_check_subscription = InlineKeyboardButton('Проверить подписку', callback_data='check')
inline_checked_get = InlineKeyboardMarkup().add(inline_btn_check_subscription)

kb_btn_create_mailing = KeyboardButton('Создать рассылку')
kb_btn_delete_mailing = KeyboardButton('Удалить рассылку')
kb_btn_add_channel = KeyboardButton('Добавить канал')
kb_btn_delete_channel = KeyboardButton('Удалить канал')
reply_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(kb_btn_create_mailing, kb_btn_delete_mailing, kb_btn_add_channel, kb_btn_delete_channel)

inline_btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
inline_btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
inline_select_mailing = InlineKeyboardMarkup().add(inline_btn_confirm, inline_btn_cancel)

def create_markup(channel_array):
    inline_channels = InlineKeyboardMarkup()
    for channel in channel_array:
        inline_btn_channel = InlineKeyboardButton(channel[0], callback_data = channel[1])
        inline_channels.add(inline_btn_channel)
    return inline_channels