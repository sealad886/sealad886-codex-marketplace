from importlib.metadata import version

def installed_version():
    return version("semver-example-python")

def greet(name):
    return f"Hello, {name}"
