# GameMaker Language (GML) Development: implementation guidance

## Events and state machines

Initialize state in Create, simulate in appropriate Step events, and draw without
unrelated gameplay mutation. The upstream state machine jumps whenever the player
leaves the ground (even falling), keeps prior hspeed when entering idle, and combines
built-in hspeed/vspeed automatic movement with move_and_collide. Choose one explicit
movement model, clear/reset velocity as required, distinguish jump from fall, and
test against ground/collision geometry. Stable state IDs and input intents help
separate control from gameplay. Instance references can become invalid; check them
at use and handle persistent-instance/room ownership explicitly.

## Resources, persistence, and performance

Use the Clean Up event for owned dynamic resources when an instance is removed;
Destroy alone does not cover all room/end removal paths. Avoid double freeing in
multiple events. DS maps/lists/grids, buffers, surfaces and other handles have their
own cleanup/lifetime rules, while structs/arrays use managed semantics. Surfaces
can be lost and need existence/recreation checks. Deactivating an instance does
not automatically reset it for pooling. Version save data and verify migration.
Use profiler evidence for broad searches/allocation cost; test target compiler,
room transitions and input/controller behavior rather than assuming editor parity.

## Primary documentation

- [Clean Up and Destroy event lifetime](https://manual.gamemaker.io/lts/en/The_Asset_Editors/Object_Properties/Object_Events.htm).
- [Explicit movement/collision API](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Movement_And_Collisions/Movement/move_and_collide.htm).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
