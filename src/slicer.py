import bpy, os, bmesh, numpy

def slicer(settings):
  dp = bpy.context.evaluated_depsgraph_get()
  f_scale = 1000 * bpy.context.scene.unit_settings.scale_length
  aob = bpy.context.active_object
  bm = bmesh.new()
  tempmesh = aob.evaluated_get(dp).to_mesh()
  bm.from_mesh(tempmesh)
  omw = aob.matrix_world
  bm.transform(omw)
  aob.evaluated_get(dp).to_mesh_clear()
  aob.select_set(False)
  mwidth = settings.material_width
  mheight = settings.material_height
  lt = settings.material_thickness/f_scale
  sepfile = settings.separate_files
  minz = min([v.co[2] for v in bm.verts])
  maxz = max([v.co[2] for v in bm.verts])
  lh = minz + lt * 0.5
  preview = settings.preview
  ct = settings.cut_thickness/f_scale
  svgpos = settings.svg_position
  dpi = settings.dpi
  yrowpos = 0
  xmaxlast = 0
  ofile = settings.ofile
  mm2pi = dpi/25.4
  scale = f_scale*mm2pi
  ydiff, rysize  = 0, 0
  lcol = settings.cut_line_color
  lthick = settings.cut_line_thickness

  if not any([o.get('Slices') for o in bpy.context.scene.objects]):
    me = bpy.data.meshes.new('Slices')
    cob = bpy.data.objects.new('Slices', me)
    cob['Slices'] = 1
    cobexists = 0
  else:
    for o in bpy.context.scene.objects:
      if o.get('Slices'):
        bpy.context.view_layer.objects.active = o

        for vert in o.data.vertices:
          vert.select = True

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.delete(type = 'VERT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        me = o.data
        cob = o
        cobexists = 1
        break

  vlen, elen, vlenlist, elenlist = 0, 0, [0], [0]
  vpos = numpy.empty(0)
  vindex = numpy.empty(0).astype(numpy.int8)
  vtlist = []
  etlist = []
  vlist = []
  elist = []
  erem = []

  while lh < maxz:
    cbm = bm.copy()
    newgeo = bmesh.ops.bisect_plane(cbm, geom = cbm.edges[:] + cbm.faces[:], dist = 0, plane_co = (0.0, 0.0, lh), plane_no = (0.0, 0.0, 1), clear_outer = False, clear_inner = False)['geom_cut']
    newverts = [v for v in newgeo if isinstance(v, bmesh.types.BMVert)]
    newedges = [e for e in newgeo if isinstance(e, bmesh.types.BMEdge)]
    voffset = min([v.index for v in newverts])
    lvpos = [v.co for v in newverts]
    vpos = numpy.append(vpos, numpy.array(lvpos).flatten())
    vtlist.append([(v.co - cob.location)[0:2] for v in newverts])
    etlist.append([[(v.co - cob.location)[0:2] for v in e.verts] for e in newedges])
    vindex = numpy.append(vindex, numpy.array([[v.index  - voffset + vlen for v in e.verts] for e in newedges]).flatten())
    vlen += len(newverts)
    elen += len(newedges)
    vlenlist.append(len(newverts) + vlenlist[-1])
    elenlist.append(len(newedges) + elenlist[-1])
    lh += lt
    cbm.free()

  bm.free()
  vs = []
  me.vertices.add(vlen)
  me.vertices.foreach_set('co', vpos)
  me.edges.add(elen)
  me.edges.foreach_get('verts', vs)
  me.edges.foreach_set('vertices', vindex)

  if not preview:
    vranges = [(vlenlist[i], vlenlist[i+1], elenlist[i], elenlist[i+1]) for i in range(len(vlenlist) - 1)]
    vtlist = []
    etlist = []

    for vr in vranges:
      vlist, elist, erem = [], [], []
      sliceedges = me.edges[vr[2]:vr[3]]
      edgeverts = [ed.vertices[0] for ed in sliceedges] + [ed.vertices[1] for ed in sliceedges]
      edgesingleverts = [ev for ev in edgeverts if edgeverts.count(ev) == 1]

      for ed in sliceedges:
        if ed.vertices[0] in [ev for ev in edgeverts if edgeverts.count(ev) > 2] and ed.vertices[1] in [ev for ev in edgeverts if edgeverts.count(ev) > 2]:
          erem.append(ed)
      for er in erem:
        sliceedges.remove(er)

      vlen = len(me.vertices)

      if edgesingleverts:
        e = [ed for ed in sliceedges if ed.vertices[0] in edgesingleverts or ed.vertices[1] in edgesingleverts][0]
        if e.vertices[0] in edgesingleverts:
          vlist.append(e.vertices[0])
          vlist.append(e.vertices[1])
        else:
          vlist.append(e.vertices[1])
          vlist.append(e.vertices[0])
        elist.append(e)
      else:
        elist.append(sliceedges[0]) # Add this edge to the edge list
        vlist.append(elist[0].vertices[0]) # Add the edges vertices to the vertex list
        vlist.append(elist[0].vertices[1])

      while len(elist) < len(sliceedges):
        va = 0
        for e in [ed for ed  in sliceedges if ed not in elist]:
           if e.vertices[0] not in vlist and e.vertices[1] == vlist[-1]: # If a new edge contains the last vertex in the vertex list, add the other edge vertex
             va = 1
             vlist.append(e.vertices[0])
             elist.append(e)

             if len(elist) == len(sliceedges):
              vlist.append(-2)

           if e.vertices[1] not in vlist and e.vertices[0] == vlist[-1]:
             va = 1
             vlist.append(e.vertices[1])
             elist.append(e)

             if len(elist) == len(sliceedges):
              vlist.append(-2)

           elif e.vertices[1] in vlist and e.vertices[0] in vlist and e not in elist: # The last edge already has it's two vertices in the vertex list so just add the edge
             elist.append(e)
             va = 2

        if va in (0, 2):
          vlist.append((-1, -2)[va == 0])

          if len(elist) < len(sliceedges):
            try:
              e1 = [ed for ed in sliceedges if ed not in elist and (ed.vertices[0] in edgesingleverts or ed.vertices[1] in edgesingleverts)][0]
              if e1.vertices[0] in edgesingleverts:
                vlist.append(e1.vertices[0])
                vlist.append(e1.vertices[1])
              else:
                vlist.append(e1.vertices[1])
                vlist.append(e1.vertices[0])

            except Exception as e:
              e1 = [ed for ed in sliceedges if ed not in elist][0]
              vlist.append(e1.vertices[0])
              vlist.append(e1.vertices[1])
            elist.append(e1)

      vtlist.append([(me.vertices[v].co, v)[v < 0]  for v in vlist])
      etlist.append([elist])

  if not sepfile:
    if os.path.isdir(bpy.path.abspath(ofile)):
      filename = os.path.join(bpy.path.abspath(ofile), aob.name+'.svg')
    else:
      filename = os.path.join(os.path.dirname(bpy.data.filepath), aob.name+'.svg') if not ofile else bpy.path.abspath(ofile)
  else:
    if os.path.isdir(bpy.path.abspath(ofile)):
      filenames = [os.path.join(bpy.path.abspath(ofile), aob.name+'{}.svg'.format(i)) for i in range(len(vlenlist))]
    else:
      if not ofile:
        filenames = [os.path.join(os.path.dirname(bpy.path.abspath(bpy.data.filepath)), aob.name+'{}.svg'.format(i)) for i in range(len(vlenlist))]
      else:
        filenames = [os.path.join(os.path.dirname(bpy.path.abspath(ofile)), bpy.path.display_name_from_filepath(ofile) + '{}.svg'.format(i)) for i in range(len(vlenlist))]

  for vci, vclist in enumerate(vtlist):
    if sepfile or vci == 0:
      svgtext = ''

    xmax = max([vc[0] for vc in vclist if vc not in (-1, -2)])
    xmin = min([vc[0] for vc in vclist if vc not in (-1, -2)])
    ymax = max([vc[1] for vc in vclist if vc not in (-1, -2)])
    ymin = min([vc[1] for vc in vclist if vc not in (-1, -2)])
    cysize = ymax - ymin + ct
    cxsize = xmax - xmin + ct

    if (sepfile and svgpos == 'TL') or (sepfile and vci == 0 and svgpos == 'ST'):
      xdiff = -xmin + ct
      ydiff = -ymin + ct

    elif (sepfile and svgpos == 'ST') or not sepfile:
      if f_scale * (xmaxlast + cxsize) <= mwidth:
        xdiff = xmaxlast - xmin + ct
        ydiff = yrowpos - ymin + ct

        if rysize < cysize:
          rysize = cysize

        xmaxlast += cxsize

      elif f_scale * cxsize > mwidth:
        xdiff = -xmin + ct
        ydiff = yrowpos - ymin + ct
        yrowpos += cysize
        if rysize < cysize:
          rysize = cysize

        xmaxlast = cxsize
        rysize = cysize

      else:
        yrowpos += rysize
        xdiff = -xmin + ct
        ydiff = yrowpos - ymin + ct
        xmaxlast = cxsize
        rysize = cysize

    elif sepfile and svgpos == 'CT':
      xdiff = mwidth/(2 * f_scale) - (0.5 * cxsize) - xmin
      ydiff = mheight/(2 * f_scale) - (0.5 * cysize) - ymin

    if preview:
      svgtext += '<g>\n'
      svgtext += "".join(['<line x1="{0[0][0]}" y1="{0[0][1]}" x2="{0[1][0]}" y2="{0[1][1]}" style="stroke:rgb({1[0]},{1[1]},{1[2]});stroke-width:{2}" />\n'.format([(scale * (xdiff + v[0]), scale * (ydiff + v[1])) for v in e], [int(255 * lc) for lc in lcol], lthick) for e in etlist[vci]])
      svgtext += '</g>\n'
    else:
      points = "{:.4f},{:.4f} {:.4f},{:.4f} ".format(scale*(xdiff+vclist[0][0]), scale*(ydiff+vclist[0][1]), scale*(xdiff+vclist[1][0]), scale*(ydiff+vclist[1][1]))
      svgtext += '<g>\n'

      for vco in vclist[2:]:
        if vco in (-1, -2):
          polyend = 'gon' if vco == -1 else 'line'
          svgtext += '<poly{0} points="{1}" style="fill:none;stroke:rgb({2[0]},{2[1]},{2[2]});stroke-width:{3}" />\n'.format(polyend, points, [int(255 * lc) for lc in lcol], lthick)
          points = ''
        else:
          points += "{:.4f},{:.4f} ".format(scale*(xdiff+vco[0]), scale*(ydiff+vco[1]))

      if points:
        svgtext += '<polygon points="{0}" style="fill:none;stroke:rgb({1[0]},{1[1]},{1[2]});stroke-width:{2}" />\n'.format(points, [int(255 * lc) for lc in lcol], lthick)

      svgtext += '</g>\n'

    if sepfile:
      svgtext += '</svg>\n'

      with open(filenames[vci], 'w') as svgfile:
        svgfile.write('<?xml version="1.0"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n\
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1"\n  width="{0}"\n  height="{1}"\n  viewbox="0 0 {0} {1}">\n\
        <desc>Laser SVG Slices from Object: Sphere_net. Exported from Blender3D with the Laser Slicer Script</desc>\n\n'.format(mwidth*mm2pi, mheight*mm2pi))

        svgfile.write(svgtext)

  if not sepfile:

    with open(filename, 'w') as svgfile:
      svgfile.write('<?xml version="1.0"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n\
        <svg xmlns="http://www.w3.org/2000/svg" version="1.1"\n  width="{0}"\n  height="{1}"\n  viewbox="0 0 {0} {1}">\n\
        <desc>Laser SVG Slices from Object: Sphere_net. Exported from Blender3D with the Laser Slicer Script</desc>\n\n'.format(mwidth*mm2pi, mheight*mm2pi))

      svgfile.write(svgtext)
      svgfile.write("</svg>\n")

  if not cobexists:
    bpy.context.scene.collection.objects.link(cob)

  bpy.context.view_layer.objects.active = cob
  bpy.ops.object.mode_set(mode = 'EDIT')
  bpy.ops.object.mode_set(mode = 'OBJECT')
  aob.select_set(True)
  bpy.context.view_layer.objects.active = aob
