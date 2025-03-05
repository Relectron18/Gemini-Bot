import settings
from discord.ext import commands
import google.generativeai as genai


genai.configure(api_key=settings.GEMINI_SDK)
DISCORD_MAX_MESSAGE_LENGTH=2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE='There was an issue with your question please try again.. '



class GeminiAgent(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    @commands.Cog.listener()
    async def on_message(self,msg):
        try:
            if msg.content == "ping gemini-agent":
                await msg.channel.send("Agent is connected..")
        except Exception as e:
            await msg.channel.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def gemini(self,ctx,question):
        try:
            response = self.gemini_generate_content(question)
            await self.send_message_in_chunks(ctx, response.text)
        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    def gemini_generate_content(self,content):
        try:
            response = self.model.generate_content(content,stream=True)
            response.resolve()
            return response
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)
        
    async def send_message_in_chunks(self,ctx,response):
        message = ""
        for chunk in response:
            message += chunk
            if len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
        if len(message) > 0:
            while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
            await ctx.send(message)