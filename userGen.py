# < (c) @xditya >
# This file is a part of RandomUserGenerator < https://github.com/xditya/RandomUserGenerator >
import logging
from telethon import TelegramClient, events, Button
from decouple import config
from requests import get

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

bottoken = None
# start the bot
print("Starting...")
apiid = 6
apihash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
try:
    bottoken = config("BOT_TOKEN")
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

if bottoken != None:
    try:
        BotzHub = TelegramClient("bot", apiid, apihash).start(bot_token=bottoken)
    except Exception as e:
        print(f"ERROR!\n{str(e)}")
        print("Bot is quiting...")
        exit()
else:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()

base_url = "https://randomuser.me/api/"
t_pic = "https://telegra.ph/file/e4383958aae2091dfd2ac.jpg"


@BotzHub.on(events.NewMessage(incoming=True, pattern="^/start"))
async def msgg(event):
    await send_start(event, "msg")


@BotzHub.on(events.callbackquery.CallbackQuery(data="gen"))
async def _gen_data(event):
    msg, pic = get_data()
    await event.edit(
        msg,
        file=pic,
        buttons=[
            [Button.inline("♻️ Another ♻️", data="gen")],
            [Button.inline("◀️ Back", data="bck")],
        ],
    )


@BotzHub.on(events.callbackquery.CallbackQuery(data="bck"))
async def bk(event):
    await send_start(event, "")


def get_data():
    d = get(base_url).json()
    data_ = d["results"][0]
    _g = data_["gender"]
    gender = "🤵" if _g == "male" else "👩‍🦰"
    name = data_["name"]
    loc = data_["location"]
    dob = data_["dob"]
    msg = """
{} **Name:** {}.{} {}

**Street:** {} {}
**City:** {}
**State:** {}
**Country:** {}
**Postal Code:** {}

**Email:** {}
**Phone:** {}

**Birthday:** {}
""".format(
        gender,
        name["title"],
        name["first"],
        name["last"],
        loc["street"]["number"],
        loc["street"]["name"],
        loc["city"],
        loc["state"],
        loc["country"],
        loc["postcode"],
        data_["email"],
        data_["phone"],
        dob["date"],
    )
    pic = data_["picture"]["large"]
    return msg, pic


async def send_start(event, mode):
    user_ = await BotzHub.get_entity(event.sender_id)
    if mode == "msg":
        await event.reply(
            f'Hi {user_.first_name}.\n\nI am a random user info generator bot!\n\nClick "Generate" to generate a random data.',
            file=t_pic,
            buttons=[
                [Button.inline("Generate", data="gen")],
                [
                    Button.url("Channel", url="https://t.me/BotzHub"),
                    Button.url(
                        "Source", url="https://github.com/xditya/RandomUserGenerator"
                    ),
                ],
            ],
        )
    else:
        await event.edit(
            f'Hi {user_.first_name}.\n\nI am a random user info generator bot!\n\nClick "Generate" to generate a random data.',
            file=t_pic,
            buttons=[
                [Button.inline("Generate", data="gen")],
                [
                    Button.url("Channel", url="https://t.me/BotzHub"),
                    Button.url(
                        "Source", url="https://github.com/xditya/RandomUserGenerator"
                    ),
                ],
            ],
        )


print("Bot has started.")
print("Do visit @BotzHub..")
BotzHub.run_until_disconnected()
