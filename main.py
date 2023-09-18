import os
import dotenv
import discord
import openai

dotenv.load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        print(f'Message from {message.author}: {message.content}')
        
        if message.author.bot:
            return
        
        elif self.user in message.mentions:

            try:
                openai.api_key = os.environ.get('GPT_KEY')

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                        "role": "user",
                        "content": f"{message.content}\nunder 100 words."
                        }
                    ],
                    temperature=1,
                    max_tokens=100,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )

                await channel.send(response.choices[0].message.content)
            
            except:
                await channel.send("Sorry, I can't answer your question 😔.")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.environ.get('DISCORD_TOKEN'))
