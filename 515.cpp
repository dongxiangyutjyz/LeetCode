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
    vector<int> largestValues(TreeNode* root) {
        if (root == NULL){
            vector<int> result;
            return result;
        }
        if (root->left==NULL && root->right==NULL){
            vector<int> result;
            result.push_back(root->val);
            return result;
        }
        deque<TreeNode> nodes;
        vector<int>nodeval;
        int level = 0;
        int maximum = INT_MIN;
        vector<int> result;
        nodes.push_front(*root);
        nodes.push_back(INT_MIN);
        while (nodes.size()!= 0){
            if (nodes.front().val==INT_MIN){
                nodes.pop_front();
                result.push_back(maximum);
                maximum = INT_MIN;
                if (nodes.size()!= 0){
                    nodes.push_back(TreeNode(INT_MIN));
                }
            }
            else{
                TreeNode currentNode = nodes.front();
                int value = currentNode.val;
                if (value > maximum){
                    maximum = value;
                }
                if (currentNode.left!=NULL){
                    nodes.push_back(*currentNode.left);
                }
                if (currentNode.right!=NULL){
                    nodes.push_back(*currentNode.right);
                }
                nodes.pop_front();
            }
        }
        return result;
    }
};
