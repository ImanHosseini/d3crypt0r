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