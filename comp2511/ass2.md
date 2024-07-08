<!-- SPDX-License-Identifier: zlib-acknowledgement -->

https://nw-syd-gitlab.cseunsw.tech/COMP2511/24T2/specs/assignment-ii-spec/-/blob/main/MVP.md
https://nw-syd-gitlab.cseunsw.tech/COMP2511/24T2/specs/assignment-ii-spec/-/blob/main/Assignment_Specification.md

modify
triggerOverlapEvent(), triggerMovingAwayEvent(), destroyEntity()

TouchEntity implements OverlapEvent
Key overlap
Bomb overlap
Potion overlap
Sword overlap
Treasure overlap
Wood overlap
Arrow, Boulder overlap
Door overlap
Player overlap
Portal overlap

DestroyEntity implements DestroyEvent
ZombieToastSpawner destroy

TouchDestroyEntity implements OverlapEvent, DestroyEvent
Enemy overlap, destroy
Mercenary overlap, destroy

Entity
Buildable, Exit, Wall 

TouchLeaveEntity implements OverlapEvent, MoveAwayEvent
Switch overlap, away

---------------------------------------------------------------------------
class PickupItem implements InventoryItem {
  void onPickup(Player p) {
    p.addToInventory(this);
    map.destroyEntity(this);
  }

  @Override onOverlap() {
    onPickup();
  }
}

class Treasure/Bomb extends PickupItem {
  @Override onPickup() {
    
  }
}
---------------------------------------------------------------------------

- buildable simple reallocation into parent class attributes
 
- add state applyBuff() etc.
Player {
  state (what potion in effect)
}

----------------------------

logical entities (activatible): 
bulb (if current) 
switch door (if current)
logical bombs (explode on condition...)

IMPORTANT: the addition of new entities results in new entries in json map parser     

IMPORTANT: cardinally adjacent (so left-right-up-down; no diagonal)

IMPORTANT: conductor activation then logical conditions

conductors:
wire, switches
OR: only 1 activated adjacent conductor
AND: all activated adjacent conductor; atleast 2 as well
XOR: only 1 activated conductor
CO_AND: 2 or more activated on same tick

current through wire or activated switch (i.e. a single switch requires no wires)


- on each tick; chained activation and deactivation

--------------------------------------

dmc.newGame()
dmc.build()
dmc.interact()

dmc.tick()
update seems to register callback actions on priority queues
cur-tick events in sub
next-tick events in addingSub


entities: static, moving, collectable, buildable

entity battles

zone goals

json dungeon maps
{
  "entities": [
    {x, y, type, colour, key}
  ],
  "goal-condition": {
    "goal": goal,
    "subgoals: []
  }
}

IMPORTANT: config_template.json

personal blog just lists tasks you have done for that week
include summarising your activities, adding links to your merge requests, and reflecting on the challenges you faced 

require branches and merge requests for pair-blog
(squash commits; don't delete branch;

Task1:
before starting blog:
 - What fields/methods you will need to add/change in a class
 - What new classes/packages you will need to create
once done, merge request:
 - A meaningful MR title that encompasses the changes
 - A brief description which outlines the changes being made
 - Make sure to keep the MR as small as possible
 - Make sure all the Continuous Integration checks (regression tests, linting, coverage) remain passing.
once approved, copy MR link into blog

a) movement code
only player can use items/potions
if (effectivePotion != null) {
  nextPos = effectivePotion.enemyMove(this, player, map)
} else {
  nextPos = enemyMove()
}
movement code for enemies with potions, also without potions
-random movement
-away from player movement
-spider movement

b) Switch is subject. Bombs observers
c) LSP violation
d) tight coupling 
e) violation of open/closed 
f) open refactoring; potions + buildable entities etc. MR for each one done

TODO: write tests for task1 or just regression?

Task2:
TBD development. Want to do 'design review', 'test lists', 'test list review'
Discuss doing have this at end

Task3:
Verify software implements requirements? Just integration tests?
Write test maps with Dungeon Map Helper https://cs2511-dungeonmania-map-generator.vercel.app/#/

