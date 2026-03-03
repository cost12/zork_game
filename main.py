import argparse
import dataclasses
import logging

from zork2.level_0.load import load_world

from logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def parser_from_dataclass(dataclass: type) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    for field in dataclasses.fields(dataclass):
        if field.default == dataclasses.MISSING:
            parser.add_argument(f"--{field.name}", type=field.type)
        else:
            parser.add_argument(f"--{field.name}", type=field.type, default=field.default)
    return parser

@dataclasses.dataclass(frozen=True)
class Args:
    players : int = 1

def parse_args() -> Args:
    logger.debug(dataclasses.is_dataclass(Args))
    parser = parser_from_dataclass(Args)
    return Args(**vars(parser.parse_args()))

def main():
    args = parse_args()
    logger.debug(args)
    world = load_world()
    logger.debug(world)

if __name__=="__main__":
    main()
