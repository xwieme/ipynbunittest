import setuptools 

setuptools.setup(
    name='ipynbtest',
    version='0.0.1',
    author='xwieme',
    description='Unit test in jupyter notebook',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    package_dir={'': '.'},
    packages=setuptools.find_namespace_packages(where='.'),
    python_requires='>= 3.7',
)