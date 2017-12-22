class DetailFilter(object):
    """description of class"""
    def __init__(self, expression, usage, element):
        self.expression = expression
        self.usage = usage
        self.element = element

    def json(self):
        {
            "expression":self.expression,
            "usage": self.usage
        }