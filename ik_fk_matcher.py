import bpy

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
            self.layout.label(text = bpy.context.object.name, icon = 'ARMATURE_DATA')
            self.layout.separator()
            self.layout.operator(MatcherAddConfig.bl_idname, text = MatcherAddConfig.bl_label)
            self.layout.separator()

            matcher_settings = bpy.context.object.matcher_settings
            for index, settings in enumerate(matcher_settings.entries):
                entry = self.layout.row()
                box = entry.box()

                row = box.row()
                row.label(text = settings.name, icon = 'CONSTRAINT_BONE')
                operator = row.operator(MatcherRemoveConfig.bl_idname, text = '', icon = MatcherRemoveConfig.bl_icon)
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
                    row.separator()

                    row = sub_box.row()
                    row.prop_search(settings, 'ik_upper', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_lower', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_pole', bpy.context.object.data, 'bones')
                    row = sub_box.row()
                    row.prop_search(settings, 'ik_end', bpy.context.object.data, 'bones')

class MatcherFKIKSettings(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = 'Name')
    expanded: bpy.props.BoolProperty(name = 'Expanded')
    fk_upper: bpy.props.StringProperty(name = 'FK Upper')
    fk_lower: bpy.props.StringProperty(name = 'FK Lower')
    fk_end: bpy.props.StringProperty(name = 'FK End Point')
    ik_upper: bpy.props.StringProperty(name = 'IK Upper')
    ik_lower: bpy.props.StringProperty(name = 'IK Lower')
    ik_pole: bpy.props.StringProperty(name = 'FK Pole Target')
    ik_end: bpy.props.StringProperty(name = 'FK End Point')

class MatcherSettings(bpy.types.PropertyGroup):
    entries: bpy.props.CollectionProperty(type = MatcherFKIKSettings)

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

    index : bpy.props.IntProperty(default = 0)

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