import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social-ethosa",
    version="0.2.0",
    author="Ethosa",
    author_email="social.ethosa@gmail.com",
    description="The social ethosa library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosa/social_ethosa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ]
)