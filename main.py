
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import meme_generator as meme
import traceback
import logging
import config as c
import sys

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])

log = logging.getLogger('main')
log.addHandler(fh)
log.setLevel(c.LOGGER_CONFIG['level'])

TO_GENERATE_MEME_INFO = 'To generate meme run /generate template_name first_phrase second_phrase and so on\n' + \
    "To see all available template's names run /templates\n" + \
    'first_phrase second_phrase - any string that you want to add to your meme\n' + \
    'Pleace, use "-" symbol instead of space'

bot = Bot(token=c.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'], )
async def send_welcome(msg: types.Message):
    log.info('start command is running')
    await msg.answer('Welcome to memes generator! Use /help to see all commands.')


@dp.message_handler(commands=['help'], )
async def help(msg: types.Message):
    log.info('help command is running')
    await msg.answer(TO_GENERATE_MEME_INFO)
    template_name = 'ClassNote'
    params = ['I_love_you']
    await msg.answer(f'For example, your command:\n/generate {template_name} {" ".join(params)}')
    await msg.answer('Few seconds to wait...')
    await bot.send_photo(msg.from_user.id, photo=meme.generate(template_name, *params),
                         caption=f'Meme {template_name} {" ".join(params)}')
    await msg.answer(f'As you can see, we got meme by template named {template_name} with one phrase: {" and ".join(params)}')


@dp.message_handler(commands=['generate'], )
async def generate(msg: types.Message):
    '''
        генерирует мемы с параметрами: 
        1. шаблон мема
        2. блок текста мема(вместо пробела знак '-'), может быть несколько, разделять пробелами
    '''
    log.info('generate command is running')
    log.info(msg.text)
    if len(msg.text.split()) < 2:
        await msg.answer(TO_GENERATE_MEME_INFO)
    else:
        command, template, *params = msg.text.split()

        if template not in meme.TEMPLATES.keys():
            await msg.answer(f'Unknown meme template "{template}"')
            await msg.answer("To see all available templates run /templates")

        else:
            await bot.send_photo(msg.from_user.id, photo=meme.generate(template, *params),
                                 caption=f'Meme {template}: {", ".join(params)}')


@dp.message_handler(commands=['templates'], )
async def get_text_messages(msg: types.Message):
    '''
        Выводит на экран все возможные шаблоны мемов
    '''
    urlkb = InlineKeyboardMarkup(row_width=4)

    for template in meme.TEMPLATES.keys():
        urlkb.insert(
            InlineKeyboardButton(
                text=template,
                callback_data=f'/generate {template} {" ".join([f"phrase_{(count + 1)}" for count in range(meme.TEMPLATES[template])])}'
            )
        )

    await msg.answer('Available templates: ', reply_markup=urlkb)

    @dp.callback_query_handler(lambda c: c.data.startswith('/generate'))
    async def callback_query(callback_query: types.CallbackQuery):
        '''
            Обработчик при нажатии на кнопку с шаблоном мема, отправляет шаблон для ознакомления
        '''
        command, template, *args = callback_query.data.split()

        if template in meme.TEMPLATES.keys():
            await bot.send_photo(msg.from_user.id, photo=meme.generate(template, *args),
                                 caption=f'Meme {template}')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await msg.answer('Unknown command. Use HELP to see all available commands.')

if __name__ == '__main__':
    executor.start_polling(dp)
