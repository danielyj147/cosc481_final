# Foggy Bottom Mystery: Game Design Document

[Recommanded Soundtrack](https://www.youtube.com/watch?v=8PydbXdAx84&list=RD8PydbXdAx84&start_radio=1)

![Foggy Bottom Observatory](https://observatory.colgate.edu/foggybot/foggybot.gif)

## Table of Contents

- [Foggy Bottom Mystery: Game Design Document](#foggy-bottom-mystery-game-design-document)
  - [Table of Contents](#table-of-contents)
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
    - [Theme Interpretation](#theme-interpretation-1)
    - [Design](#design)
  - [Audio](#audio)
    - [Music](#music)
    - [Sound Effects](#sound-effects)
  - [Game Experience](#game-experience)
    - [UI](#ui)
    - [Controls](#controls)
  - [Development Timeline](#development-timeline)
    - [Minimum Lovable Product](#minimum-lovable-product)
  - [References](#references)

---


## Introduction

### Game Summary Pitch

Have you ever been to Colgate University's Foggy Bottom Observatory? 

Me neither. 

What is this place, really? What is going on in there?? Why is it called Foggy Bottom??? 

A newly hired Astronomy Professor arrives at Colgate, eager and naive. He hears whispers about the observatory - an old dome tucked away on the edge of campus, built in the 1950s. Students avoid it. Faculty don't talk about it. One night, curiosity wins. He walks in. The floor gives. He falls.

He wakes up at the bottom - legs broken, surrounded by fog and old brick. The only way out is up. Luckily, there's a hook and a rope.

To the foggy bottom...

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

The player wakes up at the bottom of a dark, foggy shaft. No jumping. No walking. Just a hook and a rope.

Left click to shoot. Swing with the mouse. Reel in to climb. Miss, and you fall - sometimes all the way back down. The hook is your only friend, and the observatory doesn't want you to leave.

Reflective surfaces bounce your hook. Crumbling walls won't hold. Every throw is a gamble. It's frustrating, funny, and deeply satisfying when it clicks.


### Platform

The game is developed to be released on Mac & Windows PC with Pyray framwork.


### Software

- VS Code
- [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/photo) (For image editing)

### Genre

Singleplayer, platformer, climbing

### Target Audience

COSC 481 students

---

## Concept

### Gameplay Overview

The player controls an Astronomy Professor, legs broken from the fall, who must climb out of the Foggy Bottom Observatory shaft using nothing but a hook and a rope. No walking. No jumping. Just throwing, swinging, and praying the brick holds.

### Theme Interpretation

Foggy background, Climb / Vertical Levels: a whimsical interpretation of the origin of the name "`Foggy` Bottom Obervatroy"

Inability to walk or jump: the character is injured from the fall.

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

The player is trapped inside a bricked shaft with thick fog rolling behind them. The character should look adventurous yet academic - a professor who wasn't dressed for this. 

The character sprite is an archaeologist(although he is an astronomy professor) with whip animations that naturally map to the hook/rope mechanic. Animations: idle, movement, roll, whip attack, whip AoE, shoot, damage, death.


### Design

Old, weathered brick - the observatory was built in the 1950s and it shows. 2D Japanese-English animation style to heighten the mysterious, puzzling nature of the situation.

**Asset Candidates:**

| Asset | Source | License |
| --- | --- | --- |
| 2D Pixel Art Archaeologist Sprites (character) | [Elthen - itch.io](https://elthen.itch.io/2d-pixel-art-archaeologist) | Free (commercial/non-commercial) |
| Brick 2D Tileset 16x16 (walls/platforms) | [DeadlyEssence01 - OpenGameArt](https://opengameart.org/content/brick-2d-tileset-sidescrollerplatformer-16x16-de) | CC0 |
| 2D Dungeon Wall 32px Brick Brown | [lukems-br - OpenGameArt](https://opengameart.org/content/2d-dungeon-wall-32px-db32-palette-brick-brown) | CC0 |
| Fog Animation (40 frames, tileable) | [AntumDeluge - OpenGameArt](https://opengameart.org/content/fog-animation) | CC0 |
<!-- | Dark Fantasy Scenery Sprites (chains, hooks) | [ETTiNGRiNDER - OpenGameArt](https://opengameart.org/content/misc-dark-fantasy-scenery-sprites) | CC0 | -->
<!-- | 16x16 Weapon Sprites (grappling hook) | [Bennyboi_hack - OpenGameArt](https://opengameart.org/content/16x16-weapon-sprites-free) | CC0 | -->

---

## Audio

### Music

Whimsical & jazzy, like Professor Layton. The music should feel like you're solving something - not like you're in danger. Light tension, not dread.

**Music Candidates:**

| Track | Source |
| --- | --- |
| "페리온 OST" | [Maple Story](https://maplestory.nexon.com/Media/Music#a) |

### Sound Effects

Dramatic sound effect when the player falls more than a certain y distance. "Hooking" sound when the hook latches (nail-into-wall). Metallic clank when reflected off a surface.

**SFX Candidates:**

| Sound | Source | License |
| --- | --- | --- |
| Grappling Hook (launch) | [16bitstudios - Freesound](https://freesound.org/people/16bitstudios/sounds/541975/) | CC0 |
| Metal Clank (hook impact / reflect) | [JustInvoke - Freesound](https://freesound.org/people/JustInvoke/sounds/446107/) | CC-BY 4.0 |
| Rope Under Tension (swing) | [gear_clinkz - Freesound](https://freesound.org/people/gear_clinkz/sounds/547862/) | CC0 |
| Whoosh (falling) | [Kinoton - Freesound](https://freesound.org/people/Kinoton/sounds/427823/) | CC0 |
| Body Fall / Thud (dramatic fall) | [Breviceps - Freesound](https://freesound.org/people/Breviceps/sounds/447922/) | CC0 |

---

## Game Experience

The professor wakes up at the bottom of the observatory shaft. Legs broken. Fog everywhere. He can't walk. He can't jump. But there's a hook and a rope lying next to him - and a long, long way up.

### UI

I want the UI to feel similar to that of `Professor Layton`, 2010's 2D animation style with the nuance of early 1900 attire. 

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
| 1 | Initial Design Doc | doc | 🟢 | April 16, 10 PM | |
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
- [Foggy Bottom Observatory](https://observatory.colgate.edu/foggybot/foggybot.html)