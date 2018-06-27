from setuptools import setup

if __name__ == '__main__':
    setup(
        name='frostsynth',
        version='0.1',
        description='Sound synthesis stuff',
        author='Lumi Pakkanen',
        author_email='lumi.pakkanen@gmail.com',
        setup_requires=['setuptools>=34.0', 'setuptools-gitver'],
        gitver=True,
    )
