#include <iostream>
#include <list>
using namespace std;

class Node{
    public:
    string token;
    string type;
    Node* next;
    Node(string aaa,string bbb):token(aaa),type(bbb),next(nullptr){};
};
Node* Match_id(string input,int &check_number,Node* Current_node);
Node* Match_strlit(string input,int &check_number,Node* Current_node);
void Printall(Node* node);

int main(){
    list<string> token;
    string input;
    Node *first_node=new Node("abc","abc");
    Node *Current_node=first_node;
    while(1){
        getline(cin,input);
        if(input==""){
            break;
        }
        token.push_back(input);
    }
    for (const string& t : token) {
        for (int position = 0; position < t.size(); position++)
        {   
            if (t[position]>=65&&t[position]<=90||t[position]>=97&&t[position]<=122||t[position]==95||t[position]<=57&&t[position]>=48){  
                Current_node=Match_id(t,position,Current_node);
                if(position+1!=t.size()){
                    position--;
                }
            }
            else if(t[position]==34){  //�ڹJ��"
                Current_node=Match_strlit(t,position,Current_node);
            }
            else if(t[position]==40){ //??????(
                Node* node=new Node( "(","LBR");
                Current_node->next=node;
                Current_node=node;
            }
            else if(t[position]==41){  //??????)
                Node* node=new Node( ")","RBR");
                Current_node->next=node;
                Current_node=node;
            }
            else if(t[position]==46){  //??????.
                Node* node=new Node(".","DOT"); 
                Current_node->next=node;
                Current_node=node;
            }
            else if(t[position]==32||t[position]==0){
            }
            else{
                cout<<"invalid input"<<endl;
                return 0;
            }
        }
    }
    first_node=first_node->next;
    Printall(first_node);
}

Node* Match_id(string input,int &check_number,Node* Current_node){

    string check="";
    for (int i = check_number; i < input.size(); i++)
    {   
        
        if(!(65<=input[i]&&input[i]<=90||input[i]>=97&&input[i]<=122||input[i]==95||input[i]<=57&&input[i]>=48)||check_number==input.size()-1){
            if(check_number==input.size()-1){
                check+=input[i];
            }
            Node* node=new Node(check,"ID");
            Current_node->next=node;
            Current_node=Current_node->next;
            return Current_node;
        }
        else{
            check+=input[i];
            check_number++;
        }
    }    
    return Current_node;
}

Node* Match_strlit(string input,int &check_number,Node* Current_node){
    string check="";
    check+=input[check_number];
    for (int i = check_number+1; i < input.size(); i++)
    {   
        check+=input[i];
        if(input[i]==34){
            Node* node=new Node(check,"STRLIT");
            Current_node->next=node;
            Current_node=Current_node->next;
            check_number++;
            return Current_node;
        }
        else{
            check_number++;
        }
    }
    cout<<"invalid input"<<endl;
    return 0;
}
void Printall(Node* node){
    Node *current_node = node;
    while (current_node != nullptr) {
        cout << current_node->type << " " << current_node->token << endl;
        current_node = current_node->next;
    }
}