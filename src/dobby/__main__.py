import click


def forward(script_name: str, *args, **kwargs) -> None:
    """Dynamically forward cli args to script identified with `script_name`"""
    print(f"{script_name=}")
    print(f"{args=}")
    print(f"{kwargs=}")


@click.command()
@click.argument('args', nargs=-1)
def main(args: str | list[str] | None) -> None:
    if not args:
        print("List all scripts")

    forward(args[0], args[1:])


if __name__ == "__main__":
    main
