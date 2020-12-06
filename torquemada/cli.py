# cli.py
# 
# Command Line Interface wrapper

import argparse
import inspect

from .__init__ import __version__
from .registry import registry
from torquemada import actions

# ===========================================================================
# Argument Management
# ===========================================================================

class ExtendedHelp(argparse.Action):
    ### This is an argparse Action that shows extended help info (not to be
    # confused with torquemada actions
    def __init__(self, **kwargs):
        kwargs['nargs'] = 0
        super(ExtendedHelp, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        description = ('\n'
            'Torquemada Actions\n'
            '==================\n\n'
            'torq runs a series of actions on the file or directory passed '
            'in on the command line. Each action can be turned off with a '
            '"--no-/action/" argument, where "/action/" is replaced with the '
            'name of the action.\n\n'
            'The following actions are run in this order:\n'
        )

        print(description)

        for action in registry:
            print(f'{action.__name__}:')
            lines = inspect.getdoc(action).split('\n')
            for line in lines:
                print('   ', line)

            print()

        parser.exit()


def get_parser():
    description = """\
        torq is a combination style checker and linter for Python scripts. It
        is used to verify compliance for code displayed in example files or a
        screencast, with a very particular, very opionated style. The command
        is built on top of Black and Flake8. Any code tortured by torq is run
        through Black, then corrected to remove double blank lines, run
        through Flake8, then run through a series of custom verifications.

        Run "torq --actions" for a detailed list of what each action does and
        in what order.
    """
    parser = argparse.ArgumentParser(description=description)

    # global args
    parser.add_argument('--quiet', action='store_true',
        help='Silences messages that are not errors')
    parser.add_argument('--version', action='version',
        version='%(prog)s {version}'.format(version=__version__ ))
    parser.add_argument('--actions', action=ExtendedHelp,
        help='Displays information on the actions torq runs')

    # args from actions
    for action in registry:
        action.add_arguments(parser)

    parser.add_argument('filename', help='Name of file or directory to process')

    return parser

# ===========================================================================
# Main
# ===========================================================================

def torture(parser_args):
    for action in registry:
        action.action(parser_args)
        print()
