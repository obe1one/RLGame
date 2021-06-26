import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RLGame",
    version="0.0.1",
    author="Chang-Sheng Kao",
    author_email="johnson30708@gmail.com",
    description="RLGame is a package provides multi-agent implementation of some classic games for Reinforcement Learning (RL).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obe1one/RLGame",
    project_urls={
        "Bug Tracker": "https://github.com/obe1one/RLGame",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)