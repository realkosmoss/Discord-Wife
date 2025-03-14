import discord
from custom.messages import Messages
from custom.lore_handling import LoreHandling

class Commands:
    def __init__(self, messages_instance: Messages):
        self.messages_instance = messages_instance
        self.messages = messages_instance.get()
    async def ProcessComands(self, message: discord.Message):
        message_content = message.content
        if "!commands" == message_content.lower():
            await message.reply("**!commands** - **Shows list of commands.**\n**!purge** - **Removes all messages and clears context.**\n**!create** - **Makes an private lore chat.** Secret Commands for !create channels:\n**!add @discord for example**\n**!remove @discord**\n**!delete <int>**\n-# Made with love. This message will be deleted after 10 seconds.", delete_after=10)
        if "!purge" == message_content.lower():
            # stupid shit
            public_server = True
            if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:  # public server use shit
                public_server = False
                lorehandler = LoreHandling(message.author.id, message.channel.id)
                _abc = False
                for i in lorehandler.channels:
                    if i == message.channel.id:
                        messages_instance_temp = lorehandler
                        _abc = True
                        break
                if not _abc:
                    return
            else:
                messages_instance_temp = self.messages_instance
            if public_server:
                if message.author.id == 456404988290269184: # Me.
                    messages_instance_temp.messages = []
                    messages_instance_temp.save()
                    await message.channel.purge()
            else:
                messages_instance_temp.messages = []
                messages_instance_temp.save()
                await message.channel.purge()
            return self.messages
        if "!create" in message_content.lower():
            channel_name = f"{message.author.display_name if message.author.display_name else message.author.global_name}s Private Layer"
            new_channel = await message.guild.create_text_channel(channel_name, nsfw=True)
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                message.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            await new_channel.edit(overwrites=overwrites)
            await new_channel.send(f"Hello {message.author.mention}, welcome to your private lore channel!\n**Custom commands**\n**!add @discord for example**\n**!remove @discord**\n**!delete <int>**\n**!purge** Removes all messages.\n**!reset** Removes any messages and deletes channel.")
            lorehandler = LoreHandling(message.author.id, message.channel.id)
            if new_channel.id not in lorehandler.channels:
                lorehandler.channels.append(new_channel.id)
                lorehandler.save_channels()
            await message.delete()
        if "!add" in message_content.lower(): # Special create command.
            if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:
                lorehandler = LoreHandling(message.author.id, message.channel.id)
                _abc = False
                for i in lorehandler.channels:
                    if i == message.channel.id:
                        #messages_instance = lorehandler
                        _abc = True
                        break
                if not _abc:
                    return
                user_id_string = message_content.replace("!add", "")
                user_id = int(user_id_string.strip().strip('<>@'))
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    message.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    await message.guild.fetch_member(user_id): discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                await message.channel.edit(overwrites=overwrites)
                lorehandler = LoreHandling(user_id, message.channel.id)
                lorehandler.channels.append(message.channel.id)
                lorehandler.save_channels()
        if "!remove" in message_content.lower(): # special create command.
            if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:
                user_id_string = message_content.replace("!remove", "")
                user_id = int(user_id_string.strip().strip('<>@'))
                lorehandler = LoreHandling(user_id, message.channel.id)
                lorehandler.channels.remove(message.channel.id)
                lorehandler.save_channels()
        if "!delete" in message_content.lower():  
            if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:
                try:  
                    messagestodelete_int = int(message.content.lower().replace("!delete", "").strip())  
                except:  
                    return  
                
                lorehandler = LoreHandling(message.author.id, message.channel.id)  
                deleted_count = 0  
                
                async for msg in message.channel.history(limit=None):  
                    if deleted_count >= messagestodelete_int + 1:  
                        break  

                    await msg.delete()
                    if not message_content in msg.content:
                        deleted_count += 1

                if deleted_count > 1:  
                    lorehandler.messages = lorehandler.messages[:-(deleted_count)]  
                    lorehandler.save()  
        if "!reset" in message_content.lower():
            if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:
                lorehandler = LoreHandling(message.author.id, message.channel.id)
                lorehandler.messages = []
                lorehandler.save()
                await message.channel.purge()
                await message.channel.delete()
                lorehandler.delete()
        # I want to add an make lore channel for specific user. Private lore better than groupchat and clears all messages leaving no trace.