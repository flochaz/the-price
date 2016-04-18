from distutils.core import setup

setup(name='alexa-skill-the-price',
      version='0.0.1',
      description="Ask the price of",
      author='Florian CHAZAL',
      author_email='florianchazal@gmail.com',
      url='https://github.com/flochaz/the-price',
      packages=['ask', 'ask.config'], 
      package_data={'ask.config': ['../data/*']},
      license='MIT',
)
