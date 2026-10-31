# ROS 2 package and node development: implementation decisions

Load this reference when implementing the relevant patterns; select the subset
that matches the installed framework, target, and requested behavior.

- Use ament_python for Python node packages and ament_cmake where appropriate; interface generation uses rosidl/CMake, commonly in a separate ament_cmake interface package. Merely adding msg files to ament_python is insufficient.

- Prefer established message types when they fit, and document units, frame_id, timestamps, topic names, and parameters.

- Validate rate_hz as positive and speed bounds as finite/nonnegative before constructing a timer or clamping commands.

- QoS compatibility is request/offered based; choose reliability, durability, history, and deadlines for actual delivery requirements.

- Use ROS time and use_sim_time for simulation/replay; resolve transforms with tf2 and handle stale/missing transforms.

- A MultiThreadedExecutor alone does not make mutually exclusive callbacks concurrent; callback groups and blocking dependencies also matter.

- Velocity clamping does not prove actuator safety. Keep hardware actuation behind explicit authorization, bounded command freshness, and the project’s control safeguards.

- Use colcon build/test and inspect test results; simulation or bag replay establishes different evidence from physical robot behavior.

## Primary documentation

These sources informed the 2026-10-31 conversion. Recheck version-specific APIs
when applying this skill; documentation review does not prove runtime acceptance.

- [ROS interfaces are generated through rosidl with CMake integration.](https://github.com/ros2/rosidl)

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
