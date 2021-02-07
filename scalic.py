from __future__ import unicode_literals
import os , sys , time,requests,json,ctypes
from halo import Halo
import discord
from random import *
import asyncio
import random
import shutil
import aiohttp
import re
from discord.ext import commands
os.system("cls")

#Notice - this bot is a selfbot to have some fun with. It's intentions aren't purely on thinks like nuking. So yes, those commands will be slow. I know and have made them fast for seperate projects.
# I'm fine with people learning from code. I originally learnt by finding scripts on github and changing things round to learn which part was doing which, but I am not a fan on people taking credit for other peoples work.
#If you feel like you have to change things like channel creation to say your name or whatever that's fine, but I'd really appreciate it if you don't change the footers on messages, this way other people can find out about my bot and use it
#Please don't sell my work either. It took ages and to give the source code out for free is kind, making money off my free work is just wrong
#This took lots of hours to work on. Signing up to github takes about 3 minutes max, starring my post  - https://github.com/scalic/scalic-selfbot - takes 5 seconds. If you wouldn't mind pressing the star I'd really appreciate it!
#Have fun :)
try:
    with open("settings.txt") as setup:
        setup = setup.readlines()

except Exception as error:
    print(f" | Did you extract me properly? Did you delete/rename settings.txt? I can't access it\n | Error : {error}")
    time.sleep(10)
    os._exit(0)

token = setup[0].replace('"',"").replace("TOKEN=","") #Removing the "" helps - some users will get their token from local storage which will lead to this I also know some people would probably delete the bit that says TOKEN= so did a foolproof way :)
#print(token)


spinner = Halo(
    text=' | Scalic Selfbot - Loading',
    spinner={
        'interval': 250,
        'frames': ['.', '..', '...']
    }
)
spinner.start()
sooo = requests.get('https://discordapp.com/api/v8/users/@me', headers={'Authorization': token.strip()})


if sooo.status_code == 200:
    spinner.succeed(' | Token valid - Starting up selfbot')    
    time.sleep(1)
    os.system("cls")
    validtoken = token

else:
    spinner.stop()
    os.system("cls")
    print(' | Invalid token. Put a valid token in settings.txt') 
    try:
        j = json.loads(sooo.text)
        errormessage = j['message']
        print(f" | Error : {errormessage}")
    except:
        pass
    time.sleep(5)
    os._exit(0)

prefix = setup[1].replace('"',"").replace("PREFIX=","") #just in case users put the details in " "
editing = setup[2].replace('"',"").replace("EDIT=","")
deletedmessagelogging = setup[3].replace('"',"").replace("DELETED-MESSAGE-LOGGER=","")
editedmessagelogging = setup[4].replace('"',"").replace("EDITED-MESSAGE-LOGGER=","")
nitrosnipe = setup[5].replace('"',"").replace("NITRO-SNIPE=","")
privnotesnipe = setup[6].replace('"',"").replace("PRIVNOTE-SNIPE=","")
giveawaysnipe = setup[7].replace('"',"").replace("GIVEAWAY-SNIPE=","")
pastebinsnipe = setup[8].replace('"',"").replace("PASTEBIN-SNIPE=","")



statusofediting = editing.strip().lower()
deletedmessagelogger = deletedmessagelogging.strip().lower()
editedmessagelogger = editedmessagelogging.strip().lower()

nitrosniping = nitrosnipe.strip().lower()
privnotesniping = privnotesnipe.strip().lower()
giveawaysniping = giveawaysnipe.strip().lower()
pastebinsniping = pastebinsnipe.strip().lower()

scalic = commands.Bot(prefix.strip(), self_bot=True)
scalic.remove_command("help") #this lets me add my own custom help cmd, rather then the ugly default one

spinner = Halo(
    text=' | Scalic Selfbot - Connecting',
    spinner={
        'interval': 250,
        'frames': ['.', '..', '...']
    }
)
spinner.start()

@scalic.event
async def on_command_error(ctx,error):
    print(error)


@scalic.event
async def on_connect():
    spinner.stop()
    os.system("cls")
    ctypes.windll.kernel32.SetConsoleTitleW(f" | {scalic.user.name} | {prefix.strip()}help |")
    print(f" | Connected To User {scalic.user.name}")

@scalic.command(aliases=['botconvert', 'botsay', 'convertbot'])
async def impersonate(ctx, member: discord.Member=None,*,message="I forgot to supply a message"):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    if ctx.guild == None:
        embed=discord.Embed(title="Use this command in a server", description="\nYou did it in dms", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.send(embed=embed)
    else:
        if not member:  
            member = ctx.message.author 
        embed=discord.Embed(title=f"Impersonating {member.name}", description=f"\nWith message: \"{message}\"", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.delete()
        #looks smoother, remove the # if you want info on the embeds
       # msg = await ctx.message.edit(content="",embed=embed)
        if len(await ctx.channel.webhooks()) != 0:
            webhook = random.choice(await ctx.channel.webhooks())
        else:

            webhook =await ctx.channel.create_webhook(name='scalic-selfbot')
        data={
          "content": f"{message}",
          "username": f"{member.name}",
          "avatar_url": f"{member.avatar_url}"
        }
            
        req = requests.post(f"{webhook.url}",json=data)
        randcolor = random.randint(0x000000, 0xFFFFFF)
        if req.status_code == 204:
            
            embed=discord.Embed(title=f"Impersonated {member.name}", description=f"\nWith message: \"{message}\"\n\nTask Completed Successfully", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            #await ctx.message.edit(content="",embed=embed,delete_after=2)            
        else:
            embed=discord.Embed(title=f"Impersonating {member.name}", description=f"\nWith message: \"{message}\"\n\nError Completing Task", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            #await ctx.message.edit(content="",embed=embed)            

@scalic.command()
async def embed(ctx,*,mesg=f"Format : {prefix.strip()}embed [words]"):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(description=mesg,color=randcolor)
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)


@scalic.command(aliases=['deletechans', 'deleteallchannels'])
async def deletechannels(ctx):
    await ctx.message.delete()
    for chan in guild.channels:
        try:
            await chan.delete()
        except:
            pass

@scalic.command(aliases=['deleterolls', 'deleteallroles'])
async def deleteroles(ctx):
    await ctx.message.delete()
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass




@scalic.command(aliases=['av', 'pfp'])
async def avatar(ctx, *,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title=f"{memb.name}'s Avatar!", description=f"Link: {memb.avatar_url}", color=randcolor)
    embed.set_thumbnail(url=memb.avatar_url)
    await ctx.message.edit(content="",embed=embed)


@scalic.command(aliases=['emojibig', 'urlemoji', 'emojiurl'])
async def bigemoji(ctx, emoji: discord.Emoji):
    await ctx.message.edit(content=emoji.url)

@scalic.command(aliases=['emojiadd', 'emadd', 'addem',"emojisteal","stealemoji"])
async def addemoji(ctx, emoji: discord.Emoji,*,nameofemoji=None):
    try:
        if nameofemoji == None:
            nameofemoji = emoji.name
        response = requests.get(emoji.url, stream=True)
        with open(f"./data/{nameofemoji}.jpeg", 'wb') as scalic_file: #have a feeling this only works with jpegs so jpeg it is :)
            shutil.copyfileobj(response.raw, scalic_file)

        with open(f"data/{nameofemoji}.jpeg", "rb") as f:
            image = f.read()
        await ctx.guild.create_custom_emoji(name = (nameofemoji), image = image)
        await asyncio.sleep(2) 
        guildemoji = discord.utils.get(scalic.get_guild(ctx.guild.id).emojis, name=nameofemoji)
        await ctx.message.edit(content=f"Successfully created emoji : {guildemoji}") #this way it will show as an emoji from the guild you just added the emoji too, rather then the original
        

    except Exception as error:
        await ctx.message.edit(content=f"Error adding emoji : {emoji}\nError : {error}")



@scalic.command(aliases=['stealserveremojis', 'stealemojis',"emojissteal", 'stealguildsemojis',"stealserversemojis","guildemojisteal",'guildemojissteal'])
async def stealguildemoji(ctx, guildid=None):
    if guildid == None:
        await ctx.message.edit(content=f"**Incorrect usage -** {prefix.strip()}emojisteal [guild-id]")
    else:
        emojisuccess = 0
        emojierror = 0
        emojiamount = 0
        emojilist = ""
        guildtostealfrom = scalic.get_guild(int(guildid))
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title=f"Scalic Selfbot - Emoji stealing from {guildtostealfrom.name}", description=f"Details:\nSuccessful emoji steals : {emojisuccess}\nErrors with emoji steals : {emojierror}", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)

        for emoji in guildtostealfrom.emojis:
            emojiamount += 1
            try:
                response = requests.get(emoji.url, stream=True)
                with open(f"./data/{emoji.name}.jpeg", 'wb') as scalic_file: #have a feeling this only works with jpegs so jpeg it is :)
                    shutil.copyfileobj(response.raw, scalic_file)

                with open(f"data/{emoji.name}.jpeg", "rb") as f:
                    image = f.read()
                await ctx.guild.create_custom_emoji(name = (emoji.name), image = image)
                await asyncio.sleep(2) 
                guildemoji = discord.utils.get(scalic.get_guild(ctx.guild.id).emojis, name=emoji.name)
                #await ctx.channel.send(content=f"Successfully created emoji : {guildemoji}") #people say this is too much spam
                emojilist = emojilist + f"{guildemoji} "
                emojisuccess += 1

            except Exception as error:
                emojierror += 1
                #await ctx.channel.send(content=f"Error adding emoji : {emoji}\nError : {error}")

            randcolor = random.randint(0x000000, 0xFFFFFF)
            embed=discord.Embed(title=f"Scalic Selfbot - Emoji stealing from {guildtostealfrom.name}", description=f"Details:\nSuccessful emoji steals : {emojisuccess}\nErrors with emoji steals : {emojierror}\n{emojilist}", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.message.edit(embed=embed)
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title=f"Scalic Selfbot - Finished emoji stealing from {guildtostealfrom.name}", description=f"Details:\nSuccessful emoji steals : {emojisuccess}\nErrors with emoji steals : {emojierror}\n{emojilist}", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(embed=embed)

@scalic.command(aliases=['embedsspam', 'spamembed', 'spamembeds'])
async def embedspam(ctx, count=5, *, desc="I forgot to specify the embed content"):
    await ctx.message.delete()
    if int(count) > 25:
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - embed spam", description=f"{count} embeds is too much - do 25 or less", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.send(embed=embed)
    else:
        for i in range(int(count)):
            randcolor = random.randint(0x000000, 0xFFFFFF)
            embed=discord.Embed(title="Scalic Selfbot - embed spam", description=desc, color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.send(embed=embed)


@scalic.command(aliases=['pinspam', 'masspin'])
async def spampin(ctx, count=None):
    if count == None:
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Pin spam", description=f"You didn't specify the amount of pins to do.\n{prefix.strip()}spampin [amount]", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")

        await ctx.message.edit(content="",embed=embed)
    else:
        async for message in ctx.message.channel.history(limit=int(count)):
            try:
                await message.pin()
            except:
                pass


@scalic.command(aliases=['purge'])
async def clear(ctx, amount):
    deleted = 0

    await ctx.message.delete()
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Message purger", description=f"Deleting messages", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    msg= await ctx.send(embed=embed)
    async for message in ctx.message.channel.history(limit=int(amount)).filter(
        lambda m: m.author == scalic.user
    ).map(lambda m: m):
        try:
            if message != msg:
                await message.delete()
                deleted = deleted + 1
                #embed=discord.Embed(title="Scalic Selfbot - Message purger", description=f"Deleted {deleted} messages", color=randcolor)
                #embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
                #embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
                #await msg.edit(embed=embed) #remove the # if you want but it'll slow it down a lot
        except:
            pass


    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Message purger", description=f"Finished.\nDeleted {deleted} messages", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await msg.edit(embed=embed,delete_after=3)

@scalic.command(aliases=['reactspam', 'massreact'])
async def spamreact(ctx, count=None, reaction=None):
    await ctx.message.delete()
    if count == None or reaction == None:
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - React spam", description=f"You didn't specify the amount of messages to react to or the reaction to use.\n{prefix.strip()}spamreact [amount]", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")

        await ctx.send(embed=embed)
    else:
        async for message in ctx.message.channel.history(limit=int(count)):
            try:
                await message.add_reaction(reaction)
            except:
                pass

@scalic.command(aliases=['editspam', 'massedit'])
async def spamedit(ctx, count=None,*, mesg=None):
    await ctx.message.delete()
    if count == None or mesg == None:
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Message edit spam", description=f"You didn't specify the amount of messages to edit or the content to edit the messages to.\n{prefix.strip()}spamedit [amount] [message]", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")

        await ctx.send(embed=embed)
    else:
        edited = 0
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Message edit spam", description=f"Editing messages", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        msg= await ctx.send(embed=embed)
        async for message in ctx.channel.history(limit=int(count)):
            try:
                if message.author == scalic.user:
                    if message != msg:
                        await message.edit(content=mesg,embed=None)
                        edited = edited + 1
            except:
                pass

        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Message edit spam", description=f"Finished.\nEdited {edited} messages", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await msg.edit(embed=embed,delete_after=3)



@scalic.command(aliases=['deletedmessagelogger', 'deletedmessageslogger',"logdeleted","deletedlogger"])
async def logdeletedmessages(ctx,deletestatus=None):
    global deletedmessagelogger 
    if deletestatus == None:
        if deletedmessagelogger == "off":
            deletedmessagelogger = "on"
        elif deletedmessagelogger == "on":
            deletedmessagelogger = "off"
    else:
        if deletestatus.lower() == "off":
            deletedmessagelogger = "off"
        if deletestatus.lower() == "on":
            deletedmessagelogger = "on"

        if deletestatus.lower() == "true": #could i of made the code shorter : yes ... but i like it this way, more clearer to scroll past
            deletedmessagelogger = "on"
        if deletestatus.lower() == "false":
            deletedmessagelogger = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Deleted message logger", description=f"Deleted message logger is now : `{deletedmessagelogger}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['editedmessagelogger', 'editedmessageslogger','editlog','logedit',"editlogger"])
async def logediteddmessages(ctx,editstatus=None):
    global editedmessagelogger 
    if editstatus == None:
        if editedmessagelogger == "off":
            editedmessagelogger = "on"
        elif editedmessagelogger == "on":
            editedmessagelogger = "off"
    else:
        if editstatus.lower() == "off":
            editedmessagelogger = "off"
        if editstatus.lower() == "on":
            editedmessagelogger = "on"

        if editstatus.lower() == "true": #could i of made the code shorter : yes ... but i like it this way, more clearer to scroll past
            editedmessagelogger = "on"
        if editstatus.lower() == "false":
            editedmessagelogger = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Deleted message logger", description=f"Deleted message logger is now : `{editedmessagelogger}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)


@scalic.command(aliases=['editmode', 'editall'])
async def edit(ctx,editstatus=None):
    global statusofediting 
    if editstatus == None:
        if statusofediting == "off":
            statusofediting = "on"
        elif statusofediting == "on":
            statusofediting = "off"
    else:
        if editstatus.lower() == "off":
            statusofediting = "off"
        if editstatus.lower() == "on":
            statusofediting = "on"

        if editstatus.lower() == "true":
            statusofediting = "on"
        if editstatus.lower() == "false":
            statusofediting = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Edit mode", description=f"Edit mode is now : `{statusofediting}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['nitrosniper', 'snipenitro'])
async def nitrosnipe(ctx,snipestatus=None):
    global nitrosniping 
    if snipestatus == None:
        if nitrosniping == "off":
            nitrosniping = "on"
        elif nitrosniping == "on":
            nitrosniping = "off"
    else:
        if snipestatus.lower() == "off":
            nitrosniping = "off"
        if snipestatus.lower() == "on":
            nitrosniping = "on"

        if snipestatus.lower() == "true":
            nitrosniping = "on"
        if snipestatus.lower() == "false":
            nitrosniping = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Nitro Sniper", description=f"Nitro sniper is now : `{nitrosniping}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['privnotesniper', 'snipeprivnote'])
async def privnotesnipe(ctx,snipestatus=None):
    global privnotesniping 
    if snipestatus == None:
        if privnotesniping == "off":
            privnotesniping = "on"
        elif privnotesniping == "on":
            privnotesniping = "off"
    else:
        if snipestatus.lower() == "off":
            privnotesniping = "off"
        if snipestatus.lower() == "on":
            privnotesniping = "on"

        if snipestatus.lower() == "true":
            privnotesniping = "on"
        if snipestatus.lower() == "false":
            privnotesniping = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Privnote Sniper", description=f"Privnote sniper is now : `{privnotesniping}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['giveawaysniper', 'snipegiveaway',"snipegw","gwsniper"])
async def giveawaysnipe(ctx,snipestatus=None):
    global giveawaysniping 
    if snipestatus == None:
        if giveawaysniping == "off":
            giveawaysniping = "on"
        elif giveawaysniping == "on":
            giveawaysniping = "off"
    else:
        if snipestatus.lower() == "off":
            giveawaysniping = "off"
        if snipestatus.lower() == "on":
            giveawaysniping = "on"

        if snipestatus.lower() == "true":
            giveawaysniping = "on"
        if snipestatus.lower() == "false":
            giveawaysniping = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Giveaway Sniper", description=f"Giveaway sniper is now : `{giveawaysniping}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['pastebinsniper', 'snipepastebins',"pastesnipe","snipepaste","snipepastebin"])
async def pastebinsnipe(ctx,snipestatus=None):
    global pastebinsniping 
    if snipestatus == None:
        if pastebinsniping == "off":
            pastebinsniping = "on"
        elif pastebinsniping == "on":
            pastebinsniping = "off"
    else:
        if snipestatus.lower() == "off":
            pastebinsniping = "off"
        if snipestatus.lower() == "on":
            pastebinsniping = "on"

        if snipestatus.lower() == "true":
            pastebinsniping = "on"
        if snipestatus.lower() == "false":
            pastebinsniping = "off"

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Pastebin Sniper", description=f"Pastebin sniper is now : `{pastebinsniping}`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['sniper', 'snipersettings',"settingsniper","sniperon","sniperoff"])
async def snipe(ctx):
    global nitrosniping
    global privnotesniping
    global giveawaysniping
    global pastebinsniping
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Sniper Info", description=f"Nitro sniper status : `{nitrosniping}`\nPrivnote sniper status : `{privnotesniping}\n`Giveaway sniper status : `{giveawaysniping}`\nPastebin sniper status : `{pastebinsniping}`\nCommands : `{prefix.strip()}nitrosnipe`,`{prefix.strip()}privnotesnipe`,`{prefix.strip()}giveawaysnipe`,`{prefix.strip()}pastebinsnipe`", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['id', 'userid',"useridtoname"])
async def idtoname(ctx, personsid: int):
    if len(str(personsid)) != 18:
        await message.edit(content = f"**This command requires a user id - Turn on developers mode, get the id and run the command again! <:Sad:793595402842538045>**")    
    else:
        user = await scalic.fetch_user(personsid)
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Id to username", description=f"ID [{str(personsid)}]  = `{user.name}#{user.discriminator}`", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/dKfTyqLt1jkqIfiMXj/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)



@scalic.command(aliases=['asci','cooltext',])
async def ascii(ctx, *,paste=f"Format is {prefix.strip()}ascii [text]"):

    if paste == f"Format is {prefix.strip()}ascii [text]":
        await ctx.message.edit(content=paste)
    else:
        finaltext = paste.replace(" ", "+")
        asciiresponse = requests.get(f"http://artii.herokuapp.com/make?text={finaltext}&font=rounded") 
        await ctx.message.edit(content=f" ``` {asciiresponse.text} ``` ")

@scalic.command(aliases=['channelnuke','nukechannel',])
async def nuke(ctx):

    channel_position = ctx.channel.position
    new_chan = await ctx.channel.clone()
    await ctx.channel.delete()
    await new_chan.edit(position = channel_position) 
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Channel Nuked", description=f"<#{new_chan.id}> - {new_chan.name} has been nuked", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/dKfTyqLt1jkqIfiMXj/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await new_chan.send(embed=embed,delete_after=10)

@scalic.event
async def on_message(ctx):
    global edit
    global nitrosniping
    global privnotesniping
    global giveawaysniping
    global pastebinsniping
    if nitrosniping == "on":
        if 'discord.gift' in ctx.content: 
            nitrotext = open("Log/nitrolog.txt","a") 
            code = re.search("discord.gift/(.*)", ctx.content).group(1)

            try:
                nitrotext.write(f"[!] Nitro Found! // Server: {ctx.guild.name} // Channel: {ctx.channel.name} // Sent By: {ctx.author.name}#{ctx.author.discriminator}\n")
            except:
                nitrotext.write(f"[!] Nitro Found! Sent By: {ctx.author.name}#{ctx.author.discriminator}\n")
            if len(code) == 24 or len(code) == 16:
                result = requests.post('https://discordapp.com/api/v6/entitlements/gift-codes/'+code+'/redeem', json={"channel_id":str(ctx.channel.id)}, headers={'authorization':token.strip()}).text
                code = re.search("discord.gift/(.*)", ctx.content).group(1)

                if 'this gift has been redeemed already.' in result.lower():
                    nitrotext.write(f"[-] discord.gift/{code} Has already been claimed\n")
                elif 'nitro' in result.lower():
                    nitrotext.write(f"[+] discord.gift/{code} WAS SNIPED!!!\n")
                elif 'unknown gift code' in result.lower():
                    nitrotext.write(f"[-] discord.gift/{code} Was an invalid code\n")
            else:
                nitrotext.write(f"[-] discord.gift/{code} Was a fake code\n") 
            nitrotext.close()
    if pastebinsniping == "on":
        if 'pastebin' in ctx.content: #while it cant exactly be "sniped" - people still drop stuff in pastebin from time to time that you might not see , depending on whether its a method or sum, still usefull to have imo
        
            code = re.search("pastebin.com/(.*)", ctx.content).group(1) 
            if len(code) == 8:
                pasteresult = requests.get(f"https://pastebin.com/raw/{code}")
                if pasteresult.status_code != 404: 
                    with open(f'Pastebin/{code}.txt', 'w+') as pastebinsave:
                        pastebinsave.write(f"[+] Results from pastebin.com/{code}:\n\n{pasteresult.text}")
                        pastebinsave.close()




    if giveawaysniping == "on":
        if 'giveaway' in str(ctx.content).lower():
            if ctx.author.id == 294882584201003009  or ctx.author.id == 673918978178940951 or ctx.author.id == 716967712844414996 or ctx.author.id == 582537632991543307 or ctx.author.id == 450017151323996173 or ctx.author.id == 574812330760863744:
                await asyncio.sleep(8) # so yall dont get accused of sniping giveaways but still enter all - min gw time for the big giveaway bot is 10 seconds
                await ctx.add_reaction("🎉")
                with open(f'Log/gwlog.txt', 'w+') as gwlog:
                    try:
                        gwlog.write(f"[!] Giveaway Entered! // Server: {ctx.guild.name} // Channel: {ctx.channel.name} // Bot: {ctx.author.name}#{ctx.author.discriminator} \n")
                    except:
                        gwlog.write(f"[+] Giveaway Entered : Server/Channel Not writable because of characters used :| //  Bot: {ctx.author.name}#{ctx.author.discriminator} \n[+] Message: {ctx.content}\n")
                


        if f'<@{scalic.user.id}>' in str(ctx.content): #
            if ctx.author.id == 294882584201003009 or ctx.author.id == 673918978178940951 or ctx.author.id == 716967712844414996 or ctx.author.id == 582537632991543307 or ctx.author.id == 450017151323996173 or ctx.author.id == 574812330760863744:
                with open(f'Log/gwlog.txt', 'w+') as gwlog:
                    try:
                        gwlog.write(f"[+] Giveaway Won: {ctx.guild.name} // Channel: {ctx.channel.name} //  Bot: {ctx.author.name}#{ctx.author.discriminator}\n[+] Message: {ctx.content}\n")
                    except:
                        gwlog.write(f"[+] Giveaway Won: Server/Channel Not writable because of characters used :| //  Bot: {ctx.author.name}#{ctx.author.discriminator}\n[+] Message: {ctx.content}\n")

    if privnotesniping == "on":
        if 'privnote' in ctx.content: 
        
            code = re.search("privnote.com/(.*)", ctx.content).group(1) 
            try:
                privnotesnipe = pn.read_note(f"https://privnote.com/{code}")
                with open(f'Privnote/{code}.txt', 'w+') as pastebinsave:
                    pastebinsave.write(f"[+] Results from privnote.com/{code}:\n\n{privnotesnipe}")
                    pastebinsave.close()
            except:
                pass



    if statusofediting == "on":
        if ctx.author.id == scalic.user.id:
            try:
                message = ctx
                await message.edit(content=f"{ctx.content} ")
            except:
                pass
    await scalic.process_commands(ctx)

@scalic.event
async def on_message_delete(ctx):
    global deletedmessagelogger
    if deletedmessagelogger == "on":
        if ctx.guild == None:
            if ctx.author.id != scalic.user.id:
                if len(str(ctx.content)) != 0: #if theyre using a sb itll show nothing so yuh
                    try:
                        await ctx.channel.send(f"**Message logged by {ctx.author.mention} : ** \n{ctx.content}")
                    except:
                        pass
    await scalic.process_commands(ctx)

@scalic.event
async def on_message_edit(before,after):
    global editedmessagelogger
    if editedmessagelogger == "on":
        if after.guild == None:
            if after.author.id != scalic.user.id:
                if before.content != after.content: #embeds sometimes mess with it
                    try:
                        await after.channel.send(f"**Message edited by {after.author.mention} : ** \n**Before : **{before.content}\n**After : **{after.content}")
                    except:
                        pass


    await scalic.process_commands(after)



    



@scalic.command(aliases=['cleardms','dmsclear',])
async def dmclear(ctx):
    usersdone = 0
    totalmessage = 0
    await ctx.message.delete()
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Message Clearer", description=f"Clearing all messages with all users", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    msg= await ctx.send(embed=embed)
    for channel in scalic.private_channels:
        if isinstance(channel, discord.DMChannel):
            async for message in channel.history(limit=9999):
                try:
                    if message.author == scalic.user:
                        if message != msg:
                            await message.delete()
                            totalmessage = totalmessage + 1
                except:
                    pass

        usersdone = usersdone + 1
        randcolor = random.randint(0x000000, 0xFFFFFF)
        embed=discord.Embed(title="Scalic Selfbot - Message Clearer", description=f"Clearing all messages with all users\nUsers Done : {usersdone}\nTotal Messages Deleted : {totalmessage}", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await msg.edit(embed=embed)  #like said before - i could get a smoother "live" update count but it slows the bot down so much


    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(title="Scalic Selfbot - Message Clearer", description=f"Clearing all messages with all users\nTask completed - Cleared messages with {usersdone} Users\nTotal Messages Deleted : {totalmessage}", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await msg.edit(embed=embed,delete_after=15)

@scalic.command()
async def joke(ctx):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    joke = requests.get("https://sv443.net/jokeapi/v2/joke/Pun?blacklistFlags=nsfw,racist,sexist&type=twopart").text
    j = json.loads(joke)
    setup = j['setup']
    delivery = j['delivery']

    embed=discord.Embed(title="Scalic Selfbot - Joke requested", description=f"{setup}\n||{delivery}||", color=randcolor)
    embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
    embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['stickbugged'])
async def stickbug(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    finalurl = str(memb.avatar_url)
    finalurl = finalurl.replace("gif","png")
    await ctx.message.edit(content="_this command takes a while, please be patient_")
    stikcbug = requests.get(f"https://nekobot.xyz/api/imagegen?type=stickbug&url={finalurl}").text
    j = json.loads(stikcbug)
    stickbugvid = j['message']
    await ctx.message.edit(content=stickbugvid)


@scalic.command(aliases=['urbandictionary',"dictionary"])
async def ud(ctx,*,wordtodefine=None):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    if wordtodefine == None:  
        embed=discord.Embed(title="Scalic Selfbot - Urban Dictionary Command", description=f"You didn't supply a word to define?", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)
    else:
        defineword = wordtodefine.replace(" ","%20")
        data = requests.get(f"https://api.urbandictionary.com/v0/define?term={defineword}")
        
        try:
            j = json.loads(data.text)
            ud_def = j['list']
            ud_def = str(ud_def)
            ud_data_yes = ud_def.split("', 'permalink'") 

            ud_data_yes = ud_data_yes[0].split(": '") 

            finaldef = ud_data_yes[1].replace("[","").replace("]","").replace("\\n","\n").replace("\\r","")
            #was losing my mind, I'll of learnt about json since but I was tryna make this and no one i knew knew how to help so yeah :)

            embed=discord.Embed(title="Scalic Selfbot - Urban Dictionary Command", description=f"Definition of `{wordtodefine}`\n{finaldef}\n\n", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.message.edit(content="",embed=embed)
        except:
            embed=discord.Embed(title="Scalic Selfbot - Urban Dictionary Command", description=f"Error when searching for the term : `{wordtodefine}`", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.message.edit(content="",embed=embed)           

@scalic.command(aliases=['deepfri'])
async def deepfry(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    finalurl = str(memb.avatar_url)
    finalurl = finalurl.replace("gif","png")
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=deepfry&image={finalurl}").text
    j = json.loads(data)
    deepfri = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=deepfri)
    await ctx.message.edit(content="",embed=embed)

@scalic.command()
async def blurpify(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    finalurl = str(memb.avatar_url)
    finalurl = finalurl.replace("gif","png")
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=blurpify&image={finalurl}").text
    j = json.loads(data)
    blurple = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=blurple)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['magicify',"magikify"])
async def magic(ctx,  memb : discord.Member=None,intense="5"):
    if memb == None:  
        memb = ctx.message.author 

    finalurl = str(memb.avatar_url)
    finalurl = finalurl.replace("gif","png")
    finalurl = finalurl.replace("webp","png")
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=magik&image={finalurl}&intensity={intense}").text
    j = json.loads(data)
    magicwoah = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=magicwoah)
    await ctx.message.edit(content="",embed=embed)


    
@scalic.command(aliases=['cylde'])
async def clyde(ctx,*, message=f"Maybe supply a message next time | {prefix.strip()}clyde [message-here]"):

    cylde = requests.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={message}").text
    j = json.loads(cylde)
    clydeimg = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=clydeimg)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['jealous',"distracted"])
async def ship(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=ship&user1={memb.avatar_url}&user2={ctx.message.author.avatar_url}").text
    j = json.loads(data)
    ship = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=ship)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['whowouldwin'])
async def www(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=whowouldwin&user1={ctx.message.author.avatar_url}&user2={memb.avatar_url}").text
    j = json.loads(data)
    ship = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=ship)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['catcha',"capture"]) #for those who cant spell
async def captcha(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=captcha&url={memb.avatar_url}&username={memb.name}").text
    j = json.loads(data)
    captcha = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=captcha)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['threats'])
async def threat(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 
    finalurl = str(memb.avatar_url)
    finalurl = finalurl.replace("gif","png")
    threatdata = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={finalurl}").text
    j = json.loads(threatdata)
    threatmeme = j['message']
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=threatmeme)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=["twitter","twittertweet"])
async def tweet(ctx, member: discord.Member,*,tweetmessage=f"Format : {prefix.strip()}tweet [member] [message]"):
    tweeter = requests.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={member.name}&&text={tweetmessage}").text
    j = json.loads(tweeter)
    finalimage = j['message']

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=finalimage)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=["cmm","changemind"])
async def changemymind(ctx,*,changemymindtext=None):
    if changemymindtext == None:
        changemymindtext = f"{ctx.message.author.name} should supply a message after doing {prefix.strip()}changemymind"
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={changemymindtext}").text
    j = json.loads(data)
    changemymindimage = j['message']

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=changemymindimage)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=["kanagen"])
async def kannagen(ctx,*,kannatext=None):
    if kannatext == None:
        kannatext = f"{ctx.message.author.name} the format is {prefix.strip()}kannagen [message]"
    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=kannagen&text={kannatext}").text
    j = json.loads(data)
    kannaimg = j['message']

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=kannaimg)
    await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=["iphoneex","phone","iphone"])
async def iphonex(ctx,  memb : discord.Member=None):
    if memb == None:  
        memb = ctx.message.author 

    data = requests.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={memb.avatar_url}").text
    j = json.loads(data)
    phonephoto = j['message']

    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=phonephoto)
    await ctx.message.edit(content="",embed=embed)

    

@scalic.command(aliases=["gender"])
async def name(ctx,*,namesupplied=None):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    if namesupplied == None:
        embed=discord.Embed(title="Scalic Selfbot - Gender command", description=f"You didn't supply a name\n{prefix.strip()}name [name]", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)
    else:
        data = requests.get(f"https://api.genderize.io/?name={namesupplied}").text
        j = json.loads(data)
        gen = j['gender']
        likely = j['probability']
        
        embed=discord.Embed(title="Scalic Selfbot - Gender command", description=f"Majority of people named {namesupplied} are {gen}", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)

@scalic.command(aliases=['qrcode'])
async def qr(ctx,*,msgg="This user didn't supply a message lel"):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    msgg = msgg.replace(" ","%20")
    randcolor = random.randint(0x000000, 0xFFFFFF)
    embed=discord.Embed(color=randcolor)
    embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={msgg}")
    await ctx.message.edit(content="",embed=embed)


@scalic.command(aliases=['deletewebhook'])
async def webhookdelete(ctx,link=None):
    randcolor = random.randint(0x000000, 0xFFFFFF)
    if link == None:
        embed=discord.Embed(title="Scalic Selfbot - No webhook supplied", description=f"{prefix.strip()}webhookdelete [webhook]", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)
    else:
        embed=discord.Embed(title="Scalic Selfbot - Deleting webhook", description=f"Sending a delete request to\n{link}", color=randcolor)
        embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
        embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
        await ctx.message.edit(content="",embed=embed)


        result = requests.delete(link)
        randcolor = random.randint(0x000000, 0xFFFFFF)
        if result.status_code == 204:
            embed=discord.Embed(title="Scalic Selfbot - Webhook Deleted", description=f"Yay", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.message.edit(embed=embed)
        else:
            embed=discord.Embed(title="Scalic Selfbot - Error Deleting Webhook", description=f"Delete request responded with status code : {result.status_code}\{result.text}", color=randcolor)
            embed.set_thumbnail(url="https://media.giphy.com/media/YpGPs0rAJQC1lngD0R/giphy.gif")
            embed.set_footer(text="https://github.com/scalic/scalic-selfbot")
            await ctx.message.edit(embed=embed)

scalic.run(token.strip(), bot=False)
