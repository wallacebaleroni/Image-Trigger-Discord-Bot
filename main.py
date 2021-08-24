import discord
import state
from postgreConnection import *
import requests
import random


def main():
    client = discord.Client()

    create_database()

    event_handlers(client)

    token = os.environ.get('TOKEN')
    client.run(token)


def event_handlers(client):
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        print("EVENT:")
        print(message)

        channel_id = message.channel.id
        text = message.content

        print("CHANNEL_ID="+message.content)
        print("MESSAGE="+text)

        if state.is_setting_keyword:
            set_keyword(text.upper(), channel_id)
            state.is_setting_keyword = False
            await message.channel.send('Ok. A palavra chave é ' + text + ".")
            return
        elif state.is_setting_imagerepo:
            set_imagerepo(text, channel_id)
            state.is_setting_imagerepo = False
            await message.channel.send('Ok. Repositório setado.')
            return

        if is_setkeyword_command(text):
            state.is_setting_keyword = True
            await message.channel.send('Qual é a palavra?')
            return
        elif is_setimagerepo_command(text):
            state.is_setting_imagerepo = True
            await message.channel.send('Qual é o link do repositório?')
            return

        keyword = get_keyword(channel_id)
        if keyword is None:
            print("KEYWORD NOT SET")
            await message.channel.send('A palavra-chave não está definida.')
            return
        print("KEYWORD=" + keyword)

        if keyword in text.upper:
            print("KEYWORD FOUND")
            image_url = get_imagerepo(channel_id)
            if image_url is None:
                print("REPO NOT SET")
                await message.channel.send('O repositório não está definido')
                return
            await message.channel.send(image_url)
        else:
            print("KEYWORD NOT FOUND")

        return


def is_setkeyword_command(text):
    if text.startswith("$setkeyword"):
        return True


def is_setimagerepo_command(text):
    if text.startswith("$setimagerepo"):
        return True


def get_image_from_repo(channel_id):
    repo_url = get_imagerepo(channel_id)

    if repo_url is None:
        return None

    repo_file = requests.get(repo_url)
    repo = repo_file.text.split('\n')

    return random.choice(repo)


main()
