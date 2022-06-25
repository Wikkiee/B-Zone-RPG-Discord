async def dm_messages(client,message):
        await client.process_commands(message)
        if(message.guild == None):
            if(message.author == client.user):
                return
            else:
                #print(message.content)
                pass