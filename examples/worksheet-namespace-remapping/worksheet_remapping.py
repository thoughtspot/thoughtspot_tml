from thoughtspot_tml import Worksheet
import argparse
import pathlib
import re


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
    parser = argparse.ArgumentParser()
    parser.add_argument("worksheet_tml", help="a worksheet.tml to remap", type=filepath)
    parser.add_argument("-s", "--src-prefix", metavar="SRC", default="DEV_", type=str, help="(default: %(default)s)")
    parser.add_argument("-d", "--dst-prefix", metavar="DST", default="TEST_", type=str, help="(default: %(default)s)")

    # Parse CLI input
    args = parser.parse_args()

    # Read from file
    tml = Worksheet.load(args.worksheet_tml)
    
    # Build a regular expression which matches the source prefix at the beginning of a string
    RE_SRC_NAMESPACE = re.compile(fr"^{args.src_prefix}.*")

    # Replace instances of DEV_ with TEST_
    tml.worksheet.name = RE_SRC_NAMESPACE.sub(args.dst_prefix, tml.worksheet.name)

    for table in tml.worksheet.tables:
        table.name = RE_SRC_NAMESPACE.sub(args.dst_prefix, table.name)

    # Save to file
    tml.dump(args.worksheet_tml)


if __name__ == '__main__':
    raise SystemExit(main())
