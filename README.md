# roblox

Code lives in `src/` and is synced into Roblox Studio with [Rojo](https://rojo.space).

| Folder        | Shows up in Studio as                              |
|---------------|----------------------------------------------------|
| `src/shared`  | `ReplicatedStorage.Shared`                          |
| `src/server`  | `ServerScriptService.Server`                        |
| `src/client`  | `StarterPlayer.StarterPlayerScripts.Client`         |

## Connecting to Roblox Studio

1. Install [Rokit](https://github.com/rojo-rbx/rokit), then run `rokit install` in this folder (installs Rojo).
2. In Studio, install the Rojo plugin: run `rojo plugin install`, or get it from the Creator Store.
3. In this folder, run `rojo serve`.
4. In Studio, open the **Rojo** plugin tab and click **Connect** (default `localhost:34872`).

Edits to files in `src/` now show up in Studio right away. Press Play to see
`Hello, server!` and `Hello, client!` in the Output window.

To build a place file without Studio: `rojo build -o game.rbxl`.
