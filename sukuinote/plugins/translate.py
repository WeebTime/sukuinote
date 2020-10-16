import html
import googletrans
from pyrogram import Client, filters
from .. import config, help_dict, log_errors, public_log_errors

PROBLEM_CODES = set(i for i in googletrans.LANGUAGES if '-' in i)
translator = googletrans.Translator()

@Client.on_message(~filters.sticker & ~filters.via_bot & ~filters.edited & filters.outgoing & filters.command(['tr', 'translate'], prefixes=config['config']['prefixes']))
@log_errors
@public_log_errors
async def translate(client, message):
    reply = message.reply_to_message
    if getattr(reply, 'empty', True):
        await message.reply_text('Reply required')
        return
    text = reply.text or reply.caption
    if not text:
        await message.reply_text('Text required')
        return
    src_lang = 'auto'
    dest_lang = 'en'
    lang = ' '.join(message.command[1:]).lower()
    for i in PROBLEM_CODES:
        if lang.startswith(i):
            src_lang = i
            lang = lang[len(i):]
            if lang:
                dest_lang = lang[1:] or 'en'
            break
    else:
        lang = lang.split('-', 1)
        if len(lang) == 1:
            dest_lang = lang.pop(0) or dest_lang
        else:
            src_lang, dest_lang = lang
    def _translate():
        return translator.translate(text, src=src_lang, dest=dest_lang)
    await message.reply_text((await client.loop.run_in_executor(None, _translate)).text, parse_mode=None)

help_dict['translate'] = ('Translate',
'''{prefix}translate <i>(as reply to text)</i> <i>[src]-[dest]</i> - Translates text and stuff
Aliases: {prefix}tr''')