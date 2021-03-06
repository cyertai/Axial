# Axial

Axial is a single player game I made for 15-112, an is inspired by Ikaruga.

In Ikaruka there are two affinities - light and dark. Enemies come in both varieties, and by switching your ship between light and dark you can prevent damage or do double damage to opponents.

Similarly in Axial, you have the same mechanic.

## Installation

Axial requires Python 2.7 and TKinter to run.

```
git clone https://github.com/cyertai/Axial.git

apt-get install python-tk
```

If not on Ubuntu, see below for installation instructions
 * https://tkdocs.com/tutorial/install.html


## Play Axial

To launch Axial, run:

```
python2 Game.py
```

The ship is immune to attacks of the same color. This mechanic is key to winning.
However you do more damage to enemies of the opposite color!

### Keyboard Controls
Movement: use WSAD or the arrow keys

Change Affinity (light/dark): C

Fire: Space Bar

### Mouse Controls
Press the left mouse button to fire.

Press the right mouse button to change affinity

Move the mouse while holding the left mouse button to move the player

### Display Items
The Health bar displays the player's health.

The score counter keeps track of your score, try to get it as big as possible!
