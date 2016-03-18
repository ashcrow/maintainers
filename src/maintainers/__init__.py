# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    (1) Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#    (2) Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
#    (3)The name of the author may not be used to
#    endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
MAINTAINER file parser.
"""

import json
import re

__version__ = '0.1.0'

LE_RX = re.compile('^(?P<login>.*) <(?P<email>.*)>$')
NEL_RX = re.compile('^(?P<name>.*) <(?P<email>.*)> \(@(?P<login>.*)\)$')


class MalformedMaintainerError(Exception):
    """
    Raised when a maintainer can not be prased.
    """
    pass


class Maintainers(list):
    """
    A bunch of maintainers.
    """

    def is_maintainer(self, instance):
        """
        Notes if a Maintainer instance is in the list.

        :param instance: A Maintainer instance.
        :type instance: Maintainer
        """
        if repr(instance) in [repr(x) for x in self]:
            return True
        return False

    def __str__(self):
        """
        Human readable version of the instance.
        """
        result = 'Maintainers: '
        for x in self:
            result = '{}\n    {}'.format(result, x)
        return result

    def __repr__(self):
        """
        Representation of the instance.
        """
        result = 'Maintainers('
        for x in self:
            result = '{}{}, '.format(result, repr(x))
        return '{})'.format(result[:-2])


class Maintainer:
    """
    A single maintainer.
    """

    __slots__ = ('name', 'login', 'email')

    def __init__(self, name=None, login=None, email=None):
        """
        Creates an instance of a Maintainer.

        :param name: The maintainers name.
        :type name: str
        :param login: The login of the maintainer.
        :type name: str
        :param email: The email of the maintainer.
        :type email: str
        """
        self.name = name
        self.login = login
        self.email = email

    def json(self):
        """
        JSON representation of this maintainer.
        """
        return json.dumps(self.__dict__)

    def __str__(self):
        """
        Human readable version of the instance.
        """
        return 'name={}, login={}, email={}'.format(
            self.name, self.login, self.email)

    def __repr__(self):
        """
        Representation of the instance.
        """
        return 'Maintainer(name="{}", login="{}", email="{}")'.format(
            self.name, self.login, self.email)


def parse(file_path, ignore_errors=False):
    """
    Parses a file and returns a list of maintainers.

    :param file_path: Full path to the maintainers file.
    :type file_path: str
    :param ignore_errors: If bad data should be skipped.
    :type ignore_errors: bool
    :returns: A list of maintainers.
    :rtype: Maintainers(Maintainer()...)
    """
    all_maintainers = Maintainers()
    with open(file_path, 'r') as maintainers_fobj:
        for line in maintainers_fobj.readlines():
            line = line[:-1]
            kwargs = {}

            if ' ' not in line:
                kwargs['login'] = line
            else:
                try:
                    kwargs = NEL_RX.search(line).groupdict()
                except AttributeError:
                    try:
                        kwargs = LE_RX.search(line).groupdict()
                    except AttributeError:
                        # Bad data
                        if ignore_errors:
                            continue
                        raise MalformedMaintainerError(file_path, line)
            all_maintainers.append(Maintainer(**kwargs))
    return all_maintainers
