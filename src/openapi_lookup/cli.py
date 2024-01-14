"""CLI module."""
import argparse

from openapi_lookup import verbosity_levels, setup_logger
from openapi_lookup.openapis import get_raw_public_apis, parse_rows


logger = setup_logger()


def filter_apis(apis: list, args: argparse.Namespace) -> list:
    """Filter APIs.

    Args:
        apis (list): List of APIs to filter.
        args (argparse.Namespace): Arguments to filter by.

    Returns:
        list: Filtered list of APIs.
    """
    if args.all is True:
        return apis

    if args.category is not None:
        apis = [api for api in apis if api["category"] == args.category]

    if args.auth_method is not None:
        # Convert auth_method to None if "none" is specified
        if args.auth_method == "none":
            args.auth_method = None

        apis = [api for api in apis if api["auth_method"] == args.auth_method]

    if args.https is not None:
        apis = [api for api in apis if api["https"] == args.https]

    if args.cors is not None:
        apis = [api for api in apis if api["cors"] == args.cors]

    return apis


def print_apis(apis: list, args: argparse.Namespace) -> None:
    """Print APIs.

    Args:
        apis (list): List of APIs to print.
        args (argparse.Namespace): Arguments to filter by.
    """
    if any(
        [
            args.list_categories,
            args.list_auth_methods,
            args.list_https,
            args.list_cors,
        ]
    ):
        if args.list_categories is True:
            print("Categories:")
            categories = sorted(list(set([api["category"] for api in apis])))
            for category in categories:
                print(f"  {category}")
            print()

        if args.list_auth_methods is True:
            print("Authentication Methods:")
            auth_methods = sorted(
                list(set([str(api["auth_method"]) for api in apis]))
            )
            for auth_method in auth_methods:
                print(f"  {auth_method}")
            print()

        if args.list_https is True:
            print("HTTPS Support:")
            https = sorted(list(set([str(api["https"]) for api in apis])))
            for https in https:
                print(f"  {https}")
            print()

        if args.list_cors is True:
            print("CORS Support:")
            cors = sorted(list(set([str(api["cors"]) for api in apis])))
            for cors in cors:
                print(f"  {cors}")
            print()

    else:
        for api in apis:
            print(f"{api['name']} - {api['description']}")
            print(f"  Auth Method: {api['auth_method']}")
            print(f"  HTTPS: {api['https']}")
            print(f"  CORS: {api['cors']}")
            print(f"  Link: {api['link']}")
            print()


def cli() -> None:
    """Command line interface."""
    parser = argparse.ArgumentParser(
        description="Open APIs CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--category",
        "-c",
        help="Filter by category",
    )
    parser.add_argument(
        "--auth-method",
        "-a",
        help="Filter by authentication method",
        choices=["apikey", "oauth", "unknown", "none"],
    )
    parser.add_argument(
        "--https",
        "-s",
        help="Filter by HTTPS support",
        choices=[True, False],
    )
    parser.add_argument(
        "--cors",
        "-o",
        help="Filter by CORS support",
        choices=[True, False],
    )
    parser.add_argument(
        "--all",
        "-A",
        help="Show all APIs",
        action="store_true",
    )
    parser.add_argument(
        "--list-categories",
        help="List all categories",
        action="store_true",
    )
    parser.add_argument(
        "--list-auth-methods",
        help="List all authentication methods",
        action="store_true",
    )
    parser.add_argument(
        "--list-https",
        help="List all HTTPS support values",
        action="store_true",
    )
    parser.add_argument(
        "--list-cors",
        help="List all CORS support values",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity",
    )
    args = parser.parse_args()

    if (
        all(
            [
                args.category is None,
                args.auth_method is None,
                args.https is None,
                args.cors is None,
                args.all is False,
            ]
        )
        is True
    ):
        print("Error: No filters specified")
        print("Specify at least one filter or use --all to show all APIs")
        exit(1)

    log_level = verbosity_levels[min(args.verbosity, len(verbosity_levels) - 1)]
    logger.setLevel(log_level)

    raw_text = get_raw_public_apis()
    apis = parse_rows(raw_text)
    apis = filter_apis(apis, args)
    print_apis(apis, args)


if __name__ == "__main__":
    cli()
