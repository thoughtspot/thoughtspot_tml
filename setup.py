import setuptools


# PEP 528 & 621 get us closer.. but this patterns allows for proper
# install regardless of `pip install .` or `python setup.py install`
if __name__ == '__main__':
    setuptools.setup(
        # see setup.cfg
    )
