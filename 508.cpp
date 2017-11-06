/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    vector<int> findFrequentTreeSum(TreeNode* root) {
        if (root == NULL){
            vector<int> result;
            return result;
        }
        vector<int> result;
        map<int,int> allSums;
        deque<TreeNode> subnodes;
        subnodes.push_back(*root);
        while (subnodes.size()>0){
            TreeNode currentNode = subnodes.front();
            subnodes.pop_front();
            allSums[subSum(&currentNode)]++;
            if (currentNode.left != NULL){
                subnodes.push_back(*currentNode.left);
            }
            if (currentNode.right != NULL){
                subnodes.push_back(*currentNode.right);
            }
        }
        int max = 0;
        for (auto it = allSums.begin();it != allSums.end();it++){
            if (it->second > max){
                max = it->second;
            }
        }
        for (auto it = allSums.begin();it != allSums.end();it++){
            if (it->second == max){
                result.push_back(it->first);
            }
        }
        return result;
    }
    int subSum(TreeNode* root){
        deque<TreeNode> subnodes;
        subnodes.push_back(*root);
        int sum = 0;
        while (subnodes.size()>0){
            TreeNode currentNode = subnodes.front();
            sum += currentNode.val;
            subnodes.pop_front();
            if (currentNode.left != NULL){
                subnodes.push_back(*currentNode.left);
            }
            if (currentNode.right != NULL){
                subnodes.push_back(*currentNode.right);
            }
        }
        return sum;
    }
};
