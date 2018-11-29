from setuptools import setup

setup(
    name='pybin',
    version='0.1.0',
    author='C. Simpson',
    author_email='c.a.simpson01@gmail.com',
    packages=['pybin'],
    include_package_data=True,
    url='https://github.com/casimp/pybin',
    download_url = 'https://github.com/casimp/pybin/tarball/v0.1.0',
    license='LICENSE.txt',
    description='Image merge/binning designed for monochromatic XRD data.',
    keywords = ['XRD', 'EDXRD', 'x-ray', 'diffraction', 'strain', 'synchrotron'],
#    long_description=open('description').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"]
)
