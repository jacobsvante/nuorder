from setuptools import setup

setup_kwargs = dict(
    name='nuorder',
    version='1.1.0',
    description="Package to make requests to NuOrder's wholesale API",
    packages=['nuorder'],
    include_package_data=True,
    author='Jacob Magnusson',
    author_email='m@jacobian.se',
    url='https://github.com/jmagnusson/nuorder',
    license='BSD',
    platforms='any',
    install_requires=[
        'requests',
    ],
    extras_require={
        'cli': [
            'argh',
            'ipython',
            'termcolor',
        ],
        'test': {
            'coverage>=4.3.4',
            'flake8>=3.3.0',
            'pytest>=3.0.7',
            'responses>=0.5.1',
        },
    },
    entry_points={
        'console_scripts': [
            'nuorder = nuorder.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

if __name__ == '__main__':
    setup(**setup_kwargs)
