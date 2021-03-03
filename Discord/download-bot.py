
import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
#@bot.command()
def get_channel(message, given_name=None):
    for channel in message.guild.channels:
        if channel.name == given_name:
            return channel

@client.event
async def on_message(mssg):
    if mssg.content.startswith('record chat'):
        with open('output.txt', 'w+') as the_file:
            async for log in get_channel(mssg, 'general').history(limit=1000000000000000):
                  #async for log in client.logs_from(get_channel('general'), limit=1000000000000000):
                  stringTime = log.created_at.strftime("%Y-%m-%d %H:%M")
                  try:
                      author = log.author
                  except:
                      author = 'invalid'
                  message = str(log.content.encode("utf-8"))[2:-1]

                  template = '[{stringTime}] <{author}> {message}\n'
                  try:
                      the_file.write(template.format(stringTime=stringTime, author=author, message=message))
                  except:
                      author = log.author.discriminator
                      the_file.write(template.format(stringTime=stringTime, author=author, message=message))
                  print(template.format(stringTime=stringTime, author=author, message=message)[:-1])
                  #template.format(stringTime=stringTime, author=author, message=message)[:-1]
                  await get_channel(mssg, 'old-general-messages').send(template.format(stringTime=stringTime, author=author, message=message)[:-1])

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

client.run('ODEwOTMzNDEyMDU1NDgyNDA4.YCq2lw.19phntWK3EinmMTwPDDFg7w6UWA', bot=True)
