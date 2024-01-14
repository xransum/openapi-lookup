"""Open APIs cli handler module."""
import argparse
import logging

from openapi_lookup import verbosity_levels, setup_logger


logger = setup_logger()


def cli() -> None:
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Open APIs CLI")
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="increase output verbosity",
    )
    args = parser.parse_args()

    log_level = verbosity_levels[min(args.verbosity, len(verbosity_levels) - 1)]
    logger.setLevel(log_level)

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    print("Hello World!")


if __name__ == "__main__":
    cli()
