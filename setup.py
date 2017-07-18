from setuptools import setup

setup(
    name='wateringsystem-mqtt-client-gh',
    version='1.0.0',
    packages=[''],
    url='https://github.com/MCeddy/wateringsystem-mqtt-client',
    license='MIT',
    author='René Schimmelpfennig',
    author_email='mail@reneschimmelpfennig.de',
    description='saves sensor values from MQTT broker.',
    install_requires=['paho–mqtt >= 1.3', 'mysqlclient >= 1.3.10', 'PyYAML >= 3.12']
)
