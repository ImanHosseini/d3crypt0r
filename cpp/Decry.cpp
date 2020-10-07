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
#include <thread>
#include <mutex>
#include "Config.h"



using namespace std;




#include "Utils.h"
#include "SData.h"
aindex_t cipher[TXT_LEN];

std::vector<std::string> split_to_vec(const std::string & s, char delimiter)
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

void split_to_array(const string& s, char delimiter, aindex_t* tokens, size_t len=TXT_LEN) {
    std::string s_token;
    std::istringstream tokenStream(s);
    auto cnt = 0;
    while (std::getline(tokenStream, s_token, delimiter))
    {
        tokens[cnt] = aindex_t(std::stoi(s_token));
        cnt++;
        if (cnt >= len) {
            return;
        }
    }
    return;
}



void read_cipher(aindex_t* cipher_v) {
    string cs;
    getline(cin, cs);
    split_to_array(cs,',',cipher_v);
    // vector<string> csv = split(cs, ',');
    // transform(csv.begin(), csv.end(), std::back_inserter(cipher_v),
    //    [](const std::string& str) { return aindex_t(std::stoi(str)); });
}





void eval(const aindex_t* cipher,const aindex_t* plain,set<aindex_t> *tbl,bool& fault) {
    // seen is a reverse tbl, mapping cipher token to plaintext token
    map<aindex_t,aindex_t> seen{};
    for (auto i = 0; i < TXT_LEN; i++) {
        aindex_t ci_v = cipher[i];
        aindex_t p_v = plain[i];
        auto itr = seen.find(ci_v);
        if (itr==seen.end()) {
            // First time seeing this token
            tbl[p_v].insert(ci_v);
            if (tbl[p_v].size() > rowlen[p_v]) {
                fault = true;
                return;
            }
            seen[ci_v] = p_v;
        }
        else {
            // This token was already seen
            aindex_t p_e = itr->second;
            if (p_e != p_v) {
                // CONTRADICTION!
                fault = true;
                return;
            }
        }
       
    }
}

bool decrypt_type1(const aindex_t* cipher) {
    bool is_type1 = false;
    for (auto idx = 0; idx < PLAINTXT_DICT_SIZE; idx++) {
        bool not_same = false;
        set<aindex_t> tbl[27];
        eval(cipher, plaintxts[idx], tbl, not_same);
        if (!not_same) {
            std::cout << plain_strs[idx] << endl;
            return true;
        }
    }
    return false;
}

typedef struct State {
    int* wstate;
    int* wslen;
    aindex_t* ptxt;
    int* plen;
    int* hits;
    set<aindex_t> *tbl;
    map<aindex_t, aindex_t> *seen;
    State(int* wstate,int* wslen,aindex_t* ptxt,int* plen,int* hits,set<aindex_t> *tbl,map<aindex_t,aindex_t> *seen) : wstate(wstate), wslen(wslen),ptxt(ptxt),plen(plen),hits(hits),tbl(tbl),seen(seen){}
    void pp_seen() {
        cout << "SEEN:\n";
        for (auto x : *seen) {
            cout << x.first << "->" << id2c[x.second] << ", ";
        }
        cout << "\n";
    }
    void pp_tbl() {
        cout << "TBL:\n";
        for (auto i = 0; i < 27; i++) {
            if (tbl[i].size() > 0) {
                cout << id2c[i] << " : ";
                for (aindex_t x : tbl[i]) {
                    cout << x << ", ";
                }
                cout << "\n";
            }
        }
       // cout << "END TBL" << "\n";
    }
    bool consume(aindex_t plc) {
       
        aindex_t c_v = cipher[*plen];
        if (hits[c_v] > 0) {
            aindex_t p_e = (*seen)[c_v];
            if (p_e != plc) {
                // Bad
                return false;
            }
            else {
                hits[c_v] += 1;
                ptxt[*plen] = p_e;
                (*plen) += 1;
                return true;
            }
        }
        else {
            if (tbl[plc].size() + 1 > rowlen[plc]) {
                // Bad
                return false;
            }
            else {
                (*seen)[c_v] = plc;
                tbl[plc].insert(c_v);
                hits[c_v] += 1;
                ptxt[*plen] = plc;
                (*plen) += 1;
                return true;
            }
        }
    }
    void rollback(int num) {
     /*   cout << "Rollback with num: " << num << endl;
        for (auto i = 0; i < ROW_SUM; i++) {
            cout << hits[i] << "|";
        }
        cout << endl;
        cout << "[" << (*plen) << "]Rmv:" ;*/
        for (auto i = 0; i < num; i++) {
            aindex_t c_v = cipher[(*plen) - i - 1];
            aindex_t p_v = ptxt[(*plen) - i - 1];
            // cout << c_v << ", ";
            hits[c_v] = hits[c_v] -  1;
            if (hits[c_v] == 0) {
                tbl[p_v].erase(c_v);
                (*seen).erase(c_v);
            }
        }
        (*plen) = (*plen) - num;
     
        // pp_tbl();
        // pp_seen();
    }
    int advance() {
        bool works = false;
        int found = 0;
        // int wdi = 0;
        
        int wdi = wstate[(*wslen)];
     
        
        while ((!works) & (wdi<WORD_DICT_SIZE)) {
            works = true;
            //if ((*wslen==56) & /* (wstate[2] == 13) &  (wstate[3] == 12) & */ (wdi==20)) {
            //    __debugbreak();
            //}
            for (auto ci = 0; ci < wlens[wdi]+1; ci++) {
                aindex_t ch = 0;
                if (ci < wlens[wdi]) {
                    ch = words[wdi][ci];
                }
                // cout << "Consuming " << id2c[ch] << " at " << (*plen) << endl;
                //  pp_tbl();
                bool cons = consume(ch);
                // cout << "cons: " << cons << "\n";
                // pp_tbl();
                if (!cons) {
                    works = false;
                    rollback(ci);
                    break;
                }
                else {
                   
                        if ((*plen) == TXT_LEN) {
                            found = true;
                            return 1;
                        }
                    
                }
            }
            if (works) {
                // print_ptxt(ptxt,*plen);
                break;
            }
            else {
            wdi++;
            }
        }
        if (works) {
            wstate[*wslen] = wdi;
            (*wslen)++;
            return 0;
        }
        else {
            
            int wwdi = wstate[(*wslen) - 1];
            wstate[(*wslen)] = 0;
            while (wwdi > (WORD_DICT_SIZE - 2)) {
                rollback(wlens[wstate[(*wslen) - 1]] + 1);
                wstate[(*wslen) - 1] = 0;
                (*wslen)--;
                if ((*wslen) < 1) {
                    return -1;
                }
                wwdi = wstate[(*wslen) - 1];
            }
            rollback(wlens[wstate[(*wslen) - 1]] + 1);
            wstate[(*wslen) - 1]++;
            (*wslen)--;
            return advance();
        }
        
    }
    
};



void decrypt_type2() {
    int wstate[TXT_LEN] = {};
    int wslen = 0;
    aindex_t ptxt[TXT_LEN] = {};
    int plen = 0;
    int hits[ROW_SUM] = {};
    set<aindex_t> tbl[27];
    map<aindex_t, aindex_t> seen{};
    State state(wstate,&wslen,ptxt,&plen,hits,tbl,&seen);
    int found = 0;
    while (found == 0) {
        found = state.advance();
    }
    print_ptxt(state.ptxt);
}

mutex p_mutex;

void find_th(int tnum, int idx) {
    int delta = WORD_DICT_SIZE / (double)tnum;

    int wstate[TXT_LEN] = {};
    int wslen = 0;
    wstate[0] = idx * delta;
    aindex_t ptxt[TXT_LEN] = {};
    int plen = 0;
    int hits[ROW_SUM] = {};
    set<aindex_t> tbl[27];
    map<aindex_t, aindex_t> seen{};
    State state(wstate, &wslen, ptxt, &plen, hits, tbl, &seen);
    int found = 0;
    while (found == 0) {
        found = state.advance();
    }
    if (found == 1) {
    p_mutex.lock();
    print_ptxt(state.ptxt);
    exit(0);
    }
    return;
}

/* thread number should be power of 2 */
void decrypt_type2_mt(int threads = 16) {
    if (threads == 1) {
        return decrypt_type2();
    }
    vector<thread> threadz{};
    for (auto i = 0; i < threads; i++) {
        threadz.push_back(thread(find_th,threads,i));
    }
    for (auto i = 0; i < threads; i++) {
        threadz[i].join();
    }
}

void decrypt_main(int t) {
    if (!decrypt_type1(cipher)) {
        // Inconclusive
        // cout << "NOT IN PDIC!" << endl;
    }
    decrypt_type2_mt(t);
}



int main(int argc, char* argv[])
{
    int t = 1;
    if (argc == 3) {
        // SHOULD be -t <thread_number>
        t = stoi(argv[2]);
        t = to_nearest_pw2(t);
    }
    else if (argc == 2) {
        // SHOULD be -mt
        t = thread::hardware_concurrency();
        t = to_nearest_pw2(t);
        if (t == 0) {
            t = 1;
        }
    }

    read_cipher(cipher);
    decrypt_main(t);
}

