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

Have you ever been to Colgate University's Foggy Bottom Obervatory? 

Me neither. 

What is this place, really? What is going on in there?? Why is it called Foggy Bottom??? A new Astrology Professor who has recently become a Colgate faculty goes out to find out the mystery of Fogggy Bottom Obervatory.

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

From the foggy bottom, the player uses a hook with rope to climb back to outside.
Player can shoot the hook with a mouse left click and swing with mouse movement. 
There are obsticles such as pivot points and reflective blocks(reflects hook).
The play must use problem solving skills and quick reflexes to get use to this rather uncommon mechanics. 


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

The player controls an Astronomy Professor who's injured in legs to climb out of 
Foggy Bottom Observatory using a hook with a rope. 

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

The background should go along with the theme of "foggy bottom". I think the background should look like the chracter is trapped inside a bricked well with heavy fog behind the character. The character should look adventurous yet academic to go along with the "newly became Colgate faculty member" theme. 


### Design

The background should be very old looking brick wall/well as the observatory was built in 1950s. 
I want the game to have 2D Japanese-English animation style to heighten the mysterious and puzzling nature of the situation.

---

## Audio

### Music

I want the background music to be whimsical & jazzy like that of Professor Layton. 

### Sound Effects

I'm thinking of playing a dramatic sound effect if player from a platform more than a certain y distance. 
I should also add "hooking" sound(sound that is similar to hammering a nail on a wall) and "reflected"(metalic clank) sound.

---

## Game Experience

The player controls the Astrology Professor who cannot walk or jump because he is injured from the fall to the "foggy bottom" of the Observatory.
However, he finds a hook & a rope. He throws the rope to climb back to the very top of the observatory.

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
- [Foggy Bottom Observatory](https://observatory.colgate.edu/foggybot/foggybot.html)