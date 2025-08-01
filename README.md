<img src="https://raw.githubusercontent.com/vyperlang/vyper/master/docs/logo.svg?sanitize=true" alt="" width="110">

[![Build Status](https://github.com/vyperlang/vyper/actions/workflows/test.yml/badge.svg)](https://github.com/vyperlang/vyper/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/vyper/badge/?version=latest)](http://docs.vyperlang.org/en/latest/?badge=latest "ReadTheDocs")
[![Discord](https://img.shields.io/discord/969926564286459934.svg?label=%23vyper)](https://discord.gg/6tw7PTM7C2)
[![Telegram](https://img.shields.io/badge/Vyperholics🐍-Telegram-blue)](https://t.me/vyperlang)
[![Twitter](https://img.shields.io/twitter/follow/vyperlang)](https://x.com/vyperlang)

[![PyPI](https://badge.fury.io/py/vyper.svg)](https://pypi.org/project/vyper "PyPI")
[![Docker](https://img.shields.io/docker/cloud/build/vyperlang/vyper)](https://hub.docker.com/r/vyperlang/vyper "DockerHub")

[![Coverage Status](https://codecov.io/gh/vyperlang/vyper/branch/master/graph/badge.svg)](https://codecov.io/gh/vyperlang/vyper "Codecov")
[![Language grade: Python](https://github.com/vyperlang/vyper/workflows/CodeQL/badge.svg)](https://github.com/vyperlang/vyper/actions/workflows/codeql.yml)

# Getting Started
See [Installing Vyper](http://docs.vyperlang.org/en/latest/installing-vyper.html) to install vyper.
See [Tools and Resources](https://docs.vyperlang.org/en/latest/resources.html) for an additional list of framework and tools with vyper support.
See [Documentation](http://docs.vyperlang.org/en/latest/index.html) for the documentation and overall design goals of the Vyper language.

See [learn.vyperlang.org](https://learn.vyperlang.org/) for **learning Vyper by building a Pokémon game**.
See [try.vyperlang.org](https://try.vyperlang.org/) to use Vyper in a hosted jupyter environment!

**Note: Vyper is constantly evolving, use with care and understand the risks associated with smart contract development.**

# Installation
See the [Vyper documentation](https://docs.vyperlang.org/en/latest/installing-vyper.html)
for build instructions.

# Compiling a contract
To compile a contract, use:
```bash
vyper your_file_name.vy
```
***generate bytecode***

    vyper -f bytecode file-name.vy > file-name.bin

***generate abi***

    vyper -f abi file-name.vy > file-name.abi

There is also an [online compiler](https://vyper.online/) available you can use to experiment with
the language and compile to ``bytecode`` and/or ``IR``.

**Note: While the vyper version of the online compiler is updated on a regular basis it might
be a bit behind the latest version found in the master branch of this repository.**

## Testing (using pytest)

(Complete [installation steps](https://docs.vyperlang.org/en/latest/installing-vyper.html) first.)

```bash
make dev-init
./quicktest.sh -m "not fuzzing"
```

## Testing (with hevm)

Install hevm by downloading it from the releases page (https://github.com/ethereum/hevm/releases/latest) and making sure it is in your PATH. hevm tests can be enabled with `--hevm` flag, and hevm tests can be selected with the `-m hevm` marker. For instance, `./quicktest.sh -m "hevm" --hevm`.

## Developing (working on the compiler)

A useful script to have in your PATH is something like the following:
```bash
$ cat ~/.local/bin/vyc
#!/usr/bin/env bash
PYTHONPATH=. python vyper/cli/vyper_compile.py "$@"
```

To run a python performance profile (to find compiler perf hotspots):
```bash
PYTHONPATH=. python -m cProfile -s tottime vyper/cli/vyper_compile.py "$@"
```

To get a call graph from a python profile, pip install `gprof2dot` and `xdot`, and run it like `gprof2dot -f pstats stats | xdot -`. (See https://stackoverflow.com/a/23164271/).

The utility timer functions `timeit`, `profileit` and `cumtimeit` are available in `vyper/utils.py`.


# Contributing
* See Issues tab, and feel free to submit your own issues
* Add PRs if you discover a solution to an existing issue
* For further discussions and questions, post in [Discussions](https://github.com/vyperlang/vyper/discussions) or talk to us on [Discord](https://discord.gg/6tw7PTM7C2)
* For more information, see [Contributing](http://docs.vyperlang.org/en/latest/contributing.html)
