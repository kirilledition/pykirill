from . import moods
from .version import VERSION


def main():
    cli_string = moods.generate_cli_string(VERSION)
    print(cli_string)


if __name__ == "__main__":
    main()
