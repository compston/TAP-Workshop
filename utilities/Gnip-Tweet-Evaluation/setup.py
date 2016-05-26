from setuptools import setup,find_packages

setup(
    name='gnip_tweet_evaluation',
    version='0.1',
    author='Jeff Kolb',
    author_email='jeffakolb@gmail.com',
    packages=find_packages(),
    scripts=['evaluate_tweets.py'],
    install_requires = ['sngrams','matplotlib','pyyaml','requests','requests_oauthlib','pyfarmhash'],
    url='https://github.com/jeffakolb/Gnip-Tweet-Evaluation',
    license='LICENSE.txt',
    description='Conversation and audience analysis of a corpus of Tweet payloads from Gnip/Twitter APIs.', 
    )
