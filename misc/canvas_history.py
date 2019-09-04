from talon import ui, ctrl, cron
from talon.engine import engine
from talon.canvas import Canvas
from talon.voice import Context

ctx = Context('history')

hist_len = 20

class History:
    def __init__(self):
        self.enabled = False
        self.history = []
        engine.register('post:phrase', self.on_phrase_post)
        self.canvas = Canvas.from_screen(ui.main_screen())
        # self.canvas = Canvas(0, 0, 640, 480, draggable=True)
        # self.canvas.set_draggable(True)
        self.canvas.register('draw', self.draw)

    def toggle_enabled(self):
        self.enabled = not self.enabled

    def parse_phrase(self, phrase):
        return ' '.join(word.split('\\')[0] for word in phrase)

    def on_phrase_post(self, j):
        phrase = self.parse_phrase(j.get('phrase', []))
        cmd = j['cmd']
        if cmd == 'p.end' and phrase:
            self.history.append(phrase)
            self.history = self.history[-hist_len:]
            # prevent from rerendering
            self.canvas.freeze()

    def draw(self, canvas):
        text = self.history[:]
        if not text or not self.enabled:
            return
        paint = canvas.paint
        paint.filter_quality = paint.FilterQuality.LOW
        paint.textsize = 15
        paint.antialias = True

        # canvas.draw_rect(ui.Rect(x - 50, y - 50, 100, 100))
        x = canvas.x + 20
        y = canvas.y + 50
        # y = canvas.y + canvas.height - 50
        text_pad = 0
        rect_pad = 10

        # measure text
        width = 0
        text_top = y
        # text_top = 0
        text_bot = y
        # text_bot = 0
        line_spacing = 0
        for line in text:
            _, trect = paint.measure_text(line)
            width = max(width, trect.width)
            line_spacing = max(line_spacing, trect.height)
            text_top = min(text_top, y - trect.height)

        x = canvas.x + 1700 - 2*rect_pad - width # this the x coord. change 1700 to adjust.
        # x = canvas.x + canvas.width - 2*rect_pad - width

        line_spacing += text_pad
        text_bot = y + (len(text) - 1) * line_spacing
        height = text_bot - text_top

        rect = ui.Rect(x - rect_pad, text_top - 2, width + rect_pad * 2, height + rect_pad + 2)
        
        #  last two digits are hexadecimal for transparency. 
        paint.color = 'ffffff44'
        paint.style = paint.Style.FILL
        canvas.draw_round_rect(rect, 10, 10)

        paint.color = '000000'
        paint.style = paint.Style.FILL
        for line in text:
            canvas.draw_text(line, x, y)
            y += line_spacing
            # y -= line_spacing consider this.

history = History()

keymap = {
    "[toggle] history [(on | off)]": lambda m: history.toggle_enabled()
}
ctx.keymap(keymap)
