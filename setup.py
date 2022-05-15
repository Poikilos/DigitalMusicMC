#!/usr/bin/env python
import setuptools
import sys
# - For the example on which this was based, see
#   https://github.com/poikilos/linux-preinstall/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/world_clock/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/nopackage/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/pypicolcd/blob/master/setup.py
# - For nose, see https://github.com/poikilos/mgep/blob/master/setup.py

# python_mr = sys.version_info.major
# versionedModule = {}
# versionedModule['urllib'] = 'urllib'
# if python_mr == 2:
#     versionedModule['urllib'] = 'urllib2'

install_requires = []

if os.path.isfile("requirements.txt"):
    with open("requirements.txt", "r") as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            install_requires.append(line)

description = (
    "Manage a large archival music collection including"
    " using optional archival syntax. Generate boolean playlists based"
    " tags, ratings, and custom rating order for the randomizer."
)
long_description = description
if os.path.isfile("readme.md"):
    with open("readme.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='dmmc',
    version='0.3.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        ('License :: OSI Approved ::'
         ' MIT License'),
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
    keywords=('music manage random boolean playlists m3u m3u8'
              ' strawberry'),
    url="https://github.com/poikilos/DigitalMusicMC",
    author="Jake Gustafson",
    author_email='7557867+poikilos@users.noreply.github.com',
    license='MIT',
    # packages=setuptools.find_packages(),
    packages=['dmmc'],
    include_package_data=True,  # look for MANIFEST.in
    # scripts=['example'],
    # ^ Don't use scripts anymore (according to
    #   <https://packaging.python.org/en/latest/guides
    #   /distributing-packages-using-setuptools
    #   /?highlight=scripts#scripts>).
    entry_points={
        'console_scripts': [
            'add-to-strawberry=dmmc.strawberry:main',
        ],
    },
    install_requires=install_requires,
    #     versionedModule['urllib'],
    # ^ "ERROR: Could not find a version that satisfies the requirement
    #   urllib (from nopackage) (from versions: none)
    #   ERROR: No matching distribution found for urllib"
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    zip_safe=False,  # It can't run zipped due to needing data files.
)
