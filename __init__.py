bl_info = {
    "name": "IK/FK Matcher",
    "blender": (2, 80, 0),
    "category": "Object",
}

if "bpy" in locals():
    from importlib import reload
    if "ik_fk_matcher" in locals():
        reload(ik_fk_matcher)
else:
    from .ik_fk_matcher import *

import bpy

classes = (
    MatcherPanel,
    MatcherFKIKSettings,
    MatcherSettings,
    MatcherAddConfig,
    MatcherRemoveConfig,
    MatcherFKSnap,
    MatcherIKSnap
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.matcher_fkik_settings = bpy.props.PointerProperty(type = MatcherFKIKSettings)
    bpy.types.Object.matcher_settings = bpy.props.PointerProperty(type = MatcherSettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.matcher_fkik_settings
    del bpy.types.Object.matcher_settings

if __name__ == "__main__":
    register()