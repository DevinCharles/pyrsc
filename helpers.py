def sortby(items, key, *args,**kwargs):
    """Sort body(ies), face(s), edge(s), point(s) by "key" where "key" is:
        - Volume
        - Area
        - Length
        - Distance (give 2 or 3 coords)
        - Coordinate (X,Y, or Z)
        
    """
    output = []
    if not isinstance(items,list):
        try:
            items = list(item)
        except:
            print('Input should be iterable')
            raise()
    
    for n,item in enumerate(items):
        if ('dist' in key.lower()):
            ## Two points to find distance
            dist = lambda x,y,z=[0,0]: ((x[1]-x[0])**2 + (y[1]-y[0])**2 + (z[1]-z[0])**2)**0.5
            # item is iterable of two Points
            try: 
                if len(item)==2:
                    x,y,z = zip(*item)
                    output.append((dist(x,y,z),item[0],n))
                else:
                    print('Input should be nested lists of two points, or a list of points with a reference point listed in the input arguements')
                    raise()
            except:
                # single reference point given
                x,y,z = zip(item,args[0])
                output.append((dist(x,y,z),item,n))
        if isinstance(item, DesignBody):
            output.append([])
        elif isinstance(item, DesignFace):
            output.append([])
        elif isinstance(item, DesignEdge):
            output.append([])
            
        elif isinstance(item, Point):
            ## Point to sort by Coordinate
            if key in [0,'x']:
                output.append((item[0],item,n))
            elif key in [1,'y']:
                output.append((item[1],item,n))
            elif key in [2,'z']:
                output.append((item[2],item,n))
                
    if 'keys' in args:
        return [x[0] for x in sorted(output)]
    elif 'index' in args:
        return [x[2] for x in sorted(output)]
    else:
        return [x[1] for x in sorted(output)]

def midpoint(item):
    """Find the midpoint of a body(ies), face(s), edge(s).
    
    Examples:
    >>> bodies = GetActivePart().GetAllBodies()
    >>> midpoint(bodies)
    Returns a list of midpoints for all bodies in active part
    
    >>> midpoint(bodies[0].Faces)
    Returns a list of midpoints for all faces in body
    
    >>> midpoint(bodies[0].Edges[0])
    Returns a <type 'Point'> for edge
    """
    output = []
    try:
        items = list(item)
    except:
        items = [item]
    for item in items:
        if 'DesignBody' in str(type(item)):
            output.append(item.MassProperties.PrincipleAxes.Origin)
        elif 'DesignFace' in str(type(item)):
            output.append(item.MidPoint().Point)
        elif 'DesignEdge' in str(type(item)):
            output.append(item.GetMidPoint().Point)
            
    if len(output)==1:
        return output[0]
    else:
        return output