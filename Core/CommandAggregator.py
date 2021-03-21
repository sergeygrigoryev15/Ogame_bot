import os


class CommandAggregator(object):

    @property
    def supported_methods(self):
        command_files = []
        path = os.path.abspath(__file__) + '/../../Commands/'
        tree = os.walk(path)
        for address, dirs, files in tree:
            files = filter(lambda el: el.endswith('.py') and '__init__' not in el, files)
            command_files.extend(files)
        command_files = set(command_files)
        methods = []
        for f in command_files:
            methods.extend(dir(f))
        return set(methods)


if __name__ == '__main__':
    a = CommandAggregator()
    print(a.supported_methods)
