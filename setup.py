from distutils.core import setup

VERSION = '0.1'

desc = """Database interface, includes a sqlite wrapper with improved error-handling."""

name = 'quelo'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages = ['quelo', 'quelo.sqlite'],
      platforms=['Any'],
      requires=['unicoder']
)