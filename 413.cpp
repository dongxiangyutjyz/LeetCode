class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& A) {
        if (A.size()<3){
            return 0;
        }
        int result = 0;
        for (int i = 2; i < A.size();i++){
            for (int j = 0;j < A.size()-i;j++){
                int difference = 0;
                int count = 0;
                for (int k = j; k < j+i;k++){
                    if ((k-j)==0){
                        difference = A[k+1]-A[k];
                    }
                    if(A[k+1]-A[k]==difference){
                        count++;
                    }
                }
                if (count == i){
                    result++;
                }
            }
        }
        return result;
    }
};
