"""Setup script for Juiced - CyTube TUI Chat Client."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='juiced',
    version='0.2.6',
    description='Terminal User Interface for CyTube chat rooms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Juiced Contributors',
    url='https://github.com/yourusername/Juiced',
    packages=find_packages(),
    package_data={
        'juiced': [
            'themes/*.json',
        ],
    },
    python_requires='>=3.7',
    install_requires=[
        'blessed>=1.19.0',
        'python-socketio[client]>=5.0.0',
        'websocket-client>=0.2.0',
        'PyYAML>=6.0',
        'requests>=2.25.0',
        'aiohttp>=3.8.0',
    ],
    entry_points={
        'console_scripts': [
            'juiced=juiced.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications :: Chat',
        'Topic :: Terminals',
    ],
    keywords='cytube chat tui terminal irc blessed juiced',
    license='MIT',
)
