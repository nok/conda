
from argparse import ArgumentDefaultsHelpFormatter
from os.path import abspath, expanduser

from anaconda import anaconda
from config import ROOT_DIR
from package_plan import create_activate_plan


def configure_parser(sub_parsers):
    p = sub_parsers.add_parser(
        'activate',
        description     = "activate available packages in the specified Anaconda enviropnment.",
        help            = "activate available packages in the specified Anaconda enviropnment.",
        formatter_class = ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--confirm",
        action  = "store",
        default = "yes",
        choices = ["yes", "no"],
        help    = "ask for confirmation before activating packages in Anaconda environment",
    )
    p.add_argument(
        "--dry-run",
        action  = "store_true",
        default = False,
        help    = "display packages to be modified, without actually executing",
    )
    p.add_argument(
        '-p', "--prefix",
        action  = "store",
        default = ROOT_DIR,
        help    = "Anaconda environment to activate packages in",
    )
    p.add_argument(
        '-f', "--follow-deps",
        action  = "store_true",
        default = False,
        help    = "activate dependencies automatically",
    )
    p.add_argument(
        'packages',
        metavar = 'package_version',
        action  = "store",
        nargs   = '*',
        help    = "package versions to install into Anaconda environment",
    )
    p.set_defaults(func=execute)


def execute(args, parser):
    conda = anaconda()

    prefix = abspath(expanduser(args.prefix))
    env = conda.lookup_environment(prefix)

    plan = create_activate_plan(env, args.packages, args.follow_deps)

    if plan.empty():
        print 'No packages found to activate, nothing to do'
        return

    print plan

    if args.dry_run: return

    if args.confirm == "yes":
        proceed = raw_input("Proceed (y/n)? ")
        if proceed.lower() not in ['y', 'yes']: return

    plan.execute(env)


