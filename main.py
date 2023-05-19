from pyrogram import Client, filters

api_id = "your_api_id"
api_hash = "your_api_hash"
bot_token = "your_bot_token"

proxy_settings = {
    "proxy_type": "your_proxy_type",
    "addr": "your_proxy_address",
    "port": "your_port",
    "username": "your_proxy_username",
    "password": "your_proxy_password",
}

client = Client(
    "my_bot",
    api_id,
    api_hash,
    bot_token=bot_token,
    proxy=proxy_settings
)

chats = {}
messages_id = {}

publication_counter = 0


async def process_content(message_obj, main_id_chat):
    """
    Функція для обробки різних типів контенту та його надсилання у вказаний чат.

    :param message_obj: Об'єкт повідомлення, який потрібно обробити
    :param main_id_chat: ID чату, куди потрібно надіслати оброблений контент
    """
    if message_obj.photo:
        if message_obj.caption:
            await client.send_photo(
                main_id_chat, message_obj.photo.file_id, message_obj.caption
            )
        else:
            await client.send_photo(main_id_chat, message_obj.photo.file_id)
    if message_obj.audio:
        if message_obj.caption:
            await client.send_audio(
                main_id_chat, message_obj.audio.file_id, message_obj.caption
            )
        else:
            await client.send_audio(main_id_chat, message_obj.audio.file_id)
    if message_obj.document:
        if message_obj.caption:
            await client.send_document(
                main_id_chat, message_obj.document.file_id, message_obj.caption
            )
        else:
            await client.send_document(
                main_id_chat, message_obj.document.file_id
            )
    if message_obj.video:
        if message_obj.caption:
            await client.send_video(
                main_id_chat, message_obj.video.file_id, message_obj.caption
            )
        else:
            await client.send_video(main_id_chat, message_obj.video.file_id)
    if message_obj.voice:
        if message_obj.caption:
            await client.send_voice(
                main_id_chat, message_obj.voice.file_id, message_obj.caption
            )
        else:
            await client.send_voice(main_id_chat, message_obj.voice.file_id)
    if message_obj.text:
        await client.send_message(main_id_chat, message_obj.text)


@client.on_message(filters.command("last_id"))
async def handle_last_message_id(client, message):
    """
    Обробник команди "/last_id".

    Відправляє останній отриманий ID повідомлення для заданого чату.

    :param client: Клієнт Pyrogram
    :param message: Отримане повідомлення
    """
    text = message.text.split()
    await message.reply_text(messages_id[text[1]])


@client.on_message(filters.command("chat_list"))
async def handle_chat_list_command(client, message):
    """
    Обробник команди "/chat_list".

    Відправляє список доступних чатів.

    :param client: Клієнт Pyrogram
    :param message: Отримане повідомлення
    """
    await message.reply_text(", ".join(chat for chat in chats.keys()))


@client.on_message(filters.command("send_message"))
async def handle_send_message_command(client, message):
    """
    Обробник команди "/send_message".

    Відправляє вказане повідомлення у вказаний чат.

    :param client: Клієнт Pyrogram
    :param message: Отримане повідомлення
    """
    global publication_counter
    text = message.text.split()
    main_id_chat = chats[text[1]]
    parse_name_chat = chats[text[2]]
    message_id = text[3]
    parse_message = await client.get_messages(
        int(parse_name_chat),
        int(message_id)
    )
    await process_content(parse_message, main_id_chat)

    publication_counter += 1
    if publication_counter % 5 == 0:
        proxy_settings = {
            "proxy_type": "your_proxy_type",
            "addr": "your_proxy_address",
            "port": "your_port",
            "username": "your_proxy_username",
            "password": "your_proxy_password",
        }
        new_client = Client(
            "my_bot",
            api_id,
            api_hash,
            bot_token=bot_token,
            proxy=proxy_settings
        )
        await new_client.start()

        await client.stop()

        client = new_client


@client.on_message(filters.group)
async def handle_group_message(client, message):
    """
    Обробник повідомлення з групового чату.

    Зберігає ID чату та останнього отриманого повідомлення в словники chats та messages_id.

    :param client: Клієнт Pyrogram
    :param message: Отримане повідомлення
    """
    chat_id = message.chat.id
    chat_title = message.chat.title
    message_id = message.id
    chats[chat_title] = chat_id
    messages_id[chat_title] = message_id


client.run()
