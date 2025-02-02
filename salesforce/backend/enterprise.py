import base64
import re
from hashlib import sha256
from typing import Optional
import django
from django.conf import settings
from salesforce.backend import max_django
from salesforce.dbapi.exceptions import LicenseError


def check_enterprise_license(  # pylint:disable=too-many-locals
        msg: Optional[str] = None, required: int = 1, key: str = ''
        ) -> None:
    """Check that a valid license key for the enterprise version exists"""
    key = key or getattr(settings, 'DJSF_LICENSE_KEY', '') or '//'
    text, level_text, signature_text = key.rsplit('/', 2)
    level = int(level_text or 1) if text else 0
    if level < max(required, 1):
        raise LicenseError(msg or "This command requires the enterprise license key")

    # This check is an integer arithmetic puzzle that does not use anything except Python
    # and Django settings. It is evaluated in less than half milisecond on a notebook CPU.
    # There is no cryptography, no network access. The license key never expires.
    # It is a safe code. Please do not discuss publicly about other aspects how the
    # license key is weak or strong. Many easier ways exist how to skip a verification
    # without analyzing this. :-)

    # A legal way to skip the enterprise check is to use django-salesforce-agpl
    # <https://github.com/django-salesforce/django-salesforce-agpl>
    # and accept the restrictive AGPL licence that requires you provide all your Django
    # source code where you use django-salesforce available to all users who could
    # use your project by network (by your web app, by your backend app etc.) and
    # publish it under a compatible license.
    # That AGPL license is useful especially for education and for exclusive open
    # source contribution. In other cases, if you want to use the enterprise features,
    # you probably need to sponsor this project to make its development sustainable.

    n, o, q, r, s, t, u, v, w, x = 32, 63, 220, 1, 8, 9223372036854775807, 63, 69, 'utf8', 'big'
    h = int.from_bytes(base64.b64decode(signature_text, b'+.'), x)
    b, f, d, e, g, j, k, h, m = 0, 0, n, r, 0, h & t, (h >> o) & u, h >> v, 0
    p = sha256(re.sub("[ &']", "-", text).strip('-').encode(w)).digest() + int.to_bytes(h, s, x)
    for a in range(o):
        p = sha256(p).digest()
        y = int.from_bytes(p, x)
        m, b = max(m, bool(a == k) * y), b ^ (bool(j & (r << a)) * y)
    for a in range(q):
        g, f, d, e = g | (bool(b & e & m) << f), f + bool(m & e), d - bool(j & e), e << r
    if g != level or level > 3 or d:
        raise LicenseError("The enterprise licence key is invalid")


def check_license_in_latest_django() -> None:
    if django.VERSION[:2] == max_django:
        check_enterprise_license(
            "License key is required for django-saleforce used with the last Django version. "
            "(read about dual-license)")
