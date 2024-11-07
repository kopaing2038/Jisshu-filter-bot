
import os
import re
import json
import aiohttp
import requests
from pyrogram import Client, filters
from info import URL, PORT, DATABASE_URI, DATABASE_NAME
import pymongo
from pymongo import MongoClient


# Set up MongoDB client
mont = MongoClient(DATABASE_URI)  # Update with your MongoDB connection string
db = mont[DATABASE_NAME]  # Replace "your_database_name" with your actual database name
collection = db["footballdb_link"] 

import os
from bson.objectid import ObjectId

async def add_link(message_s):
    result = collection.insert_one({"_id": str(ObjectId()), "link": message_s})
    return result.inserted_id


@Client.on_message(filters.command(["tgpaste", "gen"]))
async def gen(client, message):
    pablo = await message.reply_text("`Please wait...`")
    tex_t = message.text
    if ' ' in message.text:
        message_s = message.text.split(" ", 1)[1]
    elif message.reply_to_message:
        message_s = message.reply_to_message.text
    else:
        await message.reply("Sorry, no input. Please reply to a text or use /gen with text.")
        return

    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Only text and documents are supported.`")
            return
        if message.reply_to_message.text:
            message_s = message.reply_to_message.text
        else:
            file = await message.reply_to_message.download()
            with open(file, "r") as f:
                message_s = f.read()
            os.remove(file)

    _id = await add_link(message_s)
    html_link = f'<a href="{URL}:{PORT}/football/{_id}">Click here</a>'
    pasted = f"**Successfully Gen **\n\n**Link:** {html_link}\n\n"
    await pablo.edit(pasted, disable_web_page_preview=True)
