class Solution {
public:
    int rob(vector<int>& nums) {
        int size = nums.size();
        if (size == 0){
            return 0;
        }
        if (size == 1){
            return nums[0];
        }
        vector<int> rob(size);
        rob[0] = nums[0];
        rob[1] = max(nums[0],nums[1]);
        if (size == 2){
            return rob[1];
        }
        for (int i = 2;i < size;i++){
            rob[i]=max(rob[i-1],rob[i-2]+nums[i]);
        }
        return max(rob[size-1],rob[size-2]);
    }
    int max(int a,int b){
        return (a>b)?a:b;
    }
};
