import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .enums import PhraseLanguage


class StoryTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    english_name = models.CharField(max_length=100)
    spanish_name = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.id} - {self.english_name}'
    

# class Phrase(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     phrase_number:int = models.AutoField(primary_key=False, editable=False)

#     topic:StoryTopic = models.ForeignKey(StoryTopic, on_delete=models.CASCADE, related_name='phrases')

#     phrase:str = models.CharField(max_length=256)

#     language:PhraseLanguage = models.IntegerField(choices=PhraseLanguage.choices, default=PhraseLanguage.ENGLISH)


#     def __str__(self):
#         return f'{self.id} - {self.phrase}'


# class StoryTopicTree(models.Model):

#     """
#         This model is used to create a tree structure for the story topics.
#         Using the phrase_number property to create a binary tree.
    
#     """

#     id:uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     phrase_node:Phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, related_name='phrase_node')

#     parent:'StoryTopicTree' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent', null=True, blank=True)
    
#     left_child:'StoryTopicTree' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='left_child', null=True, blank=True)
#     right_child:'StoryTopicTree' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='right_child', null=True, blank=True)


#     root:'StoryTopicTree' = models.ForeignKey('self', on_delete=models.CASCADE, related_name='root', null=True, blank=True)


#     @property
#     def is_root(self) -> bool:
#         return self.root == None
    

#     @property
#     def is_leaf(self) -> bool:
#         return self.left_child == None and self.right_child == None
        

#     @property
#     def has_left_child(self) -> bool:
#         return self.left_child != None
    

#     @property
#     def has_right_child(self) -> bool:
#         return self.right_child != None
    

#     def add_node(self, phrase_node:Phrase) -> 'StoryTopicTree':
#         """

#             This method is used to add a new node to the tree.
#             Have in mind that the phrase_node is always greater than the greatest node in the tree.
#             This is because the phrase_number is an auto increment field.
#             So, we need a way to balance the tree and keep it as balanced as possible.
        
#         """

#         if self.phrase_node.phrase_number < phrase_node.phrase_number:
#             if self.has_left_child:
#                 return self.left_child.add_node(phrase_node)
#             else:
#                 self.left_child = StoryTopicTree.objects.create(phrase_node=phrase_node, parent=self, root=self.root)
#                 return self.left_child
#         else:
#             if self.has_right_child:
#                 return self.right_child.add_node(phrase_node)
#             else:
#                 self.right_child = StoryTopicTree.objects.create(phrase_node=phrase_node, parent=self, root=self.root)
#                 return self.right_child
            
        

#     def balance_tree(self) -> 'StoryTopicTree':
#         """

#             This method is used to balance the tree.
#             It will check if the tree is balanced, if it is not, it will balance it.
#             This method is called after the tree is created.
        
#         """

#         if self.is_leaf:
#             return self

#         elif self.has_left_child and self.has_right_child:
#             left_height = self.left_child.get_height()
#             right_height = self.right_child.get_height()

#             if left_height > right_height:
#                 self.rotate_right()
#             elif right_height > left_height:
#                 self.rotate_left()
#             else:
#                 pass

#             self.left_child.balance_tree()
#             self.right_child.balance_tree()

#         elif self.has_left_child:
#             left_height = self.left_child.get_height()

#             if left_height > 1:
#                 self.rotate_right()
#                 self.left_child.balance_tree()
#                 self.right_child.balance_tree()

#         elif self.has_right_child:
#             right_height = self.right_child.get_height()

#             if right_height > 1:
#                 self.rotate_left()
#                 self.left_child.balance_tree()
#                 self.right_child.balance_tree()
        
#         return self


#     def find_node(self, phrase_number:int) -> 'StoryTopicTree':
#         if self.phrase_node.phrase_number == phrase_number:
#             return self
#         elif self.left_child:
#             return self.left_child.find_node(phrase_number)
#         elif self.right_child:
#             return self.right_child.find_node(phrase_number)
#         else:
#             return None
    

#     def __str__(self):
#         return f'{self.phrase_node}'
    

# class TreeNode:
#     def __init__(self, key):
#         self.key = key
#         self.left = None
#         self.right = None
#         self.height = 1

# class BalancedBinaryTree:
#     def __init__(self):
#         self.root = None

#     def insert(self, key):
#         if not self.root:
#             self.root = TreeNode(key)
#         else:
#             self.root = self._insert(self.root, key)
#             self.root = self._balance_tree(self.root)

#     def _insert(self, node, key):
#         if not node:
#             return TreeNode(key)

#         if key < node.key:
#             node.left = self._insert(node.left, key)
#         else:
#             node.right = self._insert(node.right, key)

#         node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
#         return self._balance_tree(node)


#     def _get_height(self, node):
#         if not node:
#             return 0
#         return node.height


#     def _get_balance(self, node):
#         if not node:
#             return 0
#         return self._get_height(node.left) - self._get_height(node.right)


#     def _balance_tree(self, node):
#         balance = self._get_balance(node)

#         if balance > 1:
#             if self._get_balance(node.left) < 0:
#                 node.left = self._rotate_left(node.left)
#             node = self._rotate_right(node)

#         if balance < -1:
#             if self._get_balance(node.right) > 0:
#                 node.right = self._rotate_right(node.right)
#             node = self._rotate_left(node)

#         return node

#     def _rotate_left(self, z):
#         y = z.right
#         T2 = y.left

#         y.left = z
#         z.right = T2

#         z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
#         y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

#         return y

#     def _rotate_right(self, y):
#         x = y.left
#         T2 = x.right

#         x.right = y
#         y.left = T2

#         y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
#         x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

#         return x
