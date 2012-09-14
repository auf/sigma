from xml.sax.saxutils import XMLGenerator


class WCSGenerator(XMLGenerator):

    def __init__(self, file, name):
        XMLGenerator.__init__(self, file, 'utf-8')
        self.name = name

    def __enter__(self):
        self.startDocument()
        self.startElement(u'formdef', {})
        self.add_element(u'name', self.name)
        self.startElement(u'fields', {})
        return self

    def __exit__(self, type, value, traceback):
        self.endElement(u'fields')
        self.endElement(u'formdef')
        self.endDocument()

    def add_element(self, tag, content):
        self.startElement(tag, {})
        self.characters(content)
        self.endElement(tag)

    def start_field(self, type, label, required=False, in_listing=False,
                    **kwargs):
        self.startElement(u'field', {})
        self.add_element(u'label', label)
        self.add_element(u'type', type)
        if not required:
            self.add_element(u'required', u'False')
        if not in_listing:
            self.add_element(u'in_listing', u'False')
        for elem, content in kwargs.iteritems():
            self.add_element(elem, unicode(content))

    def end_field(self):
        self.endElement(u'field')

    def add_page(self, label):
        self.start_field(u'page', label)
        self.end_field()

    def add_title(self, label):
        self.start_field(u'title', label)
        self.end_field()

    def add_string_field(self, label, **kwargs):
        self.start_field(u'string', label, **kwargs)
        self.end_field()

    def add_item_field(self, label, items, **kwargs):
        self.start_field(u'item', label, **kwargs)
        self.startElement(u'items', {})
        if not kwargs.get('show_as_radio', False):
            self.add_element(u'item', u'---')
        for item in items:
            self.add_element(u'item', item)
        self.endElement(u'items')
        self.end_field()

    def add_date_field(self, label, **kwargs):
        self.start_field(u'date', label, **kwargs)
        self.end_field()

    def add_email_field(self, label, **kwargs):
        self.start_field(u'email', label, **kwargs)
        self.end_field()

    def add_text_field(self, label, **kwargs):
        self.start_field(u'text', label, **kwargs)
        self.end_field()
