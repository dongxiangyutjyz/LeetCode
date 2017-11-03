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
    int findBottomLeftValue(TreeNode* root) {
        int value;
        deque<TreeNode> nodes;
        nodes.push_back(*root);
        while (nodes.size()>0){
            TreeNode currentNode = nodes.front();
            nodes.pop_front();
            if (currentNode.right != NULL){
                nodes.push_back(*currentNode.right);
            }
            if (currentNode.left != NULL){
                nodes.push_back(*currentNode.left);
            }
            value = currentNode.val;
        }
        return value;
    }
};
