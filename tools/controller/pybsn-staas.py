#!/usr/bin/env python3

#Implements interactive DMF API command interface pybsn-repl in a terminal window (see https://github.com/bigswitch/pybsn)

#Usage - At prompt []: root.core.switch_config.match(name='staas-dell-s4112f')()
#Tip - replace `-' with `_' in node names (switch-config --> switch_config)

import pybsn
import controller_info
import argparse
import logging
import textwrap
import re
import os, sys
from traitlets.config.loader import Config
from IPython.terminal.ipapp import TerminalIPythonApp
from IPython.core.magic import Magics, magics_class, line_magic

def env_var(value):
    if value not in os.environ:
        raise argparse.ArgumentTypeError("'%s' is not an environment variable" % value)
    return os.environ[value]

parser = argparse.ArgumentParser(description=__doc__)

token_source = parser.add_mutually_exclusive_group()
token_source.add_argument('--token', '-t', type=str, help="Session/Token to use")
token_source.add_argument('--env-token', '-e', type=env_var, dest='token',
                          help="Environment variable of session/token to use")

parser.add_argument('--host', '-H', type=str, default=controller_info.HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD , help="Password")
parser.add_argument('--verbose', '-v', action="count", default=0, help="Debug output")
parser.add_argument('--command', '-c', help="Command e.g., root.core.switch_config.()")

args = parser.parse_args()


def config_logger():
    #logger.setLevel(logging.INFO) replace with 2 lines for verbose arg
    logging.basicConfig(level=logging.DEBUG if args.verbose > 0 else logging.INFO)
    logging.getLogger('staas').setLevel(logging.DEBUG if args.verbose > 1 else logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
           '%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger = logging.getLogger('staas')
config_logger()

if args.token:
    ctrl = pybsn.connect(host=args.host, token=args.token, login=False)
else:
    ctrl = pybsn.connect(host=args.host, username=args.user, password=args.password)


def line_transform(lines):
    def convert(line):
        if line.endswith('#'):
            return "show_schema(%s)" % line[:-1]
        else:
            return line

    return [convert(li.strip()) + "\n" for li in lines]


@magics_class
class BsnMagics(Magics):
    @line_magic
    def help(self, s):
        print(__doc__.strip())


def show_schema(root, max_depth=1, verbose=True):
    def pretty_type(node):
        if 'typeSchemaNode' not in node:
            return node['leafType'].lower()

        t = node['typeSchemaNode']

        if t['leafType'] == 'ENUMERATION':
            names = [x for x in t['typeValidator'] if x['type'] == 'ENUMERATION_VALIDATOR'][0]['names']
            return "enum { %s }" % ', '.join(names)
        elif t['leafType'] == 'UNION':
            names = [x['name'] for x in t['typeSchemaNodes']]
            return "union { %s }" % ', '.join(names)
        else:
            return t['leafType'].lower()

    def traverse(node, depth=0, name="root", max_depth=None):
        def output(*s, **kw):
            d = kw.get("depth", depth)
            print(" " * (d * 2) + ' '.join(s))

        if max_depth is not None and depth > max_depth:
            return

        if verbose and 'description' in node:
            description = re.sub(r"\s+", " ", node['description'])
            indent = " "*(depth*2) + "  # "
            description = "\n" + textwrap.fill(
                description,
                initial_indent=indent,
                subsequent_indent=indent,
                width=70 - depth*2)
        else:
            description = ''

        if verbose:
            config = "config" in node.get('dataSources', []) and "(config)" or ""
        else:
            config = ""

        if node['nodeType'] == 'CONTAINER' or node['nodeType'] == 'LIST_ELEMENT':
            if node['nodeType'] == 'CONTAINER':
                output(name, description)
            for child_name, child in node.get('childNodes', {}).items():
                traverse(child, depth+1, child_name, max_depth=max_depth)
        elif node['nodeType'] == 'LIST':
            output(name, "(list)", description)
            traverse(node['listElementSchemaNode'], depth, name, max_depth=max_depth)
        elif node['nodeType'] == 'LEAF':
            output(name, ":", pretty_type(node), config, description)
        elif node['nodeType'] == 'LEAF_LIST':
            output(name, ":", "list of", pretty_type(node['leafSchemaNode']), config, description)
        elif node['nodeType'] == 'RPC':
            output(name, "(rpc)", description)
            if max_depth is not None and depth < max_depth:
                for name, item in (("in", "inputSchemaNode"), ("out", "outputSchemaNode")):
                    if item in node:
                        traverse(node[item], depth+1, name, max_depth=None)
                    else:
                        output(name, "(NONE)", depth=depth+1)
        else:
            assert False, "unknown node type %s" % node['nodeType']

    traverse(root.schema(), name=root._path, max_depth=max_depth)


config = Config()
config.TerminalInteractiveShell.banner1 = "Interactive STAAS Controller\nAt prompt []: root.core.switch_config.match(name='staas-dell-s4112f')()"
config.TerminalInteractiveShell.confirm_exit = False

user_ns = dict(ctrl=ctrl, root=ctrl.root, show_schema=show_schema)

app = TerminalIPythonApp(config=config)
app.interact = not args.command
app.initialize(argv=[])
app.shell.push(user_ns, interactive=False)
app.shell.input_transformers_cleanup.append(line_transform)
app.shell.register_magics(BsnMagics(app.shell))
if args.command:
    app.shell.run_cell(args.command)
app.start()
