maintainers
===========

Python3 library for parsing MAINTAINERS files. It can parse the non toml formats listed at [lgtm](https://lgtm.co/docs/maintainers/).


Example
-------
```python

import maintainers


all_maintainers = maintainers.parse('/path/to/MAINTAINERS')
for maintainer in all_maintainers:
    print('Name: {}'.format(maintainer.name))    # Name: Jane Developer
    print('Login: {}'.format(maintainer.login))  # Login: janesgithub_username
    print('Email: {}'.format(maintainer.email))  # Email: jdeveloper@example.com
    print(maintainer)  # name=Jane Developer, login=janesgithub_username, email=jdeveloper@example.com
    print(maintainer.json())  # '{"name": "Jane Developer", "login": "janesgithub_username", "email": "jdeveloper@example.com"}'


jane = maintainer.Maintainer(name='Jane Developer', login='janesgithub_username', email="jdeveloper@example.com")
jill = maintainer.Maintainer(name='Jill Engineer', login='jillsgithub_username', email="jengineer@example.com")
print(all_maintainers.is_maintainer(jane))  # True
print(all_maintainers.is_maintainer(jill))  # False
```
