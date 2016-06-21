import Arch, Draft, Drawing

# Storing all objects (i.e parts of building like column, beams and slabs)
# in obj_list
obj_list = FreeCAD.ActiveDocument.Objects

# Adding object 'Compound' in active document. The Compound object stores
# all parts of the building
App.activeDocument().addObject("Part::Compound","Compound")

# Links all the objects present in obj_list to Compound
App.activeDocument().Compound.Links = obj_list

# Adding the object 'Page' in active document
App.ActiveDocument.addObject('Drawing::FeaturePage','Page')

# Choose the specific template
App.ActiveDocument.Page.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_Landscape.svg'

########################################################################
#
# This class stores all the information which is require to draw the
# drawing of different objects on the drawing sheet.
#
# name: It represent the name of the view.
#
# obj: It store the name of the object which can be draw on drawing sheet
#
# x_dir y_dir z_dir: These are the axis like (x_dir, y_dir, z_dir) from
# which point source can see the object.
#
# x_pos y_pos: It represents position of the drawing to be drawn on a
# drawing sheet.
#
# hid_lines: If it is 'True' then all hidden lines is drawn on the drawing
# sheet.
#
# scale_size: It represent the size to be draw on the drawing sheet.
#
# rotation: If it is 90 then the view on the drawing sheet is rotate
# 90 degree.
#
########################################################################
class obj_view_specs:
    # Declaring a constructor
    def __init__(self, name, obj, x_dir, y_dir, z_dir, x_pos, y_pos, hid_lines,
            scale_size, rotation):
        self.name = name
        self.obj = obj
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.z_dir = z_dir
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.hid_lines = hid_lines
        self.scale_size = scale_size
        self.rotation = rotation

########################################################################
#
# The draw function projects the projections of the object on the
# drawing sheet. It takes the object of 'view_Specs' as argument, which
# stores all the detail which are require to draw the drawing of the
# object on the drawing sheet.
#
########################################################################
def draw_obj_view(view, page_name):
    # Add the object in the active document of specific name
    App.ActiveDocument.addObject('Drawing::FeatureViewPart',view.name)
    # view_ref stores the object having name view.name
    view_ref = App.ActiveDocument.getObject(view.name)
    # obj_ref stores the object having name view.obj
    obj_ref = App.ActiveDocument.getObject(view.obj)
    view_ref.Source = obj_ref
    view_ref.Direction = (view.x_dir, view.y_dir, view.z_dir)
    view_ref.X = view.x_pos
    view_ref.Y = view.y_pos
    view_ref.ShowHiddenLines = view.hid_lines
    view_ref.Scale = view.scale_size
    view_ref.Rotation = view.rotation
    page_ref = App.ActiveDocument.getObject(page_name)
    page_ref.addObject(view_ref)
    App.ActiveDocument.recompute()

########################################################################
#
# This class stores all information which will require to draw the
# sectional view of the object at any angle and at any position.
#
# obj: It store the name of the object which can be draw on drawing sheet
#
# x_dir, y_dir, z_dir: It represent the position of the sectional plane
#
# axis_x, axis_y, axis_z: It represent the axis of the sectional plane
#
# angle2axis: Represent the angle of the sectional plane to the axis
#
# x_pos y_pos: It represents position of the drawing to be drawn on a
# drawing sheet.
#
# scale_size: It represent the size to be draw on the drawing sheet.
#
# rotation: If it is 90 then the view on the drawing sheet is rotate
# 90 degree.
#
#######################################################################

class section_view_specs:
    def __init__(self, obj, x_dir, y_dir, z_dir, axis_x, axis_y, axis_z,
            angle2axis, x_pos, y_pos, scale, rotation):
        self.obj = obj
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.z_dir = z_dir
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.axis_z = axis_z
        self.angle2axis = angle2axis
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.scale = scale
        self.rotation = rotation

def draw_section_view(view, page_name):
    obj_ref = App.ActiveDocument.getObject(view.obj)
    view_ref = Arch.makeSectionPlane([obj_ref])
    view_ref.Placement = App.Placement(App.Vector(view.x_dir, view.y_dir,
        view.z_dir), App.Rotation(App.Vector(view.axis_x, view.axis_y,
            view.axis_z), view.angle2axis))
    Draft.makeShape2DView(view_ref)
    page_ref = App.ActiveDocument.getObject(page_name)
    draw_ref = Draft.makeDrawingView(view_ref, page_ref)
    draw_ref.X = view.x_pos
    draw_ref.Y = view.y_pos
    draw_ref.Scale = view.scale
    draw_ref.Rotation = view.rotation
    App.ActiveDocument.recompute()

view = obj_view_specs("view", "Compound", 0, 0, 1, 30, 100, False, 2, 0)
draw_obj_view(view, "Page")

viewIso = obj_view_specs("viewIso", "Compound", 1, 1, 1, 335, 60, True, 2, 120)
draw_obj_view(viewIso, "Page")

sec_obj = section_view_specs("Compound", 10, 0, 0, 0, 0, 1, 0, 50, 200, 2, 0)
draw_section_view(sec_obj, "Page")

#sec_obj2 = section_view_specs("Compound", 10 , 10, 10, 1, 0, 1, 30, 100, 300, 2, 0)
#draw_section_view(sec_obj2, "Page")
