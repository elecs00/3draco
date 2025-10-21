from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'slampibot_examples'

setup(
    name=package_name,
    version='7.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='erail',
    maintainer_email='edurobotailab@gmail.com',
    description='ROS2 Humble Packages for Slampibot',
    license='Apache License, Version 2.0',    
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'topic_publisher = slampibot_examples.topic_publisher:main',
            'topic_subscriber = slampibot_examples.topic_subscriber:main',
            'service_server = slampibot_examples.service_server:main',
            'service_client = slampibot_examples.service_client:main',
            'action_server = slampibot_examples.action_server:main',
            'action_client = slampibot_examples.action_client:main',
            'action_client_parameters = slampibot_examples.action_client_parameters:main',
        ],
    },
)

