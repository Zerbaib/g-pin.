import disnake
from disnake.ext import commands
import sqlite3

class unSuscribeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'🔩 /unregister has been loaded') 

    @commands.slash_command(name='unsuscribe', description="Delete your account of the manager.")
    async def del_account(self, inter):
        role_id = 1130975208061288450
        role = disnake.utils.get(inter.guild.roles, id=role_id)
        embed = disnake.Embed(
            title="Deleting your account",
        )
        conn = sqlite3.connect('bdd.db')
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE client_id = " + str(inter.author.id))
            result = cur.fetchall()
            if result:
                if role in inter.author.roles:
                    try:
                        cur.execute("DELETE FROM users WHERE client_id = " + str(inter.author.id))
                        conn.commit()
                        await inter.author.remove_roles(role)
                        embed.description = "You have been unsubscribed from the program, GLM6 is disappointed to see you leave and wishes you good luck!"
                        embed.colour = disnake.Colour.green()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "An error occurred while communicating with the database, please contact an administrator as soon as possible: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    try:
                        cur.execute("DELETE FROM users WHERE client_id = " + str(inter.author.id))
                        conn.commit()
                        embed.description = "You're on the database but you don't have the role, no worries, you're no longer part of the team..."
                        embed.colour = disnake.Colour.red()
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed.description = "An error occurred while communicating with the database, please contact an administrator as soon as possible: ```" + str(e) + "```"
                        embed.colour = disnake.Colour.red()
                        inter.response.send_message(embed=embed, ephemeral=True)
            else:
                if role in inter.author.roles:
                    await inter.author.remove_roles(role)
                    embed.description = "You are not on the database but you have a role, no worries, you are no longer part of the team..."
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    embed.description = "You cannot unsubscribe if you are not part of the program."
                    embed.colour = disnake.Colour.red()
                    await inter.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed.description = "An error occurred while verifying your account, please contact an administrator as soon as possible: ```" + str(e) + "```"
            embed.colour = disnake.Colour.red()
            await inter.response.send_message(embed=embed, ephemeral=True)
        conn.close()

def setup(bot):
    bot.add_cog(unSuscribeCommand(bot))