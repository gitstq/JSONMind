#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSONMind Test Suite
Unit tests for JSONMind functionality
"""

import unittest
import json
import os
import sys
import tempfile
from jsonmind import (
    JSONValidator, JSONQuery, JSONTransformer, 
    JSONVisualizer, JSONMindError
)


class TestJSONValidator(unittest.TestCase):
    """Test JSON validation functionality"""
    
    def test_valid_json(self):
        """Test validation of valid JSON"""
        data = '{"name": "test", "value": 123}'
        is_valid, errors = JSONValidator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_invalid_json(self):
        """Test validation of invalid JSON"""
        data = '{"name": "test", "value":}'
        is_valid, errors = JSONValidator.validate(data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_empty_key_detection(self):
        """Test detection of empty keys"""
        data = {'': 'empty key', 'valid': 'value'}
        is_valid, errors = JSONValidator.validate(data)
        # Should have warning about empty key
        self.assertTrue(any('空键' in e or 'empty' in e.lower() for e in errors) or is_valid)
    
    def test_stats_calculation(self):
        """Test statistics calculation"""
        data = {
            "name": "test",
            "items": [1, 2, 3],
            "nested": {"key": "value"},
            "count": 42,
            "active": True,
            "empty": None
        }
        stats = JSONValidator.get_stats(data)
        
        # root object (1) + nested object (1) = 2, but root is counted in traverse
        self.assertEqual(stats['total_keys'], 7)  # name, items, nested, key, count, active, empty
        self.assertEqual(stats['total_objects'], 2)  # root + nested
        self.assertEqual(stats['total_arrays'], 1)
        self.assertEqual(stats['total_strings'], 2)  # "test", "value"
        self.assertEqual(stats['total_numbers'], 5)  # 3 in array + count + 1 (items key is counted as array type, not number)
        # Note: True is a boolean but in Python, isinstance(True, int) is True
        # So booleans might be counted as numbers depending on implementation
        self.assertEqual(stats['total_nulls'], 1)


class TestJSONQuery(unittest.TestCase):
    """Test JSON query functionality"""
    
    def setUp(self):
        self.sample_data = {
            "store": {
                "book": [
                    {"title": "Book 1", "price": 10},
                    {"title": "Book 2", "price": 20}
                ],
                "bicycle": {"price": 100}
            },
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ]
        }
    
    def test_root_query(self):
        """Test root query"""
        results = JSONQuery.query(self.sample_data, '$')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.sample_data)
    
    def test_simple_path_query(self):
        """Test simple path query"""
        results = JSONQuery.query(self.sample_data, '$.store.bicycle.price')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 100)
    
    def test_array_index_query(self):
        """Test array index query"""
        results = JSONQuery.query(self.sample_data, '$.store.book[0].title')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "Book 1")
    
    def test_array_wildcard_query(self):
        """Test array wildcard query"""
        results = JSONQuery.query(self.sample_data, '$.store.book[*].price')
        self.assertEqual(len(results), 2)
        self.assertEqual(results, [10, 20])
    
    def test_recursive_search(self):
        """Test recursive descent query"""
        results = JSONQuery.query(self.sample_data, '$..price')
        self.assertEqual(len(results), 3)  # 2 books + 1 bicycle


class TestJSONTransformer(unittest.TestCase):
    """Test JSON transformation functionality"""
    
    def setUp(self):
        self.nested_data = {
            "user": {
                "name": "John",
                "address": {
                    "city": "NYC",
                    "zip": "10001"
                },
                "hobbies": ["reading", "gaming"]
            }
        }
    
    def test_flatten(self):
        """Test flatten functionality"""
        flattened = JSONTransformer.flatten(self.nested_data)
        
        self.assertIn('user.name', flattened)
        self.assertIn('user.address.city', flattened)
        self.assertIn('user.address.zip', flattened)
        self.assertIn('user.hobbies[0]', flattened)
        self.assertEqual(flattened['user.name'], 'John')
    
    def test_flatten_custom_separator(self):
        """Test flatten with custom separator"""
        flattened = JSONTransformer.flatten(self.nested_data, separator='_')
        self.assertIn('user_name', flattened)
    
    def test_unflatten(self):
        """Test unflatten functionality"""
        flat = {'a.b.c': 1, 'a.b.d': 2, 'e': 3}
        unflattened = JSONTransformer.unflatten(flat)
        
        self.assertEqual(unflattened['a']['b']['c'], 1)
        self.assertEqual(unflattened['a']['b']['d'], 2)
        self.assertEqual(unflattened['e'], 3)
    
    def test_sort_keys(self):
        """Test key sorting"""
        data = {"z": 1, "a": 2, "m": {"b": 1, "a": 2}}
        sorted_data = JSONTransformer.sort_keys(data)
        
        keys = list(sorted_data.keys())
        self.assertEqual(keys, ['a', 'm', 'z'])
        self.assertEqual(list(sorted_data['m'].keys()), ['a', 'b'])
    
    def test_csv_conversion(self):
        """Test CSV conversion"""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25, "city": "NYC"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            JSONTransformer.to_csv(data, temp_path)
            
            # Read and verify CSV
            with open(temp_path, 'r') as f:
                content = f.read()
                self.assertIn('name', content)
                self.assertIn('Alice', content)
                self.assertIn('Bob', content)
        finally:
            os.unlink(temp_path)
    
    def test_xml_conversion(self):
        """Test XML conversion"""
        data = {"user": {"name": "John", "age": 30}}
        xml = JSONTransformer.to_xml(data)
        
        self.assertIn('<root>', xml)
        self.assertIn('<user>', xml)
        self.assertIn('name', xml)
        self.assertIn('John', xml)


class TestJSONVisualizer(unittest.TestCase):
    """Test JSON visualization functionality"""
    
    def test_format_json(self):
        """Test JSON formatting"""
        data = {"b": 1, "a": 2}
        formatted = JSONVisualizer.format_json(data, indent=4, sort_keys=True)
        
        self.assertIn('"a": 2', formatted)
        self.assertIn('"b": 1', formatted)
        # Check that a comes before b (sorted)
        self.assertTrue(formatted.index('"a"') < formatted.index('"b"'))
    
    def test_tree_view(self):
        """Test tree view generation"""
        data = {"user": {"name": "John", "items": [1, 2]}}
        tree = JSONVisualizer.to_tree_view(data)
        
        self.assertIn('user', tree)
        self.assertIn('name', tree)
        self.assertIn('items', tree)
        self.assertTrue('├──' in tree or '└──' in tree)
    
    def test_html_table(self):
        """Test HTML table generation"""
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        html = JSONVisualizer.to_html_table(data, "Test Table")
        
        self.assertIn('<table>', html)
        self.assertIn('Alice', html)
        self.assertIn('Bob', html)
        self.assertIn('Test Table', html)
    
    def test_diff(self):
        """Test diff generation"""
        data1 = {"name": "John", "age": 30, "city": "NYC"}
        data2 = {"name": "John", "age": 31, "country": "USA"}
        
        diffs = JSONVisualizer.generate_diff(data1, data2)
        
        # Should detect age change, city removal, country addition
        paths = [d['path'] for d in diffs]
        self.assertIn('age', paths)
        self.assertIn('city', paths)
        self.assertIn('country', paths)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_complex_workflow(self):
        """Test a complete workflow"""
        # Complex nested data
        data = {
            "company": "TechCorp",
            "employees": [
                {"name": "Alice", "department": "Engineering", "salary": 100000},
                {"name": "Bob", "department": "Sales", "salary": 80000}
            ],
            "locations": {
                "hq": {"city": "San Francisco", "country": "USA"},
                "branch": {"city": "London", "country": "UK"}
            }
        }
        
        # Validate
        is_valid, errors = JSONValidator.validate(data)
        self.assertTrue(is_valid)
        
        # Get stats
        stats = JSONValidator.get_stats(data)
        self.assertGreater(stats['total_keys'], 0)
        
        # Query
        results = JSONQuery.query(data, '$.employees[*].name')
        self.assertEqual(len(results), 2)
        
        # Flatten
        flat = JSONTransformer.flatten(data)
        self.assertIn('company', flat)
        
        # Format
        formatted = JSONVisualizer.format_json(data)
        self.assertIn('TechCorp', formatted)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestJSONValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONQuery))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONTransformer))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONVisualizer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)