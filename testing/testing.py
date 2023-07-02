from linkedin_slack_bot.slack_bot import Linkedin_Bot

username = "?"
password = "?"
slack_token = "?"
channel_name = "#?"
interval = 60


bot = Linkedin_Bot(username , password , slack_token , channel_name , interval)
bot.run()
