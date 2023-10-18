#include <iostream>
#include <string>
#include <vector>

using namespace std;

string now="";
int position=0;
int correct=1;
void stmt(string input);
void classgo(string input);
void fun(string input);
void classname(string input);
void funcname(string input);
void leftP(string input);
void rightP(string input);
void Args(string input);
void Arg(string input);


class token{
    public:
    char key;
    string type;
    token(char aaa,string bbb):key(aaa),type(bbb){};
};
vector<token> token_all;

void stmt(string input){
    if(input[position]>='A' && input[position]<='Z'){
        classgo(input);
    }
    else if(input[position]=='('){
        fun(input);
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
    }
}

void classgo(string input){
    classname(input);
    if(input[position]=='('){
        leftP(input);
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
        return;
    }
    if(input[position]==')'){
        rightP(input);
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
        return;
    }
    Args(input);
}
void fun(string input){
    leftP(input);
    if(input[position]>='a' && input[position]<='z'){
        funcname(input);
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
        return;
    }
    Args(input);
    if(input[position]==')'){
        rightP(input);
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
        return;
    }
}
void classname(string input){
    token newtoken(input[position],"classname");
    token_all.push_back(newtoken);
    position++;
    return;
}
void funcname(string input){
    token newtoken(input[position],"funcName");
    token_all.push_back(newtoken);
    position++;
    return ;
}
void leftP(string input){
    token newtoken(input[position],"leftParen");
    token_all.push_back(newtoken);
    position++;
    return ;
}
void rightP(string input){
    token newtoken(input[position],"rightParen");
    token_all.push_back(newtoken);
    position++;
    return ;
}
void Args(string input){
    if(input[position]>='0' && input[position]<='9' || input[position]=='('){
        Arg(input);
        Args(input);
        return;
    }
    else{
        return;
    }
}
void Arg(string input){
    if(input[position]>='0' && input[position]<='9'){
        token newtoken(input[position],"num");
        token_all.push_back(newtoken);
        position++;
        return ;
    }
    else if(input[position]=='('){
        fun(input);
        return;
    }
    else{
        cout<<"Invaild input"<<endl;
        correct=0;
        return;
    }
}

int main(){
    string input="";
    getline(cin,input);
    string fix;
    for(char a:input){
        if(!isspace(a)){
            fix+=a;
        }
    }
    stmt(fix);
    if(correct){
        for(token a:token_all){
            cout<<a.type<<" "<<a.key<<endl;
        }
    }
    
}

//會因為position問題，抓不到一些值，要用void，全域position一直給他++，幹全部重改雞巴[]
