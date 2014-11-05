from git import Repo
from git.errors import GitCommandError

import os
import re

NO_RELEASE = []
NO_CHANGES = []
PACKAGES = []
CHANGES = {}


def handle_git(package):
    repo = Repo('./src/{0}'.format(package))
    try:
        describe = repo.git.describe()
    except GitCommandError:
        # no tags
        NO_RELEASE.append(package)
        return

    # no commits after last tag
    if describe.find('-') == -1:
        NO_CHANGES.append(package)
        return

    # last commit is the version bump
    if 'Back to development:' in repo.heads[0].commit.message:
        NO_CHANGES.append(package)
        return

    # add package to pending to be released
    PACKAGES.append(package)

    # TODO: add the list of changes added since the last release
    CHANGES[package] = []


for package in os.listdir('./src'):
    if '.git' in os.listdir('./src/{0}'.format(package)):
        handle_git(package)
    else:
        print '{0} uses subversion, checks not done'.format(package)

msg = '\n\nAll collected: {0} packages in total'
print msg.format(len(NO_CHANGES) + len(NO_RELEASE) + len(PACKAGES))

msg = '\n{0} packages do not have changes.\n'
print msg.format(len(NO_CHANGES))

msg = '\n{0} packages did not have any release so far:\n'
print msg.format(len(NO_RELEASE))

NO_RELEASE.sort()
for pkg in PACKAGES:
    print pkg

msg = '\n{0} packages have changes pending to be released:\n'
print msg.format(len(PACKAGES))

PACKAGES.sort()
for pkg in PACKAGES:
    print pkg
