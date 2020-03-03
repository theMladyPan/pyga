import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygenal",
    version="1.0.4",
    author="Stanislav Rubint",
    author_email="stanislav@rubint.sk",
    description="Python implementation of Genetic Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/themladypan/pyga",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
)
