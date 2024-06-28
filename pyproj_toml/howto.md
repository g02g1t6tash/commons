To use a pyproject.toml file in your Python project, follow these steps:

1. Create the file:
Place a file named `pyproject.toml` in the root directory of your project.

2. Specify the build system:
At minimum, include a [build-system] section to specify the build backend and requirements:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

3. Define project metadata:
Add a [project] section with basic information about your package:

```toml
[project]
name = "your-package-name"
version = "0.1.0"
description = "A short description of your package"
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
```

4. Specify dependencies:
List your project's dependencies in the [project] section:

```toml
dependencies = [
    "requests>=2.25.1",
    "numpy>=1.20.0",
]
```

5. Add optional configurations:
You can include additional sections for tools like pytest, black, or flake8:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
]

[tool.black]
line-length = 88
target-version = ['py38']
```

6. Use with pip:
To install your package and its dependencies, run:

```
pip install .
```

Or for an editable install:

```
pip install -e .
```

7. Build your package:
To build distribution packages, use:

```
python -m build
```

This will create both source and wheel distributions in the `dist/` directory.

By using pyproject.toml, you centralize your project's configuration, making it easier to manage dependencies, build settings, and tool configurations in one place. This approach is becoming the standard for Python packaging and is supported by modern build tools and package managers[1][2][3][4].

