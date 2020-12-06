import os, json

def long_fn(one, two, three, four, five, six, seven, eight, nine, ten, eleven,
        twelve, thirteen, fourteen):
    print(one)
    print(two)
    print(three)
    print(four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, 
        fourteen)


def print_os():
    long_fn(*range(0, 14))
    print(os.name)

class Thing:
    def __init__(self, *args, **kwargs):
        self.stuff = args[0]

    def do_it(self):
        print(self.stuff)
