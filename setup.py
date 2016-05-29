from distutils.core import setup
from pip.req import parse_requirements


# resolv version from file
version_file = open('VERSION')
version = version_file.read().strip()

# resolv deps from requirements.txt file
install_reqs = parse_requirements('requirements.txt', session=False)
dependencies = [str(ir.req) for ir in install_reqs]


setup(name='alexa-skill-the-price',
      version=version,
      description="Ask the price of",
      author='Florian CHAZAL',
      author_email='florianchazal@gmail.com',
      url='https://github.com/flochaz/the-price',
      packages=[
          'ask',
          'ask.config',
          'the_price',
          'the_price.search_engines',
          'the_price.utils',
          'the_price.interfaces'],
      package_data={'ask.config': ['../data/*']},
      license='MIT',
      install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'ask-the-price = the_price.interfaces.command_line:ask_the_price_of',
        ],
    }
)
