---
name: ros2-robotics
description: "Use when implementing ROS 2 packages, nodes, interfaces, QoS, frames, launch configuration, or colcon tests."
---

# ROS 2 package and node development

## When to invoke

Use when implementing ROS 2 packages, nodes, interfaces, QoS, frames, launch configuration, or colcon tests.
Keep the requested change within the repository's conventions and authority.

## Inputs and evidence

Inspect ROS distribution, build types, rclpy/rclcpp APIs, topic/service/action contracts, frames, units, and simulation/hardware boundaries.
Inspect installed versions, existing implementation, project instructions,
and available checks before selecting APIs or changing dependencies.

## Workflow

1. Choose topics, services, or actions from communication and cancellation requirements.
2. Implement declared parameters, supported interface generation, launch composition, and intentional QoS.
3. Build/test in the ROS environment, then verify time, transforms, delivery, and failure behavior in simulation.

Read [implementation decisions](references/patterns.md) only for the relevant
API, configuration, or failure-handling detail. Consult primary documentation
for the project's installed major version before adapting an example.

## Outputs and handoff

Deliver the scoped implementation or review with changed behavior, relevant
configuration, verification results, and remaining runtime or version limits.

## Completion evidence

Build packages, run colcon tests, verify QoS/time/frame failures in simulation, and identify any unperformed hardware acceptance.
Report actual check outcomes; distinguish static review from executed behavior.

## Must not

Do not replace project conventions with arbitrary style preferences, expose
secrets, or introduce dependencies without a task need. Do not publish, deploy,
modify external resources, or run destructive commands without user authority.
Do not issue actuator commands or modify a robot’s live control configuration under documentation-review authority.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../NOTICE.md).
