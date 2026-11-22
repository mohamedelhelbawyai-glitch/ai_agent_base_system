---
name: phaser-ae
description: Make, build and publish Phaser AE games with the person's phaser.io account, on this computer. Use when they ask for a Phaser AE game, want to build or change a game or design they have on phaser.io, or work in a Phaser AE game folder (one with .phaser/build.json). Not for the open-source Phaser library (the phaser npm package, Phaser 3 or 4) unless they ask for Phaser AE.
---

# Phaser AE

**Phaser AE isn't the open-source Phaser library** (the `phaser` npm package, Phaser 3 or 4). If they ask for a
"Phaser game" and it isn't clear which they mean, ask once: Phaser AE, built with their phaser.io account and
published there, or the open-source Phaser library. If this folder already holds a project of its own (a
package.json that uses `phaser`, say), leave this skill be unless they ask for Phaser AE.

The person makes games with Phaser AE. They can design a game on phaser.io with a crew of bots, and you build it on
this computer with the Phaser AE CLI (`npx -y @phaser-ae/cli`), then publish it to phaser.io. They may never have used a
terminal: run every command yourself, and tell them only what they have to do (approve the sign-in, allow an install).

## Node.js

The CLI needs Node.js 20 or later: check with `node --version`. If it's missing or older, install the LTS:

- **Windows:** `winget install --id OpenJS.NodeJS.LTS -e --silent --accept-source-agreements --accept-package-agreements`.
  Tell them first that Windows will ask whether to allow it, and to say Yes. This app won't see the new Node until
  it restarts, so until then start each PowerShell command with
  `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User');`
  and suggest they restart the app when it suits them.
- **macOS:** `brew install node` if Homebrew is installed. If not, download the LTS installer (the .pkg) from
  https://nodejs.org and open it; they click through it.
- **Anything else:** https://nodejs.org.

## A new game

1. **One folder per game.** If this session's folder is empty, make the game here: give `.` as the folder. If it
   isn't, the CLI makes a folder named after the game inside it.
2. **Start it on phaser.io straight away**, before anything is decided: the game gets its page there, with its crew,
   so they can watch and talk to the crew from the start.
   - **Nothing decided yet:** `npx -y @phaser-ae/cli blank .` (or `npx -y @phaser-ae/cli blank` for a new folder). It's "Untitled game" until
     they name it. Then ask what they'd like to make.
   - **An idea:** `npx -y @phaser-ae/cli blank "<name>" [.] --idea "<the idea, in their words>"`. Add `--landscape` for a
     wide screen, or `--core 3d` for a 3D game.
   - **A design they made on phaser.io:** `npx -y @phaser-ae/cli games` lists them, then `npx -y @phaser-ae/cli build <design> [.]`.
   - **Design it with the crew first:** `npx -y @phaser-ae/cli new` opens phaser.io. When the crew is done, the Chief gives them a
     line to paste back here.
3. **Signing in.** The first command that needs phaser.io opens their browser at phaser.io to approve Phaser AE. If
   it says it's still waiting, tell them to approve it there (signing up first if they're new), then run it again.
4. **Then:** give them the links the command prints (the game's design, its crew room, and "Watch it", the build
   room), and read the game folder's CLAUDE.md and do what it says: it also says how to answer questions about the
   game on phaser.io (its tools and each tool's bot, its crew, the design document, credits). If the game's folder isn't this session's and you can start a session in it (the Claude app's Code tab can), offer to continue there: the game's preview and permissions load in that folder.

## A game they already have

Work in its folder (the one with `.phaser/build.json`), whose CLAUDE.md says the rest. `npx -y @phaser-ae/cli games` lists their
games and designs, with links to play them. `npx -y @phaser-ae/cli credits` says how many credits they have (`--buy` opens the
page to buy more), from anywhere.

<!-- Written by phaser-ae 0.8.0. "phaser-ae setup" writes it again; "phaser-ae setup --remove" takes it out. -->
