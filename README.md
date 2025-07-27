<p align="center">
  <a href="https://pypi"><img src="./docs/charmcli.png" alt="Charmcli"></a>

</p>
<p align="center">
    <em>Charmcli, build great CLIs. Easy to code. Based on Python type hints.</em>
</p>

---

Charmcli is a library for building command-line (CLI) apps that are both fun to use and easy to build. It’s powered by Python type hints.

The key features are:

- **Intuitive to write**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
- **Easy to use**: Automatically adds help messages, commands and args based on type annotation.
- **Less code**: Avoid repeating yourself. One line of code can do a lot. Fewer mistakes.
- **Quick setup**: You can integrate it into your app almost instantly.
- **Grow large**: Grow in complexity as much as you want, create arbitrarily complex trees of commands and groups of subcommands, with options and arguments.

## Installation

Create and activate a virtual environment and then install **Charmcli**:

<div class="termy">

```console
$ pip install charmcli
---> 100%
Successfully installed charmcli
```

</div>

## Example

### Use Charmcli in your code

Create a `charmcli.Charmcli()` app, and create two commands with their parameters.

```Python hl_lines="3  6  11  20"
import charmcli

app = charmcli.Charmcli()

@app.command()
def hello(name: str):
    """Greet a user"""
    print(f"Hello {name}")

@app.command()
def goodbye(name: Annotated[str, "name of a user"], msg: str = "Goodbye"):
    """Farewell a user"""
    print(f"{msg}, Mr {name}.")

if __name__ == "__main__":
    app()
```

And that will:

- Explicitly create a `charmcli.Charmcli` app.
- Add two subcommands with `@app.command()`.
- Execute the `app()` itself

### Run the example

Check the help:

<div class="termy">

```console
$ python main.py

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Positional arguments:
  hello                Greet a user
  goodbye              Farewell a user

Options:
  -h, --help           show this help message and exit

// You have 2 commands (the 2 functions): goodbye and hello
// Params are the postional arguments and options for the command.
// Docstring is used as help text for command.
```

</div>

Now check the help for the `hello` command:

<div class="termy">

```console
$ python main.py hello --help

Usage: main.py hello [-h] name

Greet a user

Positional arguments:
  name

Options:
  -h, --help           show this help message and exit
```

</div>

And now check the help for the `goodbye` command:

<div class="termy">

```console
$ python main.py goodbye --help

Usage: main.py goodbye [-h] [--greet GREET] name

Farewell a user

Positional arguments:
  name                 name of a user

Options:
  --msg MSG            (default: Goodbye)
  -h, --help           show this help message and exit
```

</div>

Now you can try out the new command line application:

<div class="termy">

```console
// Use it with the hello command

$ python main.py hello Chad

Hello Chad

// And with the goodbye command

$ python main.py goodbye Chad

Goodbye Chad.

$ python main.py goodbye Chad --msg 'Bye Bye'

Bye Bye Chad.
```

</div>

### Recap

In summary, you declare **once** the types of parameters (_CLI arguments_ and _CLI options_) as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python**.

For example, for an `int`:

```Python
total: int
```

or for a `bool` flag:

```Python
force: bool
```

**TODO**: add **files**, **paths**, **enums** (choices), etc. And tools to create **groups of subcommands**, add metadata, extra **validation**, etc.

**You get**: great editor support, including **completion** and **type checks** everywhere.

## Dependencies

**Charmcli** uses no external dependencies it works with just standard Python.
Internally, it includes lightweight modules for features like text coloring and hyperlink support, built using ASCII sequences. This ensures compatibility with a wide range of environments, including older terminals that may not support modern features.

## License

This project is licensed under the terms of the MIT license.

## Screenshots

<img src="./docs/cmd-ss.png" alt="Charmcli" style="max-width: 100%; width: 600px;">
