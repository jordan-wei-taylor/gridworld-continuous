import setuptools

def read(path):
    with open(path, encoding = 'utf-8') as f:
        return f.read()


setuptools.setup(
    name="gridworld-continuous",
    version="0.0.1",
    author="Jordan Taylor",
    author_email="jt2006@bath.ac.uk",
    description="A simple implementation of a continuous GridWorld",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/jordan-wei-taylor/continuous-gridworld",
    project_urls={
        "Bug Tracker": "https://github.com/jordan-wei-taylor/continuous-gridworld/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
    license=read('LICENSE'), 
    install_requires=[
        'matplotlib>=3.5.2',
        'numpy>=1.22.3',
    ]
)