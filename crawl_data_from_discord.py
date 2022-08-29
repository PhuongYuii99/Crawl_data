import csv
import discord
import datetime

csv_rows = []

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    with open('discord_tmp/discord_message.csv', mode='a') as f:
        writer = csv.writer(f)
        csv_rows.append(datetime.datetime.now())
        csv_rows.append(message.guild.id)
        csv_rows.append(message.guild.name)
        csv_rows.append(message.id)
        csv_rows.append(message.content)
        csv_rows.append(message.channel.id)
        csv_rows.append(message.channel.name)
        csv_rows.append(message.author.id)
        csv_rows.append(message.author.name)
        writer.writerow(csv_rows)
        csv_rows.clear()
    
@client.event
async def on_member_join(member):
    with open('discord_tmp/discord_member.csv', mode='a') as a:
        csv_members = []
        for g in client.guilds:
            if g == member.guild:
                writer = csv.writer(a)
                csv_members.append(datetime.datetime.now())
                csv_members.append(member.guild.id)
                csv_members.append(member.guild.name)
                csv_members.append(member.id)
                csv_members.append(member.name)
                csv_members.append("joined")
                csv_members.append(len(g.members))
                writer.writerow(csv_members)
                csv_members.clear()
                break

@client.event      
async def on_member_remove(member):
    with open('discord_tmp/discord_member.csv', mode='a') as a:
        csv_members = []
        for g in client.guilds:
            if g == member.guild:
                writer = csv.writer(a)
                csv_members.append(datetime.datetime.now())
                csv_members.append(member.guild.id)
                csv_members.append(member.guild.name)
                csv_members.append(member.id)
                csv_members.append(member.name)
                csv_members.append("left")
                csv_members.append(len(g.members))
                writer.writerow(csv_members)
                csv_members.clear()
                break

    
client.run('your_bot_token')
