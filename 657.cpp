class Solution {
public:
    bool judgeCircle(string moves) {
        map<char,int> move;
        for (int i = 0; i < moves.length(); i++){
            move[moves[i]]++;
        }
        return move['U']==move['D']&&move['L']==move['R'];
    }
};
