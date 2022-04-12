async def dm_messages(client,message):
        await client.process_commands(message)
        if(message.guild == None):
            if(message.author == client.user):
                print(message)
                return
            else:
                pass