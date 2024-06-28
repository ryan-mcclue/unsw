<!-- SPDX-License-Identifier: zlib-acknowledgement -->

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

a) movement code to strategy?
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

