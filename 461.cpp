class Solution {
public:
    int hammingDistance(int x, int y) {
        vector<int> bin1 = dec2bin(x);
        vector<int> bin2 = dec2bin(y);
        int count = 0;
        while (bin1.size() > bin2.size()){
            bin2.push_back(0);
        }
        while (bin1.size() < bin2.size()){
            bin1.push_back(0);
        }
        for (int i = 0; i < bin1.size(); i++){
            if (bin1[i]!=bin2[i]){
                count++;
            }
        }
        return count;
    }
    vector<int> dec2bin(int a){
        vector<int> bin;
        int n = a;
        while(n>0){
            bin.push_back(n%2);
            n = n / 2;
        }
        return bin;
    }
};
