# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared utilities used by both downloads and uploads."""


from gooresmed import exceptions


def _do_nothing():
    """Simple default callback."""


def header_required(response, name, callback=_do_nothing):
    """Checks that a specific header is in a headers dictionary.

    Args:
        response (object): An HTTP response object, expected to have a
            ``headers`` attribute that is a ``Mapping[str, str]``.
        name (str): The name of a required header.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        str: The desired header.

    Raises:
        ~gooresmed.exceptions.InvalidResponse: If the header is missing.
    """
    headers = response.headers
    if name not in headers:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Response headers must contain header', name)

    return headers[name]


def get_status_code(response):
    """Access the status code from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        int: The status code.
    """
    return response.status_code


def require_status_code(response, status_codes, callback=_do_nothing):
    """Require a response has a status code among a list.

    Args:
        response (object): The HTTP response object.
        status_codes (tuple): The acceptable status codes.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        int: The status code.

    Raises:
        ~gooresmed.exceptions.InvalidResponse: If the status code is not
            one of the values in ``status_codes``.
    """
    status_code = get_status_code(response)
    if status_code not in status_codes:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Request failed with status code',
            status_code, u'Expected one of', *status_codes)
    return status_code