import numpy as np
import scipy
from shapely.geometry import Polygon, LineString, Point
from scipy import spatial 

class myVoronoi(scipy.spatial.Voronoi): 
    def __init__(self, points, window, furthest_site=False, incremental=False, qhull_options=None):
        super().__init__(points, furthest_site, incremental, qhull_options)
        oldregions=self.regions
    
        points=self.points
        vertices=self.vertices
        regions=self.regions
        ridge_points=self.ridge_points
        ridge_vertices=self.ridge_vertices

#Goal: replace regions with -1 with  regions containing indeces
 #           Steps: 
 #               1) add new Voronoi vertices by intersection of infinite ridge_lines (replace Voronoi_vertices) 
 #               2) replace the ridge lines: (e.g. [i,j] instead [i,-1])
 #               3) replace the regions: e.g. [i,k,l,j] instead [i,k,-1]
            
        # Get center 
        center = points.mean(axis=0)
        # Get length of bounding box of window
        box = window.minimum_rotated_rectangle

        # get coordinates of polygon vertices
        x, y = box.exterior.coords.xy

        # get length of bounding box edges
        edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))

        # get length of polygon as the longest edge of the bounding box
        length = max(edge_length)

        #list of vertices
        verticesL=list(vertices)
        #Delete vertices outside window and replace by -1 in ridge vertices 
        for i in range(len(verticesL)):
            if window.contains(Point(verticesL[i]))==0:
                k=0
                for pair in ridge_vertices:
                    if np.any(np.array(pair)==i):
                        newpair=np.array(pair)
                        ridge_vertices[k]=list(np.where(newpair==i , -1, newpair))
                    k=k+1
                k=0
                for region in regions: 
                    if np.any(np.array(region)==i):
                        newregion=np.array(region)
                        regions[k]=list(np.where(newregion==i , -1, newregion))
                    k=k+1
        indx=0
        for pointidx, simplex in zip(ridge_points, ridge_vertices):
            simplex = np.asarray(simplex)
            if np.any(simplex < 0)& np.any(simplex>=0):
                i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

                t = points[pointidx[1]] - points[pointidx[0]]  # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = points[pointidx].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vertices[i] + direction * length

                line = [vertices[i],far_point]
                shapely_line = LineString(line)

                intersection_line= window.intersection(shapely_line).coords

                # add new vertex 
                verticesL.append(np.array(intersection_line[1]))

                # replace ridge vertices
                if simplex[0]==i:
                    ridge_vertices[indx]=[i,len(verticesL)-1]
                else:
                    ridge_vertices[indx]=[len(verticesL)-1,i]

                #replace regions for ridge points
                i0=pointidx[0]
                r0=self.point_region[i0]
                if -1 in regions[r0]:
                    regions[r0]=[i for i in regions[r0] if i != -1]
                regions[r0].append(len(verticesL)-1)

                if len(set(regions[r0]))>2:
                    # bring vertices of region in right order
                    region=regions[r0]
                    permutation=spatial.ConvexHull(np.array(verticesL)[region]).vertices
                    
                    regions[r0]=[region[i] for i in permutation]

                i1=pointidx[1]
                if i1!=i0: 
                    r1=self.point_region[i1]
                    if -1 in regions[r1]:
                        regions[r1]=[i for i in regions[r1] if i != -1]
                    regions[r1].append(len(verticesL)-1)

                    if len(set(regions[r1]))>2:
                        region=regions[r1]
                         # bring vertices of region in right order
                        permutation=spatial.ConvexHull(np.array(verticesL)[regions[r1]]).vertices
                        regions[r1]=[region[i] for i in permutation]
            
            indx=indx+1

        x,y = window.exterior.coords.xy
        for x1,y1 in zip(x,y):
            verticesL.append([x1,y1])

            i=np.argmin(np.linalg.norm(points-[x1,y1],axis=1))
            j=self.point_region[i]

            
            regions[j].append(len(verticesL)-1)
            permutation=spatial.ConvexHull(np.array(verticesL)[regions[j]]).vertices
            region=regions[j]
            regions[j]=[region[i] for i in permutation]
            verticesL.append([x1,y1])


        self.vertices=np.array(verticesL)
        self.ridge_vertices=ridge_vertices
        self.regions=regions
                
   
