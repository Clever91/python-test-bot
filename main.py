from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
import logging
from speedtest import Speedtest

# logger
logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# buttons
buttons_start = ReplyKeyboardMarkup([['Statistika'], ['Dunyo'], ['Speedtest']], resize_keyboard=True)
buttons_back = ReplyKeyboardMarkup([['Back']], resize_keyboard=True)


def start(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(f'Salom {update.effective_user.first_name}', reply_markup=buttons_start)
  return 1

def stat(update: Update, context: CallbackContext) -> int:
	update.message.reply_text(f'Statistika bosildi', reply_markup=buttons_back)
	return 2

def speedtest(update: Update, context: CallbackContext) -> int:
	update.message.reply_text(f'Please, waiting...')
	s = Speedtest()
	try:
		s.get_best_server()
		s.download()
		s.upload()
		s.results.share()
		res = s.results.dict()
		stats = "⬆️ {:.0f} kBit/s\n⬇️ {:.0f} kBit/s\n⏱ {:.0f} ms".format(
			res['download'] / 1000,
			res['upload'] / 1000,
			res['ping']
		)
		update.message.reply_text(stats, reply_markup=buttons_back)
	except Exception as e:
		print(e)
	return 2

def world(update: Update, context: CallbackContext) -> int:
	update.message.reply_text(f'Dunto bosildi', reply_markup=buttons_back)
	return 2

updater = Updater('1417079413:AAH2XEg6mDPLT2aGRuyZWZn73IVKkOP9cFU')
conver_handler = ConversationHandler(
	entry_points = [ CommandHandler('start', start) ],
	states = {
		1: {
			MessageHandler(Filters.regex('^(Statistika)$'), stat),
			MessageHandler(Filters.regex('^(Dunyo)$'), world),
			MessageHandler(Filters.regex('^(Speedtest)$'), speedtest)
		},
		2: {
			MessageHandler(Filters.regex('^(Back)$'), start),
		}
	},
	fallbacks = [ MessageHandler(Filters.text, start) ]
)
updater.dispatcher.add_handler(conver_handler)

updater.start_polling()
updater.idle()