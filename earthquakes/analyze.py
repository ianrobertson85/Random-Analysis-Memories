#!/usr/bin/env python

def shaperead(file_shape):
    '''Reads data from a shape file and returns some vertices.'''
    import shapefile

    sf = shapefile.Reader(file_shape)
    all_verts = []
    #Grabs all the vertices
    for shape in sf.shapes():
        all_verts.append([(point[0],point[1]) for point in shape.points])       
        identifiers = [rec[2] for rec in sf.records()]
    return (all_verts, identifiers)
