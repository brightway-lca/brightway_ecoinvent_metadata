from setuptools import setup
import os

packages = []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)


# Probably should be changed, __init__.py is no longer required for Python 3
for dirpath, dirnames, filenames in os.walk('bw_ecoinvent_metadata'):
    # Ignore dirnames that start with '.'
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='bw_ecoinvent_metadata',
    version="0.1",
    packages=packages,
    author='Chris Mutel',
    author_email='cmutel@gmail.com',
    license="BSD 3-clause",
    package_data={'bw_ecoinvent_metadata': package_files(os.path.join('bw_ecoinvent_metadata', 'data'))},
    install_requires=[
        'bw_io',
        'bw_projects',
        'bw_default_backend',
        'lxml',
        'xlrd',
    ],
    url="https://github.com/brightway-lca/bw_ecoinvent_metadata",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    description='Versioned ecoinvent flows, methods, and characterization factors for Brightway',
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)
