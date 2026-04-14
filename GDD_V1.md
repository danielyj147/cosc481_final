# Game Design Document

[Recommanded Soundtrack](https://www.youtube.com/watch?v=8PydbXdAx84&list=RD8PydbXdAx84&start_radio=1)

## Table of Contents

- [Introduction](#introduction)
  - [Game Summary Pitch](#game-summary-pitch)
  - [Inspiration](#inspiration)
  - [Player Experience](#player-experience)
  - [Platform](#platform)
  - [Software](#software)
  - [Genre](#genre)
  - [Target Audience](#target-audience)
- [Concept](#concept)
  - [Gameplay Overview](#gameplay-overview)
  - [Theme Interpretation](#theme-interpretation)
  - [Primary Mechanics](#primary-mechanics)
  - [Secondary Mechanics](#secondary-mechanics)
- [Art](#art)
- [Audio](#audio)
- [Game Experience](#game-experience)
- [Development Timeline](#development-timeline)

---

## Introduction

### Game Summary Pitch

Hooked on a feeling

### Inspiration

**Professor Layton**

_Professor Layton_ acts as an inspiration for the visual and musical elements. It has a Japanese-European 2D animation style and whimsical & classical soundtrack that encapsulates player's attention. The cadance of the music and the play is also a huage part of the game.

![Professor Layton and Curious Village](https://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Professor_Layton_and_the_Curious_Village_NA_Boxart.JPG/250px-Professor_Layton_and_the_Curious_Village_NA_Boxart.JPG)

**Getting Over It with Bennett Foddy**

_Getting Over It_(GOI) is famous for its unintuivie and frustrating mechanics. It is also rather infamous for its level design that doesn't guarantee consistent progress. You can climb up to right before the finishline, but still can fall down to the very beginning of the game with just one misclick. The dry and passive agressive voice over when the player falls from a platform also adds to the fun of the game. 

![Getting Over It in game](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Getting_Over_It_with_Bennett_Foddy_screenshot.jpg/250px-Getting_Over_It_with_Bennett_Foddy_screenshot.jpg)

**Terraria**

_Terraria_ has hooking mechanism that allows user to move between platforms using a hook item. The idea of using such mechanism in a 2D game is very appealing to me and I think the mechanism is much more interesting that just jumping.

![terraria hook](/assets/terraria_hook.png)

### Player Experience

In 5 carefully crafted levels inside a gothic yet cartoony tower, the player must traverse **platforming** sections using **snappy movement** aided by creative applications of potions. The trek also features **light combat and exploration elements**. The player must use **quick reflexes and patience** to master the skill curve of the movement and potions to progress.

### Platform

The game is developed to be released on Mac & Windows PC with Pyray framwork.


### Software

- VS Code
- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/photo)

### Genre

Singleplayer, platformer, climbing

### Target Audience

COSC 481 students

---

## Concept

### Gameplay Overview

<!-- The player controls a blue owl alchemist (affectionately named the Owlchemist), attempting to reclaim his alchemist tower from a powerful shadow wizard. In each level, the player must use **jumping, gliding, and potion throwing** to platform around deadly obstacles and ascend the tower. -->

### Theme Interpretation (Shadows and Alchemy)

<!-- **'Shadows' interpretation:** The player is tasked with defeating a shadow wizard and is challenged by several enemies corrupted by shadow.

**'and' interpretation:** By including transitions to all of the UI elements, there is a sense of movement from one state to another, giving further cohesion to the entire game.

**'Alchemy' interpretation:** The player plays as an alchemist who can use potions to traverse, fight enemies, and overcome obstacles through levels of a tower that have repeated alchemical motifs throughout.

**Alchemy** makes itself incredibly prevalent throughout the theming and setting of the game, as the player controls an alchemist who uses multiple types of potions as a primary means of problem-solving and traversal. Conversely, **shadows** represent the game's opposition, with the main antagonist being a shadow wizard who has sent forth multiple types of shadow minions to challenge the player. Shadows also pervade as a motif in the gothic, "spooky" theming of the alchemist's tower. -->

### Primary Mechanics

| Mechanic | Description |
| --- | --- |
| **Hook** | Left clicking shoots a hook from a player and the hook gets stick to a surface |
| **Climb/Reel in** | Right clicking reels in the rope, ma |
| **Swing** | After the hook gets stuck to a surface, you can move around the mouse to swing |
| **Reflect** | There are surfaces where the hook gets reflected rather than getting hooked |

### Secondary Mechanics

| Mechanic | Description |
| --- | --- |
| **Reflecting Obstacles** | There are surfaces where the hook gets reflected rather than getting hooked |
| **Powerups** | Allows user to throw the hook further. | 

---

## Art

### Theme Interpretation

<!-- The design of the characters and settings is influenced by the 'alchemy' theme, with the main character being a stylized alchemist and several alchemical props (potions, cauldrons, etc.) throughout the game. The 'shadows' theme comes into play with the design of the enemies and the dark, Castlevania-esque architecture and theming of the game. -->

### Design

<!-- The game has a very cartoony, **simplistic pixel art style** reminiscent of SNES-era games. The characters have **exaggerated, whimsical designs**, and the movement and animation is designed to feel **stretchy and cartoony**, with the art of the general game and setting intended to feel charming and lived in. -->

---

## Audio

### Music

<!-- The main genres of Owlchemist are chiptune, orchestral, and EDM. These provide a nice energy and allow us to implement a wide variety of ideas. -->

### Sound Effects

<!-- Using ChipTone, we made simple yet charming NES-inspired sound effects. The SFX is meant to enhance the gameplay experience and overall feel without being intrusive or disruptive, which is why only some actions have sounds while others do not. -->

---

## Game Experience

### UI

<!-- The UI fits with the tone of animation in the rest of the game by feeling very squishy, responsive, and juicy. UI elements have transitional animations and haptic feedback whenever interacted with. The game consists of a main and pause menu with adjustable settings. -->

### Controls

**Mouse**

Left Click: shoots/releaes the hook

Hold Left + Release: shoot hook further

Hold Right: reels in the hook

Mouse Movement: decide the direction of the hook. 


---

## Development Timeline

### Minimum Lovable Product

| # | Assignment | Type | Status | Finish By | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Initial Design Doc | doc | 🟡 | April 16, 10 PM | |
| 2 | Code Commit V1 | dev | 🟡 | April 19, 10 PM | |
| 3 | Final Code | dev | 🔴 |  Apirl 30, 5 PM| |
| 4 | Final Design Doc | doc | 🔴 | May 4, 10 PM | |
| 5 | Demo Vid | doc | 🔴 | May 4, 10 PM | |
| 6 | Presentation | other | 🔴 | May 6, ??:?? | |

<!-- ### Stretch Goals

| Feature | Type | Status | Notes |
| --- | --- | --- | --- |
| Final Boss | Coding | Finished | Shadow Wizard is responsible for taking over the main character's tower. | -->

## References

- [Owl Chemist GDD](https://docs.google.com/document/d/1_iPOdIFm9iiRNyMTM2WL3YTD0CGeOks3YKBjTsDJvd8/edit?tab=t.0#heading=h.k2hqrk99qjg6)