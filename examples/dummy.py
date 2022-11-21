from thoughtspot_tml import Worksheet
import argparse
import pathlib


def filepath(fp: str) -> pathlib.Path:
    """
    Converts a string to a pathlib.Path.
    """
    path = pathlib.Path(fp)

    if not path.exists():
        raise argparse.ArgumentTypeError(f"path '{fp!r}' does not exist")

    if not path.is_file():
        raise argparse.ArgumentValueError(f"path must be a file, got '{fp!r}'")

    return path


def main():
    # Create a command line application
    #   - argument for a WORKSHEET.worksheet.tml
    #   - options for the "before" and "after" tabling naming conventions
    parser = argparse.ArgumentParser("worksheet")
    parser.add_argument("worksheet_tml", help="a worksheet.tml to remap", type=filepath)
    parser.add_argument("-s", "--src-prefix", metavar="SRC", default="DEV_", type=str, help="(default: %(default)s)")
    parser.add_argument("-d", "--dst-prefix", metavar="DST", default="", type=str, help="(default: %(default)s)")

    # Parse CLI input
    args = parser.parse_args()

    # Read from file
    tml = Worksheet.load(args.worksheet_tml)
    
    # Replace instances of DEV_ with nothing
    for table in tml.worksheet.tables:
        if table.name.startswith(args.source_prefix):
            _, prefix, name = table.name.partition(args.source_prefix)
            table.name = f'{args.target_prefix}{name}'

    # Save to file
    tml.dump(args.worksheet_tml)


if __name__ == '__main__':
    raise SystemExit(main())
