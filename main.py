import telebot      # module with telegram bot api
import random
import time


###########
# CLASSES
###########


class Game:

    count = 0

    def __init__(self, chat_id=None):

        # assign properties
        self.chatId = chat_id
        self.robots = []
        self.robotChoice = False
        self.propertyChoice = False
        self.difficulty = False
        self.time = 10
        self.numberOfRobots = 3

        Game.count += 1

        self.names = ['Олег', 'Петр', 'Феофан', 'Прокопий', 'Анатолий',
                      'Ярополк', 'Илон', 'Папич', 'Боб']
        self.books = ['Библия', 'Коран', 'Псалтырь', 'Тора', 'Камасутра',
                      'Моя Борьба', 'Укус Питона', 'Википедия', 'Орфографический Словарь']
        self.jobs = ['Сантехник', 'Стример', 'Трубочист', 'Лыжник', 'Уборщик',
                     'Торпедист', 'Тракторист', 'Паромщик', 'Геймер']

        self.index = Game.count - 1

    def __del__(self):
        Game.count -= 1

    # create new robot
    def create_robot(self, number):

        # choose random parameters
        name = random.choice(self.names)
        book = random.choice(self.books)
        job = random.choice(self.jobs)

        # update lists
        self.names.remove(name)
        self.books.remove(book)
        self.jobs.remove(job)

        robot = Robot(name=name, book=book, job=job, game_index=self.index, number=number)      # create robot
        self.robots.append(robot)                                                               # add robot to the list
        robot.handle_robot()                                                                    # display robot

        return robot

    # choose which property and which robot to ask
    def choose_question(self):

        self.robotChoice = random.choice(self.robots)
        self.propertyChoice = random.choice((self.robotChoice.name, self.robotChoice.job, self.robotChoice.book))

        return self.robotChoice, self.propertyChoice

    # prepare game
    def prepare_game(self):

        # manage difficulty settings
        if self.difficulty == 2:            # if difficulty is 2

            self.time = 5                   # change time for each robot
            self.numberOfRobots = 5         # change number of robots

        elif self.difficulty == 3:          # if difficulty is 3

            self.time = 3                   # change time for each robot
            self.numberOfRobots = 8         # change number of robots

        else:                               # default
            pass

        # create robots
        for i in range(self.numberOfRobots):
            self.create_robot(number=i+1)

    # start game
    def start_game(self):

        self.prepare_game()             # create robots
        self.choose_question()          # choose what to show to user

        # create markup
        markup = telebot.types.ReplyKeyboardMarkup()
        for i in range(self.numberOfRobots):
            markup.add(telebot.types.KeyboardButton(str(i+1)))

        if self.propertyChoice == self.robotChoice.name:
            bravo_bot.send_message(self.chatId,
                                   'Кого по счёту робота так зовут: {}?\n'.format(self.propertyChoice),
                                   reply_markup=markup)

        elif self.propertyChoice == self.robotChoice.book:
            bravo_bot.send_message(self.chatId,
                                   'У какого по счёту робота эта книга - любимая: {}?\n'.format(self.propertyChoice),
                                   reply_markup=markup)

        else:
            bravo_bot.send_message(self.chatId,
                                   'У какого по счёту робота такая работа: {}?\n'.format(self.propertyChoice),
                                   reply_markup=markup)

    # finish game
    def finish_game(self):

        bravo_bot.send_message(self.chatId,
                               '*_Game Over_*',
                               reply_markup=default_markup,
                               parse_mode='MarkdownV2')         # display message
        games.remove(self)                                      # remove game from the list


class Robot:

    def __init__(self, name=None, book=None, job=None, game_index=None, number=None):

        # assign properties
        self.gameIndex = game_index
        self.name = name
        self.book = book
        self.job = job

        self.number = number               # robots order

    def __str__(self):

        string = '''
*Робот {}*
        
*Имя:* _{}_
*Любимая Книга:* _{}_
*Работа:* _{}_
        
        '''.format(self.number, self.name, self.book, self.job)

        return string

    # when robot is created
    def handle_robot(self):

        # output robot
        reply = bravo_bot.send_message(games[self.gameIndex].chatId,
                                       str(self),
                                       parse_mode='MarkdownV2')              # show robots properties
        time.sleep(games[self.gameIndex].time)  # wait
        bravo_bot.delete_message(chat_id=games[self.gameIndex].chatId,
                                 message_id=reply.id)                        # delete robots properties from chat


###########
# VARIABLES
###########

games = []                                                                           # list of current games
greeting = '''                                                                      
*Добро пожаловать в нашу игру\!*\n

*_Правила игры:_*_
    \- вам поочереди покажут несколько роботов и их параметры
    \- вам необходимо запомнить порядок и параметры каждого
    \- после чего вам будет предложено угадать к какому по счёту роботу принадлежал определенный параметр
    \- время для просмотра параметров одного робота, количество роботов и их параметров зависит от уровня сложности
    \- всего в игре три уровня от 1 до 3_
    
*_Удачи\!_*

_Введите команду_ */go* _, чтобы начать\._\n
'''                                                                                  # greeting string

bravo_bot = telebot.TeleBot('1548233193:AAEMJqtwfayxXx_CeHnxjld-f8nECzziTeM')        # initializing bot object

# create default markup
default_markup = telebot.types.ReplyKeyboardMarkup()
default_markup.add(telebot.types.KeyboardButton('/start'),
                   telebot.types.KeyboardButton('/go'))


###########
# MAIN
###########

# get current game instance
def get_game(chat_id):

    current_game = False

    # check if game is on for this chat
    for game in games:
        if game.chatId == chat_id:
            current_game = game

    return current_game


###########
# MAIN
###########

# start bot
@bravo_bot.message_handler(commands=['start'])
def start_command(message):     # launch bot
    bravo_bot.send_message(message.chat.id,
                           greeting,
                           reply_markup=default_markup,
                           parse_mode='MarkdownV2')              # send greeting message


# start game
@bravo_bot.message_handler(commands=['go'])
def go_command(message):        # launch bot

    # get current game instance
    current_game = get_game(message.chat.id)

    if current_game:            # if game is running
        bravo_bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    else:
        games.append(Game(message.chat.id))                                     # create game

        # show message with markup
        markup = telebot.types.ReplyKeyboardMarkup()                            # create markup
        markup.add(telebot.types.KeyboardButton('1'),
                   telebot.types.KeyboardButton('2'),
                   telebot.types.KeyboardButton('3'))                           # create buttons
        bravo_bot.send_message(message.chat.id,
                               'Выберете уровень сложности',
                               reply_markup=markup)                             # show message


# main message handler
@bravo_bot.message_handler(content_types=['text'])
def get_answer(message):

    # get current game instance
    current_game = get_game(message.chat.id)

    # if gabe is on
    if current_game:

        # if difficulty is chosen
        if current_game.difficulty:

            # if choice is already made
            if current_game.robotChoice:

                if message.text == str(current_game.robotChoice.number):            # if the answer is right

                    # finish game
                    bravo_bot.send_message(message.chat.id, '*Молодец\!*', parse_mode='MarkdownV2')
                    current_game.finish_game()
                else:                                                               # if the answer is wrong
                    bravo_bot.send_message(message.chat.id, '_Попробуй ещё раз_', parse_mode='MarkdownV2')

            # if choice is not yet made
            else:
                bravo_bot.delete_message(chat_id=message.chat.id, message_id=message.id)

        # if difficulty needs to be chosen
        else:

            if message.text in ('1', '2', '3'):                 # check for proper input

                current_game.difficulty = int(message.text)     # set difficulty
                current_game.start_game()                       # start game
            else:
                bravo_bot.delete_message(chat_id=message.chat.id, message_id=message.id)

    # if no game is on
    else:
        bravo_bot.delete_message(chat_id=message.chat.id, message_id=message.id)


bravo_bot.polling()     # make bot wait

# TODO: stickers as robots' property
# TODO: use properties
# TODO: properties as difficulty setting
# TODO: clear markup
