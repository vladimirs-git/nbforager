"""unittests package"""
import ast
import re
from pathlib import Path

from vhelpers import vdate, vdict, vpath, vre, vlist

from nbforager.types_ import LStr, LPath

ROOT = Path(__file__).parent.parent
PYPROJECT_D = vdict.pyproject_d(ROOT)


def _check_function_name(function_name: str, lines: LStr) -> None:
    """Check if the function name is present in the given lines of code.

    :param function_name: Name of the function to check.
    :param lines: Lines of code to search for the function name.
    :raises ValueError: If the function name is not found or if docstring is absent.
    """
    # tested function name
    is_docstring = ""
    expected_func_name = ""
    for line in lines:
        # function name in docstring
        if not expected_func_name:
            is_docstring = vre.find1(r'^\s+"""', line)
            items: LStr = vlist.split(line, ignore="_")
            if function_name in items:
                # magic function name
                if re.match("__[a-z]+__$", function_name):
                    break
                # usual function name
                expected_func_name = function_name
                continue

            # private method detected
            if f"_{function_name}" in items:
                function_name = f"_{function_name}"
                expected_func_name = function_name
                continue

            # constant
            if function_name.upper() in items:
                function_name = function_name.upper()
                expected_func_name = function_name
                continue
            continue

        # next test detected
        if line.startswith("def test_"):
            raise ValueError(f"{expected_func_name=} is required in")

        # looking function name in the code
        items = vlist.split(line, ignore="_")
        if expected_func_name in items:
            break
    else:
        if is_docstring:
            raise ValueError("Docstring is required,")
        if expected_func_name:
            raise ValueError(f"{expected_func_name=} is required in")


def test__version__readme():
    """Version in README, URL."""
    expected = PYPROJECT_D["tool"]["poetry"]["version"]
    package = PYPROJECT_D["tool"]["poetry"]["name"].replace("_", "-")
    # readme = PYPROJECT_D["tool"]["poetry"]["readme"]
    # readme_text = Path.joinpath(ROOT, readme).read_text(encoding="utf-8")
    url_toml = "pyproject.toml project.urls.DownloadURL"
    url_text = PYPROJECT_D["tool"]["poetry"]["urls"]["Download URL"]

    for source, text in [
        # (readme, readme_text),
        (url_toml, url_text),
    ]:
        regexes = [fr"{package}.+/(.+?)\.tar\.gz", fr"{package}@(.+?)$"]
        versions = [v for s in regexes for v in re.findall(s, text, re.M)]
        assert expected in versions, f"version {expected} not in {source}"


def test__version__changelog():
    """Version in CHANGELOG."""
    path = Path.joinpath(ROOT, "CHANGELOG.rst")
    with open(str(path), encoding="utf-8") as file:
        text = file.read()
    regex = r"(.+)\s\(\d\d\d\d-\d\d-\d\d\)$"
    actual = vre.find1(regex, text, re.M)

    expected = PYPROJECT_D["tool"]["poetry"]["version"]
    assert actual == expected, f"version in {path=}"


def test__version__docs():
    """Version in docs/config.py."""
    path = Path.joinpath(ROOT, "docs", "conf.py")
    with open(str(path), encoding="utf-8") as file:
        code = file.read()
    tree = ast.parse(code)

    actual = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "release":
                    actual = ast.literal_eval(node.value)
                    break

    expected = PYPROJECT_D["tool"]["poetry"]["version"]
    assert actual == expected, f"version in {path=}"


def test__last_modified_date():
    """Last modified date in CHANGELOG."""
    path = Path.joinpath(ROOT, "CHANGELOG.rst")
    with open(str(path), encoding="utf-8") as file:
        text = file.read()
    regex = r".+\((\d\d\d\d-\d\d-\d\d)\)$"
    actual = vre.find1(regex, text, re.M)

    extensions = [r"\.py$", r"\.toml$"]
    files = [s for ext in extensions for s in vpath.get_files(ROOT, ext)]
    expected = vdate.last_modified(files)
    assert actual == expected, "last modified file"


def test__tested_function_names():
    """Check unittest function names."""
    skip_files = ["test__package.py"]
    skip_tests: LStr = ["test__init_extra_keys"]

    root = ROOT.joinpath("tests")
    paths: LPath = [Path(s) for s in vpath.get_files(root, r"\btest_\S+\.py$")]
    paths = [o for o in paths if not o.name == skip_files]

    for path in paths:
        lines: LStr = path.read_text(encoding="utf-8").splitlines()
        for line_id, line in enumerate(lines):
            if not line.startswith("def test_"):
                continue

            # tested function name
            test_name = line.split()[1].split("(")[0]
            if [s for s in skip_tests if s == test_name]:
                continue
            if re.match("test_(?!_)", test_name):
                raise ValueError(f"{test_name=} start with `test__` is required, {path}")

            function_name = vre.find1("^test(__[a-z]+__)", test_name)  # magic method
            if not function_name:
                function_name = test_name.split("__")[1]  # with description section

            lines_of_test = lines[line_id + 1:]
            try:
                _check_function_name(function_name, lines_of_test)
            except ValueError as ex:
                raise ValueError(f"{ex} {test_name=}, {path}") from ex
