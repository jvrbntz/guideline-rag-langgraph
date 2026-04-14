#!/usr/bin/env python3
"""
Logging configuration

Provides a configured logger for each module in the pipeline.
Import and call get_logger(__name__) at the top of each module

Usage:
    from logger import get_logger
    logger = get_logger(__name__)
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger
