# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. Example garbling map."""

TRANS = (
    ('>Rock', '>Lounge'),
    ('>Track', '>Rock'),
    ('>Autotrack', '>Autorock'),
    ('rock r', 'lounge r'),
    ('track r', 'rock r'),
)
