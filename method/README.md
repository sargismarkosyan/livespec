# The method

The part of this that does not change between repositories.

| | |
|---|---|
| [process.md](process.md) | The loop, who does what, and the rules that fall out of it. Read this first. |
| [repository.md](repository.md) | Layout, branches, pull requests, commits, issues, and the moving picture every version ships. |
| [gates.md](gates.md) | What the two gates have to mean, the id system, and the faults to inject to prove they fire. |
| [testing.md](testing.md) | Behaviour tests, unit tests, and why a flaky one is worse than none. |
| [claude-md.md](claude-md.md) | What a repository's CLAUDE.md must contain, and what must stay out of it. |

Alongside them: [the seven skills](../skills/) that run the loop,
[templates](../templates/) for a change spec, a persona, a journey, a workflow
and a feature, and [`setup`](../skills/setup/SKILL.md) — the skill that installs all
of it into a repository.

**Nothing here names a command, a threshold, a filename or a language.** Those
are bindings, and every repository writes its own down in
`specs/setup/README.md`. The test for which is: could this sentence survive a
repository with pytest and a Makefile?

## Adding the marketplace and the plugin

Two steps, in Claude Code:

```
/plugin marketplace add sargismarkosyan/livespec
/plugin install livespec@livespec
```

The first registers this repository as a marketplace; the second installs the
plugin from it. `/plugin` on its own opens the browser if you would rather click.

**To check it took**, start a session and look at the skill names: they arrive
prefixed, as `livespec:refine-spec`, `livespec:feedback`, `livespec:setup` and so
on. `setup` is the only one Claude will never start by itself — type
`/livespec:setup` when you want it. A bare `refine-spec` with no prefix means a local copy in `.claude/skills/`
is shadowing the plugin.

### Wire it into the repository instead of the machine

Better than installing by hand: commit the declaration, so anybody who clones the
repository gets the process on their first session. In `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "livespec": {
      "source": { "source": "github", "repo": "sargismarkosyan/livespec" }
    }
  },
  "enabledPlugins": { "livespec@livespec": true }
}
```

That is what [`setup`](../skills/setup/SKILL.md) writes on its way out, and it is
the only livespec-shaped file the method asks a repository to carry.

### Updating

```
/plugin marketplace update livespec
```

The plugin is pinned to what the marketplace last resolved, so a change here
reaches a repository when it updates, not before. **Nothing records which version
of the method built a given commit** — where a change to the method would read
badly against old commits, say so in the change that makes it.

### Working on the method itself

Point the marketplace at a local checkout rather than at GitHub, and a skill edit
is live in the next session with no publish step:

```
/plugin marketplace add ~/Projects/livespec
```

Iterate there, and push when something settles. The alternative — editing the
skills in `.claude/skills/` of whatever repo you are in — is how two copies of a
method start disagreeing, which is the thing this plugin exists to stop.
