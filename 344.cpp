class Solution {
public:
    string reverseString(string s) {
        if (s.length() == 2){
            char result = s[1];
            s[1] = s[0];
            s[0] = result;
        }else{
        for (int i = 0; i < s.length()/2; i++){
            cout<<i<<endl;
            char index = s[i];
            cout<<index;
            s[i] = s[s.length()-i-1];
            s[s.length()-i-1] = index;
        }
        }
        
        return s;
    }
};
