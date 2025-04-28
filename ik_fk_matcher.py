import bpy
from mathutils import Matrix, Vector

class MatcherPanel(bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_matcher'
    bl_label = 'FK/IK Matching'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Matcher'

    @classmethod
    def poll(cls, context):
        return context.object.mode == 'POSE'

    def draw(self, context):
        if bpy.context.object.type == 'ARMATURE':
            layout = self.layout

            layout.label(text = bpy.context.object.name, icon = 'ARMATURE_DATA')
            layout.separator()
            layout.operator(MatcherAddConfig.bl_idname, text = MatcherAddConfig.bl_label)
            layout.separator()

            matcher_settings = bpy.context.object.matcher_settings
            layout.prop(matcher_settings, 'auto_key')
            layout.prop(matcher_settings, 'auto_constraint')
            layout.separator()

            for index, settings in enumerate(matcher_settings.entries):
                entry = layout.row()
                box = entry.box()

                row = box.row()
                row.label(text = settings.name, icon = 'CONSTRAINT_BONE')
                operator = row.operator(MatcherRemoveConfig.bl_idname, text = '', icon = MatcherRemoveConfig.bl_icon)
                operator.index = index

                row = box.row()
                column = row.column()
                column.enabled = not settings.fk_upper == '' and not settings.fk_lower == '' and not settings.fk_end == '' and not settings.ik_upper == '' and not settings.ik_lower == '' and not settings.ik_end == ''
                operator = column.operator(MatcherFKSnap.bl_idname, text = MatcherFKSnap.bl_label, icon = MatcherFKSnap.bl_icon)
                operator.index = index
                column = row.column()
                column.enabled = not settings.fk_upper == '' and not settings.fk_lower == '' and not settings.fk_end == '' and not settings.ik_pole == '' and not settings.ik_end == ''
                operator = column.operator(MatcherIKSnap.bl_idname, text = MatcherIKSnap.bl_label, icon = MatcherIKSnap.bl_icon)
                operator.index = index

                row = box.row()
                row.prop(settings, 'expanded',
                    icon='TRIA_DOWN' if settings.expanded else 'TRIA_RIGHT',
                    icon_only=True, emboss=False
                )
                row.label(text = 'Configuration')

                if settings.expanded:
                    sub_box = box.box()
                    row = sub_box.row()

                    row.prop(settings, 'name')

                    row = sub_box.row()
                    row.separator()

                    row = sub_box.row()
                    row.prop_search(settings, 'fk_upper', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'fk_lower', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'fk_end', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'fk_layer', bpy.context.object.data, 'collections')

                    row = sub_box.row()
                    row.separator()

                    row = sub_box.row()
                    row.prop_search(settings, 'ik_upper', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_lower', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_pole', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_end', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_layer', bpy.context.object.data, 'collections')

class MatcherFKIKSettings(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = 'Name')
    expanded: bpy.props.BoolProperty(name = 'Expanded')
    fk_upper: bpy.props.StringProperty(name = 'FK Upper')
    fk_lower: bpy.props.StringProperty(name = 'FK Lower')
    fk_end: bpy.props.StringProperty(name = 'FK End Point')
    fk_layer: bpy.props.StringProperty(name = 'FK Bone Collection')
    ik_upper: bpy.props.StringProperty(name = 'IK Upper')
    ik_lower: bpy.props.StringProperty(name = 'IK Lower')
    ik_pole: bpy.props.StringProperty(name = 'IK Pole Target')
    ik_end: bpy.props.StringProperty(name = 'IK End Point')
    ik_layer: bpy.props.StringProperty(name = 'IK Bone Collection')

class MatcherSettings(bpy.types.PropertyGroup):
    entries: bpy.props.CollectionProperty(type = MatcherFKIKSettings)
    auto_key: bpy.props.BoolProperty(name = 'Auto Keyframe', default = True)
    auto_constraint: bpy.props.BoolProperty(name = 'Auto Constraint Influence', default = True)

class MatcherAddConfig(bpy.types.Operator):
    bl_idname = 'matcher.add_config'
    bl_label = 'New FK-IK Pair'
    bl_options = { 'INTERNAL', 'UNDO' }

    @classmethod
    def poll(cls, context):
        if bpy.context.object.type is not None:
            return bpy.context.object.type == 'ARMATURE'
        else:
            return false

    def execute(self, context):
        if bpy.context.object.type == 'ARMATURE':
            matcher_settings = bpy.context.object.matcher_settings
            fkik_settings = matcher_settings.entries.add()
            fkik_settings.name = 'New FK-IK Configuration'
            fkik_settings.expanded = True

        return { 'FINISHED' }

class MatcherRemoveConfig(bpy.types.Operator):
    bl_idname = 'matcher.remove_config'
    bl_label = 'Remove'
    bl_icon = 'PANEL_CLOSE'
    bl_options = { 'INTERNAL', 'UNDO' }

    index: bpy.props.IntProperty(default = 0)

    @classmethod
    def poll(cls, context):
        if bpy.context.object.type is not None:
            return bpy.context.object.type == 'ARMATURE'
        else:
            return false

    def execute(self, context):
        if bpy.context.object.type == 'ARMATURE':
            matcher_settings = bpy.context.object.matcher_settings
            matcher_settings.entries.remove(self.index)

        return { 'FINISHED' }

class MatcherFKSnap(bpy.types.Operator):
    bl_idname = 'matcher.fksnap'
    bl_label = 'FK'
    bl_icon = 'BONE_DATA'
    bl_options = { 'INTERNAL', 'UNDO' }

    index: bpy.props.IntProperty(default = 0)

    @classmethod
    def poll(cls, context):
        if bpy.context.object.type is not None:
            return bpy.context.object.type == 'ARMATURE'
        else:
            return false

    def execute(self, context):
        if bpy.context.object.type == 'ARMATURE':
            matcher_settings = bpy.context.object.matcher_settings
            settings = bpy.context.object.matcher_settings.entries[self.index]
            bones = bpy.context.object.pose.bones
            collections = bpy.context.object.data.collections

            # reference: Byron Mallett's IK/FK Snapping addon

            fk_upper = bones[settings.fk_upper]
            ik_upper = bones[settings.ik_upper]
            fk_upper.matrix = ik_upper.matrix

            fk_lower = bones[settings.fk_lower]
            ik_lower = bones[settings.ik_lower]
            fk_lower.matrix = ik_lower.matrix

            fk_end = bones[settings.fk_end]
            ik_end = bones[settings.ik_end]
            fk_relative_to_ik = ik_end.bone.matrix_local.inverted() @ fk_end.bone.matrix_local
            fk_end.matrix = ik_end.matrix @ fk_relative_to_ik

            if not settings.fk_layer == '':
                collections[settings.fk_layer].is_visible = True

            if not settings.ik_layer == '':
                collections[settings.ik_layer].is_visible = False

            if matcher_settings.auto_key:
                frame = bpy.context.scene.frame_current
                # todo: detect if quaternion or euler angles are specified
                fk_upper.keyframe_insert('rotation_quaternion', frame = frame)
                fk_lower.keyframe_insert('rotation_quaternion', frame = frame)
                fk_end.keyframe_insert('rotation_quaternion', frame = frame)

            if matcher_settings.auto_constraint:
                frame = bpy.context.scene.frame_current
                for constraint in fk_end.constraints:
                    constraint.influence = 0.0
                    if matcher_settings.auto_key:
                        constraint.keyframe_insert('influence', frame = frame)

            bpy.context.view_layer.update()

        return { 'FINISHED' }

class MatcherIKSnap(bpy.types.Operator):
    bl_idname = 'matcher.iksnap'
    bl_label = 'IK'
    bl_icon = 'BONE_DATA'
    bl_options = { 'INTERNAL', 'UNDO' }

    index: bpy.props.IntProperty(default = 0)

    @classmethod
    def poll(cls, context):
        if bpy.context.object.type is not None:
            return bpy.context.object.type == 'ARMATURE'
        else:
            return false

    def execute(self, context):
        if bpy.context.object.type == 'ARMATURE':
            matcher_settings = bpy.context.object.matcher_settings
            settings = bpy.context.object.matcher_settings.entries[self.index]
            bones = bpy.context.object.pose.bones
            collections = bpy.context.object.data.collections

            # reference: Byron Mallett's IK/FK Snapping addon

            fk_end = bones[settings.fk_end]
            ik_end = bones[settings.ik_end]
            ik_relative_to_fk = fk_end.bone.matrix_local.inverted() @ ik_end.bone.matrix_local
            ik_end.matrix = fk_end.matrix @ ik_relative_to_fk

            fk_upper = bones[settings.fk_upper]
            fk_lower = bones[settings.fk_lower]
            pv_normal = ((fk_lower.vector.normalized() + fk_upper.vector.normalized() * -1)).normalized()

            ik_pole = bones[settings.ik_pole]
            pv_matrix_loc = fk_lower.matrix.to_translation() + (pv_normal * -0.2)
            pv_matrix = Matrix.LocRotScale(pv_matrix_loc, ik_pole.matrix.to_quaternion(), None)
            ik_pole.matrix = pv_matrix

            if not settings.fk_layer == '':
                collections[settings.fk_layer].is_visible = False

            if not settings.ik_layer == '':
                collections[settings.ik_layer].is_visible = True

            if matcher_settings.auto_key:
                frame = bpy.context.scene.frame_current
                ik_end.keyframe_insert('location', frame = frame)
                # todo: detect if quaternion or euler angles are specified
                ik_end.keyframe_insert('rotation_quaternion', frame = frame)
                ik_pole.keyframe_insert('location', frame = frame)

            if matcher_settings.auto_constraint:
                frame = bpy.context.scene.frame_current
                for constraint in fk_end.constraints:
                    constraint.influence = 1.0
                    if matcher_settings.auto_key:
                        constraint.keyframe_insert('influence', frame = frame)

            bpy.context.view_layer.update()

        return { 'FINISHED' }