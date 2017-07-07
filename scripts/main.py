#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "James Shiffer"

import logging as log
import asyncio
import discord
import sys
from Config import TOKEN, PREFIX

import Commands

# Enable logging
log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=log.DEBUG,
                filename='../logs/logging.log')

logger = log.getLogger(__name__)

ch = log.StreamHandler(sys.stdout)
ch.setFormatter(log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
ch.setLevel(log.DEBUG)
logger.addHandler(ch)

games = {}

# The bot client.
bot = discord.Client()

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


@bot.event
async def on_ready():
    """Called once the bot has logged in."""
    log.info('Logged in as name "{}" with ID "{}".'.format(bot.user.name, bot.user.id))

    # Begin updating status every 5 seconds
    await update_status()


@bot.event
async def on_message(msg):
    """Handles messages sent to the bot."""

    msg_content = msg.content.strip()

    # Only care about messages that start with prefix
    if not msg_content.startswith(PREFIX):
        return

    # Bot won't take commands from itself
    if msg.author.id == bot.user.id:
        return

    # Take off prefix, split command and arguments
    cmd, *args = msg_content.split()
    cmd = cmd[len(PREFIX):].lower().strip()

    try:
        cmd_func = getattr(Commands, 'command_' + cmd)
    except AttributeError:
        log.debug('Invalid command "sh?' + cmd + '"')
        return

    await bot.send_typing(msg.channel)
    log.debug('"command_' + cmd + '" called')
    await cmd_func(bot, msg, args)


async def update_status():
    while True:
        await bot.change_presence(
            game=discord.Game(
                name="{}help | {} servers".format(PREFIX, len(bot.servers))
            )
        )
        await asyncio.sleep(5)


def main():
    """Starts the bot."""
    log.info("Script started.")

    # Log in
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
