#!/usr/bin/env python3
"""
Logging configuration

Provides a named logger for each module in the pipeline.
Logging is configured once at application entry points.

Usage:
    from logger import get_logger
    logger = get_logger(__name__)
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for the given module."""
    return logging.getLogger(name)
