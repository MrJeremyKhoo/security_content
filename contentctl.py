import os
import sys
import argparse
from bin import validate as validator
from bin import generate as generator
from pathlib import Path

VERSION = 1


def init(args):
    path = args.path
    print("""
Running Splunk Security Content Control Tool (contentctl) v{0}
starting program loaded for TIE Fighter...
      _                                            _
     T T                                          T T
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                   ____                   | |
     | |            ___.r-"`--'"-r.____           | |
     | |.-._,.,---~"_/_/  .----.  \_\_"~---,.,_,-.| |
     | ]|.[_]_ T~T[_.-Y  / \  / \  Y-._]T~T _[_].|| |
    [|-+[  ___]| [__  |-=[--()--]=-|  __] |[___  ]+-|]
     | ]|"[_]  l_j[_"-l  \ /  \ /  !-"_]l_j  [_]~|| |
     | |`-' "~"---.,_\"\  "o--o"  /"/_,.---"~" `-'| |
     | |             ~~"^-.____.-^"~~             | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     | |                                          | |
     l_i                                          l_j -Row

    """.format(VERSION))

    # parse config
    security_content_path = Path(path).resolve()
    if security_content_path.is_dir():
        print("contentctl is reading from path {0}".format(
            security_content_path))
    else:
        print("ERROR: contentctl failed to find security_content project")
        sys.exit(1)
    return str(security_content_path)


def new(args):
    security_content_path = init(args)

def validate(args):
    security_content_path = init(args)
    # hard setting verbosity for now
    VERBOSE = True
    print("contentctl is validating all content under {0}".format(security_content_path))
    validator.new(security_content_path, VERBOSE)


def generate(args):
    security_content_path = init(args)
    # hard setting verbosity for now
    VERBOSE = True

    output = Path(args.output).resolve()
    if output.is_dir():
        print("contentctl is using folder {0} to write deployment".format(
            output))
    else:
        print("ERROR: contentctl failed to find folder for deployment {0}".format(output))
        sys.exit(1)

    print("contentctl is generating a new splunk_app under ".format(output))
    generator.new(security_content_path, args.output, VERBOSE)


def main(args):
    # grab arguments
    parser = argparse.ArgumentParser(
        description="Use `contentctl.py action -h` to get help with any Splunk Security Content action")
    parser.add_argument("-p", "--path", required=False, default=".",
                        help="path to the Splunk Security Content. Defaults to `.`")
    parser.add_argument("-v", "--version", default=False, action="version", version="version: {0}".format(VERSION),
                        help="shows current contentctl version")
    parser.set_defaults(func=lambda _: parser.print_help())

    actions_parser = parser.add_subparsers(title="Splunk Security Content actions", dest="action")
    new_parser = actions_parser.add_parser("new", help="Create new content (detections, stories, workbooks)")
    validate_parser = actions_parser.add_parser("validate", help="Validates written content")
    generate_parser = actions_parser.add_parser("generate", help="Generates a deployment package for different platforms (splunk_app)")

    # new arguments
    new_parser.add_argument("-t", "--type", required=False, type=str, default="detection",
                                 help="Type of new content to create, please chose between detection, workbook, or story")
    new_parser.set_defaults(func=new)

    # validate arguments
    validate_parser.set_defaults(func=validate, epilog="""
        Validates security manifest for correctness, adhering to spec and other common items.
        VALIDATE DOES NOT PROCESS RESPONSES SPEC for the moment.""")

    # generate arguments
    generate_parser.add_argument("-f", "--format", required=False, type=str, default="splunk_app",
                                 help="Format of our deployment package, defaults to `splunk_app`.\n The deployment `splunk_app` runs on product Splunk Enterprise Security and Splunk Enterprise.")
    generate_parser.add_argument("-o", "--output", required=False, type=str, default="package",
                                     help="Path where to store the deployment package, defaults to `package`")
    generate_parser.set_defaults(func=generate)

    # # parse them
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
