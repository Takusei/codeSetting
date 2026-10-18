# VS Code

`settings.json` is the original settings file, renamed from `profile.code-profile`.
It uses VS Code's JSON-with-comments syntax. It is not a full exported profile.
The installer links it to the default stable VS Code user settings location;
existing settings are backed up, not merged.

Extensions are not bundled. On the machine whose extension selection you want to
preserve, run from the repository root:

```sh
code --list-extensions > vscode/extensions.txt
```

Review that list before committing. To install the saved list on another machine:

```sh
while IFS= read -r extension; do
  [ -z "$extension" ] || code --install-extension "$extension"
done < vscode/extensions.txt
```

No extension inventory has been fabricated from settings: referencing an extension
in a setting does not prove it is currently installed. The saved settings reference
Biome, Ruff, theme/icon extensions, and other tools that must be installed separately.
The relative Marp theme `classmethod.css` is not included; provide it or remove that
setting if unused. Review terminal auto-approval preferences for each machine.

For a complete portable profile including selected extensions, use VS Code's
[Export Profile](https://code.visualstudio.com/docs/configure/profiles) action and
import the resulting `.code-profile` file. Choose either that workflow or the
linked-settings workflow deliberately to avoid competing sources of settings.
