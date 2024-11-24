import os
from pathlib import Path

import hikari
import lightbulb
import requests
from lxml import html
from dotenv import load_dotenv


load_dotenv()

bot = hikari.GatewayBot(os.getenv("DISCORD_TOKEN"))
client = lightbulb.client_from_app(bot)

bot.subscribe(hikari.StartingEvent, client.start)


@client.register
class Discipline(
    lightbulb.SlashCommand,
    name="discipline",
    description="Discipline description",
):
    discipline = lightbulb.string("discipline", "discipline")
    level = lightbulb.integer("level", "level")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        text_return = ""

        url = f"https://guidetothemasquerade.weebly.com/{self.discipline}.html"
        response = requests.get(url)

        if response.status_code == 200:
            tree = html.fromstring(response.content)

            xpath_query = (
                './/*[contains(concat(" ", normalize-space(@class), " "), " paragraph ")]//ul//li'
                f"[(count(preceding-sibling::*) + 1) = {self.level}]"
            )
            try:
                discipline_text = tree.xpath(xpath_query)[0].text_content()
                text_return = f"**{self.discipline.capitalize()}** {discipline_text}"
            except IndexError:
                text_return = "No matching element found at the specified level."
        else:
            text_return = (
                f"Failed to fetch the page. Status code: {response.status_code}"
            )

        await ctx.respond(text_return)


bot.run()
