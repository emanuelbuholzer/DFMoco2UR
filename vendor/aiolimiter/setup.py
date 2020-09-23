# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiolimiter']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.3.0,<2.0.0'],
 'docs': ['sphinx>=2.2.1,<4.0.0',
          'aiohttp-theme>=0.1.6,<0.2.0',
          'sphinx-autodoc-typehints>=1.10.3,<2.0.0',
          'sphinxcontrib-spelling>=4.3,<6.0',
          'toml>=0.10.0,<0.11.0']}

setup_kwargs = {
    'name': 'aiolimiter',
    'version': '1.0.0b1',
    'description': 'asyncio rate limiter, a leaky bucket implementation',
    'long_description': '# aiolimiter\n\n[![Azure Pipelines status for master branch][azure_badge]][azure_status]\n[![codecov.io status for master branch][codecov_badge]][codecov_status]\n[![Latest PyPI package version][pypi_badge]][aiolimiter_release]\n[![Latest Read The Docs][rtd_badge]][aiolimiter_docs]\n\n[azure_badge]: https://dev.azure.com/mjpieters/aiolimiter/_apis/build/status/CI?branchName=master\n[azure_status]: https://dev.azure.com/mjpieters/aiolimiter/_build/latest?definitionId=4&branchName=master "Azure Pipelines status for master branch"\n[codecov_badge]: https://codecov.io/gh/mjpieters/aiolimiter/branch/master/graph/badge.svg\n[codecov_status]: https://codecov.io/gh/mjpieters/aiolimiter "codecov.io status for master branch"\n[pypi_badge]: https://badge.fury.io/py/aiolimiter.svg\n[aiolimiter_release]: https://pypi.org/project/aiolimiter "Latest PyPI package version"\n[rtd_badge]: https://readthedocs.org/projects/aiolimiter/badge/?version=latest\n[aiolimiter_docs]: https://aiolimiter.readthedocs.io/en/latest/?badge=latest "Latest Read The Docs"\n\n## Introduction\n\nAn efficient implementation of a rate limiter for asyncio.\n\nThis project implements the [Leaky bucket algorithm][], giving you precise control over the rate a code section can be entered:\n\n```python\nfrom aiolimiter import AsyncLimiter\n\n# allow for 100 concurrent entries within a 30 second window\nrate_limit = AsyncLimiter(100, 30)\n\n\nasync def some_coroutine():\n    async with rate_limit:\n        # this section is *at most* going to entered 100 times\n        # in a 30 second period.\n        await do_something()\n```\n\nIt was first developed [as an answer on Stack Overflow][so45502319].\n\n## Documentation\n\nhttps://aiolimiter.readthedocs.io\n\n## Installation\n\n```sh\n$ pip install aiolimiter\n```\n\nThe library requires Python 3.6 or newer.\n\n## Requirements\n\n- Python >= 3.6\n\n## License\n\n`aiolimiter` is offered under the [MIT license](./LICENSE.txt).\n\n## Source code\n\nThe project is hosted on [GitHub][].\n\nPlease file an issue in the [bug tracker][] if you have found a bug\nor have some suggestions to improve the library.\n\n## Developer setup\n\nThis project uses [poetry][] to manage dependencies, testing and releases. Make sure you have installed that tool, then run the following command to get set up:\n\n```sh\npoetry install -E docs && poetry run doit devsetup\n```\n\nApart from using `poetry run doit devsetup`, you can either use `poetry shell` to enter a shell environment with a virtualenv set up for you, or use `poetry run ...` to run commands within the virtualenv.\n\nTests are run with `pytest` and `tox`. Releases are made with `poetry build` and `poetry publish`. Code quality is maintained with `flake8`, `black` and `mypy`, and `pre-commit` runs quick checks to maintain the standards set.\n\nA series of `doit` tasks are defined; run `poetry run doit list` (or `doit list` with `poetry shell` activated) to list them. The default action is to run a full linting, testing and building run. It is recommended you run this before creating a pull request.\n\n[leaky bucket algorithm]: https://en.wikipedia.org/wiki/Leaky_bucket\n[so45502319]: https://stackoverflow.com/a/45502319/100297\n[github]: https://github.com/mjpieters/aiolimiter\n[bug tracker]: https://github.com/mjpieters/aiolimiter/issues\n[poetry]: https://poetry.eustace.io/\n',
    'author': 'Martijn Pieters',
    'author_email': 'mj@zopatista.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mjpieters/aiolimiter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
