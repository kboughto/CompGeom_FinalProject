# Created by the script cgal_create_CMakeLists
# This is the CMake script for compiling a set of CGAL applications.

cmake_minimum_required(VERSION 3.12...3.31)

project( CompGeom_FinalProject )


# CGAL and its components
# find_package( CGAL QUIET COMPONENTS  )
find_package(CGAL REQUIRED)
if ( NOT CGAL_FOUND )

  message(STATUS "This project requires the CGAL library, and will not be compiled.")
  return()

endif()


# Boost and its components
find_package( Boost REQUIRED )

if ( NOT Boost_FOUND )

  message(STATUS "This project requires the Boost library, and will not be compiled.")

  return()

endif()

# Source Files
add_executable(final_project CDT.cpp)

# Copying ConvexHull vertices list into the build folder 
configure_file(ConvexHullPoints.txt ConvexHullPoints.txt COPYONLY)

# Linking CGAL & Boost
target_link_libraries(final_project CGAL::CGAL Boost::boost)
