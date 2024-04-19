import telegram
from telegram.ext import Updater, CommandHandler
import random

# Простая реализация метода цепей Маркова для генерации текста
class MarkovChain:
    def __init__(self):
        self.chain = {}

    def add_to_chain(self, text):
        words = text.split()
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            if current_word in self.chain:
                self.chain[current_word].append(next_word)
            else:
                self.chain[current_word] = [next_word]

    def generate_text(self, length=10):
        current_word = random.choice(list(self.chain.keys()))
        text = current_word
        for _ in range(length - 1):
            if current_word in self.chain:
                next_word = random.choice(self.chain[current_word])
                text += " " + next_word
                current_word = next_word
            else:
                break
        return text

# Создание экземпляра бота
bot = telegram.Bot(token='7087795116:AAHn5gYFq3hERArfb4IpqNF0223RN57oOFI')

# Создание экземпляра метода цепей Маркова
markov_chain = MarkovChain()

# Загрузка обучающего текста из файла
with open("/home/marina/projects/tg_bot/bot/training_data.txt", "r", encoding="utf-8") as file:
    training_text = file.read()

# Обучение метода цепей Маркова на обучающем тексте
markov_chain.add_to_chain(training_text)

# Функция для обработки команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я бот, который генерирует предсказание настроения на день. Просто введите /generate для получения текста.")

# Функция для обработки команды /generate
def generate_text(update, context):
    # Генерация текста с помощью метода цепей Маркова
    generated_text = markov_chain.generate_text(length=20)
    context.bot.send_message(chat_id=update.effective_chat.id, text=generated_text)

def main():
    # Создание объекта бота и обработчика команд
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    # Добавление обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("generate", generate_text))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
