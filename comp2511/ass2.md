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
abstract class CollectableEntity extends Entity {
  void pickedUp(Player p) {
    if (pickUpCheck(p)) {
      p.addToInventory(this);
      map.destroyEntity(this);
      postPickup(p);
    }
  }
  boolean pickUpCheck(Player p) { return true; }
  void postPickup(Player p) {}
}

class Potion/Arrow/Key/Sword/Wood extends CollectableEntity {}

class Bomb extends CollectableEntity {
  @Override
  boolean pickUpCheck(Player p) {
    return (state == State.SPAWNED);
  }
  @Override
  void postPickup(Player p) {
    subs.stream().forEach(s -> s.unsubscribe(this));
    this.state = State.INVENTORY;
  }
}

class Treasure extends CollectableEntity {
  @Override
  void postPickup(Player p) {
    p.incTreasureCount();
  }
}


---------------------------------------------------------------------------

- buildable simple reallocation into parent class attributes

public interface BattleItem {
    public BattleStatistics applyBuff(BattleStatistics origin);
    public void use(Game game);
    public int getDurability();
}

abstract class BattleEntity extends Entity implements BattleItem {
  curBattleStatistics;
  void setBattleStatistic();

  BattleEntity(Position p) {
    super(p);
  }

  void use() {
      durability--;
      if (durability <= 0) {
          game.getPlayer().remove(this);
      } 
  } 

  applyBuff(origin) {
    return BattleStatistics.applyBuff(origin, curBattleStatisics);
  }
}

public abstract class Potion extends BattleEntity {
  @Override
  void use() { return; }
} 
public class InvisiblePotion {
  InvisibilityPotion() {
    setBattleStatistic(new BattleStatistics(0, 0, 0, 1, 1, false, false));
  }
}

public class InvinciblePotion {
  new BattleStatistics(0, 0, 0, 1, 1, true, true));
}

public abstract class Buildable extends BattleEntity {} 
Bow {
  new BattleStatistics(0, 0, 0, 2, 1)); 
}
Sheild {
  new BattleStatistics(0, 0, defence, 1, 1));
}
public class Sword extends BattleEntity {
  new BattleStatistics(0, attack, 0, 1, 1));
} 

Bow
health=0, attack=0, defence=0, attackmag=2, damagered=1

Shield
health=0, attack=0, defence=defence, attackmag=1, damagered=1
 
- add state applyBuff() etc.
Player {
  state (what potion in effect)
}

-   public void translate(Direction direction) {
      Position newPosition = Position.translateBy(this.position, direction);
      setPosition(newPosition);
    }
    public void translate(Position offset) {
      Position newPosition = Position.translateBy(this.position, offset);
      setPosition(p)
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

