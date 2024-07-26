<!-- SPDX-License-Identifier: zlib-acknowledgement -->

// re-merge task1c-entityinheritance removed task1a

https://nw-syd-gitlab.cseunsw.tech/COMP2511/24T2/specs/assignment-ii-spec/-/blob/main/MVP.md
https://nw-syd-gitlab.cseunsw.tech/COMP2511/24T2/specs/assignment-ii-spec/-/blob/main/Assignment_Specification.md

git clone https://z5346008@nw-syd-gitlab.cseunsw.tech/COMP2511/24T2/teams/W14A_ASPARAGUS/assignment-ii.git

TODO: mention steps to find them
- spawner not destroyed
- zombie on portal
- any bribe radius
        // fail to bribe
        assertThrows(InvalidActionException.class, () -> dmc.interact(mercId));

        Position playerDiff = Position.calculatePositionBetween(player.getPosition(), this.getPosition());
        boolean isInRadius = (playerDiff.getX() <= bribeRadius && playerDiff.getY() <= bribeRadius);
        return isInRadius && player.countEntityOfType(Treasure.class) >= bribeAmount;
- multiple key pickup

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

Bow {

  Bow() {
    this.battleItemActions = new BattleItemActions(new BattleStatistics(0, 0, 0, 2, 1));
  } 
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

-------------------------------------------------------------------

int treasureGoal = config.optInt("treasure_goal", 1);

if (entity instanceof Player) {
    Player player = (Player) entity;
    map.getGame().battle(player, this);
}
-------------------------------------------------------------------

logical entities (activatible): 
bulb (if current) 
switch door (if current)
logical bombs (explode on condition...)

IMPORTANT: the addition of new entities results in new entries in json map parser     

IMPORTANT: cardinally adjacent (so left-right-up-down; no diagonal)

IMPORTANT: conductor activation then logical conditions

conductors:
wire, switches (only a conductor if switched on)

current through wire or activated switch (i.e. a single switch requires no wires)


interface LogicalCondition {
  boolean condition(Gamemap m, Position p);
}

class OrLogicalCondition implements LogicalCondition {
  public boolean condition(Gamemap map, Position pos) {
    List<Position> positions = pos.getCardinallyAdjacentPositions();
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Conductor) {
          Conductor c = (Conductor)e;
          if (c.isConducting()) {
            return true;
          }
        }
      }
    } 
    return false;
  }
}

class AndLogicalCondition implements LogicalCondition {
  boolean condition(Gamemap map, Position pos) {
    List<Position> positions = pos.getCardinallyAdjacentPositions();
    int conductorCount = 0;
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Conductor) {
          conductorCount += 1;
          Conductor c = (Conductor)e;
          if (!c.isConducting()) {
            return false;
          }
        }
      }
    } 
    return conductorCount >= 2;
  }

class XorLogicalCondition implements LogicalCondition {
  boolean condition(Gamemap map, Position pos) {
    List<Position> positions = pos.getCardinallyAdjacentPositions();
    int activeConductorCount = 0;
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Conductor) {
          Conductor c = (Conductor)e;
          if (c.isConducting()) {
            activeConductorCount += 1;
          }
        }
      }
    }
    return activeConductorCount == 1;
  }

class CoAndLogicalCondition implements LogicalCondition {
  boolean condition(Gamemap map, Position pos) {
    List<Position> positions = pos.getCardinallyAdjacentPositions();
    int activeConductorCount = 0;
    int tickActivated = -1;
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Conductor) {
          Conductor c = (Conductor)e;
          if (c.isConducting()) {
            if (tickActivated == -1) {
              tickActivated = c.getActivationTick();
              activeConductorCount += 1;
            } else {
              if (c.getActivationTick() == tickActivated) {
                activeConductorCount += 1;
              }
            }
          }
        }
      }
    }
    return activeConductorCount >= 2;
  }
}


interface LogicalEntity {
  boolean isLogicallyOn();
}

class LightBulbOn extends Entity implements LogicalEntity {
  private LogicalCondition lc;

  public LightBulbOn(Position p, LogicalCondition c) {

  }

  public boolean isLogicallyOn() {
    return lc.condition();
  }
}

class LightBulbOff extends Entity implements LogicalEntity {
  private LogicalCondition lc;

  public LightBulbOff(Position p, LogicalCondition c) {

  }

  public boolean isLogicallyOn() {
    return lc.condition();
  }
}


class SwitchDoor extends Entity implements LogicalEntity {
  boolean opened = false; 

  private LogicalCondition lc;
  public boolean isLogicallyOn() {
    return lc.condition();
  }

  public boolean canMoveOnto(GameMap map, Entity entity) {
    if (open || entity instanceof Spider) {
        return true;
    }
    return (entity instanceof Player && isLogicallyOn());
  }
}

interface Conductor {
  boolean isConducting();
  int getActivationTick();
  void activate();
  void deactivate();
}

class Switch implements Conductor {
  @Override
  boolean onOverlap() {
    activate()
  }

  void activate() {
    if (this.tick == -1) {
      this.tick = game.getTick();
    }
    this.on = true;

    List<Position> positions = pos.getCardinallyAdjacentPositions();
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Wire) {
          Wire w = (Wire)w;
          w.activate(map, this, new HashSet<>());
        }
      }
    }
  }

  @Override
  public void onMovedAway(GameMap map, Entity entity) {
    this.tick = -1;
    deactivate()
  }

  void deactivate(Switch sourceSwitch) {
    this.tick = -1;
    this.on = false;

    List<Position> positions = pos.getCardinallyAdjacentPositions();
    for (Position p: positions) {
      for (Entity e: map.getEntities(p)) {
        if (e instanceof Wire) {
          Wire w = (Wire)w;
          w.deactivate(map, this, new HashSet<>());
        }
      }
    }
  
}

class Wire extends Entity implements Conductor {
  @Override
  public boolean canMoveOnto(GameMap map, Entity entity) {
    // is boulder considered movable?
    return (entity instanceof Enemy || entity instanceof Player);
  }
}

public abstract class ExplodableEntity extends CollectableEntity {
    public enum State {
        SPAWNED, INVENTORY, PLACED
    }

    public static final int DEFAULT_RADIUS = 1;
    private State state;
    private int radius;

    public Bomb(Position position, int radius) {
        super(position);
        state = State.SPAWNED;
        this.radius = radius;
    }

    @Override
    public boolean collectCheck(Player p) {
        return (state == State.SPAWNED);
    }

    abstract void onPutDown(GameMap map, Position p);

    public void explode(GameMap map) {
        int x = getPosition().getX();
        int y = getPosition().getY();
        for (int i = x - radius; i <= x + radius; i++) {
            for (int j = y - radius; j <= y + radius; j++) {
                List<Entity> entities = map.getEntities(new Position(i, j));
                entities = entities.stream().filter(e -> !(e instanceof Player)).collect(Collectors.toList());
                for (Entity e : entities)
                    map.destroyEntity(e);
            }
        }
    }

    public State getState() {
        return state;
    }
}

class Bomb extends ExplodableEntity {
    //private List<Switch> subs = new ArrayList<>();

    //public void subscribe(Switch s) {
    //    this.subs.add(s);
    //}

    //public void notify(GameMap map) {
    //    explode(map);
    //}

    @Override
    public void postCollect(Player p) {
        subs.stream().forEach(s -> s.unsubscribe(this));
        this.state = State.INVENTORY;
    }

    public void onPutDown(GameMap map, Position p) {
        translate(Position.calculatePositionBetween(getPosition(), p));
        map.addEntity(this);
        this.state = State.PLACED;
        List<Position> adjPosList = getPosition().getCardinallyAdjacentPositions();
        adjPosList.stream().forEach(node -> {
            List<Entity> entities = map.getEntities(node).stream().filter(e -> (e instanceof Switch))
                    .collect(Collectors.toList());
            entities.stream().map(Switch.class::cast).forEach(s -> s.subscribe(this, map));
            entities.stream().map(Switch.class::cast).forEach(s -> this.subscribe(s));
        });
    }
}

class LogicalBomb extends ExplodableEntity implements LogicalEntity {
    @Override
    public void postCollect(Player p) {
        this.state = State.INVENTORY;
    }

    public void onPutDown(GameMap map, Position p) {
        translate(Position.calculatePositionBetween(getPosition(), p));
        map.addEntity(this);
        this.state = State.PLACED;
    }

    private LogicalCondition lc;
    public boolean isLogicallyOn() {
      return lc.condition();
    }
}

- on each tick; chained activation and deactivation
{
  "type": "light_bulb_off/switch_door/bomb",
  "x": 1,
  "y": 1,
  "logic": "and/or/xor/co_and"
}
IMPORTANT: conductor logic first, then logical entities
Game.tick() {
  void updateLightBulbs() {
    for (Entity e: map.getEntities()) {
      if (e instanceof LightBulbOn) {
        LightBulbOn l = (LightBulbOn)e;
        if (!l.isLogicallyOn()) {
          map.destroyEntity(l);
          map.addEntity(new LightBulbOff());
        }
      } else if (e instanceof LightBulbOff) {
  
      } else if (e instanceof LogicBomb) {
        if (b.getState() != INVENTORY && b.isLogicallyOn()) {
          b.explode();
        }
      }
    }
  }

}

GraphNodeFactory.constructEntity() {
  case "light_bulb_off":
  case "wire":
  case "switch_door":

  EntityFactory.constructEntity() {
    case "light_bulb_off":
      String logic = jsonEntity.getString("logic");
      return buildLightBulbOff(pos, logic);
  }
}

default.json:
  "light_bulb_off": "images/tileset/entities/lightbulboff.png",
  "light_bulb_on": "images/tileset/entities/lightbulb.png",
  "wire": "images/tileset/entities/wire.png",
  "switch_door": "images/tileset/entities/door.png",


edit: NameConverter.java?
TODO: look into Customisations.md for task3 actions

--------------------------------------
tests/task2

NOTE: test plan just specify what is considered a unit test, and what is a system test

Task Requirements:
  - Technical
  - Product
  - Assumptions

Design: 
  - What fields/methods you will need to add/change in a class
    * Enemy onDestroy() to count enemies destroyed
    * ZombieToastSpawner interact() to be destroyed on interaction
    * GoalFactory createGoal() to create "enemies" goal
    * Game getNumEnemiesDestroyed() and incNumEnemiesDestroyed()
    +
  - What new classes/packages you will need to create
    * EnemyGoal class 
    + 

Design Review: 
  - Have your partner review the design, and go back and iterate on the design if needed.

Create a Test List: 
  - Once the design is approved, write a test list (a list of all the tests you will write) for the task. 

Test List Review: 
  - Have someone else in your team review the test list to make sure the test cases all make sense and cover the input space.

Create the Skeleton: 
  - Stub out anything you need to with class/method prototypes.

Write the tests: 
  - which should be failing assertions currently since the functionality hasn't been implemented.

Development:
  - Implement the functionality so that your tests pass.
  - Run a usability test (check your functionality works on the frontend).

MR:
  - In most cases, MR should just be able to link to your design/test list blog.
  - Code Review from your partner, iterate where needed then they should approve the MR.














------------------------------------

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

b)
Gamemap.game
GameMap initRegisterSpawners() (double spawn zombie toast for all existing; spawn spider) 
and initRegisterMovables() (all existing enemy movements) on Game class
register to callback for each. so, on each tick, call the observable function
on particular entity removal, unsubscribe()

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

