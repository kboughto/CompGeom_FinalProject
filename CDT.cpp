/**
 * Author: Nadezhda Dominguez Salinas
 * This file includes code to triangulate a 2d classroom environment containing obstacles(desks/chairs.
 * The constrained delaunay triangulation is completed using packages from CGAL Constrained Delaunay Traingulation library.
*/
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Constrained_Delaunay_triangulation_2.h>
#include <CGAL/draw_constrained_triangulation_2.h>
#include <CGAL/mark_domain_in_triangulation.h>
#include <fstream>
#include <string>
#include <iostream>
#include <vector>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Triangulation_vertex_base_2<K> Vb;
typedef CGAL::Constrained_triangulation_face_base_2<K> Fb;
typedef CGAL::Triangulation_data_structure_2<Vb, Fb> Tds;
typedef CGAL::Constrained_Delaunay_triangulation_2<K, Tds> CDT;
typedef K::Point_2 Point;

/**
 * Takes in the list of convex hull vertices and places constrained edges between the vertices.
*/
void complete_hulls(CDT& cdt, std::vector<CDT::Vertex_handle>& hull_vertices){

    // Do not consider hulls with less than 3 vertices, as these are not polygons
    if(hull_vertices.size() < 3){
        hull_vertices.clear();
        return;
    }

    const size_t n = hull_vertices.size();

    // Place a constraint between each of the vertices to create the obstacle edges
    for (size_t i = 0; i < n; i++){
        cdt.insert_constraint(hull_vertices[i],hull_vertices[(i+1)%n]);
    }
    hull_vertices.clear();
}

/**
 * Creates an svg file of the constrained Delaunay Triangulation for visualization purposes.
*/
void export_svg(const CDT& cdt, const std::string& filename) {
    std::ofstream out(filename);

    out << "<svg xmlns='http://www.w3.org/2000/svg' width='900' height='900' "
           "viewBox='0 0 900 900'>\n";

    for (auto f = cdt.finite_faces_begin(); f != cdt.finite_faces_end(); ++f) {
        Point p0 = f->vertex(0)->point();
        Point p1 = f->vertex(1)->point();
        Point p2 = f->vertex(2)->point();

        out << "<polygon points='"
            << p0.x() << "," << p0.y() << " "
            << p1.x() << "," << p1.y() << " "
            << p2.x() << "," << p2.y()
            << "' fill='none' stroke='black' stroke-width='0.8'/>\n";
    }

    out << "</svg>\n";
}

/**
 * Takes in the convex hull points and states whether or not they are valid to use for CDT, then inserts the vertices into CDT.
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

    if(!process_hulls("ConvexHullPoints.txt",cdt)){
        std::cerr << "Could not load Convex Hull Points.\n";
        return 1;
    }

    std::cout <<"Vertices:" << cdt.number_of_vertices() << "\n";
    std::cout <<"Triangles:" << cdt.number_of_faces() << "\n";

    export_svg(cdt, "Triangulation.svg");
    std::cout << "Made Triangulation.svg\n";
}

// // Original Simple Example of polygon and CDT, plus it's visualizations
//Make a square
// Point p1(0,0), p2(10,0), p3(10,10), p4(0,10);

// // Edge constraints
// CDT::Vertex_handle v1 = cdt.insert(p1);
// CDT::Vertex_handle v2 = cdt.insert(p2);
// CDT::Vertex_handle v3 = cdt.insert(p3);
// CDT::Vertex_handle v4 = cdt.insert(p4);

// cdt.insert_constraint(v1,v2);
// cdt.insert_constraint(v2,v3);
// cdt.insert_constraint(v3,v4);
// cdt.insert_constraint(v4,v1);

// std::cout <<"Number of faces: " << cdt.number_of_faces() << std::endl;

// export_svg(cdt, "triangulation.svg");