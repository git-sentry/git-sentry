# git-sentry
A Git Access configuration tool, aimed to grant access to organisations, repositories and teams from a centralised
repository.


The only command available is `apply`. It takes a path to a directory containing `toml` user configuration files.
```shell script
Usage: sentry [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  apply  Apply Git config from path

```
It operates by collating all `toml` files and generating the configuration objects. Since it is incremental, the order
doesn't matter, as it doesn't remove user or team access, nor does it support demoting. **That might change in the future.**
 
The main building blocks for configuration are groups and orgs. `Groups` are used to define a collection of people, to reduce
the overhead of specifying all users individually. `Orgs` refer to the entire org configuration.

The shape of a group is quite simple. It has a `name`, which is used to identify and retrieve the group,
`usernames`, a list of individual user `login` ids, and a `groups` field, representing a list of other
groups that it contains. Both `usernames` and `groups` default to an empty list if not specified.

For the example below, `Shield Agents` contains `Black Widow` and `Hawkeye`, while `Original Avengers`
contains `Thor`, `Iron Man`, `Bruce Banner`, `Captain America`, as well as the `Shield Agents`.
```toml
[[group]]
name = 'Original Avengers'
usernames = [
    'Thor',
    'Iron Man',
    'Bruce Banner',
    'Captain America',
]
groups = [
    'Shield Agents'
]

[[group]]
name = 'Shield Agents'
usernames = [
    'Black Widow',
    'Hawkeye',
]
``` 

An organisation has a more complex structure.

```toml
[[org]]
pattern = 'a regex pattern' 
# e.g. '.*' = catch-all pattern, matching all orgs, useful for a global configuration.
# ^my-org$ = an exact match for `my-org`
# ^my.* = matches any org whose name starts with `my`

[org.members]
# all the users defined here will be given member access to the matching orgs
usernames = 'list of individual usernames'
groups = 'a list of group names'

[org.admins]
# all the users defined here will be given admin rights over the matching organisations
usernames = 'list of individual usernames'
groups = 'a list of group names'

[[org.team]]
name = 'team1'

[org.team.members]
usernames = 'a list of individual usernames'
groups = 'a list of group names'

[org.team.admins]
usernames = 'a list of individual usernames'
groups = 'a list of group names'

[[org.team.repo]]
pattern = 'a pattern to match the name of the repository by'
# e.g. '.*' = catch-all pattern, matching all repositories in the matching orgs, useful for a global configuration.
# ^my-repo$ = an exact match for `my-repo` under the matching orgs
# ^my.* = matches any repository whose name starts with `my` under the matching orgs

permission = 'pull|push|admin'
# The team permission to give to the repository

[[org.team]]
name = 'team2'

[org.team.members]
usernames = 'a list of individual usernames'
groups = 'a list of group names'

[org.team.admins]
usernames = 'a list of individual usernames'
groups = 'a list of group names'

[[org.team.repo]]
pattern = 'a pattern to match the name of the repository by'
# e.g. '.*' = catch-all pattern, matching all repositories in the matching orgs, useful for a global configuration.
# ^my-repo$ = an exact match for `my-repo` under the matching orgs
# ^my.* = matches any repository whose name starts with `my` under the matching orgs

permission = 'pull|push|admin'
# The team permission to give to the repository
```

# Installation and configuration
`Sentry` reads its configuration from the environment variables `GIT_TOKEN` and `GIT_URL`, or from `~/.config/sentry/sentry.ini`, if the environment variables aren't set.
The token needs to have at least these privileges: `repo, admin:org, user`.

The structure of the file is:
```toml
[github-url]
token = 'git-token'
```

You can then install `Sentry` by running `pip3 install .` inside this repository. 
