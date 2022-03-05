import os, json
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 17610132
API_HASH = "cb0d413e6f5ea5a0d8b97c2a3cd8e811"
BOT_TOKEN = "5286706406:AAF50uqs_IqVR6Cx-Y_gNL8G9JHs5COdMPI" #INSERISCI BOT TOKEN
DEFAULT_ADMINS = [5033189090] #INSERISCI UNO O PIU' FOUNDER ID SEPARATI DA VIRGOLE
CHANNEL = "antololp" #INSERISCI CANALE ! IMPORTANTE ! INSERIRLO SENZA LA @ DAVANTI

# CARICAMENTO SALVATAGGI #
if os.path.exists("storage.json"):
    with open("storage.json", "r+") as f:
        SAVES = json.load(f)
else:
    SAVES = {"Groups": [], "Scammers": [], "Staff": DEFAULT_ADMINS}
    with open("storage.json", "w+") as f:
        json.dump(SAVES, f)
    

def save():
    global SAVES
    with open("storage.json", "w+") as f:
        json.dump(SAVES, f)
    

###########################

bot = Client("sessin", API_ID, API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.new_chat_members)
async def joinManager(client, message):
    global SAVES
    for user in message.new_chat_members:
        if user.is_self:
            if not message.chat.id in SAVES["Groups"]:
                # MESSAGGIO APPENA METTI IL BOT NEL GRUPPO
                await message.reply_text("**Grazie per avermi aggiunto, per usare tutte le funzioni del bot mettimi admin e invia il comando /add.**")
        elif message.chat.id in SAVES["Groups"] and not user.is_bot:
            if user.id in SAVES["Scammers"]:
                await client.kick_chat_member(message.chat.id, user.id)
                if user.username == None:
                    if user.last_name == None:
                        mention = f"[{user.first_name}](tg://user?id={user.id})"
                    else:
                        mention = f"[{user.first_name} {user.last_name}](tg://user?id={user.id})"
                else:
                    mention = "@" + user.username
                # MESSAGGIO QUANDO ENTRA UNO SCAMMER
                await message.reply_text(f"⚠️ [{user.first_name}](tg://user?id={user.id}) **era uno scammer ed è stato bannato ⚠️**")
            
        
    

@bot.on_message(filters.text)
async def commandsManager(client, message):
    global SAVES, CHANNEL   
    if message.text.startswith("/addamministratore"):
     if message.from_user.id in SAVES["Staff"]:
        if message.reply_to_message == None:
            st = message.text.split(" ")
            if st.__len__() == 2:
                try:
                    usr = await client.get_users(st[1])
                    if usr == None:
                        await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                        return
                    else:
                        ID = usr.id
                except:
                    await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                    return
            else:
                await message.reply_text("**⚠️ Specificare l' ID o la @ dell' utente ⚠️**")
                return
        else:
            ID = message.reply_to_message.from_user.id
        if not ID in SAVES["Staff"]:
            SAVES["Staff"].append(ID)
            save()
            await message.reply_text("**👮Utente reso Supporter**")
            try:
                await client.send_message(ID, "**👮Sei un amministratore del bot ecco i tuoi comandi**\n\n🎛Comandi🎛\n/netban id o @ link proof\n/netunban id")
            except:
                pass
        else:
            await message.reply_text("**👮Quest utente è già un amministratore**")
    elif message.text.startswith("/removeamministratore"):
        if message.reply_to_message == None:
            st = message.text.split(" ")
            if st.__len__() == 2:
                try:
                    usr = await client.get_users(st[1])
                    if usr == None:
                        await message.reply_text("**🤔Utente Non Trovato**")
                        return
                    else:
                        ID = usr.id
                except:
                    await message.reply_text("**🤔Utente Non Trovato**")
                    return
            else:
                await message.reply_text("**🔎Specificare l' ID o la @ dell' utente**")
                return
        else:
            ID = message.reply_to_message.from_user.id
        if ID in SAVES["Staff"]:
            SAVES["Staff"].remove(ID)
            save()
            await message.reply_text("**😔Utente rimosso dalla lista degli amministratori**")
            try:
                await client.send_message(ID, "**❌Sei stato rimosso dalla lista degli amministratori**")
            except:
                pass
        else:
            await message.reply_text("**⚠️ Quest utente non è un amministratore⚠️**")
    elif message.text.startswith("/netban"):
        if message.from_user.id in SAVES["Staff"]:
            st = message.text.split(" ")
            if st.__len__() == 3 and st[2].startswith("http"):
                if st[1].isnumeric():
                    user = int(st[1])
                else:
                    user = st[1]
                try:
                    usr = await client.get_users(user)
                    if usr == None:
                        await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                        return
                except:
                    await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                    return
                if not usr.id in SAVES["Scammers"]:
                    if message.from_user.username == None:
                        if message.from_user.last_name == None:
                            admin = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                        else:
                            admin = f"[{message.from_user.first_name} {message.from_user.last_name}](tg://user?id={message.from_user.id})"
                    else:
                        admin = "@" + message.from_user.username
                    msg = await message.reply_text("__Sto netbannando attendere.....__")
                    if usr.username == None:
                        if usr.last_name == None:
                            mention = f"[{usr.first_name}](tg://user?id={usr.id})"
                        else:
                            mention = f"[{usr.first_name} {usr.last_name}](tg://user?id={usr.id})"
                    else:
                        mention = "@" + usr.username
                    c = 0
                    for group in SAVES["Groups"]:
                        try:
                            await client.kick_chat_member(group, usr.id)
                            # MESSAGGIO NETBAN
                            await client.send_message(group, f"⚠️UTENTE NETBANNATO⚠️              Informazioni utente          \n\n👤Utente:{mention}\n🆔 ID:`{usr.id}`\n\n🚫Netbannato da🚫\n👮🏻‍♂Staff:{admin}\n🆔:`{message.from_user.id}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Prove", url=st[2])]]))
                            c += 1
                        except:
                            await client.send_message(group, "**⚠️ Per funzionare al meglio il bot ha bisogno dei permessi admin ⚠️**")
                    await msg.edit(f"**✅ Utente netbannato correttamente in {c} gruppi ✅**")
                    # MESSAGGIO NETBAN CAMBIARE ANCHE QUI
                    await client.send_message(CHANNEL, f"⚠️UTENTE NETBANNATO⚠️                    Informazioni utente                             \n\n👤Utente:{mention}\n🆔 ID:`{usr.id}`\n\n🚫Netbannato da🚫\n👮🏻‍♂Staff:{admin}\n🆔:`{message.from_user.id}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Prove", url=st[2])]]))
                    SAVES["Scammers"].append(usr.id)
                    save()
                else:
                    await message.reply_text("**⚠️ Utente già netbannato ⚠️**")
            else:
                await message.reply_text("**⚠️ Sintassi Errata ⚠️\nes»`/netban id o @ del utente link proof`**")
    elif message.text.startswith("/netunban"):
        if message.from_user.id in SAVES["Staff"]:
            st = message.text.split(" ")
            if st.__len__() == 2:
                if st[1].isnumeric():
                    user = int(st[1])
                else:
                    user = st[1]
                try:
                    usr = await client.get_users(user)
                    if usr == None:
                        await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                        return
                except:
                    await message.reply_text("**⚠️ Utente Non Trovato ⚠️**")
                    return
                if usr.id in SAVES["Scammers"]:
                    if message.from_user.username == None:
                        if message.from_user.last_name == None:
                            admin = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                        else:
                            admin = f"[{message.from_user.first_name} {message.from_user.last_name}](tg://user?id={message.from_user.id})"
                    else:
                        admin = "@" + message.from_user.username
                    msg = await message.reply_text("__NetUnban in corso...__")
                    if usr.username == None:
                        if usr.last_name == None:
                            mention = f"[{usr.first_name}](tg://user?id={usr.id})"
                        else:
                            mention = f"[{usr.first_name} {usr.last_name}](tg://user?id={usr.id})"
                    else:
                        mention = "@" + usr.username
                    c = 0
                    for group in SAVES["Groups"]:
                        try:
                            await client.unban_chat_member(group, usr.id)
                            # MESSAGGIO SBAN
                            await client.send_message(group, f"✅UTENTE NETUNBANNATO✅\n\n👤Utente:{mention}\n🆔 ID: `{usr.id}`\n\n👀Sbannato da👀\n👮🏻‍♂Staff:{admin}\n🆔:`{message.from_user.id}`                       TUTTO LO STAFF SI SCUSA PER L'ERRORE")
                            c += 1
                        except:
                            await client.send_message(group, "**⚠️ Per funzionare al meglio il bot ha bisogno dei permessi admin ⚠️**")
                    await msg.edit(f"**✅ Utente sbannato correttamente in {c} gruppi ✅**")
                    # MESSAGGIO SBAN CAMBIARE ANCHE QUI
                    await client.send_message(CHANNEL, f"✅UTENTE NETUNBANNATO✅\n\n👤Utente:{mention}\n🆔 ID: `{usr.id}`\n\n👀Sbannato da👀\n👮🏻‍♂Staff:{admin}\n🆔:`{message.from_user.id}`                             TUTTO LO STAFF SI SCUSA PER L'ERRORE")
                    SAVES["Scammers"].remove(usr.id)
                    save()
                else:
                    await message.reply_text("**⚠️ Quest utente non è netbannato ⚠️**")
            else:
                await message.reply_text("**⚠️ Sintassi Errata ⚠️\nes»'/netunban id o @ del utente`**")
    elif message.text.startswith("/check"):
        st = message.text.split(" ", 1)
        if st.__len__() == 2:
            if st[1].isnumeric():
                ID = int(st[1])
            else:
                try:
                    usr = await client.get_users(st[1])
                    if usr == None:
                        await message.reply_text("**⚠️Utente non trovato ⚠️\nes»`/check id o @`**")
                        return
                    else:
                        ID = usr.id
                except:
                    await message.reply_text("**⚠️non trovato ⚠️\nes»`/check id o @`**")
                    return
            if ID in SAVES["Scammers"]:
           
                await message.reply_text("**❌Utente presente nel nostro database**")
            else:
             
                await message.reply_text("**✅Utente non presente nel database ma attento questo non significa che non sia uno scammer **")
    elif message.chat.type == "private":
        if message.text == "/start":
            if message.chat.username == None:
                if message.chat.last_name == None:
                    mention = f"[{message.chat.first_name}](tg://user?id={message.chat.id})"
                else:
                    mention = f"[{message.chat.first_name} {message.chat.last_name}](tg://user?id={message.chat.id})"
            else:
                mention = "@" + message.chat.username
            # MESSAGGIO BENVENUTO CON BOTTONI
            await message.reply_text(f"👋🏻Benvenuto {mention} grazie per aver avviato il bot\n\n__aggiungi il bot come amministartore e fai /add per rendere al sicuro il tuo gruppo__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Aggiungimi in un gruppo ➕", url="https://t.me/" + (await client.get_me()).username + "/?startgroup=startgroup")],[InlineKeyboardButton("👑 Staff👑", "staff"),InlineKeyboardButton("🚫Segnala", url="https://t.me/antiscamantosupportbot")],[InlineKeyboardButton("♻️Prove", url="https://t.me/+gf--4IyKBSU4Zjdk"),InlineKeyboardButton("🗂Archivio", url="https://t.me/AntoAntiscamArchivio")],[InlineKeyboardButton("🖇Gruppo supporto", url="https://t.me/grupposupportoantiscamanto")],[InlineKeyboardButton("🔎 Check Scammer🔎", "check")], [InlineKeyboardButton("🧑‍💻Developer🧑‍💻", url="https://t.me/appenderti")]]))
    elif message.text.startswith("/add"):
        if not message.chat.id in SAVES["Groups"]:
            if (await client.get_chat_member(message.chat.id, "me")).status == "administrator":
                await message.reply_text("**😁Gruppo aggiunto Correttamente da ora bannerò tutti gli scammer**")
                SAVES["Groups"].append(message.chat.id)
                save()
            else:
                await message.reply_text("**⚠️ Ho bisogno di tutti i permessi amministratore ⚠️**")
            
        
    

@bot.on_callback_query()
async def callbackQueryManaer(client, query):
    global SAVES, CHANNEL
    if query.data == "back":
        if query.message.chat.username == None:
            if query.message.chat.last_name == None:
                mention = f"[{query.message.chat.first_name}](tg://user?id={query.message.chat.id})"
            else:
                mention = f"[{query.message.chat.first_name} {query.message.chat.last_name}](tg://user?id={query.message.chat.id})"
        else:
            mention = "@" + query.message.chat.username
        # MESSAGGIO BENVENUTO CON BOTTONI CAMBIARE ANCHE QUI
        await query.message.edit(f"**👋🏻Benvenuto {mention} grazie per aver avviato il bot\n\n__aggiungi il bot come amministartore e fai /add per rendere al sicuro il tuo gruppo__", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➕ Aggiungimi in un gruppo ➕", url="https://t.me/" + (await client.get_me()).username + "/?startgroup=startgroup")],[InlineKeyboardButton("👑 Staff👑", "staff"),InlineKeyboardButton("🚫Segnala", url="https://t.me/antiscamantosupportbot")],[InlineKeyboardButton("♻️Prove", url="https://t.me/+gf--4IyKBSU4Zjdk"),InlineKeyboardButton("🗂Archivio", url="https://t.me/AntoAntiscamArchivio")],[InlineKeyboardButton("🖇Gruppo supporto", url="https://t.me/grupposupportoantiscamanto")],[InlineKeyboardButton("🔎 Check Scammer🔎", "check")], [InlineKeyboardButton("🧑‍💻Developer🧑‍💻", url="https://t.me/appenderti")]]))
    elif query.data == "staff":
        # MESSAGGIO LISTA STAFF
        msg = "**👑 LISTA STAFF 👑**\n"
        for admin in SAVES["Staff"]:
            try:
                usr = await client.get_users(admin)
                if usr == None:
                    canMention = False
                else:
                    canMention = True
            except:
                canMention = False
            if canMention:
                if usr.username == None:
                    if usr.last_name == None:
                        mention = f"[{usr.first_name}](tg://user?id={usr.id})"
                    else:
                        mention = f"[{usr.first_name} {usr.last_name}](tg://user?id={usr.id})"
                else:
                    mention = "@" + usr.username
            else:
                mention = "???"
            msg += f"\n{mention} | `{admin}`"
        await query.message.edit(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Indietro", "back")]]))
    elif query.data == "check":
        # MESSAGGIO CHECK SCAMMER
        await query.message.edit("**👀Per controllare se un utente è presente nel nostro database devi semplicemente digitare /check [@ o ID]!\n\nEsempio: /check 1777483871**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Indietro", "back")]]))
    

print("Bot Avviato Correttamente!")

bot.run() 