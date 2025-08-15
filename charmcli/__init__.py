import argparse
import inspect
import sys
from dataclasses import dataclass
from typing import (
    Annotated,
    Any,
    Callable,
    Iterable,
    NoReturn,
    Optional,
    Type,
    Union,
    get_args,
    get_origin,
)

from charmcli import excepthook, text_styler


@dataclass
class CommandInfo:
    name: str
    command: Callable[..., Any]


class CharmHelpFormatter(argparse.HelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 40,
        width: Optional[int] = None,
    ) -> None:
        self.ts = text_styler.TextStyler()
        super().__init__(prog, indent_increment, max_help_position, width)

    def add_usage(
        self,
        usage: Optional[str],
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._MutuallyExclusiveGroup],  # pyright: ignore[reportPrivateUsage]
        prefix: Optional[str] = None,
    ) -> None:
        if prefix is None:
            prefix = self.ts.style("yellow")("\nUsage: ")

        has_subparsers = any(
            isinstance(action, argparse._SubParsersAction)  # pyright: ignore[reportPrivateUsage]
            for action in actions
        )
        if has_subparsers:
            usage = "main.py [OPTIONS] COMMAND [ARGS]..."
        return super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading: Optional[str]) -> None:
        if heading:
            heading = self.ts.style("yellow")(heading.capitalize())
        super().start_section(heading)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings:
            metavar = self._get_default_metavar_for_positional(action)
            args_string = self._format_args(action, metavar)
            return self.ts.style("cyan")(args_string)
        else:
            opts = ", ".join(
                self.ts.style("green")(opt) for opt in action.option_strings
            )
            parts = [opts]
            if action.nargs != 0:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                parts.append(self.ts.style("cyan")(args_string))
            return " ".join(parts)

    def _get_help_string(self, action: argparse.Action) -> str:
        """Get the help string for an action, including default values"""
        help_text = action.help or ""
        if "%(default)" not in help_text and action.default not in (
            argparse.SUPPRESS,
            None,
            False,
            [],
        ):
            default_text = self.ts.style("dim")(
                f"(default: {self.ts.style('yellow')('%(default)s')})"
            )
            if action.nargs != 0:
                help_text = (
                    f"{help_text} {default_text}" if help_text else f"{default_text}"
                )
        return help_text

    def _format_action(self, action: argparse.Action) -> str:
        """Format a single action with improved styling"""
        if isinstance(action, argparse._SubParsersAction):  # pyright: ignore[reportPrivateUsage]
            try:
                lines = []
                for key, subparser in action.choices.items():  # type: ignore
                    lines.append(  # pyright: ignore[reportUnknownMemberType]
                        f"  {self.ts.style('cyan')(key):<{self._max_help_position - 10}} {subparser.description}\n"  # pyright: ignore[reportUnknownMemberType]
                    )
                return "".join(lines)  # pyright: ignore[reportUnknownArgumentType]
            except Exception:
                return ""

        action_invocation = self._format_action_invocation(action)
        help_text = self._expand_help(action)

        if not action.option_strings:
            return (
                f"  {action_invocation:<{self._max_help_position - 10}} {help_text}\n"
                if help_text
                else f"  {action_invocation}\n"
            )
        else:
            if help_text:
                if len(action_invocation) <= self._max_help_position:
                    return f"  {action_invocation:<{self._max_help_position}} {help_text}\n"
                else:
                    return f"  {action_invocation}{' ' * self._max_help_position}{help_text}\n"
            return f"  {action_invocation}\n"


class CharmArgumentParser(argparse.ArgumentParser):
    def print_help(self, file: Optional[Any] = None) -> None:
        print(self.format_help())

    def error(self, message: str) -> NoReturn:
        ts = text_styler.TextStyler()
        usage = self.format_usage()
        print(usage)
        print(
            ts.style("dim")(f"Try {ts.style('cyan')(self.prog + ' --help')} for help.")
        )
        if self._subparsers:
            print(f"\n{ts.style('red')('Error:')} Missing command.\n")
        else:
            print(f"\n{ts.style('red')('Error:')} {message}\n")
        self.exit(2)


class Charmcli:
    def __init__(
        self,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        formatter_cls: Optional[Type[argparse.HelpFormatter]] = None,
        pretty_errors: bool = True,
    ) -> None:
        if pretty_errors:
            sys.excepthook = excepthook.charmcli_excepthook
        self.formatter_class = formatter_cls or CharmHelpFormatter
        self.parser = CharmArgumentParser(
            description=help, epilog=epilog, formatter_class=self.formatter_class
        )
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)
        self.commands: dict[str, CommandInfo] = {}

    def command(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            if not func.__annotations__:
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
                is_param_bool = param.annotation is bool

                if has_annotation:
                    origin = get_origin(param.annotation)
                    args = get_args(param.annotation)
                    optional_by_type = (
                        origin
                        in (
                            Union,
                            getattr(__import__("types"), "UnionType", type(None)),
                        )
                        and type(None) in args
                    )

                    if (
                        origin
                        in (
                            Union,
                            getattr(__import__("types"), "UnionType", type(None)),
                        )
                        and not optional_by_type
                    ):
                        raise ValueError(
                            "Charmcli doesn't support multiple types for args."
                        )

                    if origin is Annotated:
                        help_text = args[1]
                        is_param_bool = args[0] is bool

                if (has_default or optional_by_type) and is_param_bool:
                    cmd_parser.add_argument(
                        f"--{name.replace('_', '-')}",
                        dest=name,
                        action=argparse.BooleanOptionalAction,
                        default=param.default if has_default else None,
                        help=help_text,
                    )
                elif has_default or optional_by_type:
                    cmd_parser.add_argument(
                        f"--{name.replace('_', '-')}",
                        dest=name,
                        default=param.default if has_default else None,
                        help=help_text,
                    )
                else:
                    cmd_parser.add_argument(name, help=help_text)

            self.commands[cmd_name] = CommandInfo(name=cmd_name, command=func)
            return func

        return decorator

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        parsed_args = self.parser.parse_args()
        args_dict = vars(parsed_args)
        cmd = self.commands.get(args_dict.pop("command"))
        if cmd:
            cmd.command(**args_dict)
