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
token = '5779680701:AAG-9j4Yq5X2vTPY087O05rOlUcOc6_zl68'
bot = telebot.TeleBot(token)
TO_CHAT_ID = -1001848377879
dev_chat_id = 338497309
check_num = False


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
        if sheetDepart.find(message.text):
            localsheets = sheetDepart.get_all_records()
            for localsheet in localsheets:
                if localsheet["Назва підрозділу"] == message.text:
                    textMessage = f'{localsheet["Назва підрозділу"]}\n\n{localsheet["Основний текст про підрозділ"]}\n\n{localsheet["Контакти та ПІБ"]}'
                    bot.send_message(message.chat.id, textMessage)
            bot.register_next_step_handler(message, faculty_profcom)
        else:
            func(message)

    def social_and_dekanat(message):
        localsheets = sheetSocial.get_all_records()
        if message.text == "Соціальні мережі ППОС НАУ \"ХАІ\"":
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
        if ((message.text != "Конкурси")
                and (message.text != "Головне меню")
                and (message.text != "Запитай Профком студентів ХАІ")
                and (message.text != "Міс ХАІ: етап факультет")
                and (message.text != "Повідомити про технічну помилку")
                and (message.text != "Зв’язок та соціальні мережі")
                and (message.text != "Пропозиції Та Скарги")
                and (message.text != "Моменти з ХАІ")
                and (message.text != "Профбюро студентів та департаменти ППОС НАУ \"ХАІ\"")
                and (message.text != "СТОП")):
            return True
        else:
            return False

    def req_(message):
        if message.text == "Реквізити для сплати навчання":
            rec_message = "Банківські реквізити для оплати за навчання\n" \
                          "IBAN-рахунок:\n" \
                          "UA878201720313271005201004199\n" \
                          "Призначення платежу:\n" \
                          "сплата за навчання ПІБ студента без скорочень , № договору\n\n" \
                          "Відділ контрактів НАУ «ХАІ»:\n" \
                          "тел.: +38 (057) 788-48-86\n" \
                          "ауд. 117 головного корпусу"
            bot.send_message(message.chat.id, rec_message)
            bot.register_next_step_handler(message, req_)
        elif message.text == "Реквізити для сплати проживання":
            rec_message = "Банківські реквізити для оплати за проживання\n" \
                          "IBAN-рахунок:\n" \
                          "UA828201720313251001202017426\n" \
                          "Призначення платежу:\n" \
                          "за проживання у гуртожитку «ХАІ» № номер гуртожитку , ПІБ студента без скорочень"
            bot.send_message(message.chat.id, rec_message)
            bot.register_next_step_handler(message, req_)
        else:
            func(message)

    def question(message):
        global check_num
        if check(message):
            if not check_num:
                bot.send_message(TO_CHAT_ID, "#ПитанняПрофкому")
                check_num = True
            bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, question)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def problem_report(message):
        global check_num
        if check(message):
            if not check_num:
                bot.send_message(dev_chat_id, "#ПовідомитиПроПомилку")
                check_num = True
            bot.forward_message(dev_chat_id, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, problem_report)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def suggestions(message):
        global check_num
        if check(message):
            if not check_num:
                bot.send_message(TO_CHAT_ID, "#ПропозиціїТаСкарги")
                check_num = True
            bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, suggestions)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def contest_moment(message):
        global check_num
        if check(message):
            if not check_num:
                bot.send_message(TO_CHAT_ID, "#Моменти_з_ХАІ")
                check_num = True
            bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
            bot.register_next_step_handler(message, contest_moment)
        elif message.text == "СТОП":
            message.text = "Головне меню"
            func(message)

    def FAQ(message):
        if message.text == "1":
            bot.send_message(message.chat.id,
                             "Ви маєте змогу написати заяву та подати пакет документів на оформлення соціальної стипендії у будь-який момент. "
                             "Соціальна стипендія буде нараховуватись з моменту написання заяви")
            bot.register_next_step_handler(message, FAQ)
        if message.text == "2":
            bot.send_message(message.chat.id,
                             "[Приклади шаблонів заяв та документів Ви можете знайти на нашому сайті в розділі “Корисні ресурси”](https://education.khai.edu/union/studresources)",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, FAQ)
        if message.text == "3":
            bot.send_message(message.chat.id,
                             "На жаль, студенти мають змогу отримувати тільки одну стипендію. Або академічну, або соціальну. "
                             "Рекомендуємо Вам оформлювати соціальну стипендію тільки тоді, коли Ви дізнаєтесь "
                             "кінцевий рейтинг на отримання академічної стипендії")
            bot.register_next_step_handler(message, FAQ)
        if message.text == "4":
            bot.send_message(message.chat.id,
                             "Соціальну стипендію необхідно оформлювати раз в семестр. "
                             "Наприклад, якщо 1 семестр курсу закінчився, то в 2 семестрі "
                             "Вам необхідно ще раз писати заяву та подати пакет документів "
                             "на оформлення соціальної стипендії")
            bot.register_next_step_handler(message, FAQ)
        if message.text == "5":
            bot.send_message(message.chat.id,
                             "Соціальні стипендії - це виплата, яку отримують студенти, які мають право на пільги.\n\n"
                             "[Перелік пільгових категорій, які мають право на оформлення соціальної стипендії](https://drive.google.com/file/d/1NJ3IWLqGvoyiw2LfYo21SpIam-d93j5n/view?usp=share_link)\n\n"
                             "Якщо Ви навчаєтесь на бюджеті, маєте підтверджувальні документи вашого статусу,  "
                             "не маєте академічних заборгованостей - то Ви маєте можливість подати до деканату "
                             "необхідний пакет документів на призначення соціальної стипендії!\n\n"
                             "Приклади заяв на соціальні стипендії та перелік всіх необхідних документів можна знайти  "
                             "у [Додатку Б  \"Положення про рейтингове оцінювання\"](https://khai.edu/assets/files/polozhennya/polozhennya-pro-stipendii.pdf).\n\n"
                             "❗️Не стосується здобувачів освіти, які отримують академічну стипендію❗️",
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, FAQ)
        else:
            func(message)

    def contest(message, localsheets):
        

    @bot.message_handler(
        content_types=['text', "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location",
                       "contact",
                       "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                       "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                       "migrate_from_chat_id", "pinned_message"])
    def func(message):
        global check_num
        if message.text == "Конкурси":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            localsheets = sheetContest.get_all_records()
            for localsheet in localsheets:
                markup.add(types.KeyboardButton(localsheet.get("Назва конкурсу")))
            markup.add(types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id,
                             "Конкурси, що тривають, або будуть проходити незабаром:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, contest)
        elif message.text == "Головне меню":
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
        elif message.text == "Профбюро студентів та департаменти ППОС НАУ \"ХАІ\"":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(types.KeyboardButton("1 факультет"),
                       types.KeyboardButton("2 факультет"),
                       types.KeyboardButton("3 факультет"),
                       types.KeyboardButton("4 факультет"),
                       types.KeyboardButton("5 факультет"),
                       types.KeyboardButton("6 факультет"),
                       types.KeyboardButton("7 факультет"),
                       types.KeyboardButton("Де КМІП"),
                       types.KeyboardButton("Де МК"),
                       types.KeyboardButton("Де СО"),
                       types.KeyboardButton("Де СОРТТ"),
                       types.KeyboardButton("Де СЗНР"),
                       types.KeyboardButton("Де ЖП"),
                       types.KeyboardButton("Де ОРДТМ"),
                       types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть профбюро, або департамент, який вас цікавить:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, faculty_profcom)
        elif message.text == "Питання/відповідь":
            check_num = False
            bot.send_message(message.chat.id, "1. Коли я можу оформити соціальну стипендію?\n"
                                              "2. Де я можу знайти приклади шаблонів заяв та документів?\n"
                                              "3. Скільки всього стипендій я можу отримувати?\n"
                                              "4. Як часто необхідно оформлювати соціальну стипендію?\n"
                                              "5. Що таке соціальні стипендії і хто має право на їх оформлення?\n")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
            markup.add(types.KeyboardButton("1"),
                       types.KeyboardButton("2"),
                       types.KeyboardButton("3"),
                       types.KeyboardButton("4"),
                       types.KeyboardButton("5"))
            markup.add(types.KeyboardButton("Головне меню"), row_width=5)
            bot.send_message(message.chat.id, "Оберіть пункт меню, що відповідає порядковому номеру питання:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, FAQ)
        elif message.text == "Пропозиції та скарги":
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
            bot.register_next_step_handler(message, suggestions)
        elif message.text == "Зв’язок з деканатом та соціальні мережі":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("Соціальні мережі ППОС НАУ \"ХАІ\""),
                       types.KeyboardButton("Зв’язок з деканатами"),
                       types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть що Вас цікавить:",
                             reply_markup=markup)
            bot.register_next_step_handler(message, social_and_dekanat)
        elif message.text == "Повідомити про технічну помилку":
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
            bot.register_next_step_handler(message, problem_report)
        elif message.text == "Положення":
            chat_message = "Положення:\n\n" \
                           "1. [Правила призначення і виплати стипендій здобувачам вищої освіти](https://khai.edu/assets/files/polozhennya/polozhennya-pro-stipendii.pdf)\n" \
                           "2. [Положення про академічну доброчесність](https://khai.edu/assets/files/polozhennya/polozhennya-pro-akademichnu-dobrochesnist.pdf)\n" \
                           "3. [Положення про рейтингове оцінювання досянень студентів](https://khai.edu/assets/files/polozhennya/polozhennya-pro-rejtingove-ocinyuvannya-dosyagnen-studentiv.pdf)\n" \
                           "4. [Про надання державної цільової підтримки деяким категоріям студентів, пов’язаної з проживанням у гутрожитках](https://khai.edu/assets/files/polozhennya/polozhennya-pro-nadannya-derzhavnoi-cilovoi-pidtrimki-studentiv-pov%E2%80%99yazanoi-z-prozhivannyam-u-gurtozhitkah.pdf)\n" \
                           "5. [Положення про навчання здобувачів вищої освіти за індивідуальним графіком](https://khai.edu/assets/files/polozhennya/polozhennya-pro-navchannya-zdobuvachiv-vishhoi-osviti-za-individualnim-grafikom.pdf)\n" \
                           "6. [Графік освітнього процесу ](https://khai.edu/ua/education/grafik-osvitnogo-procesu-2020/2021/denna-forma-navchannya6/)\n" \
                           "7. [Положення про студентський гуртожиток](https://khai.edu/assets/files/polozhennya/polozhennya_gurtozhitki_hai_2015.PDF)\n"
            bot.send_message(message.chat.id, chat_message, parse_mode="Markdown")
        elif message.text == "Реквізити":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(types.KeyboardButton("Реквізити для сплати навчання"),
                       types.KeyboardButton("Реквізити для сплати проживання"),
                       types.KeyboardButton("Головне меню"))
            bot.send_message(message.chat.id, "Оберіть які саме реквізити Вам потрібні:", reply_markup=markup)
            bot.register_next_step_handler(message, req_)
        elif message.text == "Запитай Профком студентів ХАІ":
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
