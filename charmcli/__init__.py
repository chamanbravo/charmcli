import argparse
import inspect
import sys
from dataclasses import dataclass
from types import UnionType
from typing import Annotated, Any, Callable, Optional, Union, get_args, get_origin

from charmcli import excepthook, text_styler


@dataclass
class CommandInfo:
    name: str
    command: Callable


class CharmHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, indent_increment=2, max_help_position=40, width=None):
        self.ts = text_styler.TextStyler()
        super().__init__(prog, indent_increment, max_help_position, width)

    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = self.ts.yellow("\nUsage: ")

        has_subparsers = any(
            isinstance(action, argparse._SubParsersAction) for action in actions
        )
        if has_subparsers:
            usage = "main.py [OPTIONS] COMMAND [ARGS]..."
            return super().add_usage(usage, actions, groups, prefix)

        return super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        if heading:
            heading = self.ts.yellow(heading.capitalize())
        super().start_section(heading)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar = self._get_default_metavar_for_positional(action)
            args_string = self._format_args(action, metavar)
            return self.ts.cyan(args_string)
        else:
            parts = []
            opts = ", ".join([f"{self.ts.green(opt)}" for opt in action.option_strings])
            parts.append(opts)
            if action.nargs != 0:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                parts.append(f"{self.ts.cyan(args_string)}")
            return " ".join(parts)

    def _get_help_string(self, action):
        """Get the help string for an action, including default values"""
        help_text = action.help or ""
        if "%(default)" not in help_text and action.default not in (
            argparse.SUPPRESS,
            None,
            False,
            [],
        ):
            default_text = self.ts.dim(f"(default: {self.ts.yellow('%(default)s')})")
            if action.nargs != 0:
                if help_text:
                    help_text += f" {default_text}"
                else:
                    help_text += f"{default_text}"

        return help_text

    def _format_action(self, action):
        """Format a single action with improved styling"""
        # Get the commands/subparsers
        if isinstance(action, argparse._SubParsersAction):
            try:
                subparser_keys = action.choices.keys()
                postional_args = []
                for key in subparser_keys:
                    postional_args.append(
                        f"  {self.ts.cyan(key):<{self._max_help_position - 10}} {action.choices[key].description}\n"
                    )
                return "".join(postional_args)
            except Exception:
                ...

        action_invocation = self._format_action_invocation(action)
        help_text = self._expand_help(action)

        if not action.option_strings:
            if help_text:
                return f"  {action_invocation:<{self._max_help_position - 10}} {help_text}\n"
            else:
                return f"  {action_invocation}\n"
        else:
            if help_text:
                if len(action_invocation) <= self._max_help_position:
                    return f"  {action_invocation:<{self._max_help_position}} {help_text}\n"
                else:
                    return f"  {action_invocation}{' ' * self._max_help_position}{help_text}\n"
            else:
                return f"  {action_invocation}\n"


class CharmArgumentParser(argparse.ArgumentParser):
    def print_help(self):
        help_text = self.format_help()
        print(help_text)

    def error(self, message):
        ts = text_styler.TextStyler()
        usage = self.format_usage()
        print(usage)
        print(ts.dim(f"Try {ts.cyan(f'{self.prog} --help')} for help."))
        if self._subparsers:
            print(f"\n{ts.red('Error')} Mission command.\n")
        else:
            print(f"\n{ts.red('Error')} {message}\n")
        self.exit(2)


class Charmcli:
    def __init__(
        self,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        formatter_cls=None,
        pretty_errors=True,
    ):
        if pretty_errors:
            sys.excepthook = excepthook.charmcli_excepthook
        self.formatter_class = formatter_cls if formatter_cls else CharmHelpFormatter
        self.parser = CharmArgumentParser(
            description=help, epilog=epilog, formatter_class=self.formatter_class
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.commands: dict[str, CommandInfo] = {}

    def command(self):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if not hasattr(func, "__annotations__"):
                raise ValueError("Function must have type annotations")

            cmd_name = "-".join(func.__name__.split("_"))
            cmd_parser = self.subparsers.add_parser(
                cmd_name,
                description=func.__doc__ or "",
                formatter_class=self.formatter_class,
            )

            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                has_default = param.default is not inspect.Parameter.empty
                has_annotation = param.annotation is not inspect.Parameter.empty
                optional_by_type = False
                help_text = ""

                if has_annotation:
                    origin = get_origin(param.annotation)
                    args = get_args(param.annotation)
                    optional_by_type = (
                        origin in (Union, UnionType) and type(None) in args
                    )

                    if origin in (Union, UnionType) and not optional_by_type:
                        raise ValueError(
                            "Charmcli doesn't support multiple types for args."
                        )

                    if origin is Annotated:
                        help_text = args[1]

                if has_default or optional_by_type:
                    cmd_parser.add_argument(
                        f"--{name.replace('_', '-')}",
                        dest=name,
                        default=param.default if has_default else None,
                        help=help_text,
                    )
                else:
                    cmd_parser.add_argument(
                        name,
                        help=help_text,
                    )

            self.commands[cmd_name] = CommandInfo(name=cmd_name, command=func)

            return func

        return decorator

    def __call__(self, *args: Any, **kwargs: Any):
        args = self.parser.parse_args()
        args_dict = vars(args)
        cmd = self.commands.get(args_dict.pop("command"))
        cmd.command(**args_dict)
