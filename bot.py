from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from pdf_creator import form_pdf
from utils import TestStates
from os import remove

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

pictures_id = {}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    pictures_id.update({message.chat.id: []})
    await state.set_state(TestStates.all()[0])
    await message.reply('Привет, отправь фотографии,' +
                        ' которые хочешь добавить в .pdf')


@dp.message_handler(state=TestStates.GET_PICTURES,
                    content_types=['photo'])
async def photo_handler(message: types.Message):
    photo = message.photo.pop()
    path = str(id(photo))+'.jpg'
    pictures_id[message.chat.id].append(path)
    await photo.download(path)


@dp.message_handler(state=TestStates.GET_PICTURES, commands=['2pdf'])
async def send_pdf(message: types.Message):
    user_id = message.chat.id
    paths = pictures_id[user_id]
    if paths:
        form_pdf(paths, user_id)
        await bot.send_document(
            message.from_user.id,
            open(f'{user_id}.pdf', 'rb')
            )
    await bot.send_message(
        message.from_user.id,
        'Введите /start если хотите продолжить работу')
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    remove(f'{user_id}.pdf')
    for path in pictures_id[user_id]:
        remove(path)


@dp.message_handler(state=TestStates.GET_PICTURES,
                    content_types=['any'])
async def process_start_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Отправьте фото')


@dp.message_handler(state=TestStates.SEND_PDF,
                    content_types=['any'])
async def wait(message: types.Message):
    pass


@dp.message_handler()
async def process_start_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Для начала работы введите /start')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
