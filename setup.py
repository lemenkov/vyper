# -*- coding: utf-8 -*-

import os
import re
import subprocess

from setuptools import setup

extras_require = {
    "test": [
        "pytest>=8.0,<9.0",
        "pytest-cov>=4.1,<5.0",
        "pytest-instafail>=0.4,<1.0",
        "pytest-xdist>=3.0,<3.4",
        "pytest-split>=0.7.0,<1.0",
        "eth_abi>=5.0.0,<6.0.0",
        "py-evm>=0.12.1b1",
        "lark==1.1.9",
        "hypothesis[lark]>=6.0,<7.0",
        "eth-stdlib==0.2.7",
        "eth-account==0.12.2",
        "setuptools",
        "hexbytes>=1.2",
        "pyrevm>=0.3.2",
    ],
    "lint": [
        "black==23.12.0",
        "flake8==6.1.0",
        "flake8-bugbear==23.12.2",
        "flake8-use-fstring==1.4",
        "isort==5.13.2",
        "mypy==1.5",
    ],
    "dev": ["ipython", "pre-commit", "pyinstaller", "twine"],
}

extras_require["dev"] = extras_require["dev"] + extras_require["test"] + extras_require["lint"]

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


# strip local version
def _local_version(version):
    return ""


def _global_version(version):
    from setuptools_scm.version import guess_next_dev_version

    # strip `.devN` suffix since it is not semver compatible
    # minor regex hack to avoid messing too much with setuptools-scm internals
    version_str = guess_next_dev_version(version)
    return re.sub(r"\.dev\d+", "", version_str)


hash_file_rel_path = os.path.join("vyper", "vyper_git_commithash.txt")
hashfile = os.path.relpath(hash_file_rel_path)

# there is no way in setuptools-scm to get metadata besides the package
# version into version.py. (and we need that version to be PEP440 compliant
# in order to get it into pypi). so, add the commit hash to the package
# separately, in order so that we can add it to `vyper --version`.
try:
    commithash = subprocess.check_output("git rev-parse --short HEAD".split())
    commithash_str = commithash.decode("utf-8").strip()
    with open(hashfile, "w") as fh:
        fh.write(commithash_str)
except subprocess.CalledProcessError:
    pass


setup(
    name="vyper",
    use_scm_version={
        "local_scheme": _local_version,
        "version_scheme": _global_version,
        "write_to": "vyper/version.py",
    },
    description="Vyper: the Pythonic Programming Language for the EVM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vyper Team",
    author_email="",
    url="https://github.com/vyperlang/vyper",
    license="Apache License 2.0",
    keywords="ethereum evm smart contract language",
    include_package_data=True,
    packages=["vyper"],
    python_requires=">=3.10,<4",
    py_modules=["vyper"],
    install_requires=[
        "cbor2>=5.4.6,<6",
        "pycryptodome>=3.5.1,<4",
        "packaging>=23.1",
        "lark>=1.0.0,<2",
        "wheel",
        "immutables",
    ],
    setup_requires=["setuptools_scm>=7.1.0,<8.0.0"],
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "vyper=vyper.cli.vyper_compile:_parse_cli_args",
            "fang=vyper.cli.vyper_ir:_parse_cli_args",
            "vyper-json=vyper.cli.vyper_json:_parse_cli_args",
            "venom=vyper.cli.venom_main:_parse_cli_args",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    package_data={"vyper.ast": ["grammar.lark"]},
    data_files=[("", [hash_file_rel_path])],
)
