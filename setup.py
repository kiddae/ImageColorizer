from setuptools import setup
setup(
    name='ImageColorizer',
    version='1.0',
    packages=['ImageColorizer'],
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': ['ImageColorizer = ImageColorizer.__main__:main']
    }
)
