from setuptools import setup

setup(
    name="pets",
    version="0.0.1",
    packages=["pets"],
    install_requires=["flask", "bcrypt","pyjwt","requests"],
    entry_points={
        "console_scripts": ["pets = pets.__main__:main"]
    }
)
