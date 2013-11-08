from .. import Client

CLIENT = None


def init(client=None, base_url="unix://var/run/docker.sock", version="1.4"):
    global CLIENT
    if client:
        CLIENT = client
    else:
        CLIENT = Client(base_url, version)


class Identifiable(object):
    def __init__(self, id):
        if isinstance(id, dict):
            id = id.get('Id')
        self.id = id


class Image(Identifiable):
    pass


class Container(Identifiable):
    @classmethod
    def new(cls, image, **kwargs):
        res = CLIENT.create_container(image, **kwargs)
        return cls(res)

    def start(self, binds=None, lxc_conf=None):
        CLIENT.start(self.id, binds, lxc_conf)

    def stop(self, timeout=10):
        CLIENT.stop(self.id)

    def restart(self, timeout=10):
        CLIENT.restart(self.id)

    def commit(self, repository=None, tag=None, message=None, author=None,
               conf=None):
        return Image(CLIENT.commit(self.id, repository, tag, message, author,
                                   conf))

    def diff(self):
        return CLIENT.diff(self.id)

    def export(self):
        return CLIENT.export(self.id)

    def kill(self):
        return CLIENT.kill(self.id)

    def logs(self):
        return CLIENT.logs(self.id)

    def port(self, private_port):
        return CLIENT.port(self.id, private_port)

    def top(self):
        return CLIENT.top(self.id)

    def remove(self, v=False):
        return CLIENT.remove_container(self.id, v)

    def wait(self):
        return CLIENT.wait(self.id)
