from setuptools import setup, find_packages

setup(
    name="shortterm-memory",
    version="0.1.0",
    author="Tadiello Sébastien",
    author_email="sebastientadiello@gmail.com",
    description="Une approche pour la gestion de la mémoire à court terme dans les chatbots.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sebDtSci/ShortTerm-memory",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
