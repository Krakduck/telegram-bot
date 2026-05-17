import telebot
import os
from telebot import types #Для того чтобы кнопки заработали нужно импортировать типы
import random
import logging
from database import UserDatabase
import time

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# ========== ИНИЦИАЛИЗАЦИЯ ==========
BotToken = os.getenv('BOT_TOKEN')
AdminToken = os.getenv('ADMIN_TOKEN')
db = UserDatabase() #экземпляр класса

#db.update_user_param(1422346075,'is_admin',True)

memes=[]
if os.path.exists('mems'): #если путь существует
    for filename in os.listdir('mems'): #перебираем все имена файлов в папке и присваиваем их переменной filename
        memes.append(filename)


bot = telebot.TeleBot(BotToken)

anekdots=[]
klikuhi = ["потлатый","либерал","пидор","хуесос","пиздолиз","водолаз","говноед","лох","хач","смешарик","клоун","анал недорого"]
with open('anekdot.txt') as file:
    anekdots.append(file.readline())

ugadai_persone=[['Лунтик в мире marvel','Танос'],
          ['Автор цитаты "2 рубля - рублями, остальное - пиздюлями", еще ебет собак','Максим кац'],
          ['"Я устал, я ухожу"','Борис Ельцин'],
          ['Автор цитаты "Всю водку выпить не возможно, но стремиться к этому надо"','Владимир Путин'],
          ['Длинный, низкий и зеленый','Крокодил'],
          ['Про кого говорится во фразе "Зелибоба, зелибоба, без тебя нам будет плохо"','Владимр Зеленский'],
          ['Узкий, высокий и зеленый в шляпе с пиджаком (только имя)','Гена'],
          ['Автор цитаты "Ну вы и крокодилы"','Нина Валентиновна химичка'],
          ['Человек, который перевернул календарь','Михаил Шуфутинский'],
          ['"А я сейчас вам покажу, откуда на Беларусь готовилось нападение"','Александр Лукашенко'],
          ['Гений, миллиардер, плейбой, филантроп','Тони Старк'],
          ['"Величайший"','Папич'],
          ['Автор фразы "Я календарь переверну"','Михаил Шуфутинский'],
           ['Так называемый boss of the gym','Билли Харрингтон'],
           ['Главный герой многих большего кол-во русских анекдотов','Штирлиц'],
           ['"Денег нет, но вы держитесь"','Дмитрий Медведев'],
           ['"Я тебя бум-бум-бум, ты меня бум-бум-бум"','Артур Пирожков'],
           ['Тот, кто съел колобка','Лиса'],
           ['"Я твой отец"','Дарт Вейдер'],
           ['Самый богатый селезень в мире','Скрудж Макдак'],
           ['курская годзила','Глеб Борисович sasavot сасавот'],
          ['Итальянский сантехник в красной кепке', 'Марио'],
          ['Скелет, который любит каламбуры', 'Санс'],
          ['Желтый колобок, который ест точки', 'Пакман'],
          ['Синий еж, который быстро бегает', 'Соник'],
          ['"Я — русский!"', 'Шаман'],
          ['"Делать деньги, вот так!"', 'алишер Моргенштерн'],
           ['Человек, который ассоциируется с ментосом и колой','мамикс its mamix'],
          ['Главный по обзорам плохого российского кино', 'BadComedian (Евгений Баженов)'],
          ['Тот, кто снимает "Шоу из заброшек" и боится призраков', 'Дима Масленников'],
          ['"Эщкере!"', 'Фейс'],
          ['Главный по интервью, который спрашивает "Сколько ты зарабатываешь?"', 'Юрий Дудь'],
           ['самый часто наблюдаемый стример в тиктоке (нарезки, мемы, вставка на фон)', 'мэлстрой мелстрой'],
           ['Главный разоблачитель мифов','utopia show'],
           ['привет, это ..., я завел себе тикток, мне много об этом говорили, правда не знаю, что здесь делать ', 'алексей навальный'],
           ['Главный фудблогер снг','vanzai ванзай'],
           ['Главный фрик twich','5opka пятерка'],
          ]

crocodile=['крокодил','байден','воробей']


# ========== РЕГИСТРАЦИЯ ==========
def save(message):
    logger.info(f'MESSAGE В SAVE(){message.text}')
    try:
        username, password = message.text.strip().split()

        logger.info(f'USERNAME/PASSWORD:{username, password}')

        # 2. Проверяем, не зарегистрирован ли уже
        existing_user = db.get_user(message.from_user.id)

        klichka = random.choice(klikuhi)

        if existing_user:
            logger.info(f'ПОЛЬЗОВАТЕЛЬ УЖЕ ЗАРЕГИСТРОВАН:{existing_user}')
            bot.send_message(message.chat.id, 'Ты уже зареган!', parse_mode='Markdown')
            menu(message)
            return

        admin = False
        # Регистрируем нового
        if message.from_user.id == AdminToken:
            admin = True
        success = db.add_user(
            telegram_id=message.from_user.id,
            is_admin=admin,
            credits=100,
            username=username,
            password=password,
            allowMEME=True, #если duel будет работать, то поставить False
            count_messages = 0,
            rating = 0,
            klichka=klichka
        )
        logger.info(f'SUCCESS:{success}')

        if success:
            #return (1, klichka)
            bot.send_message(message.chat.id, f'Отлично, {username} {klichka}, считай ты уже почти как свой (временное предупреждение: если уже раньше регался, а сейчас видишь это, значит я снес базу данных)')
            menu(message)
        else:
            #return (0,)
            bot.send_message(message.chat.id, 'Не расслышал, повтори', parse_mode='Markdown')
    except ValueError as e:
        logger.info(f'ошибка регистрации: {e}')



# ========== ОБРАБОТЧИКИ ==========

hod = 0
kombinacia=[]
score_player = 0
score_bot = 0
stavka = 0
neobhodimoe_chislo=0
zagadka_ugadai=''
otvet_ugadai=''


def calculate_points(rolls):
    if rolls.count(neobhodimoe_chislo) == 1: return 1
    if rolls.count(neobhodimoe_chislo) == 2: return 2
    if rolls.count(neobhodimoe_chislo) == 3: return 15
    if rolls[0] == rolls[1] == rolls[2] and rolls[0] != neobhodimoe_chislo: return 5
    return 0

def feedback(message):
    bot.forward_message(1422346075, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Принято. Разберемся.")

@bot.message_handler(content_types=['dice'])

def dice(message):
    logger.info('функция dice')
    global hod,kombinacia,score_player,score_bot,stavka
    score = message.dice.value
    logger.info(f'SCORE:{score}')
    kombinacia.append(score)
    logger.info(f'kombinacia:{kombinacia}')

    if len(kombinacia) == 3:
        logger.info('условие на длину выполнено')
        logger.info(f'ход:{hod}')
        points = calculate_points(kombinacia)
        score_player += points
        bot.send_message(message.chat.id, f'Ты набрал {points}. \nСчет: Ты {score_player}, Я {score_bot}.\nМой ход')
        if score_player == 15:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton('Главное меню', callback_data='Главное меню')
            keyboard.add(btn)
            bot.send_message(message.chat.id, f'Поздравляю, ты выиграл {stavka} кредитов!\nСыграем еще партейку?',reply_markup=keyboard)
            score_player = 0
            score_bot = 0

            info_user = db.get_user(message.chat.id)
            credits = info_user.get('credits')
            db.update_user_param(message.chat.id, 'credits',credits + stavka)
        elif score_player > 15:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton('Главное меню', callback_data='Главное меню')
            keyboard.add(btn)
            bot.send_message(message.chat.id, f'Ууу, у тебя больше 15 очков.. А это значит, что ты выбыл, а я выиграл {stavka} кредитов у тебя!',reply_markup=keyboard)
            score_player = 0
            score_bot = 0

            info_user = db.get_user(message.chat.id)
            credits = info_user.get('credits')
            db.update_user_param(message.chat.id, 'credits', credits - stavka)

            # ТЕПЕРЬ ХОД БОТА (прямо тут)
        kombinacia = []  # Очищаем список для бота

        bot_rolls = []
        for _ in range(3):
            msg = bot.send_dice(message.chat.id, emoji='🎲')
            bot_rolls.append(msg.dice.value)

            # Считаем очки бота СРАЗУ
        bot_points = calculate_points(bot_rolls)
        score_bot += bot_points

            # ПЕРЕМЕННАЯ HOD увеличивается дважды (за игрока и за бота) или просто не меняется так часто.
            # Но чтобы не ломать твою логику с %, просто выводим итог:
        bot.send_message(message.chat.id, f'Я набрал {bot_points}. \nСчет: Ты {score_player}, Я {score_bot}. \nТвой ход')

        if score_bot == 15:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton('Главное меню', callback_data='Главное меню')
            keyboard.add(btn)
            bot.send_message(message.chat.id, f'ДА, я выиграл {stavka} кредитов у тебя, а ты лох!\nСыграем еще партейку?',reply_markup=keyboard)
            score_player = 0
            score_bot = 0

            info_user = db.get_user(message.chat.id)
            credits = info_user.get('credits')
            db.update_user_param(message.chat.id, 'credits', credits - stavka)
        elif score_bot > 15:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn = types.InlineKeyboardButton('Главное меню', callback_data='Главное меню')
            keyboard.add(btn)
            bot.send_message(message.chat.id, f'Ууу, у меня больше 15 очков.. А это значит, что я выбыл, а ты выиграл {stavka} кредитов!',reply_markup=keyboard)
            score_player = 0
            score_bot = 0

            info_user = db.get_user(message.chat.id)
            credits = info_user.get('credits')
            db.update_user_param(message.chat.id, 'credits', credits + stavka)

        kombinacia = []  # Очищаем для следующего хода игрока


@bot.message_handler(commands=['shop'])# Декоратор, который указывает, что функция ниже будет обрабатывать команды. В данном случае обрабатывается команда '/start'
def shop(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создание новых кнопок  ReplyKeyboardMarkup(resize_keyboard=False)
    btn1 = types.InlineKeyboardButton('Подписка на мемы за 300', callback_data='Купить мемы')
    # btn2 = types.InlineKeyboardButton('Перевод пользователю', callback_data='Перевод')
    keyboard.add(btn1)  # ,btn2)
    bot.send_message(message.chat.id, 'Что хотите приобрести?', reply_markup=keyboard)

@bot.message_handler(commands=['game'])# Декоратор, который указывает, что функция ниже будет обрабатывать команды. В данном случае обрабатывается команда '/start'
def game(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Кости(Бак Дайс)', callback_data='Кости(Бак Дайс)')
    btn2 = types.InlineKeyboardButton('Угадай персонажа', callback_data='Угадай персонажа')
    btn3 = types.InlineKeyboardButton('Крокодил', callback_data='Крокодил')
    keyboard.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Во что играем?)', reply_markup=keyboard)

@bot.message_handler(commands=['start'])# Декоратор, который указывает, что функция ниже будет обрабатывать команды. В данном случае обрабатывается команда '/start'
def start(message):
    bot.send_message(message.chat.id, "👋 Чтобы зарегестрироваться введите команду /reg",parse_mode='Markdown')

@bot.message_handler(commands=['reg'])
def promezutok(message):
    msg = bot.send_message(message.chat.id, 'Введи имя и пароль через пробел')
    bot.register_next_step_handler(msg, save)

@bot.message_handler(commands=['send'])
def perehvat(message):
    msg = bot.send_message(message.chat.id, 'Сколько и кому перевести? Напиши телеграмм id и сумм через пробел')
    # 2. Вешаем "перехватчик" на следующее сообщение именно этого пользователя
    bot.register_next_step_handler(msg, send)
def send(message):
    logger.info(message.text)
    tgid, count = message.text.split()[1:]
    count = int(count)
    logger.info(f'tgid:{tgid}, count:{count}')
    info1 = db.get_user(tgid)
    logger.info(info1)
    if info1 is None:
        bot.send_message(message.chat.id, f"Данный пользователь не зарегистрирован", parse_mode='Markdown')
    else:
        info = db.get_user(message.chat.id)
        logger.info(info)
        credits = info.get('credits')
        succes = db.update_user_param(message.from_user.id, 'credits', credits-count)
        logger.info(f'succes:{succes}')
        succes1 = db.update_user_param(tgid, 'credits', credits+count)
        logger.info(f'succes1:{succes1}')
        if succes:
            bot.send_message(message.chat.id, f"Перевод совершен", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"Ошибка перевода", parse_mode='Markdown')
        if succes1:
            bot.send_message(tgid, f"Вам перевели {count} кредитов", parse_mode='Markdown')

@bot.message_handler(commands=['credits'])

def get_message(message):
    if db.get_user(message.from_user.id).get('is_admin') ==1:
        msg= bot.send_message(message.chat.id, 'сколько кредитов выдать?')
    # 2. Вешаем "перехватчик" на следующее сообщение именно этого пользователя
        bot.register_next_step_handler(msg, credits_accruals)
    else:
        bot.send_message(message.chat.id,'Ты не админ, что б такое спрашивать', parse_mode='Markdown')
def credits_accruals(message):
    if message.text.isdigit():
        success = db.update_user_param(message.from_user.id, 'credits', int(message.text))
        if success:
             user_info = db.get_user(message.from_user.id)
             a = user_info.get('credits')
             bot.send_message(message.from_user.id,f'у пользователя теперь столько кредитов:{a}')
        else:
             bot.send_message(message.from_user.id, 'ошибка')

@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создание новых кнопок  ReplyKeyboardMarkup(resize_keyboard=False)
    btn1 = types.InlineKeyboardButton('Рассказать анекдот', callback_data='Рассказать анекдот')
    btn2 = types.InlineKeyboardButton('Пояснить за Deepseek', callback_data='Пояснить за Deepseek')
    btn3 = types.InlineKeyboardButton('Мемы', callback_data='Мемы')
    btn6 = types.InlineKeyboardButton('Игры, да не простые, а очень сука веселые', callback_data='Игры')
    btn4 = types.InlineKeyboardButton('Инфо пользователя', callback_data='Инфо пользователя')
    btn5 = types.InlineKeyboardButton('Жалобы и предложения', callback_data='Жалобы и предложения')
    btn7 = types.InlineKeyboardButton('Магазин', callback_data='Магазин')
    keyboard.add(btn1, btn2, btn3, btn6, btn4, btn5, btn7)
    bot.send_message(message.chat.id, 'что от меня требуется-то?', reply_markup=keyboard)

@bot.message_handler(commands=['rating'])
def rating(message):
    logger.info('rating вызван')
    spisok = db.get_all_users_stat()
    logger.info(f'spisok: {spisok}')
    logger.info(f'spisoktype: {type(spisok)}')
    text = 'Общий рейтинг:\n'
    for i in spisok:
        text +=f'имя: {i[0]}\n число текстовых сообщений: {i[1]}\n рейтинг: {i[2]}\n'
        logger.info(f'i: {i}')
    bot.send_message(message.chat.id,text)

def change_password(message):
    a =db.update_user_param(message.from_user.id, 'password', message.text)
    if a:
        bot.send_message(message.chat.id, f'Операция выполнена', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Операция не выполнена', parse_mode='Markdown')

def change_name(message):
    a =db.update_user_param(message.from_user.id, 'username', message.text)
    if a:
        bot.send_message(message.chat.id, f'Операция выполнена', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Операция не выполнена', parse_mode='Markdown')

UGADAI_GAME_ispolzovano=[]

def ugadai_game(message):
    global zagadka_ugadai,otvet_ugadai,UGADAI_GAME_ispolzovano
    logger.info('1 функция вызвана')
    if len(UGADAI_GAME_ispolzovano) == len(ugadai_persone):
        UGADAI_GAME_ispolzovano=[]
    a= ugadai_persone[random.randint(0,len(ugadai_persone)-1)]
    logger.info(f'a:{a}')
    if a not in UGADAI_GAME_ispolzovano:
        logger.info(f'загадка еще не использована')
        zagadka_ugadai,otvet_ugadai = a
        UGADAI_GAME_ispolzovano.append(a)
    else:
        logger.info(f'загадка уже использована')
        ugadai_game(message)
    logger.info(f'загадка:{zagadka_ugadai},ответ:{otvet_ugadai}')
    msg = bot.send_message(message.chat.id, f'{zagadka_ugadai}', parse_mode='Markdown')
    bot.register_next_step_handler(msg, ugadai_game2)

def ugadai_game2(message):
    logger.info('2 функция вызвана')
    logger.info(f'ответ такой: {message.text}')
    logger.info(f'тип message.text: {type(message.text)}')
    global otvet_ugadai
    if message.text.strip().lower() == 'стоп':
        bot.send_message(message.chat.id, f'Игра окончена', parse_mode='Markdown')
    elif message.text.lower().strip() in otvet_ugadai.lower():
        info = db.get_user(message.from_user.id)
        rating = info.get('rating')
        db.update_user_param(message.from_user.id, 'rating', rating+1)
        logger.info('ответ верный')
        bot.send_message(message.chat.id, f'Абсолютно верно!', parse_mode='Markdown')
        ugadai_game(message)
    else:
        logger.info('ответ НЕ верный')
        msg = bot.send_message(message.chat.id, f'Не верно', parse_mode='Markdown')
        bot.register_next_step_handler(msg, ugadai_game2)

who=0
croco_ispolzovano=[]
zagadka_croco=''

vedushy=''
croco_bool =False
def crocodile_game(message):
    logger.info('crocodile_game вызвана')
    global who,croco_ispolzovano, zagadka_croco, croco_bool,vedushy
    users = db.get_all_users_stat()
    users_id = [i[3] for i in users]
    logger.info(f'users_id: {users_id}')
    if len(croco_ispolzovano) == len(crocodile):
        croco_ispolzovano = []
    a = crocodile[random.randint(0, len(crocodile) - 1)]
    logger.info(f'a:{a}')
    if a not in croco_ispolzovano:
        logger.info(f'загадка еще не использована')
        zagadka_croco =a
        UGADAI_GAME_ispolzovano.append(a)
    if who>=len(users_id):
        who=0
    logger.info(who)
    vedushy=users_id[who]
    bot.send_message(vedushy, f'Твоя задача объяснить слово "{zagadka_croco}" всем в группе')
    msg =bot.send_message(message.chat.id, f'Задание уже отправлено!')
    who+=1
    bot.register_next_step_handler(msg, crocodile_game2)

def crocodile_game2(message):
    logger.info('crocodile_game2 вызвана')
    global zagadka_croco
    if message.text.strip().lower() == 'стоп':
        bot.send_message(message.chat.id, f'Игра окончена', parse_mode='Markdown')
    elif (message.text.lower().strip() in zagadka_croco.lower()) and message.from_user.id != vedushy :
        info = db.get_user(message.from_user.id)
        rating = info.get('rating')
        credits = info.get('credits')
        db.update_user_param(message.from_user.id, 'rating', rating + 1)
        db.update_user_param(message.from_user.id, 'credits', credits + 10)
        logger.info('ответ верный')
        bot.send_message(message.chat.id, f'Абсолютно верно! Ваш рейтинг повышен на 1, начислено 10 кредитов', parse_mode='Markdown')
        crocodile_game(message)
    else:
        logger.info('ответ НЕ верный')
        msg = bot.send_message(message.chat.id, f'Не верно', parse_mode='Markdown')
        bot.register_next_step_handler(msg, crocodile_game2)


@bot.message_handler(content_types=['text']) #content_types=['text'] означает, что функция будет вызываться при получении ЛЮБОГО текстового сообщения
def get_text_messages(message):
    info = db.get_user(message.from_user.id)
    if 'СТАВКА' in message.text:
        global stavka, neobhodimoe_chislo
        credit = info.get('credits')
        stavka  = int(message.text.split()[1])
        logger.info(f'ставка: {stavka}')
        if stavka>credit:
            bot.send_message(message.chat.id, f'ХАХАХХАХ у тебя денег столько нет, бомжара!',parse_mode='Markdown')
        else:
            neobhodimoe_chislo = random.randint(1,6)
            bot.send_message(message.chat.id, f'Отлично, ставка принята.\nНачинай ты, пришли 3 эмодзи игрального кубика. Будем считать необходимым числом {neobhodimoe_chislo}', parse_mode='Markdown')

    count = info.get('count_messages')
    db.update_user_param(message.from_user.id, 'count_messages',count+1 )



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    logger.info(f"call.data:{call.data}")
    if call.data == 'вход':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Введите имя, используя "@" и пароль через пробел ', parse_mode='Markdown')
    elif call.data == 'Мемы':
        user_info = db.get_user(call.from_user.id)
        bot.answer_callback_query(call.id)
        if user_info:
            if user_info.get('allowMEME')==1: #get- метод словаря, который возвращает значение опредленного ключа ('allowMEME')
                 path = 'mems'+'/'+random.choice(memes)
                 with open(path, 'rb') as photo:
                     logger.info(f'фото отправляется:{photo}')
                     bot.send_photo(call.message.chat.id, photo)
            else:
                bot.send_message(call.message.chat.id, 'Сорян, но я не помню, чтобы ты был в списке тех, кому разрешено смотреть на эти мемы,(',parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id,'А ты кто вообще? Походу ты не прошел авторизацию. А ну быстро метнулся а начало по команде /start ',parse_mode='Markdown')
    elif call.data == 'Рассказать анекдот':
        bot.answer_callback_query(call.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Анекдот про Штирлица',callback_data='Анекдот про Штирлица')
        btn2 = types.InlineKeyboardButton('Главное меню',callback_data='Главное меню')
        keyboard.add(btn1, btn2)
        bot.send_message(call.message.chat.id, 'Какой анекдот рассказать?', reply_markup=keyboard)
    elif call.data == 'Пояснить за Deepseek' :
        bot.answer_callback_query(call.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Почему дипсик говно?',callback_data='Почему дипсик говно?')
        btn2 = types.InlineKeyboardButton('Как обращаться с дипсиком?',callback_data='Как обращаться с дипсиком?')
        btn3 = types.InlineKeyboardButton('Чем ты лучше дипсика?',callback_data='Чем ты лучше дипсика?')
        btn4 = types.InlineKeyboardButton('Главное меню',callback_data='Главное меню')
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(call.message.chat.id, 'Что именно пояснить?', reply_markup=keyboard)
    elif call.data == 'Жалобы и предложения' :
        msg = bot.send_message(call.message.chat.id, "Напиши на что именно мне забить хер:")
        # 2. Вешаем "перехватчик" на следующее сообщение именно этого пользователя
        bot.register_next_step_handler(msg, feedback)
    elif call.data == 'Инфо пользователя' :
        bot.answer_callback_query(call.id)
        user_info = db.get_user(call.from_user.id)# в перменной храним значение функции из класса  Если пользователь найден, в переменную user_info записывается словарь
        logger.info(f'user_info:{user_info}')
        if user_info:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton('Поменять ник', callback_data='Поменять ник')
            btn2 = types.InlineKeyboardButton('Поменять пароль', callback_data='Поменять пароль')
            keyboard.add(btn1, btn2)
            name = user_info.get('username')
            klichka = user_info.get('klichka')
            password = user_info.get('password')
            podpiska= user_info.get('allowMEME')
            credits=user_info.get('credits')
            count_messages = user_info.get('count_messages')
            bot.send_message(call.message.chat.id, f'Имя: {name}\n'
                                                   f'Погоняло: {klichka}\n'
                                                   f'Пароль: {password}\n'
                                                   f'Подписка на мемы: {podpiska}\n'
                                                   f'Кол-во кредитов:{credits}\n'
                                                   f'Кол-во сообщений:{count_messages}', reply_markup=keyboard)

    elif call.data == 'Поменять пароль' :
        msg = bot.send_message(call.message.chat.id, f'Пришли новый пароль')
        bot.register_next_step_handler(msg, change_password)

    elif call.data == 'Поменять ник' :
        msg = bot.send_message(call.message.chat.id, f'Пришли новое имя')
        bot.register_next_step_handler(msg, change_name)

    elif call.data == 'Анекдот про Штирлица':
        bot.answer_callback_query(call.id)
        anekdot = random.choice(anekdots)
        bot.send_message(call.message.chat.id, f'**{anekdot}**', parse_mode='Markdown')
    elif call.data == 'Почему дипсик говно?':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Потому что. что за тупые вопросы?', parse_mode='Markdown')
    elif call.data == 'Как обращаться с дипсиком?':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Как с опущенным', parse_mode='Markdown')
    elif call.data == 'Чем ты лучше дипсика?':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Меня не делала команда маленьких китайских детей-рабов', parse_mode='Markdown')
    elif call.data == 'Игры':
        bot.answer_callback_query(call.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Кости(Бак Дайс)',callback_data='Кости(Бак Дайс)')
        btn2 = types.InlineKeyboardButton('Угадай персонажа', callback_data='Угадай персонажа')
        btn3 = types.InlineKeyboardButton('Крокодил', callback_data='Крокодил')
        keyboard.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, 'Во что играем?)', reply_markup=keyboard)
    elif call.data == 'Кости(Бак Дайс)':
        bot.answer_callback_query(call.id)
        user_info = db.get_user(call.from_user.id)
        credits = user_info.get('credits')
        bot.send_message(call.message.chat.id, f'Правила игры:\n\n'
                                               f'1)Для игры необходимо как минимум 3 игральные кости\n\n'
                                               f'2)Если на одном из кубиков появляется необходимое число — игрок получает одно очкo.Когда игровое очко появляется сразу на двух костях, игрок получает два балла.Если игрок выкинул три одинаковых числа, отличных от игрового — это пять очков.Когда игровое очко появляется на всех трёх костях, игрок получает сразу 15 очков.\n\n'
                                               f'3)После собирания 15 очков игра останавливается. Если игрок собрал >15 очков, то он проиграл\n\n'
                                               f'Прежде чем начать, выбери ставку. Отправь сообщение в формате "СТАВКА 100". Напоминаю, что твой текущий бюджет {credits}, ты конечно можешь уйти в минус, но знай, что в долг товары у нас не отпускают)', parse_mode='Markdown')
        bot.send_message(call.message.chat.id,'ВНИМАНИЕ, ЭТА ФУНКЦИЯ МОЖЕТ РАБОТАТЬ НЕ КОРЕКТНО В ГРУППАХ, ТАК КАК МНЕ В ПАДЛУ С НЕ РАЗБИРАТЬСЯ, НУ А МОЖЕТ И ВСЕ ХОРОШО РАБОТАЕТ')
    elif call.data == 'Магазин':
        bot.answer_callback_query(call.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)  # создание новых кнопок  ReplyKeyboardMarkup(resize_keyboard=False)
        btn1 = types.InlineKeyboardButton('Подписка на мемы за 300', callback_data='Купить мемы')
        keyboard.add(btn1)
        bot.send_message(call.message.chat.id, 'Что хотите приобрести?', reply_markup=keyboard)

    elif call.data == 'Купить мемы':
        bot.answer_callback_query(call.id)
        userinfo = db.get_user(call.from_user.id)
        credits = userinfo.get('credits')
        if credits<300:
            bot.send_message(call.from_user.id, 'Ага, разбежался он! Иди заработай сначала столько!', parse_mode='Markdown')
        else:
            success = db.update_user_param(call.from_user.id, 'allowMEME', 1) and db.update_user_param(call.from_user.id, 'credits', credits-300)

            if success:
                bot.send_message(call.from_user.id, f'Оплата прошла! Хочешь опробовать новую функцию?', parse_mode='Markdown')
            else:
                bot.send_message(call.from_user.id, 'Ошибка')

    elif call.data == 'Угадай персонажа':
        bot.answer_callback_query(call.id)
        logger.info('угадай перса услышан')
        ugadai_game(call.message)

    elif call.data == 'Крокодил':
        bot.answer_callback_query(call.id)
        logger.info('крокодил услышан')
        crocodile_game(call.message)

    elif call.data == 'Главное меню':
        bot.answer_callback_query(call.id)
        keyboard = types.InlineKeyboardMarkup(row_width=1)  # создание новых кнопок  ReplyKeyboardMarkup(resize_keyboard=False)
        btn1 = types.InlineKeyboardButton('Рассказать анекдот', callback_data='Рассказать анекдот')
        btn2 = types.InlineKeyboardButton('Пояснить за Deepseek', callback_data='Пояснить за Deepseek')
        btn3 = types.InlineKeyboardButton('Мемы', callback_data='Мемы')
        btn6 = types.InlineKeyboardButton('Игры, да не простые, а очень сука веселые', callback_data='Игры')
        btn4 = types.InlineKeyboardButton('Инфо пользователя', callback_data='Инфо пользователя')
        btn5 = types.InlineKeyboardButton('Жалобы и предложения', callback_data='Жалобы и предложения')
        btn7 = types.InlineKeyboardButton('Магазин', callback_data='Магазин')
        keyboard.add(btn1, btn2, btn3, btn6, btn4, btn5, btn7)
        bot.send_message(call.message.chat.id,'что от меня требуется-то?',reply_markup=keyboard)

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    logger.info("🚀 Запуск...")

    # Удаляем вебхуки
    bot.remove_webhook()
    time.sleep(1)

    # Запускаем polling - без while True!
    logger.info("✅ Бот готов!")
    bot.infinity_polling(timeout=10, long_polling_timeout=10)
