import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="soccer",
    version="1.0.0",
    url="http://qflw.de/",
    license="BSD",
    maintainer="Qubeflow",
    maintainer_email="soccer@qflw.de",
    description="The soccer bet app built with Flask.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "flask_sqlalchemy"],
    extras_require={"test": ["pytest", "coverage"]},
)
