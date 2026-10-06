# Astro Jump

**Course:** Programación API · **Group 9**  
**Team:** Matías Alejandro Peralta, Nahuel Eberle, Lautaro Barjas  
**Built with:** Python + Pygame

## Gameplay

The player controls an astronaut who must make his way through a 2D map built as a hard-to-navigate maze. Along the way, the player has to manage the astronaut's oxygen by collecting tanks when needed, avoid space spikes, and pick up as many coins as possible. To win, the player must reach the **Omega Device** at the end of the level.

## Technical overview

### Player movement

The astronaut can move left, move right, and jump. For smoother movement, the controller uses an **acceleration and friction** system.

Gravity changes during a jump. It depends on whether the player holds the jump button, releases it, or presses down mid-air, which gives finer control over each jump.

### Coyote time and jump buffer

- **Coyote time** lets the player still jump for a short moment after leaving a platform, so jumps feel more precise.
- **Jump buffer** registers a jump pressed just before landing and performs it automatically on touchdown.

Both windows are set to roughly **0.10–0.15 seconds**, so they help the player without being noticeable.

### Oxygen

The player has an oxygen bar that drains constantly. When it reaches zero, the astronaut dies and the game restarts.

## Game elements

| Element | Behavior |
|---|---|
| **Spikes** | Kill the player on contact and restart the game. |
| **Oxygen tanks** | Fully refill the oxygen bar when collected. |
| **Coins** | Increase the coin counter; collectibles that raise the final score. |
| **Omega Device** | Win condition: touching it completes the level. |
| **Platforms** | Form the floor and walls of the level. |

## State machine

The game uses a state machine to handle navigation between screens: **main menu, game, victory, options, and credits**. Each screen has buttons that trigger the transitions between states.

## How to play

**Windows:** download the latest `.zip` from [Releases](../../releases), extract it and run `AstroJump.exe`.

**From source:**

```
pip install -r requirements.txt
python main.py
```
