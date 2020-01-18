import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywebcrawler", # Replace with your own username
    version="0.0.1",
    author="Karthik E C",
    author_email="eckarthik39@gmail.com",
    description="A fast web crawler to satisfy all your needs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eckarthik/PyWebCrawler",
    packages=setuptools.find_packages(),
    install_requires=["requests", "bs4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'pywebcrawler': ['data/mimetypes.txt','data/useragents.txt']},
    include_package_data=True,
    python_requires='>=3.6',
)