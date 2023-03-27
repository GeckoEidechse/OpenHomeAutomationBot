from . import __version__
import logging


def main():
    # Set log level
    logging.basicConfig(level=logging.INFO)

    logging.info("Hello, World!")
    logging.info(f"My package version is {__version__}")


if __name__ == "__main__":
    main()
