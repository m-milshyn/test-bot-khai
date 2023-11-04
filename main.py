import telebot
import gspread
from telebot import types
import time
from datetime import datetime

sa = gspread.service_account(filename="gentle-bot-389616-bcfea1c7d626.json")
sh = sa.open("BOT sheets data")
sheetDekanat = sh.worksheet("DekanatContact")
sheetDepart = sh.worksheet("Profcom faculty&department")
sheetSocial = sh.worksheet("Social")
sheetContest = sh.worksheet("Contest")
sheetDoc = sh.worksheet("Regulatory documents")
sheetRequisites = sh.worksheet("Requisites")
sheetFAQ = sh.worksheet("FAQ")
token = '5779680701:AAG-9j4Yq5X2vTPY087O05rOlUcOc6_zl68'
bot = telebot.TeleBot(token)
TO_CHAT_ID = -1001848377879
dev_chat_id = 338497309
check_num = False
contests = []
FAQs = []
message_appeals = ""
chosen_contest = " "
found_contest = None
localsheets = None
allowed_values = [
    "Конкурси",
    "Головне меню",
    "Відправити",
    "Запитай Профком студентів ХАІ",
    "Повідомити про технічну помилку",
    "Зв’язок та соціальні мережі",
    "Пропозиції Та Скарги",
    "Профбюро студентів та департаменти ППОС НАУ \"ХАІ\"",
    "СТОП"
]


class Contest:
    def __init__(self, name, start_date, end_date, description):
        self.name = name
        self.hashtag = "#" + name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description


class FAQ_data:
    def __init__(self, number, question, answer, link):
        self.number = number
        self.question = question
        self.answer = answer
        if link:
            self.link = link
        else:
            self.link = None


class Appeals:
    def __init__(self, name, hashtag, chat_id):
        self.name = name
        self.hashtag = hashtag
        self.chat_id = chat_id


appeals_data = [
    Appeals("Запитай Профком студентів ХАІ", "#ПитанняПрофкому", TO_CHAT_ID),
    Appeals("Пропозиції та скарги", "#ПропозиціїТаСкарги", TO_CHAT_ID),
    Appeals("Повідомити про технічну помилку", "#ПовідомитиПроПомилку", dev_chat_id)]


def telegram_bot():
    @bot.message_handler(commands=["start"])
    def send_welcome(message: types.Message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton("Конкурси"),
                   types.KeyboardButton("Положення"),
                   types.KeyboardButton("Реквізити"),
                   types.KeyboardButton("Запитай Профком студентів ХАІ"),
                   types.KeyboardButton("Повідомити про технічну помилку"),
                   types.KeyboardButton("Пропозиції та скарги"),
                   types.KeyboardButton("Зв’язок з деканатом та соціальні мережі"),
                   types.KeyboardButton("Питання/відповідь"),
                   types.KeyboardButton("Профбюро студентів та департаменти ППОС НАУ \"ХАІ\""))
        chat_message = "Обери пункт, який тобі необхіден"
        bot.send_message(message.chat.id, "Привіт, хайовець!\n"
                                          "Тебе вітає Профком студентів ХАІ! ✌️ ")
        bot.send_message(message.chat.id, chat_message, reply_markup=markup)

    def faculty_profcom(message):
        localsheet_dict = {sheet["Назва підрозділу"]: sheet for sheet in localsheets}

        if message.text in localsheet_dict:
            sheet = localsheet_dict[message.text]
            textMessage = f'{sheet["Назва підрозділу"]}\n\n{sheet["Основний текст про підрозділ"]}\n\n{sheet["Контакти та ПІБ"]}'
            bot.send_message(message.chat.id, textMessage)
            bot.register_next_step_handler(message, faculty_profcom)
        else:
            func(message)

    def social_and_dekanat(message):
        global localsheets
        if message.text == "Соціальні мережі ППОС НАУ \"ХАІ\"":
            localsheets = sheetSocial.get_all_records()
            bot.send_message(message.chat.id, "Почекайте, оновлюємо інформацію")
            for localsheet in localsheets:
                textMessage = localsheet["Факультет"] + ":\n"
                if localsheet["Instagram username"].__len__() != 0 and localsheet["Instagram link"].__len__() != 0:
                    textMessage += f'Instagram: [{localsheet["Instagram username"]}]({localsheet["Instagram link"]})\n'
                if localsheet["Telegram username"].__len__() != 0 and localsheet["Telegram link"].__len__() != 0:
                    textMessage += f'Telegram: [{localsheet["Telegram username"]}]({localsheet["Telegram link"]})\n'
                if localsheet["Tiktok username"].__len__() != 0 and localsheet["Tiktok link"].__len__() != 0:
                    textMessage += f'Tiktok: [{localsheet["Tiktok username"]}]({localsheet["Tiktok link"]})\n'
                if localsheet["Website"].__len__() != 0 and localsheet["Website link"].__len__() != 0:
                    textMessage += f'Website: [{localsheet["Website"]}]({localsheet["Website link"]})\n'
                bot.send_message(message.chat.id, textMessage, parse_mode="Markdown")
            bot.register_next_step_handler(message, social_and_dekanat)
        elif message.text == "Зв’язок з деканатами":
            bot.send_message(message.chat.id, "Почекайте, оновлюємо інформацію")
            localsheets = sheetDekanat.get_all_records()
            for localsheet in localsheets:
                textMessage = f'{localsheet["Факультет"]} \n\nКонтакти:\n{localsheet["Контакти"]}\n\nЧас роботи:\n{localsheet["Час роботи"]}'
                bot.send_message(message.chat.id, textMessage)
                time.sleep(1)
            bot.register_next_step_handler(message, social_and_dekanat)
        else:
            func(message)

    def check(message):
        return message.text not in allowed_values

    def req_(message):
        for localsheet in localsheets:
            if message.text == localsheet.get("Назва"):
                rec_message = localsheet.get("Опис")
                bot.send_message(message.chat.id, rec_message)
                bot.register_next_step_handler(message, req_)
        func(message)

    def question(message):
        global check_num
        if check(message):
            for data in appeals_data:
                if data.name == message_appeals:
                    if not check_num:
                        bot.send_message(data.chat_id, data.hashtag)
                        check_num = True
                    bot.forward_message(data.chat_id, message.chat.id, message.message_id)
                    bot.register_next_step_handler(message, question)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def FAQ(message):
        if message.text == "Головне меню":
            func(message)
        answer_text = f""
        for data in FAQs:
            if str(data.number) == message.text:
                answer_text += f"{data.answer}"
                if data.link is not None:
                    answer_text += f'\n\n{data.link}'
                bot.send_message(message.chat.id, answer_text)
                bot.register_next_step_handler(message, FAQ)

    def contest_send(message):
        global check_num
        if check(message):
            if not check_num:
                bot.send_message(TO_CHAT_ID, found_contest.hashtag)
                check_num = True
            bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, contest_send)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def check_contest():
        global found_contest
        for contest in contests:
            if contest.name == chosen_contest:
                found_contest = contest
                return True
        return False

    def contest_func(message):
        global chosen_contest
        global found_contest
        global check_num
        check_num = False
        chosen_contest = message.text
        current_datetime = datetime.now()
        if check_contest():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(types.KeyboardButton("Відправити"),
                       types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, found_contest.description, parse_mode="Markdown", reply_markup=markup)
            bot.register_next_step_handler(message, contest_func)
        if message.text == "Відправити":
            if found_contest.start_date <= current_datetime <= found_contest.end_date:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton("СТОП")
                markup.add(btn)
                bot.send_message(message.chat.id, "Щоб завершити подачу заявки натисніть на кнопку \"СТОП\"",
                                 reply_markup=markup)
                bot.register_next_step_handler(message, contest_send)
            elif found_contest.start_date > current_datetime:
                bot.send_message(message.chat.id, f"‼️Подачу заявок ще не розпочато‼️\n "
                                                  f"Конкурс буде проводитися з {found_contest.start_date} до {found_contest.end_date} включно")
                bot.register_next_step_handler(message, contest_func)
            else:
                bot.send_message(message.chat.id, f"‼️Подачу заявок припинено‼️\n "
                                                  f"Конкурс проводився з {found_contest.start_date} до {found_contest.end_date} включно")
                bot.register_next_step_handler(message, contest_func)
        elif message.text == "Головне меню":
            func(message)

    @bot.message_handler(
        content_types=['text', "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location",
                       "contact",
                       "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                       "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                       "migrate_from_chat_id", "pinned_message"])
    def func(message):
        global check_num
        global localsheets
        global message_appeals
        if message.text == "Головне меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(types.KeyboardButton("Конкурси"),
                       types.KeyboardButton("Положення"),
                       types.KeyboardButton("Реквізити"),
                       types.KeyboardButton("Запитай Профком студентів ХАІ"),
                       types.KeyboardButton("Повідомити про технічну помилку"),
                       types.KeyboardButton("Пропозиції та скарги"),
                       types.KeyboardButton("Зв’язок з деканатом та соціальні мережі"),
                       types.KeyboardButton("Питання/відповідь"),
                       types.KeyboardButton("Профбюро студентів та департаменти ППОС НАУ \"ХАІ\""))
            chat_message = "Головне меню:\n" \
                           "1. Конкурси\n" \
                           "2. Положення\n" \
                           "3. Реквізити\n" \
                           "4. Запитай Профком студентів ХАІ\n" \
                           "5. Повідомити про технічну помилку\n" \
                           "6. Пропозиції та скарги\n" \
                           "7. Зв’язок з деканатом та соціальні мережі\n" \
                           "8. Питання/відповідь\n" \
                           "9. Профбюро студентів та департаменти ППОС НАУ \"ХАІ\""
            bot.send_message(message.chat.id, chat_message, reply_markup=markup)
        elif message.text == "Конкурси":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            localsheets = sheetContest.get_all_records()
            buttons_group = []
            current_datetime = datetime.now()
            message_text = f"Конкурси, що тривають, або будуть проходити незабаром:\n\n"
            i = 1
            for localsheet in localsheets:
                contest = Contest(
                    localsheet["Назва конкурсу"],
                    datetime.strptime(localsheet["Дата проведення початку"], "%Y-%m-%d"),
                    datetime.strptime(localsheet["Дата кінець"], "%Y-%m-%d"),
                    localsheet["Супровід текст"])
                contests.append(contest)
                button = types.KeyboardButton(localsheet.get("Назва конкурсу"))
                message_text += f'{i}. {localsheet.get("Назва конкурсу")} - '
                if contest.start_date > current_datetime:
                    message_text += f'ще не розпочався\n'
                elif contest.start_date <= current_datetime <= contest.end_date:
                    message_text += f'триває\n'
                else:
                    message_text += f'завершився\n'
                i += 1
                buttons_group.append(button)
                if len(buttons_group) == 2:
                    markup.add(*buttons_group)
                    buttons_group = []

            if buttons_group:
                markup.add(*buttons_group)

            markup.add(types.KeyboardButton("Головне меню"), row_width=2)
            bot.send_message(message.chat.id,
                             message_text,
                             reply_markup=markup)
            bot.register_next_step_handler(message, contest_func)
        elif message.text == "Профбюро студентів та департаменти ППОС НАУ \"ХАІ\"":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            localsheets = sheetDepart.get_all_records()
            buttons_group = []
            for localsheet in localsheets:
                button = types.KeyboardButton(localsheet.get("Назва підрозділу"))
                buttons_group.append(button)
                if len(buttons_group) == 2:
                    markup.add(*buttons_group)
                    buttons_group = []
            if buttons_group:
                markup.add(*buttons_group)
            markup.add(types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть профбюро, або департамент, який вас цікавить:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, faculty_profcom)
        elif message.text == "Питання/відповідь":
            check_num = False
            localsheets = sheetFAQ.get_all_records()
            i = 1
            buttons_group = []
            message_text = f""
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
            for localsheet in localsheets:
                button = types.KeyboardButton(i)
                buttons_group.append(button)
                FAQs.append(
                    FAQ_data(i, localsheet.get("Питання"), localsheet.get("Відповідь"), localsheet.get("Посилання")))
                message_text += f'{i}. {localsheet.get("Питання")}\n'
                if len(buttons_group) == 5:
                    markup.add(*buttons_group)
                    buttons_group = []
                i += 1
            if buttons_group:
                markup.add(*buttons_group)
            bot.send_message(message.chat.id, message_text)
            markup.add(types.KeyboardButton("Головне меню"), row_width=5)
            bot.send_message(message.chat.id, "Оберіть пункт меню, що відповідає порядковому номеру питання:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, FAQ)
        elif message.text == "Пропозиції та скарги":
            message_appeals = message.text
            check_num = False
            bot.send_message(message.chat.id,
                             "Хайовцю, напиши свою пропозицію чи скаргу та обов'язково в кінці залиште свої контактні дані для отримання зворотного зв’язку:\n"
                             "1. ПІБ\n"
                             "2. Номер групи\n"
                             "3. Номер телефону\n"
                             "4. Telegram або Instagram\n")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("СТОП")
            markup.add(btn)
            bot.send_message(message.chat.id, "Щоб завершити подачу заявки натисніть на кнопку \"СТОП\"",
                             reply_markup=markup)
            bot.register_next_step_handler(message, question)
        elif message.text == "Зв’язок з деканатом та соціальні мережі":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Соціальні мережі ППОС НАУ \"ХАІ\""),
                       types.KeyboardButton("Зв’язок з деканатами"),
                       types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть що Вас цікавить:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, social_and_dekanat)
        elif message.text == "Повідомити про технічну помилку":
            message_appeals = message.text
            check_num = False
            bot.send_message(message.chat.id, "Шановні хайовці!👩🏼‍💻\n"
                                              "Якщо ви помітили, що сайт Профкому студентів ХАІ чи "
                                              "система для дистанційного навчання “Ментор” працює некоректно, то "
                                              "прохання повідомити нам.\n\n"
                                              "Щоб це зробити надайте будь-ласка таку інформацію:\n"
                                              "1. ПІБ, номер групи;\n"
                                              "2. Де саме на сайті ви помітили помилку;\n"
                                              "3. Надайте розгорнутий опис проблеми, яку ви помітили.")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("СТОП")
            markup.add(btn)
            bot.send_message(message.chat.id, "Щоб завершити подачу заявки натисніть на кнопку \"СТОП\"",
                             reply_markup=markup)
            bot.register_next_step_handler(message, question)
        elif message.text == "Положення":
            localsheets = sheetDoc.get_all_records()
            bot.send_message(message.chat.id, "Почекайте, оновлюємо інформацію")
            counter = 1
            textMessage = ""
            for localsheet in localsheets:
                textMessage += f'{counter}. [{localsheet["Назва положення"]}]({localsheet["Посилання"]})\n'
                counter += 1
            bot.send_message(message.chat.id, textMessage, parse_mode="Markdown")
        elif message.text == "Реквізити":
            localsheets = sheetRequisites.get_all_records()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for localsheet in localsheets:
                markup.add(types.KeyboardButton(localsheet.get("Назва")))
            markup.add(types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть які саме реквізити Вам потрібні:", reply_markup=markup)
            bot.register_next_step_handler(message, req_)
        elif message.text == "Запитай Профком студентів ХАІ":
            message_appeals = message.text
            check_num = False
            bot.send_message(message.chat.id, "Напишіть своє питання та обов'язково в кінці "
                                              "залиште свої контактні дані(ПІБ, номер групи, номер телефону, telegram або instagram)")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("СТОП")
            markup.add(btn)
            bot.send_message(message.chat.id, "Щоб завершити подачу заявки натисніть на кнопку \"СТОП\"",
                             reply_markup=markup)
            bot.register_next_step_handler(message, question)

    bot.polling(none_stop=True)


def main():
    telegram_bot()


if __name__ == '__main__':
    main()
