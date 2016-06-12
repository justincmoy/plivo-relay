class Action():
    def __init__(self, from_number, prev_output=[]):
        self.from_number = from_number
        self.output = prev_output

    def process(self, *args, **kwargs):
        pass

    @property
    def output_comma(self):
        return ', '.join(self.output)

    @property
    def output_html(self):
        return '<br/>'.join(self.output)

    @property
    def output_text(self):
        return '\r\n'.join(self.output)
