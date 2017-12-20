import os, sys
import vtk
from vtk.util.colors import tomato

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.vtk_adaptor import VtkAdaptor

from tessagon.types import *
from tessagon.misc.shapes import *

lut = None

def main():
  global lut

  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  lut = vtk.vtkLookupTable()
  lut.SetHueRange(0.6, 0.6)
  lut.SetSaturationRange(.5, .5)
  lut.SetValueRange(0.2, 1.0)
  lut.SetNumberOfColors(256)
  lut.Build()

  offset = 15
  row = 0
  column = 0
  # Color patterns
  ren.AddActor(hex_tessagon([column, row, 0]))
  ren.AddActor(hex_tessagon([column, row - offset, 0], color_pattern=1))
  ren.AddActor(hex_tessagon([column, row - 2*offset, 0], color_pattern=2))
  column += offset
  ren.AddActor(tri_tessagon([column, row, 0]))
  ren.AddActor(tri_tessagon([column, row - offset, 0], color_pattern=1))
  ren.AddActor(tri_tessagon([column, row - 2*offset, 0], color_pattern=2))
  ren.AddActor(tri_tessagon([column, row - 3*offset, 0], color_pattern=3))
  column += offset
  ren.AddActor(dissected_square_tessagon([column, row, 0]))
  ren.AddActor(dissected_square_tessagon([column, row - offset, 0],
                                         color_pattern=1))
  ren.AddActor(dissected_square_tessagon([column, row - 2*offset, 0],
                                         color_pattern=2))
  column += offset
  ren.AddActor(floret_tessagon([column, row, 0]))
  ren.AddActor(floret_tessagon([column, row - offset, 0],
                               color_pattern=1))
  ren.AddActor(floret_tessagon([column, row - 2*offset, 0],
                               color_pattern=2))
  ren.AddActor(floret_tessagon([column, row - 3*offset, 0],
                               color_pattern=3))
  column += offset
  column += offset
  start_column = column

  # Row 1
  ren.AddActor(rhombus_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(octo_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(hex_tri_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(hex_square_tri_tessagon([column, row, 0]))

  column = start_column
  row -= offset
  # Row 2
  ren.AddActor(square_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(pythagorean_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(brick_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(dodeca_tessagon([column, row, 0]))

  column = start_column
  row -= offset
  # Row 3
  ren.AddActor(square_tri_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(weave_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(hex_big_tri_tessagon([column, row, 0]))
  column += offset
  ren.AddActor(zig_zag_tessagon([column, row, 0]))

  ren.SetBackground(0.3, 0.3, 0.3)
  renWin.SetSize(800, 600)
  iren.Initialize()
  ren.ResetCamera()
  renWin.Render()
  iren.Start()

def tessellate(f, tessagon_class, **kwargs):
  global lut

  extra_args = {'function': f,
                'adaptor_class' : VtkAdaptor}
  tessagon = tessagon_class(**{**kwargs, **extra_args})

  poly_data = tessagon.create_mesh()
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(poly_data)
  mapper.SetLookupTable(lut)
  mapper.SetScalarRange(poly_data.GetScalarRange())

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().SetColor(tomato)
  actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)
  actor.GetProperty().EdgeVisibilityOn()
  actor.SetPosition(kwargs['position'])

  return actor

def rotated_cylinder(u,v):
  (x, y, z) = cylinder(u, v)
  return [x, z, y]

def hex_tessagon(position, **kwargs):

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 3,
    'u_cyclic': True,
    'v_cyclic': False,
    'position': position
  }
  return tessellate(rotated_cylinder, HexTessagon, **{**kwargs, **options})

def tri_tessagon(position, **kwargs):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 36,
    'v_num': 12,
    'position': position
  }
  return tessellate(torus, TriTessagon, **{**kwargs, **options})

def rhombus_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6,
    'v_twist': True,
    'position': position
  }
  return tessellate(klein, RhombusTessagon, **options)

def octo_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 4,
    'v_num': 40,
    'v_cyclic': True,
    'u_cyclic': False,
    'u_twist': True,
    'position': position
  }
  return tessellate(mobius, OctoTessagon, **options)

def hex_tri_tessagon(position):
  options = {
    'u_range': [-1.0, 1.0],
    'v_range': [-1.0, 1.0],
    'u_num': 15,
    'v_num': 10,
    'u_cyclic': False,
    'v_cyclic': False,
    'position': position
  }
  return tessellate(paraboloid, HexTriTessagon, **options)

def hex_square_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 5,
    'position': position
  }
  return tessellate(torus, HexSquareTriTessagon, **options)

def square_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 4,
    'rot_factor': 2,
    'position': position
  }
  return tessellate(torus, SquareTessagon, **options)

def pythagorean_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 6,
    'position': position
  }
  return tessellate(torus, PythagoreanTessagon, **options)

def brick_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 3,
    'rot_factor': 3,
    'position': position
  }
  return tessellate(torus, BrickTessagon, **options)

def dodeca_tessagon(position):
  options = {
    'u_range': [-1.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 4,
    'v_num': 10,
    'u_cyclic': False,
    'v_cyclic': True,
    'position': position
  }
  return tessellate(one_sheet_hyperboloid, DodecaTessagon, **options)

def square_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 20,
    'v_num': 4,
    'position': position
  }
  return tessellate(torus, SquareTriTessagon, **options)

def weave_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 6,
    'v_cyclic': False,
    'rot_factor': 1,
    'position': position
  }
  return tessellate(sphere, WeaveTessagon, **options)

def floret_torus(u, v):
  # u_cyclic = True, v_cyclic = True
  r1 = 5.0
  r2 = 1.5
  return general_torus(r1, r2, v, warp_var(u, 0.2))

def floret_tessagon(position, **kwargs):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 2,
    'v_num': 12,
    'position': position
  }
  return tessellate(floret_torus, FloretTessagon, **{**kwargs, **options})

def hex_big_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 5,
    'v_num': 2,
    'position': position
  }
  return tessellate(torus, HexBigTriTessagon, **options)

def zig_zag_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 10,
    'v_num': 2,
    'rot_factor': 2,
    'position': position
  }
  return tessellate(torus, ZigZagTessagon, **options)

def dissected_square_tessagon(position, **kwargs):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 32,
    'v_num': 4,
    'u_cyclic': True,
    'v_cyclic': False,
    'position': position
  }
  return tessellate(rotated_cylinder, DissectedSquareTessagon,
                    **{**kwargs, **options})
main()
