#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Constrained_Delaunay_triangulation_2.h>
#include <CGAL/draw_constrained_triangulation_2.h>
#include <fstream>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Triangulation_vertex_base_2<K> Vb;
typedef CGAL::Constrained_triangulation_face_base_2<K> Fb;
typedef CGAL::Triangulation_data_structure_2<Vb, Fb> Tds;
typedef CGAL::Constrained_Delaunay_triangulation_2<K, Tds> CDT;
typedef K::Point_2 Point;

void export_svg(const CDT& cdt, const std::string& filename) {
    std::ofstream out(filename);

    out << "<svg xmlns='http://www.w3.org/2000/svg' width='500' height='500' "
           "viewBox='0 -10 10 10'>\n";

    for (auto f = cdt.finite_faces_begin(); f != cdt.finite_faces_end(); ++f) {
        Point p0 = f->vertex(0)->point();
        Point p1 = f->vertex(1)->point();
        Point p2 = f->vertex(2)->point();

        out << "<polygon points='"
            << p0.x() << "," << -p0.y() << " "
            << p1.x() << "," << -p1.y() << " "
            << p2.x() << "," << -p2.y()
            << "' fill='none' stroke='black' stroke-width='0.05'/>\n";
    }

    out << "</svg>\n";
}

int main( ) {
CDT cdt;

// Make a square
Point p1(0,0), p2(10,0), p3(10,10), p4(0,10);

// Edge constraints
CDT::Vertex_handle v1 = cdt.insert(p1);
CDT::Vertex_handle v2 = cdt.insert(p2);
CDT::Vertex_handle v3 = cdt.insert(p3);
CDT::Vertex_handle v4 = cdt.insert(p4);

cdt.insert_constraint(v1,v2);
cdt.insert_constraint(v2,v3);
cdt.insert_constraint(v3,v4);
cdt.insert_constraint(v4,v1);

std::cout <<"Number of faces: " << cdt.number_of_faces() << std::endl;

export_svg(cdt, "triangulation.svg");
}