# IK-FK Matcher
Blender addon to handle IK-FK matching for custom rigs. Configuration is stored as a custom property directly on the armature, so it persists in the Blender file and rigs with an IK-FK switch can easily be shared. Some code (the math behind positioning the IK pole target) was referenced from [Byron Mallett's IK-FK Snapping addon](https://github.com/Mystfit/IK-FK-Snapping-for-Blender).

## Features
* Snap FK upper, lower, and end point bones to IK
* Snap IK end point and pole target to FK
* Switches bone collection visibility so that you can instantly hide your FK or IK bones whenever switching modes
* Automatically keyframes the location and rotation of FK and IK bones (and correctly recognises if the bone is set to quaternion, euler angle, or axis angle)
* Automatically toggles the IK constraint (and any other constraints, like copy rotation) on the FK end point

## Requirements
* Blender 4.0+ (Currently only supports bone collections, which were introduced in Blender 4.0. If I get around to it I'll try to support older versions of Blender with the old layer system)

## Download
Download .zip [here](https://github.com/squiddingme/IKFKMatcher/archive/refs/heads/master.zip) and install from Blender add-ons menu (Edit -> Preferences -> Add-ons -> Install)

## License
This work is licensed under the terms of the MIT license.