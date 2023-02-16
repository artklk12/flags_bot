import asyncio, requests, json, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
HOST = 'https://flags-server.onrender.com'
# HOST = 'http://127.0.0.1:8000'



class ClientStatesGroup(StatesGroup):
    in_menu = State()
    inviting = State()
    get_invited = State()
    confirmation = State()
    round1 = State()
    round2 = State()
    round3 = State()
    round4 = State()
    round5 = State()
    round6 = State()
    round7 = State()
    round8 = State()
    round9 = State()
    round10 = State()
    finished_answer = State()

round_states = (ClientStatesGroup.round1,ClientStatesGroup.round2,ClientStatesGroup.round3,ClientStatesGroup.round4,ClientStatesGroup.round5,ClientStatesGroup.round6,ClientStatesGroup.round7,ClientStatesGroup.round8,ClientStatesGroup.round9,ClientStatesGroup.round10)

def get_keyboard(host_id):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(text='Готов', callback_data=f'is_ready_to_fight_with_{host_id}'))
    kb.add(InlineKeyboardButton(text='Не готов', callback_data=f'is_ready_not_to_fight_with_{host_id}'))
    return kb


def get_end_match_kb():
    kb = ReplyKeyboardMarkup(one_time_keyboard=True)
    kb.add(KeyboardButton(text='Завершить матч'))
    return kb


def go_keyboard():
    kb = ReplyKeyboardMarkup(one_time_keyboard=True)
    kb.add(KeyboardButton(text='Начать матч'))
    return kb


def get_answers_keyboard(answers):
    kb = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    buttons = []
    for answer in answers:
        btn = KeyboardButton(text=f'{answer}')
        buttons.append(btn)
    kb.add(*buttons)
    return kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.delete()
    await ClientStatesGroup.in_menu.set()
    msg = await bot.send_message(chat_id=message.chat.id, text=f"Привет, твой id: {message.chat.id}")
    async with state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id



@dp.message_handler(commands=['test'])
async def test(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_photo(chat_id=message.chat.id, photo='https://countryflagsapi.com/png/br')

@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    await message.delete()
    await bot.send_message(chat_id=message.chat.id, text="Состояние сброшено")
    await state.finish()


@dp.message_handler(commands=['play'], state=ClientStatesGroup.in_menu)
async def play_solo(message: types.Message, state: FSMContext):
    await message.delete()
    msg = await bot.send_message(chat_id=message.chat.id, text="Запускаю соло матч")
    match_id = json.loads(requests.get(f'{HOST}/create_game/{message.from_user.id}/').text)['game_id']
    async with state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id
        data['match_id'] = match_id
        data['round'] = 1
        data['ready'] = False
        data['oponent'] = None
        data['cur_answer'] = None
        data['after_round_delete'] = []

    await ClientStatesGroup.round1.set()
    p1_time = await bot.send_message(chat_id=message.from_user.id, text=f"Матч начинается")
    for second in range(1, 4):
        await asyncio.sleep(0.5)
        await p1_time.edit_text("Матч начинается" + '.' * second)
    await p1_time.edit_text("Матч начался")
    round_info = json.loads(requests.get(f'{HOST}/game/{match_id}/get_round/{1}/').text)
    p1_msg1_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
    async with state.proxy() as data:
        data['after_round_delete'].append(p1_msg1_del)
        data['ready'] = True


@dp.message_handler(commands=['create_room'], state=ClientStatesGroup.in_menu)
async def create_room(message: types.Message, state: FSMContext):
    await message.delete()
    msg = await bot.send_message(chat_id=message.chat.id, text="Введите id соперника")
    async with state.proxy() as data:
        data['last_bot_msg_id'] = msg.message_id
    await ClientStatesGroup.inviting.set()


@dp.message_handler(state=ClientStatesGroup.inviting)
async def inviting(message: types.Message, state: FSMContext):
    oponent_id = message.text
    await message.delete()
    async with state.proxy() as data:
        last_msg_id = data['last_bot_msg_id']
    try:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=last_msg_id, text=f"Отправил вызов игроку {oponent_id}")
        msg = await bot.send_message(chat_id=oponent_id, text=f"Тебя вызвал: {message.chat.id}, готов принять вызов?", reply_markup=get_keyboard(message.from_user.id))
        oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
        async with oponent_state.proxy() as data:
            data['last_bot_msg_id'] = msg.message_id
        await oponent_state.set_state(ClientStatesGroup.get_invited)
    except:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=last_msg_id, text=f"Не удалось найти игрока с таким id")

@dp.callback_query_handler(lambda e: e.data.startswith("is_ready"), state=ClientStatesGroup.get_invited)
async def ready_callback(call: types.CallbackQuery, state: FSMContext):
    host_id = call.data.split('with_')[1]
    opponent_id = call.from_user.id
    player1_state = dp.current_state(chat=host_id, user=host_id)
    player2_state = dp.current_state(chat=opponent_id, user=call.from_user.id)

    async with player2_state.proxy() as data:
        opponent_last_msg_id = data['last_bot_msg_id']

    if 'not' in call.data:
        await player1_state.set_state(ClientStatesGroup.in_menu)
        await player2_state.set_state(ClientStatesGroup.in_menu)
        await bot.edit_message_text(chat_id=opponent_id, message_id=opponent_last_msg_id, text=f'Вы отклонили приглашение игрока: {call.from_user.id}')
        await bot.edit_message_reply_markup(chat_id=opponent_id, message_id=call.message.message_id, reply_markup=None)
    else:
        await bot.delete_message(chat_id=opponent_id, message_id=opponent_last_msg_id)
        await bot.send_message(chat_id=host_id, text='Противник принял вызов')


        match_id = json.loads(requests.get(f'{HOST}/create_game/{host_id}x{opponent_id}/').text)['game_id']
        async with player1_state.proxy() as data:
            data['match_id'] = match_id
            data['round'] = 1
            data['ready'] = False
            data['oponent'] = opponent_id

        async with player2_state.proxy() as data:
            data['match_id'] = match_id
            data['round'] = 1
            data['ready'] = False
            data['oponent'] = host_id

        await player1_state.set_state(ClientStatesGroup.confirmation)
        await player2_state.set_state(ClientStatesGroup.confirmation)
        host_msg = await bot.send_message(chat_id=host_id, text="Готовы начать матч?", reply_markup=go_keyboard())
        oponent_msg = await bot.send_message(chat_id=opponent_id, text="Готовы начать матч?", reply_markup=go_keyboard())
        async with player1_state.proxy() as data:
            data['last_bot_msg_id'] = host_msg.message_id
            data['waiting_msg'] = None
        async with player2_state.proxy() as data:
            data['last_bot_msg_id'] = oponent_msg.message_id
            data['waiting_msg'] = None

@dp.message_handler(state=ClientStatesGroup.confirmation)
async def wait_for_ready_both(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text == 'Начать матч':
        async with state.proxy() as data:
            match_id = data['match_id']
            round_id = data['round']
            data['ready'] = True
            oponent_id = data['oponent']
            data['cur_answer'] = None
            data['after_round_delete'] = []
        async with state.proxy() as data:
            ready = data['ready']
        if ready:
            oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
            async with oponent_state.proxy() as data:
                oponent_ready = data['ready']
            if not oponent_ready:
                await asyncio.sleep(0.5)
                try:
                    async with state.proxy() as data:
                        last_msg_id = data['last_bot_msg_id']
                    await bot.delete_message(chat_id=message.chat.id, message_id=last_msg_id)
                    msg = await bot.send_message(chat_id=message.chat.id, text="Ждём, пока противник нажмёт НАЧАТЬ МАТЧ")
                    async with state.proxy() as data:
                        data['last_bot_msg_id'] = msg.message_id
                except Exception:
                    await asyncio.sleep(0.3)
            else:
                async with state.proxy() as data:
                    last_msg_id = data['last_bot_msg_id']
                    data['ready'] = False
                async with oponent_state.proxy() as data:
                    opponent_last_msg_id = data['last_bot_msg_id']
                    data['ready'] = False
                try:
                    await bot.delete_message(chat_id=oponent_id, message_id=opponent_last_msg_id)
                except Exception:
                    pass
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=last_msg_id)
                except Exception:
                    pass
                await asyncio.sleep(1)
                await state.set_state(ClientStatesGroup.round1)
                await oponent_state.set_state(ClientStatesGroup.round1)
                p1_time = await bot.send_message(chat_id=message.chat.id, text=f"Матч начинается")
                p2_time = await bot.send_message(chat_id=oponent_id, text=f"Матч начинается")
                for second in range(1, 4):
                    await asyncio.sleep(0.5)
                    await p1_time.edit_text("Матч начинается" + '.' * second)
                    await p2_time.edit_text("Матч начинается" + '.' * second)
                await p1_time.edit_text("Матч начался")
                await p2_time.edit_text("Матч начался")
                round_info = json.loads(requests.get(f'{HOST}/game/{match_id}/get_round/{round_id}/').text)
                p1_msg1_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                p2_msg1_del = await bot.send_photo(chat_id=oponent_id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                async with state.proxy() as data:
                    data['after_round_delete'].append(p1_msg1_del)
                    data['ready'] = True
                async with oponent_state.proxy() as data:
                    data['after_round_delete'].append(p2_msg1_del)
                    data['ready'] = True
        else:
            await message.delete()

@dp.message_handler(state=round_states)
async def play_in_room(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        match_id = data['match_id']
        round_id = data['round']
        oponent_id = data['oponent']
        cur_answer = data['cur_answer']
        data['after_round_delete'].append(message)
        ready = data['ready']
    round_info = json.loads(requests.get(f'{HOST}/game/{match_id}/get_round/{round_id}/').text)

    if not cur_answer and ready:
        requests.post(f'{HOST}/game/{match_id}/get_round/{round_id}/', json={'player_id': message.from_user.id, 'player_answer': message.text, 'correct_answer': round_info['country']})
        await ClientStatesGroup.next()
        async with state.proxy() as data:
            data['ready'] = False
            data['cur_answer'] = message.text
        if round_info['country'] == message.text:
            msg3_del = await message.answer(text="Правильный ответ")
        else:
            msg3_del = await message.answer(text="Неправильный ответ")
        async with state.proxy() as data:
            data['after_round_delete'].append(msg3_del)
        if oponent_id:
            oponent_state = dp.current_state(chat=oponent_id, user=oponent_id)
            async with oponent_state.proxy() as data:
                op_cur = data['cur_answer']
                op_last_bot_msg = data['last_bot_msg_id']
        if not oponent_id or (await state.get_state() == await oponent_state.get_state() and op_cur):
            async with state.proxy() as data:
                data['cur_answer'] = None
                data['round'] += 1
                data['ready'] = False
            if oponent_id:
                async with oponent_state.proxy() as data:
                    data['cur_answer'] = None
                    data['round'] += 1
                    data['ready'] = False
            if round_id == 10:
                if oponent_id:
                    try:
                        await bot.delete_message(chat_id=oponent_id, message_id=op_last_bot_msg)
                    except:
                        await asyncio.sleep(1)
                        try:
                            await bot.delete_message(chat_id=oponent_id, message_id=op_last_bot_msg)
                        except:
                            pass
                    all_msg_del = []
                    msg7_del = await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил {op_cur}")
                    msg8_del = await bot.send_message(chat_id=oponent_id, text=f"Противник ответил {message.text}")
                    await asyncio.sleep(3)
                    async with state.proxy() as data:
                        data['after_round_delete'].extend((msg8_del, msg7_del))
                        all_msg_del.extend(data['after_round_delete'])
                    async with oponent_state.proxy() as data:
                        all_msg_del.extend(data['after_round_delete'])
                    results = json.loads(requests.get(f'{HOST}/game/{match_id}/', json={'user_id': message.from_user.id, 'oponent_id': oponent_id}).text)
                    user_result = results['user_result']

                    oponent_result = results['oponent_result']
                    await bot.send_message(chat_id=message.chat.id, text=f"Вы ответили правильно на {user_result}/{round_id} вопросов")
                    await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил правильно на {oponent_result}/{round_id} вопросов", reply_markup=get_end_match_kb())
                    await bot.send_message(chat_id=oponent_id, text=f"Вы ответили правильно на {oponent_result}/{round_id} вопросов", reply_markup=get_end_match_kb())
                    await bot.send_message(chat_id=oponent_id, text=f"Противник ответил правильно на {user_result}/{round_id} вопросов",)
                    await asyncio.sleep(1)
                    await state.set_state(ClientStatesGroup.finished_answer)
                    await oponent_state.set_state(ClientStatesGroup.finished_answer)
                    for msg in all_msg_del:
                        try:
                            await msg.delete()
                        except Exception:
                            continue
                else:
                    all_msg_del = []
                    async with state.proxy() as data:
                        all_msg_del.extend(data['after_round_delete'])
                    results = json.loads(requests.get(f'{HOST}/game/{match_id}/', json={'user_id': message.from_user.id, 'oponent_id': None}).text)
                    user_result = results['user_result']
                    await bot.send_message(chat_id=message.chat.id, text=f"Вы ответили правильно на {user_result}/{round_id} вопросов", reply_markup=get_end_match_kb())
                    await asyncio.sleep(1)
                    await state.set_state(ClientStatesGroup.finished_answer)
                    for msg in all_msg_del:
                        try:
                            await msg.delete()
                        except Exception:
                            continue
            else:
                if oponent_id:
                    try:
                        await bot.delete_message(chat_id=oponent_id, message_id=op_last_bot_msg)
                    except:
                        await asyncio.sleep(2)
                        try:
                            await bot.delete_message(chat_id=oponent_id, message_id=op_last_bot_msg)
                        except:
                            pass
                    msg2_del = await bot.send_message(chat_id=oponent_id, text=f"Противник ответил {message.text}")
                    msg4_del = await bot.send_message(chat_id=message.chat.id, text=f"Противник ответил {op_cur}")
                    round_info = json.loads(requests.get(f'{HOST}/game/{match_id}/get_round/{round_id + 1}/').text)
                    await asyncio.sleep(3)
                    msg5_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                    msg7_del = await bot.send_photo(chat_id=oponent_id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                    async with state.proxy() as data:
                        data['after_round_delete'].extend((msg2_del, msg4_del, msg5_del, msg7_del))
                        data['ready'] = True
                    async with oponent_state.proxy() as data:
                        data['ready'] = True
                else:
                    round_info = json.loads(requests.get(f'{HOST}/game/{match_id}/get_round/{round_id + 1}/').text)
                    await asyncio.sleep(3)
                    msg5_del = await bot.send_photo(chat_id=message.chat.id, photo=round_info['image'], reply_markup=get_answers_keyboard(round_info['answers']))
                    async with state.proxy() as data:
                        data['after_round_delete'].append(msg5_del)
                        data['ready'] = True
        else:
            msg = await bot.send_message(chat_id=message.chat.id, text="Ждём, пока противник закончит раунд")
            async with state.proxy() as data:
                data['last_bot_msg_id'] = msg.message_id
                data['after_round_delete'].append(msg)
    else:
        await message.delete()


@dp.message_handler(state=ClientStatesGroup.finished_answer)
async def finished(message: types.Message, state: FSMContext):
    if message.text == "Завершить матч":
        await message.answer("Спасибо за игру!", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ClientStatesGroup.in_menu)
    else:
        await message.delete()


@dp.message_handler(state=ClientStatesGroup.in_menu)
async def msg(message: types.Message):
    await message.answer(text=message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)