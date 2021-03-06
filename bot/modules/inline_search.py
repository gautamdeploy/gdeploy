from bot import app, LOGGER
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from pyrogram.errors import QueryIdInvalid

thumb = "https://telegra.ph/file/08c580abaebfa493d3a06.jpg"

@app.on_inline_query()
async def inline_search(_, event: InlineQuery):
    answers = list()
    LOGGER.info(event.query)
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Your Desired File Here",
                input_message_content=InputTextMessageContent(
                    "You can search your files anywhere anytime using inline method\n\nUse Search Button Below"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Search",
                                switch_inline_query_current_chat=""
                            )
                        ]
                    ]
                )
            )
        )
    else:
        key = event.query
        gdrive = GoogleDriveHelper()
        file_title, desc, drive_url, index_url, view_link = gdrive.drive_list_inline(
            key, isRecursive=False, itemType="both")
        if file_title:
            for title in file_title:
                if file_title.index(title) < 49:
                    answers.append(
                        InlineQueryResultArticle(
                            title=title,
                            description=desc[file_title.index(title)],
                            thumb_url=thumb,
                            input_message_content=InputTextMessageContent(
                                message_text=f"Title : {title}\n{desc[file_title.index(title)]}",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton(
                                    "View Link", url=view_link[file_title.index(title)])],
                                [InlineKeyboardButton(
                                    "Drive Link", url=drive_url[file_title.index(title)])],
                                [InlineKeyboardButton(
                                    "Index Link", url=index_url[file_title.index(title)])],
                                [InlineKeyboardButton(
                                    "Search Again", switch_inline_query_current_chat="")],
                            ])
                        )
                    )
        else:
            answers.append(
                InlineQueryResultArticle(
                    title=f"No Result Found for {key}",
                    description="Try with another search key",
                    input_message_content=InputTextMessageContent(
                        message_text="No Result Found For Your Search Key\nTry with another search"
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "Search Again", switch_inline_query_current_chat="")]
                    ])
                )
            )
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
    except QueryIdInvalid:
        LOGGER.info(f"QueryIdInvalid: {event.query}")


@app.on_message(filters.command("updated"))
async def quit_group(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text="yes updated",
        reply_to_message_id=update.message_id
    )
    # await bot.leave_chat(
    #     chat_id=update.chat.id
    # )
