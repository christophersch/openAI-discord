import discord
import openai
import json

client = discord.Client()
prefix = "!generate"

# open config file
conf_file = open('config.json')
conf_data = json.load(conf_file)
conf_file.close()


def textcompletion(prompt):
    try:
        tokens = int(len(prompt)/3)+1

        completion = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=4096 - tokens
        )
        response = f"**{prompt}** {completion.get('choices')[0].get('text')}"

    except openai.InvalidRequestError:
        response = 'Try rephrasing your prompt, something went wrong'
    except openai.error.RateLimitError:
        response = "OpenAI's server is currently overloaded with other requests. Are you happy now?"

    return response


# lets me know it woke up
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)+'. Father is pleased.')


# ai stuff
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif f"{prefix} " in message.content:
        async with message.channel.typing():

            input_prompt = str(message.content).replace(f"{prefix} ", '')

            output = textcompletion(input_prompt)[:3999]

            await message.reply(output)
    return

openai.api_key = conf_data.get('openai_api_key')
client.run(conf_data.get('discord_bot_key'))
