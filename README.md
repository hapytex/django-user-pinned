# Django-user-pinned

[![PyPi version](https://badgen.net/pypi/v/django-user-pinned/)](https://pypi.python.org/pypi/django-user-pinned/)
[![Documentation Status](https://readthedocs.org/projects/django-user-pinned/badge/?version=latest)](http://django-user-pinned.readthedocs.io/?badge=latest)
[![PyPi license](https://badgen.net/pypi/license/django-user-pinned/)](https://pypi.python.org/pypi/django-user-pinned/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Users usually show preferences by "liking" or "pinning" items: marking the item as a favorite.

This package aims to abstract away some common tasks such as defining a `ManyToManyField` to the user model to determine who pinned the items.

It also adds a custom `QuerySet` named `PinnableQuerySet` which has four extra methods to annotate and sort by the number of pins, or by whether the given user(s) have pinned the item.

For the real models that subclass the `PinnableModel`, one can use the `PinnableAdminMixin` which adds `pin` and `unpin` actions for the logged in user, and also displays the number of pins as the last column in the table.

It also defines a `PinnedViewMixin` which essentially adds a `.is_pinned` attribute to the objects arising from the `QuerySet` such that can for example filter on these, or in a listview display whether the item is pinned.

Finally the `PinAPIViewMixin` is a mixin for an `APIView` that adds an extra action `/pin` to the `APIView` that can handle a GET, POST, or DELETE request to retrieve whether an item is pinned, or pin an item, or unpin it (in case of a DELETE request).