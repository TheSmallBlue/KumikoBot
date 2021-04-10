import discord
import os
import praw
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SECRET = os.getenv('REDDIT_SECRET')

subreddit = praw.Reddit(client_id='yvXh2hrDELw6eg', \
                     client_secret=SECRET, \
                     user_agent='KumikoBot').subreddit('rarekumikos')
hot_subreddit = subreddit.hot(limit=500)

totalimgs = 0
posts = []
authors = []
posturls = []
def refresh_posts():
	print('Refreshing posts!')
	posts.clear()
	authors.clear()
	posturls.clear()
	global totalimgs
	totalimgs=0
	i=0
	for submission in subreddit.hot(limit=500):
		#_ = os.system('clear')
		i = i + 1
		totalimgs = totalimgs + 1
		print('Getting submission number '+ str(i) +' / 500!')
		if ".jpg" not in submission.url and ".png" not in submission.url:
			print('Post is not a jpg or png --------------------------')
			print(str(submission.url))
			totalimgs = totalimgs - 1
			continue
		posts.append(submission.url)
		authors.append(submission.author)
		posturls.append(submission.permalink)
	print('Total amount of images: '+str(totalimgs))


def create_embed(post,author,posturl):
	embed = discord.Embed(
		color = discord.Colour.dark_orange()
		)
	embed.set_image(url=post)
	embed.description ='['+str(author)+'](https://www.reddit.com'+str(posturl)+')'
	return embed

refresh_posts()

client = discord.Client()

@client.event
async def on_ready():
	print('Connected servers: ')
	print([x.name for x in client.guilds])
	print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if "showmeakumiko" in message.content.lower().replace(' ',''):
		
		postnumber = random.randint(1,totalimgs)
		try:
			print('Someone over at', message.guild.name, 'asked for a Kumiko, and it was sent succesfully!')
			await message.channel.send(embed = create_embed(posts[postnumber],authors[postnumber],posturls[postnumber]))
		except discord.errors.Forbidden:
			print('Someone over at', message.guild.name, 'asked for a Kumiko, but I couldnt type in there so I sent it through DMs instead!')
			await message.author.send("I don't have enough permissions to talk on that channel! So I'll send your Kumiko through here instead!")
			await message.author.send(embed = create_embed(posts[postnumber],authors[postnumber],posturls[postnumber]))


	if "refresh the kumikos" in message.content.lower():
		refresh_posts()

client.run(TOKEN)