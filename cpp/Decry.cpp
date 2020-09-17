// Decry.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <map>
#include <set>
#include <fstream>

#define A 27
#define T 106
#define L 500
using namespace std;

constexpr char id2c[27] = 
{ ' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' };

map<char, short> c2id = { {' ',0}, {'a',1}, {'b',2 }, {'c',3}, {'d',4},{'e',5},{'f',6},{'g',7},{'h',8},{'i',9},{'j',10},{'k',11},{'l',12},{'m',13},{'n',14},{'o',15},{'p',16},{'q',17},{'r',18},{'s',19},{'t',20},{'u',21},{'v',22},{'w',23},{'x',24},{'y',25},{'z',26} }; 


constexpr int rowlen[27] = {19,7,1,2,4,10,2,2,5,6,1,1,3,2,6,6,2,1,5,5,7,2,1,2,1,2,1};

#include "Utils.h"
#include "SData.h"

std::vector<std::string> split(const std::string & s, char delimiter)
{
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(s);
    while (std::getline(tokenStream, token, delimiter))
    {
        tokens.push_back(token);
    }
    return tokens;
}




void read_cipher(vector<short>& cipher_v) {
    string cs;
    getline(cin, cs);
    vector<string> csv = split(cs, ',');
    transform(csv.begin(), csv.end(), std::back_inserter(cipher_v),
        [](const std::string& str) { return short(std::stoi(str)); });
}

void eval(vector<short>& cipher,vector<short>& plain,vector<set<short>>& tbl,bool fault) {
    
    for (auto i = 0; i < cipher.size(); i++) {
        short ci_v = cipher[i];
        short p_v = plain[i];
        tbl[p_v].insert(ci_v);
        if (tbl[p_v].size() > rowlen[p_v]) {
            fault = true;
            return;
        }
    }
}


int main()
{
    char x = c2id['a'];
    std::cout << "Hello World!\n"<<c2id['c']<<"\n";
    std::cout << read_file("./t.txt") << "\n";
    string cipher_s;
    vector<short> cipher_v;
    read_cipher(cipher_v);
    

    for (auto i = 0; i < cipher_v.size(); i++) {
        cout << "I:" << cipher_v[i] << "\n";
    }
}

