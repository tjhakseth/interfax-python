from inflection import underscore


class Response(object):
    def __init__(self, client, data):
        self.__dict__.update([(underscore(k), v) for k, v in data.items()])
        self.client = client

    def __repr__(self):
        return "{0}(id={1})".format(self.__class__.__name__, repr(self.id))

class InboundFax(Response):
    @property
    def id(self):
        return self.message_id

    def image(self):
        return self.client.inbound.image(self.id)

    def reload(self):
        return self.client.inbound.find(self.id)

    def mark(self, read=True):
        return self.client.inbound.mark(self.id, read)

    def resend(self, email=None):
        return self.client.inbound.resend(self.id, email)

    def emails(self):
        return self.client.inbound.emails(self.id)


class OutboundFax(Response):
    def image(self):
        return self.client.outbound.image(self.id)

    def reload(self):
        return self.client.outbound.find(self.id)

    def cancel(self):
        return self.client.outbound.cancel(self.id)


class ForwardingEmail(Response):
    def __repr__(self):
        return "{0}(email_address={1})".format(self.__class__.__name__, 
                                       repr(self.email_address))


class Document(Response):
    @property
    def id(self):
        return self.uri.split('/')[-1]

    def upload(self, range_start, range_end, chunk):
        return self.client.documents.upload(self.id, range_start, range_end,
                                            chunk)

    def cancel(self):
        return self.client.documents.cancel(self.id)

    def reload(self):
        return self.client.documents.find(self.id)

    def __repr__(self):
        return "{0}(uri={1})".format(self.__class__.__name__, 
                                       repr(self.uri))


class Image(Response):
    def save(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.data)

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)
