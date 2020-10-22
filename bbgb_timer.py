import time
import threading


class BBGBTimer:
    def __init__(self, guild, timer_length, callback, message_channel):
        self.message_channel = message_channel
        self.started_at = time.time()
        self.timer_length = timer_length
        self.timer = None
        self.guild = guild
        self.callback = callback

    async def start(self):
        self.timer = threading.Timer(self.timer_length, self.callback, ("timer done", self.guild, self.message_channel))
        await self.timer.start()