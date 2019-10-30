import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social-ethosa",
    version="0.4.12",
    author="Ethosa",
    author_email="social.ethosa@gmail.com",
    description="The social ethosa library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethosa/social_ethosa",
    packages=setuptools.find_packages(),
    license="MIT",
    keywords="vk api botwrapper network math social ethosa",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Github" : "https://github.com/Ethosa/social_ethosa",
        "Documentation" : "https://github.com/Ethosa/social_ethosa/blob/master/README.md",
    },
    python_requires=">=3",
    install_requires=[
        "requests"
    ]
)