"""
Identity Resolution Package
Resolves entities across multiple sources into canonical identities
"""

from .resolver import IdentityResolver, ResolvedEntity
from .matcher import (
    AttributeMatcher,
    PhoneMatcher,
    EmailMatcher,
    PhoneticMatcher,
    AddressMatcher,
    RelationshipMatcher
)

__all__ = [
    "IdentityResolver",
    "ResolvedEntity",
    "AttributeMatcher",
    "PhoneMatcher",
    "EmailMatcher",
    "PhoneticMatcher",
    "AddressMatcher",
    "RelationshipMatcher"
]