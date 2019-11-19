from setuptools import setup, find_packages

setup(
    name="Streets of Helsinki",
    version="0.1",
    description="Streamlit app to show the streets in Helsinki",
    url="https://github.com/neliseiska/streets_of_helsinki",
    author="Jonne Haapalainen",
    author_email="jonne.haapalainen@gmail.com",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "geopandas",
        "matplotlib",
        "descartes",
        "black",
    ],
)
