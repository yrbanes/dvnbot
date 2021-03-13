import vk_api, sqlite3, gspread, json, schedule, time
from vk_api.longpoll import VkLongPoll, VkEventType
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sqlite3 import Error
from oauth2client.service_account import ServiceAccountCredentials

def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")




gid = '202590390'
token = '9f5a73d994028dacf3390f7964aaf9b3ab3f52059d797d15ce91b8540aebd60c8ef0b13ebfbcc54cf1fab'
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)
vktools = vk_api.tools.VkTools



db = sqlite3.connect('user_list.db')
sql = db.cursor()
database = sqlite3.connect('pupils67.db')
database_10B = sqlite3.connect('10B.db')
database_10A = sqlite3.connect('10A.db')
sql10B = database_10B.cursor()
sql10A = database_10A.cursor()
sql10A.execute("SELECT * FROM cls")
sql10B.execute("SELECT * FROM cls")
select_10A = "SELECT * from cls"
select_10B = "SELECT * from cls"
select_adm = "SELECT * from admins"
select_users = "SELECT * from users"




A10 = execute_read_query(sqlite3.connect('10A.db'), select_10A)
B10 = execute_read_query(sqlite3.connect('10B.db'), select_10B)
admins = execute_read_query(sqlite3.connect('admin_list'), select_adm)
users = execute_read_query(sqlite3.connect('user_list.db'), select_users)
link = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
my_creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', link)
client = gspread.authorize(my_creds)
sheet = client.open('schl67')
sheet1 = sheet.get_worksheet(0)
sheet2 = sheet.get_worksheet(1)
sheet3 = sheet.get_worksheet(2)




ids_10_A = []
ids_10_B = []
user_ids = []
adm_ids = []
all_commands = ['хай', 'привет', 'ку', 'здравствуйте', 'начать', 'специальные возможности (для учителей)', 'занесение в базу', '1']
hi_words = ['хай', 'привет', 'ку', 'здравствуйте', 'начать']
adm_command = ['1']





def sender1(id, text):
    keyboard1 = {
        "one_time": False,
        "buttons": [
            [get_but('Специальные возможности (для учителей)', 'negative')], [get_but('Занесение в базу', 'positive')]
        ]
    }
    keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
    keyboard1 = str(keyboard1.decode('utf-8'))
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard1})


def sender2(id, text):
    keyboard2 = {
        "one_time": False,
        "buttons": [
            [get_but('1', 'primary')]
        ]
    }
    keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
    keyboard2 = str(keyboard2.decode('utf-8'))
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard2})


def sender3(id, text):
    keyboard3 = {
        "one_time": False,
        "buttons": [
            [get_but('Специальные возможности (для учителей)', 'negative')]
        ]
    }
    keyboard3 = json.dumps(keyboard3, ensure_ascii=False).encode('utf-8')
    keyboard3 = str(keyboard3.decode('utf-8'))
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard3})


def getuser_list():
    html1 = urlopen('https://vk.com/search?c[section]=people&c[group]=202590390')
    session = BeautifulSoup(html1, 'html.parser')
    user_list = session.findAll('span', {'class': 'si_owner'})
    for user in user_list:
        print(user.get_text())


def rutine():
    print('bot is active')
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            otext = event.text
            id = event.user_id
            html2 = urlopen('https://vk.com/id' + str(id))
            session = BeautifulSoup(html2, 'html.parser')
            y_link = 'https://vk.com/id' + str(id)
            y_info = str(session.find('h2', {'class': 'op_header'}).get_text())
            user_info = 'https://vk.com/id' + str(id) + " " + str(
                session.find('h2', {'class': 'op_header'}).get_text())
            text1 = 'Здравствуйте, ' + str(session.find('h2', {'class': 'op_header'}).get_text()) + '!' + '\n'
            text2 = 'Снова привет, ' + str(session.find('h2', {'class': 'op_header'}).get_text()) + '!' + '\n' + '\nЯ всё так же отслеживаю посещяемость уроков. 🤓'
            for id1 in A10:
                ids_10_A.append(id1[0])
            for id2 in B10:
                ids_10_B.append(id2[0])
            for user in users:
                user_ids.append(user[0])
            for adm in admins:
                adm_ids.append(adm[0])
            if y_link not in user_ids:
                if msg not in all_commands:
                    if y_link in user_ids:
                        sender1(id, 'Не понял вашего сообщения, напишите "Начать".')
                    else:
                        sender1(id, 'Привет!')
                elif msg in hi_words:
                    print(user_info)
                    sender1(id, text1 + '\nДанный чат-бот является проектом команды "Banana Business". Я оповещаю родителей о прогулах учеников.\n\nЕсли вы ранее не пользовались ботом, то вас надо будет занести в базу.')
                    sql.execute(f"SELECT link FROM users WHERE link = '{y_link}'")
                    if sql.fetchone() is None:
                        sql.execute(f"INSERT INTO users VALUES (?,?)", (y_link, y_info))
                        db.commit()
                elif msg in hi_words:
                    sender1(id, text2)
                elif msg == 'занесение в базу':
                    sender1(id, 'По поводу занесения вас в базу, писать: vk.com/nilinmh\n\nP.S Бот не сможет отправить вам сообщение если у вас закрытый профиль. Подпишитесь на @dnevnbot(сообщество)! <3')
                elif msg == 'специальные возможности (для учителей)' and (y_link not in adm_ids):
                    sender1(id, 'Недостаточно прав')
                elif msg == '1' and (y_link in adm_ids):
                    sender1(id, 'Пишите объявление:')
                elif msg == '1' and (y_link not in adm_ids):
                    sender1(id, 'Недостаточно прав')
                elif msg == 'нет' and (y_link in adm_ids):
                    sender1(id, "Досвидания, " + user_info + ":((")
                elif msg == 'да' and (y_link in adm_ids):
                    sender2(id, "Ваши спец. возможности:\n1. Рассылка объявления ученикам")
                elif msg == 'специальные возможности (для учителей)' and (y_link in adm_ids):
                    sender2(id, text1 + "Ваши спец. возможности:\n1. Рассылка сообщения родителей")
                elif (otext not in adm_command) and (y_link in adm_ids):
                    if len(otext) > 7:
                        if str(id) == sheet1.cell(37, 1).value:
                            rows = sql10B.fetchall()
                            for row in rows:
                                print(row[0])
                                sender1(row[0], otext)
                            sender1(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                        elif str(id) == sheet2.cell(37, 1).value:
                            rows = sql10A.fetchall()
                            for row in rows:
                                print(row[0])
                                sender1(row[0], otext)
                            sender1(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                        else:
                            sender1(id, 'Сообщение не может быть отправлено.')
                else:
                    sender1(id, text2)
            elif id in ids_10_A or ids_10_B:
                if msg in hi_words:
                    sender3(id, text2)
                elif msg == 'специальные возможности (для учителей)' and (y_link not in adm_ids):
                    sender3(id, 'Недостаточно прав')
                elif msg == '1' and (y_link in adm_ids):
                    sender3(id, 'Пишите объявление:')
                elif msg == '1' and (y_link not in adm_ids):
                    sender3(id, 'Недостаточно прав')
                elif msg == 'нет' and (y_link in adm_ids):
                    sender3(id, "Досвидания, " + user_info + ":((")
                elif msg == 'да' and (y_link in adm_ids):
                    sender2(id, "Ваши спец. возможности:\n1. Рассылка объявления ученикам")
                elif msg == 'специальные возможности (для учителей)' and (y_link in adm_ids):
                    sender2(id, text1 + "Ваши спец. возможности:\n1. Рассылка сообщения родителей")
                elif (otext not in adm_command) and (y_link in adm_ids):
                    if len(otext) > 7:
                        if str(id) == sheet1.cell(37, 1).value:
                            rows = sql10B.fetchall()
                            for row in rows:
                                print(row[0])
                                sender3(row[0], otext)
                            sender3(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                        elif str(id) == sheet2.cell(37, 1).value:
                            rows = sql10A.fetchall()
                            for row in rows:
                                print(row[0])
                                sender3(row[0], otext)
                            sender3(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                    else:
                        sender3(id, 'Ошибка. Напишите "Начать".')
                        msg = 'ку'
                if msg not in all_commands:
                    sender3(id, 'Ошибка. Напишите "Начать".')
            elif y_link in adm_ids:
                if msg in hi_words:
                    sender3(id, text2)
                elif msg == 'специальные возможности (для учителей)' and (y_link not in adm_ids):
                    sender3(id, 'Недостаточно прав')
                elif msg == '1' and (y_link in adm_ids):
                    sender3(id, 'Пишите объявление:')
                elif msg == '1' and (y_link not in adm_ids):
                    sender3(id, 'Недостаточно прав')
                elif msg == 'нет' and (y_link in adm_ids):
                    sender3(id, "Досвидания, " + user_info + ":((")
                elif msg == 'да' and (y_link in adm_ids):
                    sender2(id, "Ваши спец. возможности:\n1. Рассылка объявления ученикам")
                elif msg == 'специальные возможности (для учителей)' and (y_link in adm_ids):
                    sender2(id, text1 + "Ваши спец. возможности:\n1. Рассылка сообщения родителей")
                elif (otext not in adm_command) and (y_link in adm_ids):
                    if len(otext) > 7:
                        if str(id) == sheet1.cell(37, 1).value:
                            rows = sql10B.fetchall()
                            for row in rows:
                                print(row[0])
                                sender3(row[0], otext)
                            sender3(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                        elif str(id) == sheet2.cell(37, 1).value:
                            rows = sql10A.fetchall()
                            for row in rows:
                                print(row[0])
                                sender3(row[0], otext)
                            sender3(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                    else:
                        sender3(id, 'Ошибка. Напишите "Начать".')
                        msg = 'ку'
                elif msg not in all_commands:
                    sender1(id, 'Ошибка. Напишите "Начать".')
            elif y_link in user_ids and id not in (ids_10_A or ids_10_B) and id not in adm_ids:
                if msg in hi_words:
                    sender1(id, text2)
                elif msg == 'занесение в базу':
                    sender1(id, 'По поводу занесения вас в базу, писать: vk.com/nilinmh\n\nP.S Бот не сможет отправить вам сообщение если у вас закрытый профиль. Подпишитесь на @dnevnbot(сообщество)! <3')
                elif msg == 'специальные возможности (для учителей)' and (y_link not in adm_ids):
                    sender1(id, 'Недостаточно прав')
                elif msg == '1' and (y_link in adm_ids):
                    sender1(id, 'Пишите объявление:')
                elif msg == '1' and (y_link not in adm_ids):
                    sender1(id, 'Недостаточно прав')
                elif msg == 'нет' and (y_link in adm_ids):
                    sender1(id, "Досвидания, " + user_info + ":((")
                elif msg == 'да' and (y_link in adm_ids):
                    sender2(id, "Ваши спец. возможности:\n1. Рассылка объявления ученикам")
                elif msg == 'специальные возможности (для учителей)' and (y_link in adm_ids):
                    sender2(id, text1 + "Ваши спец. возможности:\n1. Рассылка сообщения родителей")
                elif (otext not in adm_command) and (y_link in adm_ids):
                    if len(otext) > 7:
                        if str(id) == sheet1.cell(37, 1).value:
                            rows = sql10B.fetchall()
                            for row in rows:
                                print(row[0])
                                sender1(row[0], otext)
                            sender1(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                        elif str(id) == sheet2.cell(37, 1).value:
                            rows = sql10A.fetchall()
                            for row in rows:
                                print(row[0])
                                sender1(row[0], otext)
                            sender1(id, 'Отправлено.\nХотите продолжить работу? (Дa/Нет)')
                    else:
                        sender1(id, 'Ошибка. Напишите "Начать".')
                        msg = 'ку'
                elif msg not in all_commands:
                    sender1(id, 'Ошибка. Напишите "Начать".')




create_connection('user_list.db')
rutine()
