class Seminar:

    summary = None
    description = None
    start = None
    end = None
    link = None

    def __init__(self):
        pass

    def parameters(self):
        return self.summary, self.description, self.start, self.end, self.link
