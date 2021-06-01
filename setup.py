from setuptools import setup, find_packages

setup(
    name='cepheus',
    version="2020060101",
    author_email="y.omae@nagoya-u.jp",
    install_requires=[
        "requests",
        "pyyaml"
    ],
    description="mdg-fiwareにデータを送信するモジュール群です",
    long_description="",
    author='yuki omae',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires='>=3',
)