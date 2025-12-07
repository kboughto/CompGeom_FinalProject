/**
 * Author: Nadezhda Dominguez Salinas
 * This file creates a constrained Delaunay Triangulation of a 2d classroom environment containing obstacles(desks/chairs).
 * The constrained delaunay triangulation is completed using packages from CGAL Constrained Delaunay Traingulation library.
*/

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Constrained_triangulation_face_base_2.h>
#include <CGAL/Triangulation_face_base_with_info_2.h>
#include <CGAL/Triangulation_vertex_base_2.h>
#include <CGAL/Triangulation_data_structure_2.h>
#include <CGAL/Constrained_Delaunay_triangulation_2.h>

#include <fstream>
#include <string>
#include <iostream>
#include <vector>
#include <queue>
#include <limits>

// Defining the kernel and set up for CDT
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Triangulation_vertex_base_2<K> Vb;
typedef CGAL::Triangulation_face_base_with_info_2<bool,K>FbInfo;
typedef CGAL::Constrained_triangulation_face_base_2<K,FbInfo> Fb;
typedef CGAL::Triangulation_data_structure_2<Vb, Fb> Tds;
typedef CGAL::Constrained_Delaunay_triangulation_2<K, Tds> CDT;
typedef K::Point_2 Point;

/**
 * Takes in the list of convex hull vertices from the obstacle polygons(desks/chairs) and places constrained edges between the vertices.
 * The output is a closed polygonal constraint to be excluded from the CDT.
*/
void complete_hulls(CDT& cdt, std::vector<CDT::Vertex_handle>& hull_vertices){

    // Do not consider hulls with less than 3 vertices, as these are not polygons
    if(hull_vertices.size() < 3){
        hull_vertices.clear();
        return;
    }

    // Inserts constraint in CDT, between each of the vertices to create the convex hull polygon constraint edges
    const size_t n = hull_vertices.size();

    for (size_t i = 0; i < n; i++){
        cdt.insert_constraint(hull_vertices[i],hull_vertices[(i+1)%n]);
    }
    
    hull_vertices.clear();
}

/**
 * Iterates through every face in the CDT and assigns whether the triangle is inside the obstacle polygon 
 * or not. Initializes all faces to false, if the face is inside obstacle polygon, it will stay false, using a Breadth First Search when iterating.
*/
void markDomain(CDT& cdt) {

    // Set all face info to false to indicate not visited yet
    for (auto f = cdt.all_faces_begin(); f != cdt.all_faces_end(); ++f)
        f->info() = false;

    // Set up queue for eligible faces
    std::queue<CDT::Face_handle> q;
    CDT::Face_handle start = cdt.finite_faces_begin();

    start->info() = true;
    q.push(start);

    // Going through the graph of obstacle polygons 
    while(!q.empty()){
        CDT::Face_handle f = q.front();
        q.pop();

        for(int i=0; i<3; i++){
            // If constrained edge, don't cross it
            if (cdt.is_constrained(std::make_pair(f, i)))
                continue;

            CDT::Face_handle nb = f->neighbor(i);
            if (!nb->info()) {
                nb->info() = true;
                q.push(nb);
            }
        }
    }
}

/**
 * Inserts the constrained Delaunay Triangulations into a svg file for visualization purposes.
 * If the CDT triangle face info is marked as true then it is used for visualization, otherwise it is part of the obstacle polygon.
*/
void export_svg(const CDT& cdt, const std::string& filename) {
    std::ofstream out(filename);

    out << "<svg xmlns='http://www.w3.org/2000/svg' width='1000' height='1000' "
           "viewBox='0 0 1000 1000'>\n";

    for (auto f = cdt.finite_faces_begin(); f != cdt.finite_faces_end(); ++f) {
        if(!f->info()) continue;

        // Gets the triangle verts
        Point p0 = f->vertex(0)->point();
        Point p1 = f->vertex(1)->point();
        Point p2 = f->vertex(2)->point();

        // Drawing the CDT triangles
        out << "<polygon points='"
            << p0.x() << "," << p0.y() << " "
            << p1.x() << "," << p1.y() << " "
            << p2.x() << "," << p2.y()
            << "' fill='none' stroke='black' stroke-width='0.8'/>\n";
    }

    out << "</svg>\n";
}

/**
 * Reads in the convex hull points from text file and states whether or not they are valid to use for CDT, 
 * then inserts the valid convex hull vertices into constrained polygons in CDT.
*/
bool process_hulls(const std::string& filename, CDT& cdt){

    // Making sure the file was able to open
    std::ifstream in(filename);
    if(!in){
        std::cerr << "Error: Could not open \n";
        return false;
    }

    std::string line;
    std::vector<CDT::Vertex_handle> hull_vertices;

    //Converting the lists of convex hull vertices into closed polygons
    while(std::getline(in,line)){
        if(line.rfind("Hull #",0)==0){
            complete_hulls(cdt,hull_vertices);
            continue;
        }

        if(line.empty()){
            complete_hulls(cdt,hull_vertices);
            continue;
        }
        
        size_t comma = line.find(',');
        // turning the convex hull vertices string into a double 
        double x = std::stod(line.substr(0,comma));
        double y = std::stod(line.substr(comma+1));

        // places the vertices into the CDT construction
        hull_vertices.push_back(cdt.insert(Point(x,y)));
        
    }
    complete_hulls(cdt,hull_vertices);
    return true;
}
int main( ) {
    CDT cdt;

    // Creating boundary of the classroom
    std::vector<Point> classroom = {
        Point(0,0),
        Point(939,0),
        Point(725,939),
        Point(0,725)
    };
    // Put the classroom vertices in the CDT
    std::vector<CDT::Vertex_handle> classroom_v;
    for(auto& p :classroom)
        classroom_v.push_back(cdt.insert(p));
    complete_hulls(cdt,classroom_v);
    // Adding all the obstacle polygons from text file
    if(!process_hulls("ConvexHullPoints.txt",cdt)){
        std::cerr << "Could not load Convex Hull Points.\n";
        return 1;
    }
    // Counts for CDT
    std::cout <<"Vertices:" << cdt.number_of_vertices() << "\n";
    std::cout <<"Triangles:" << cdt.number_of_faces() << "\n";

    markDomain(cdt);
    export_svg(cdt, "Triangulation.svg");
    std::cout << "Made Triangulation.svg\n";
}