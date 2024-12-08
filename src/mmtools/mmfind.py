"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = mmtools.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import os
import json5
import pkg_resources  # to list installed packages
import re
from dataclasses import dataclass

from mmtools import __version__

__author__ = "Yuyao Huang"
__copyright__ = "Yuyao Huang"
__license__ = "MIT"

_logger = logging.getLogger(__name__)

_config_dir = os.path.expanduser('~/.config/mmtools')
if not os.path.exists(_config_dir):
    os.makedirs(_config_dir)

# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from mmtools.skeleton import fib`,
# when using this Python module as a library.

@dataclass
class MMPackage:
    name: str
    location: str
    version: str = None

    def __repr__(self):
        return f"{self.name} {self.version or ''} ({self.location})"

def find_mm_packages():
    """Find path to all the mm family packages
    """
    p: pkg_resources.DistInfoDistribution
    # p.location: str, the absolute path to the package.
    # p.project_name: str, the name of the package.

    packages = [
        MMPackage(p.project_name, os.path.join(p.location, p.project_name), p.version)
        for p in pkg_resources.working_set if p.project_name.startswith('mm') and p.project_name!='mmtools']

    if os.path.exists(f'{_config_dir}/mm_packages.json'):
        with open(f'{_config_dir}/mm_packages.json', 'r') as f:
            packages_json = json5.load(f)
            for p in packages_json:
                if os.path.exists(p['location']):
                    packages.append(MMPackage(**p))

    # logging
    for p in packages:
        _logger.info(f"Found MMPackage: {repr(p)}")
    
    return packages


def find_mm_types(keyword):
    """Find the definition of a mm class definition

    Args:
      keyword (str): keyword to search for

    Returns:
      str: definition of the mm type
    """
    
    mm_packges = find_mm_packages()

    # find the file and the line that includes the keyword
    results = []
    for p in mm_packges:
        for root, dirs, files in os.walk(p.location):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        for i, line in enumerate(f.readlines()):
                            if line.strip().startswith('class ') \
                                and keyword.lower() in line.lower():

                                class_name = re.findall(r'class\s+(\w+)', line)[0]
                                if keyword.lower() in class_name.lower():
                                    # the relative path to p.location
                                    relative_path = os.path.relpath(root, os.path.dirname(p.location))
                                    # regex to match the class name
                                    result = {
                                        "definition": line.strip(),
                                        "path": f"{os.path.join(root, file)}:{i+1}",
                                        "import_statement": f"from {relative_path.replace('/', '.')}.{file[:-3]} import {class_name}",
                                    }
                                    results.append(result)

    # print the results
    if len(results) == 0:
        print(f"No definition found for {keyword}")
    else:
        for result in results:
            print(f"{result['path']}\n\t{result['definition']}\n\t>> {result['import_statement']}\n")



# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Find the definition of a mm class definition.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"mmtools {__version__}",
    )
    parser.add_argument(dest="keyword", help="keyword to search for", type=str, metavar="KEYWORD")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Script starting ...")
    find_mm_types(args.keyword)
    _logger.debug("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m mmtools.skeleton 42
    #
    run()
