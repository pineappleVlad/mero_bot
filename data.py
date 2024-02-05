from datetime import datetime

from telebot import types

cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"]
buttons = ['Опубликовать', 'Создать объявление заново']
channel_ids_long = {'Новосибирск': '-1002010810169', 'Москва': '-1002115842002', 'Екатеринбург': '-1002028710164', 'Санкт-Петербург': '-1002144192009'}
channel_ids_short = {'Новосибирск': '-1002120433604', 'Москва': '-1002106897762', 'Екатеринбург': '-1002008160160', 'Санкт-Петербург': '-1001856471244'}


base_headings = {'Бизнес': '#biz ',
            'Психология': '#Psy ',
            'Эзотерические': '#magic ',
            'Мужские': '#мужские ',
            'Женские': '#женские ',
            'Детские(с детьми)': '#детские ',
            'Образование/тренинги/обучение': '#обучение ',
            'Культура и искусство': '#культура ',
            'Музыкально-танцевальные': '#муз ',
            'Здоровье и спорт': '#здоровье ',
            'Настолки и дружеские встречи': '#games ',
            'Бесплатные': '#free💚 '}


biz_hashtags =  ['#networking', '#gameBiz', '#forum', '#marketing', '#sale', '#тренинг', '#manBiz', '#wonanBiz', '#ИИbiz']
psyco_hashtags = ['#отношения', '#тренинг']
magic_hashtags = ['#тренинг']
men_hashtags = ['#тренинг']
women_hashtags = ['#тренинг', '#девишник']
children_hashtags = ['#длямам']
edu_hashtags = ['#тренинг']
culture_hashtags = ['#театр', '#выставка']
music_hashtags = ['#концерт']
health_hashtags = ['#йога', '#хоккей', '#баскетбол', '#волейбол', '#футбол']
friends_hashtags = ['#мафия', '#НЕТворкинг', '#мозгоштурмы']
free_hashtags = ['#знакомства', '#молодёжное_пространство']

other_hashtags = {
    'Бизнес': biz_hashtags,
    'Психология': psyco_hashtags,
    'Эзотерические': magic_hashtags,
    'Мужские': men_hashtags,
    'Женские': women_hashtags,
    'Детские(с детьми)': children_hashtags,
    'Образование/тренинги/обучение': edu_hashtags,
    'Культура и искусство': culture_hashtags,
    'Музыкально-танцевальные': music_hashtags,
    'Здоровье и спорт': health_hashtags,
    'Настолки и дружеские встречи': friends_hashtags,
    'Бесплатные': free_hashtags
}



def post_text_for_channel_send(user_data, chat_id, channel_type, bot, channel_id):
    if 'date' in user_data:
        date_res_hash = datetime.strptime(str(user_data['date']), "%Y-%m-%d")
        output_date_hash = f"#{date_res_hash.strftime('%b_%d_%y').lower()}"

        user_data['data_hashtag'] = output_date_hash
        date_res = datetime.strptime(str(user_data['date']), "%Y-%m-%d")
        output_date = date_res.strftime("%d %B (%A)")
    else:
        output_date, output_date_hash = "", ""

    if 'offer' in user_data:
        if user_data['offer'] == 'skip':
            offer = ''
        else:
            offer = user_data['offer']
    else:
        offer = ''
    pattern = '\n'

    post_text = f'<strong>{user_data.get("topic", "")}</strong>\n' \
                f'«{user_data.get("event_name", "")}»\n \n' \
                f'{user_data.get("description", "")} \n \n' \
                f'🗓{output_date}\n' \
                f'⏰{user_data.get("time", "")}\n' \
                f'👥Кол-во участников: {user_data.get("people_count", "")}\n' \
                f'🏢Место: {user_data.get("address", "")} \n' \
                f'💸Цена: {user_data.get("price", "")} \n \n' \
                f'{offer}\n \n' \
                f'Разместил: @{user_data.get("username", "")} \n \n' \
                f'{output_date_hash} {user_data.get("hashtags", "").replace(pattern, " ").strip()}'

    post_text_short = f'<strong>{user_data.get("topic", "")}</strong>\n' \
                f'«{user_data.get("event_name", "")}»\n \n' \
                f'🗓{output_date}\n' \
                f'⏰{user_data.get("time", "")}\n' \
                f'👥Кол-во участников: {user_data.get("people_count", "")}\n \n' \
                f'{offer}\n \n' \
                f'{output_date_hash} {user_data.get("hashtags", "").replace(pattern, " ").strip()}'

    url_button, inline_keyboard = None, None
    if 'url' in user_data:
        url_button = types.InlineKeyboardButton("Регистрация", url=user_data['url'])
        inline_keyboard = types.InlineKeyboardMarkup().row(url_button) if url_button else None
    if 'image' not in user_data:
        user_data['image'] = 'skip'

    if len(post_text) <= 1024:
        if channel_type == 'long':
            if user_data['image'] == 'skip':
                bot.send_message(channel_id, post_text, parse_mode='HTML', reply_markup=inline_keyboard)
            else:
                bot.send_photo(channel_id, user_data.get('image', ''), caption=post_text, parse_mode='HTML',
                               reply_markup=inline_keyboard)
        elif channel_type == 'short':
            if user_data['image'] == 'skip':
                bot.send_message(channel_id, post_text_short, parse_mode='HTML')
            else:
                bot.send_photo(channel_id, user_data.get('image', ''), caption=post_text_short, parse_mode='HTML')
    else:
        bot.send_message(chat_id, 'Объявление получилось слишком длинным и бот не может его обработать, создание отменено\n'
                                  'Сократите текст и создайте объявление заново командой /start')