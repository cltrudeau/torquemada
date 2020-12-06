# actions.py
#
# Contains the actions that torq takes on the target files

import os, re, sys
from pathlib import Path

from .registry import register

# ===========================================================================

class Base:
    @classmethod
    def add_arguments(cls, parser):
        name = cls.__name__.lower()
        parser.add_argument(f'--no-{name}', action='store_true', 
            help=f'Stops the {name} action from running')

    @classmethod
    def action(cls, parsed_args):
        # check if the the --no-action flag is set for this action
        if getattr(parsed_args, f'no_{cls.__name__.lower()}'):
            if not parsed_args.quiet:
                print('🙅 Skipping', cls.__name__)
                return

        if not parsed_args.quiet:
            print('🏃', cls.__name__)

        cls._do_action(parsed_args)


def path_visitor(filename, parser_args, fn, ext='.py'):
    path = Path(filename)
    if path.is_file() and ext and path.suffix == ext:
        fn(path, parser_args)
        return

    for item in path.iterdir():
        if item.is_file() and ext and item.suffix == ext:
            fn(item, parser_args)
        elif item.is_dir():
            path_visitor(item, parser_args, fn, ext)

# ===========================================================================
# Registered Actions
# ===========================================================================

@register
class Black(Base):
    """Runs the Black Python code formatter with a line length of 80"""

    @classmethod
    def _do_action(cls, parsed_args):
        import black
        sys.argv = ['black', parsed_args.filename, '-l', 80]
        try:
            black.main()
        except SystemExit:
            # black calls quit(), ignore it
            pass
        

@register
class SingleSpace(Base):
    """Removes double blank lines on files ending in .py, undoing part of the
    Black formatting"""

    @classmethod
    def _do_action(cls, parsed_args):
        def remove_double_spacing(path, parsed_args):
            with open(path, 'r') as f:
                current = list(f.readlines())

            # borrowed from Jim's markplates
            replaced = []
            prev_line = ""  # empty line here will remove leading blank space
            for line in current:
                if len(line.strip()) or len(prev_line.strip()):
                    replaced.append(line)
                prev_line = line

            if current != replaced:
                print('Single spaced', path)
                with open(path, 'w') as f:
                    f.write(''.join(replaced))

        path_visitor(parsed_args.filename, parsed_args, remove_double_spacing)


@register
class HeaderCheck(Base):
    """Verifies that .py files start with a comment including the file name"""

    @classmethod
    def _do_action(cls, parsed_args):
        def check(path, parsed_args):
            with open(path) as f:
                first = f.readline()
                parts = first.split()

                # must start with a comment and end with the name of the file,
                # file name may or may not include some pathing information
                filename = str(path)
                if first[0] != '#' or not filename.endswith(parts[-1]):
                    print('File header missing for', path)

        path_visitor(parsed_args.filename, parsed_args, check)


@register
class REPLTest(Base):
    """Runs doctest on files ending in .repl"""

    @classmethod
    def _do_action(cls, parsed_args):
        def check_repl(path, parsed_args):
            import doctest
            doctest.testfile(str(path.resolve()), module_relative=False)

        path_visitor(parsed_args.filename, parsed_args, check_repl, '.repl')


@register
class Flake(Base):
    """Runs the Flake8 Python linter"""

    @classmethod
    def _do_action(cls, parsed_args):
        from flake8.main.cli import main
        try:
            sys.argv = ['black', parsed_args.filename]
            main()
        except SystemExit:
            # flake8 calls quit(), ignore it
            pass
