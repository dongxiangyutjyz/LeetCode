class Solution {
public:
    int findComplement(int num) {
        vector<int> bin;
        bin = dec2bin(num);
        int newnum = 0;
        for (int i = 0; i < bin.size();i++){
            if (bin[i] == 0){
                bin[i] = 1;
            }
            else{
                bin[i] = 0;
            }
            newnum += bin[i]*pow(2,i);
        }
        return newnum;
    }
    vector<int> dec2bin(int num){
        vector<int> bin;
        int newnum = num;
        while(newnum > 0){
            bin.push_back(newnum%2);
            newnum = newnum/2;
        }
        return bin;
    }
};
