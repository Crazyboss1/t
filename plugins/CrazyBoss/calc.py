"""
Fetch App Details from Playstore.
.app <app_name> to fetch app details.
  © [cHAuHaN](http://t.me/amnd33p)
"""

import io
import sys
import traceback
from plugins.helper_functions.events import register
from telethon import types
from telethon.tl import functions

plugin_category = "utils"


@register(pattern=r"^/calc ?(.*)")
async def calculator(event):
    "To solve basic mathematics equations."
    cmd = event.text.split(" ", maxsplit=1)[1]
    event = await event.reply("Calculating ...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    san = f"print({cmd})"
    try:
        await aexec(san, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sorry I can't find result for the given equation"
    final_output = "**EQUATION**: `{}` \n\n **SOLUTION**: \n`{}` \n".format(
        cmd, evaluation
    )
    await event.edit(final_output)


async def aexec(code, event):
    exec("async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))

    return await locals()["__aexec"](event)
