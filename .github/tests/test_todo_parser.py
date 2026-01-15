import sys
import os
import unittest
from pathlib import Path

# Add the scripts directory to path to allow importing
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from todo_to_issues import parse_metadata, extract_labels_from_metadata, similarity_ratio, find_duplicate, load_config

class TestTodoParser(unittest.TestCase):
    def setUp(self):
        self.default_config = {
            'default_labels': ['todo', 'tech-debt']
        }

    def test_parse_metadata_simple(self):
        metadata_str = "PRIORITY: high, TYPE: bug"
        expected = {'PRIORITY': 'high', 'TYPE': 'bug'}
        self.assertEqual(parse_metadata(metadata_str), expected)

    def test_parse_metadata_mixed_case_keys(self):
        metadata_str = "priority: high, Type: bug, assignee: johndoe"
        expected = {'PRIORITY': 'high', 'TYPE': 'bug', 'ASSIGNEE': 'johndoe'}
        self.assertEqual(parse_metadata(metadata_str), expected)

    def test_parse_metadata_empty(self):
        self.assertEqual(parse_metadata(""), {})
        self.assertEqual(parse_metadata(None), {})

    def test_extract_labels(self):
        metadata = {'PRIORITY': 'critical', 'TYPE': 'security', 'EPIC': 'auth-rewrite'}
        labels = extract_labels_from_metadata(metadata, self.default_config)
        
        self.assertIn('todo', labels)
        self.assertIn('priority:critical', labels)
        self.assertIn('type:security', labels)
        self.assertIn('epic:auth-rewrite', labels)

    def test_extract_labels_unknown_values(self):
        metadata = {'PRIORITY': 'super-duper-high', 'TYPE': 'unicorn'}
        labels = extract_labels_from_metadata(metadata, self.default_config)
        
        # Should only have defaults
        self.assertEqual(labels, ['todo', 'tech-debt'])

    def test_similarity_ratio(self):
        s1 = "Fix login bug"
        s2 = "Fix login bugs"
        # Should be very similar
        self.assertGreater(similarity_ratio(s1, s2), 0.9)
        
        s3 = "Rewrite database"
        self.assertLess(similarity_ratio(s1, s3), 0.5)

    def test_find_duplicate(self):
        existing = ["Fix navigation menu", "Update user profile"]
        
        # Exact match / High similarity
        match = find_duplicate("Fix navigation menus", existing, threshold=0.8)
        self.assertEqual(match, "Fix navigation menu")
        
        # No match
        match = find_duplicate("Delete user account", existing, threshold=0.8)
        self.assertIsNone(match)

if __name__ == '__main__':
    unittest.main()
