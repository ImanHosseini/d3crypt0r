#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <map>
#include <set>
#include <fstream>


// Note: CWD is project main dir
string read_file(string name) {
    std::ifstream t(name);
    std::string str((std::istreambuf_iterator<char>(t)),
        std::istreambuf_iterator<char>());
    return str;
}

/*
Algorithm looked up from: http://graphics.stanford.edu/~seander/bithacks.html#RoundUpPowerOf2
*/
int to_nearest_pw2(int v) {
    unsigned int v_ = (unsigned int)v;
    v--;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v++;
    return (int)v;
}

/* 
The following function is copy-pasted from stack-overflow:
https://stackoverflow.com/questions/17248462/is-there-any-way-to-output-the-actual-array-in-c
*/
template <typename T, std::size_t N>
void print_array(const T(&a)[N], std::ostream& o = std::cout)
{
    o << "{";
    for (std::size_t i = 0; i < N - 1; ++i)
    {
        o << a[i] << ", ";
    }
    o << a[N - 1] << "}\n";
}