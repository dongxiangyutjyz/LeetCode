class Solution {
public:
    int minMoves2(vector<int>& nums) {
        sort(nums.begin(),nums.end());
        int size = nums.size();
        int middle = nums[floor(size/2)];
        int result = 0;
        for (int i = 0; i < nums.size();i++){
            result+= abs(nums[i]-middle);
        }
        return result;
    }
};
