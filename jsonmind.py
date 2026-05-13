#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 JSONMind - Lightweight JSON Data Intelligence Processing & Visualization Engine
轻量级JSON数据智能处理与可视化引擎

A powerful CLI tool for JSON validation, transformation, querying, and visualization.
支持JSON验证、转换、查询、可视化的强大CLI工具。

Author: JSONMind Team
License: MIT
Version: 1.0.0
"""

import json
import sys
import os
import re
import argparse
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Union, Optional, Tuple
from datetime import datetime
from collections import Counter
import html


class JSONMindError(Exception):
    """Base exception for JSONMind"""
    pass


class JSONValidator:
    """JSON validation and schema checking"""
    
    @staticmethod
    def validate(json_data: Union[str, dict]) -> Tuple[bool, List[str]]:
        """
        Validate JSON data and return detailed error messages
        验证JSON数据并返回详细错误信息
        """
        errors = []
        
        if isinstance(json_data, str):
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                errors.append(f"❌ JSON解析错误: {e}")
                return False, errors
        else:
            data = json_data
        
        # Check for common issues
        issues = JSONValidator._check_common_issues(data)
        errors.extend(issues)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _check_common_issues(data: Any, path: str = "root") -> List[str]:
        """Check for common JSON issues"""
        issues = []
        
        if isinstance(data, dict):
            # Check for empty keys
            for key in data.keys():
                if not key or not isinstance(key, str):
                    issues.append(f"⚠️  [{path}] 存在空键或非字符串键")
                # Check for duplicate keys (Python handles this, but it's bad practice)
            
            # Check for null values
            for key, value in data.items():
                if value is None:
                    issues.append(f"ℹ️  [{path}.{key}] 值为 null")
                elif isinstance(value, (dict, list)):
                    issues.extend(JSONValidator._check_common_issues(value, f"{path}.{key}"))
                    
        elif isinstance(data, list):
            if len(data) == 0:
                issues.append(f"ℹ️  [{path}] 空数组")
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    issues.extend(JSONValidator._check_common_issues(item, f"{path}[{i}]"))
        
        return issues
    
    @staticmethod
    def get_stats(data: Union[str, dict]) -> Dict[str, Any]:
        """Get comprehensive JSON statistics"""
        if isinstance(data, str):
            data = json.loads(data)
        
        stats = {
            "total_keys": 0,
            "total_arrays": 0,
            "total_objects": 0,
            "total_strings": 0,
            "total_numbers": 0,
            "total_booleans": 0,
            "total_nulls": 0,
            "max_depth": 0,
            "total_size_bytes": len(json.dumps(data).encode('utf-8')),
            "key_types": Counter(),
            "sample_keys": []
        }
        
        def traverse(obj, depth=0):
            stats["max_depth"] = max(stats["max_depth"], depth)
            
            if isinstance(obj, dict):
                stats["total_objects"] += 1
                for key, value in obj.items():
                    stats["total_keys"] += 1
                    stats["key_types"][type(value).__name__] += 1
                    if len(stats["sample_keys"]) < 20:
                        stats["sample_keys"].append(key)
                    traverse(value, depth + 1)
                    
            elif isinstance(obj, list):
                stats["total_arrays"] += 1
                for item in obj:
                    traverse(item, depth + 1)
                    
            elif isinstance(obj, str):
                stats["total_strings"] += 1
            elif isinstance(obj, (int, float)):
                stats["total_numbers"] += 1
            elif isinstance(obj, bool):
                stats["total_booleans"] += 1
            elif obj is None:
                stats["total_nulls"] += 1
        
        traverse(data)
        return stats


class JSONQuery:
    """JSONPath-like query engine"""
    
    @staticmethod
    def query(data: Union[str, dict], query_path: str) -> List[Any]:
        """
        Simple JSONPath-like query
        支持简单的JSONPath风格查询
        
        Examples:
            $.store.book[0].title
            $.store.book[*].author
            $..price
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        if query_path == '$':
            return [data]
        
        # Handle recursive descent pattern first (e.g., "$..price")
        if '..' in query_path:
            # Remove leading $ if present
            key = query_path.lstrip('$..')
            results = []
            JSONQuery._recursive_search(data, key, results)
            return results
        
        # Remove leading $
        path = query_path.lstrip('$').lstrip('.')
        
        results = []
        JSONQuery._traverse_query(data, path.split('.'), 0, results)
        return results
    
    @staticmethod
    def _traverse_query(obj: Any, parts: List[str], index: int, results: List[Any]):
        """Traverse object according to query parts"""
        if index >= len(parts):
            results.append(obj)
            return
        
        part = parts[index]
        
        # Handle array indexing like book[0] or book[*]
        array_match = re.match(r'(\w+)\[(\*|\d+)\]', part)
        if array_match:
            key = array_match.group(1)
            idx = array_match.group(2)
            
            if isinstance(obj, dict) and key in obj:
                arr = obj[key]
                if isinstance(arr, list):
                    if idx == '*':
                        for item in arr:
                            JSONQuery._traverse_query(item, parts, index + 1, results)
                    else:
                        i = int(idx)
                        if 0 <= i < len(arr):
                            JSONQuery._traverse_query(arr[i], parts, index + 1, results)
        
        # Handle recursive descent like ..price
        elif part.startswith('..'):
            key = part[2:]
            JSONQuery._recursive_search(obj, key, results)
        
        # Handle wildcard *
        elif part == '*':
            if isinstance(obj, dict):
                for value in obj.values():
                    JSONQuery._traverse_query(value, parts, index + 1, results)
            elif isinstance(obj, list):
                for item in obj:
                    JSONQuery._traverse_query(item, parts, index + 1, results)
        
        # Normal key access
        elif isinstance(obj, dict) and part in obj:
            JSONQuery._traverse_query(obj[part], parts, index + 1, results)
    
    @staticmethod
    def _recursive_search(obj: Any, key: str, results: List[Any]):
        """Recursively search for key"""
        if isinstance(obj, dict):
            if key in obj:
                results.append(obj[key])
            for value in obj.values():
                JSONQuery._recursive_search(value, key, results)
        elif isinstance(obj, list):
            for item in obj:
                JSONQuery._recursive_search(item, key, results)


class JSONTransformer:
    """JSON transformation utilities"""
    
    @staticmethod
    def flatten(data: Union[str, dict], separator: str = '.') -> Dict[str, Any]:
        """
        Flatten nested JSON structure
        扁平化嵌套JSON结构
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        result = {}
        
        def _flatten(obj, prefix=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_key = f"{prefix}{separator}{key}" if prefix else key
                    _flatten(value, new_key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_key = f"{prefix}[{i}]"
                    _flatten(item, new_key)
            else:
                result[prefix] = obj
        
        _flatten(data)
        return result
    
    @staticmethod
    def unflatten(flat_data: Dict[str, Any], separator: str = '.') -> Any:
        """
        Unflatten flattened JSON structure
        反扁平化JSON结构
        """
        result = {}
        
        for key, value in flat_data.items():
            parts = key.split(separator)
            target = result
            
            for part in parts[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            
            target[parts[-1]] = value
        
        return result
    
    @staticmethod
    def to_csv(data: Union[str, list], output_path: str):
        """Convert JSON array to CSV"""
        if isinstance(data, str):
            data = json.loads(data)
        
        if not isinstance(data, list) or len(data) == 0:
            raise JSONMindError("JSON must be a non-empty array for CSV conversion")
        
        # Flatten each object
        flattened = [JSONTransformer.flatten(item) for item in data]
        
        # Get all unique keys
        all_keys = set()
        for item in flattened:
            all_keys.update(item.keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(flattened)
    
    @staticmethod
    def to_xml(data: Union[str, dict], root_name: str = 'root') -> str:
        """Convert JSON to XML"""
        if isinstance(data, str):
            data = json.loads(data)
        
        def _to_xml(obj, name):
            elem = ET.Element(name)
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    child = _to_xml(value, key)
                    elem.append(child)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    child = _to_xml(item, 'item')
                    child.set('index', str(i))
                    elem.append(child)
            else:
                elem.text = str(obj)
                elem.set('type', type(obj).__name__)
            
            return elem
        
        root = _to_xml(data, root_name)
        return ET.tostring(root, encoding='unicode')
    
    @staticmethod
    def sort_keys(data: Union[str, dict], reverse: bool = False) -> Any:
        """Recursively sort all object keys"""
        if isinstance(data, str):
            data = json.loads(data)
        
        if isinstance(data, dict):
            return {k: JSONTransformer.sort_keys(v, reverse) 
                    for k, v in sorted(data.items(), reverse=reverse)}
        elif isinstance(data, list):
            return [JSONTransformer.sort_keys(item, reverse) for item in data]
        else:
            return data


class JSONVisualizer:
    """JSON visualization and formatting"""
    
    @staticmethod
    def format_json(data: Union[str, dict], indent: int = 2, 
                    sort_keys: bool = False) -> str:
        """Format JSON with customizable indentation"""
        if isinstance(data, str):
            data = json.loads(data)
        
        return json.dumps(data, indent=indent, ensure_ascii=False, 
                         sort_keys=sort_keys, separators=(',', ': '))
    
    @staticmethod
    def to_tree_view(data: Union[str, dict], max_depth: int = 10) -> str:
        """
        Generate ASCII tree view of JSON structure
        生成JSON结构的ASCII树形视图
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        lines = []
        
        def _tree(obj, prefix='', is_last=True, depth=0):
            if depth > max_depth:
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}... (max depth reached)")
                return
            
            connector = '└── ' if is_last else '├── '
            
            if isinstance(obj, dict):
                items = list(obj.items())
                for i, (key, value) in enumerate(items):
                    is_last_item = i == len(items) - 1
                    lines.append(f"{prefix}{connector}{key}")
                    
                    extension = '    ' if is_last_item else '│   '
                    _tree(value, prefix + extension, is_last_item, depth + 1)
                    
            elif isinstance(obj, list):
                if len(obj) == 0:
                    lines.append(f"{prefix}{connector}[ ] (empty array)")
                else:
                    for i, item in enumerate(obj[:10]):  # Limit to first 10
                        is_last_item = i == min(len(obj), 10) - 1
                        lines.append(f"{prefix}{connector}[{i}]")
                        
                        extension = '    ' if is_last_item else '│   '
                        _tree(item, prefix + extension, is_last_item, depth + 1)
                    
                    if len(obj) > 10:
                        lines.append(f"{prefix}{'    ' if is_last else '│   '}└── ... ({len(obj) - 10} more items)")
            else:
                value_str = str(obj)
                if len(value_str) > 50:
                    value_str = value_str[:50] + '...'
                lines.append(f"{prefix}{connector}{value_str} ({type(obj).__name__})")
        
        _tree(data)
        return '\n'.join(lines)
    
    @staticmethod
    def to_html_table(data: Union[str, list], title: str = "JSON Data") -> str:
        """Convert JSON array to HTML table"""
        if isinstance(data, str):
            data = json.loads(data)
        
        if not isinstance(data, list):
            data = [data]
        
        # Flatten all items
        flattened = [JSONTransformer.flatten(item) for item in data]
        all_keys = sorted(set().union(*(d.keys() for d in flattened)))
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            f'<title>{html.escape(title)}</title>',
            '<style>',
            'body { font-family: Arial, sans-serif; margin: 20px; }',
            'table { border-collapse: collapse; width: 100%; }',
            'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
            'th { background-color: #4CAF50; color: white; }',
            'tr:nth-child(even) { background-color: #f2f2f2; }',
            '</style>',
            '</head>',
            '<body>',
            f'<h1>{html.escape(title)}</h1>',
            '<table>',
            '<tr>' + ''.join(f'<th>{html.escape(k)}</th>' for k in all_keys) + '</tr>'
        ]
        
        for item in flattened:
            row = ''.join(f'<td>{html.escape(str(item.get(k, "")))}</td>' for k in all_keys)
            html_parts.append(f'<tr>{row}</tr>')
        
        html_parts.extend([
            '</table>',
            '</body>',
            '</html>'
        ])
        
        return '\n'.join(html_parts)
    
    @staticmethod
    def generate_diff(json1: Union[str, dict], json2: Union[str, dict]) -> List[Dict[str, Any]]:
        """
        Generate diff between two JSON objects
        生成两个JSON对象的差异对比
        """
        if isinstance(json1, str):
            json1 = json.loads(json1)
        if isinstance(json2, str):
            json2 = json.loads(json2)
        
        diffs = []
        
        def _compare(obj1, obj2, path=''):
            if type(obj1) != type(obj2):
                diffs.append({
                    'path': path or 'root',
                    'type': 'type_changed',
                    'old': f"{type(obj1).__name__}: {obj1}",
                    'new': f"{type(obj2).__name__}: {obj2}"
                })
            elif isinstance(obj1, dict):
                all_keys = set(obj1.keys()) | set(obj2.keys())
                for key in all_keys:
                    new_path = f"{path}.{key}" if path else key
                    if key not in obj1:
                        diffs.append({'path': new_path, 'type': 'added', 'value': obj2[key]})
                    elif key not in obj2:
                        diffs.append({'path': new_path, 'type': 'removed', 'value': obj1[key]})
                    else:
                        _compare(obj1[key], obj2[key], new_path)
            elif isinstance(obj1, list):
                if len(obj1) != len(obj2):
                    diffs.append({
                        'path': path or 'root',
                        'type': 'array_length_changed',
                        'old_length': len(obj1),
                        'new_length': len(obj2)
                    })
                for i in range(min(len(obj1), len(obj2))):
                    _compare(obj1[i], obj2[i], f"{path}[{i}]")
            elif obj1 != obj2:
                diffs.append({'path': path or 'root', 'type': 'modified', 'old': obj1, 'new': obj2})
        
        _compare(json1, json2)
        return diffs


class JSONMindCLI:
    """Command Line Interface for JSONMind"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog='jsonmind',
            description='🧠 JSONMind - Lightweight JSON Data Intelligence Processing Engine',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  jsonmind validate data.json              # Validate JSON file
  jsonmind stats data.json                 # Show JSON statistics
  jsonmind format data.json -o pretty.json # Format JSON file
  jsonmind query data.json '$.users[*].name' # Query JSON data
  jsonmind flatten data.json -o flat.json  # Flatten nested JSON
  jsonmind tree data.json                  # Show tree view
  jsonmind csv data.json -o data.csv       # Convert to CSV
  jsonmind diff file1.json file2.json      # Compare two JSON files
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate JSON file')
        validate_parser.add_argument('file', help='JSON file to validate')
        validate_parser.add_argument('-v', '--verbose', action='store_true', 
                                     help='Show detailed validation info')
        
        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show JSON statistics')
        stats_parser.add_argument('file', help='JSON file to analyze')
        stats_parser.add_argument('-f', '--format', choices=['text', 'json'], 
                                  default='text', help='Output format')
        
        # Format command
        format_parser = subparsers.add_parser('format', help='Format JSON file')
        format_parser.add_argument('file', help='JSON file to format')
        format_parser.add_argument('-o', '--output', help='Output file')
        format_parser.add_argument('-i', '--indent', type=int, default=2, 
                                   help='Indentation spaces (default: 2)')
        format_parser.add_argument('-s', '--sort-keys', action='store_true', 
                                   help='Sort object keys')
        
        # Query command
        query_parser = subparsers.add_parser('query', help='Query JSON data')
        query_parser.add_argument('file', help='JSON file to query')
        query_parser.add_argument('query', help='Query path (e.g., $.users[*].name)')
        query_parser.add_argument('-o', '--output', help='Output file')
        
        # Flatten command
        flatten_parser = subparsers.add_parser('flatten', help='Flatten nested JSON')
        flatten_parser.add_argument('file', help='JSON file to flatten')
        flatten_parser.add_argument('-o', '--output', help='Output file')
        flatten_parser.add_argument('-s', '--separator', default='.', 
                                    help='Key separator (default: .)')
        
        # Tree command
        tree_parser = subparsers.add_parser('tree', help='Show JSON tree view')
        tree_parser.add_argument('file', help='JSON file to display')
        tree_parser.add_argument('-d', '--max-depth', type=int, default=10, 
                                 help='Maximum depth to display')
        
        # CSV command
        csv_parser = subparsers.add_parser('csv', help='Convert JSON to CSV')
        csv_parser.add_argument('file', help='JSON file to convert')
        csv_parser.add_argument('-o', '--output', required=True, help='Output CSV file')
        
        # XML command
        xml_parser = subparsers.add_parser('xml', help='Convert JSON to XML')
        xml_parser.add_argument('file', help='JSON file to convert')
        xml_parser.add_argument('-o', '--output', help='Output XML file')
        xml_parser.add_argument('-r', '--root', default='root', help='Root element name')
        
        # HTML command
        html_parser = subparsers.add_parser('html', help='Convert JSON to HTML table')
        html_parser.add_argument('file', help='JSON file to convert')
        html_parser.add_argument('-o', '--output', required=True, help='Output HTML file')
        html_parser.add_argument('-t', '--title', default='JSON Data', help='Page title')
        
        # Diff command
        diff_parser = subparsers.add_parser('diff', help='Compare two JSON files')
        diff_parser.add_argument('file1', help='First JSON file')
        diff_parser.add_argument('file2', help='Second JSON file')
        diff_parser.add_argument('-o', '--output', help='Output file')
        diff_parser.add_argument('-f', '--format', choices=['text', 'json'], 
                                 default='text', help='Output format')
        
        return parser
    
    def _load_json(self, filepath: str) -> Any:
        """Load JSON from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise JSONMindError(f"❌ File not found: {filepath}")
        except json.JSONDecodeError as e:
            raise JSONMindError(f"❌ Invalid JSON in {filepath}: {e}")
    
    def _save_output(self, data: Any, output_path: Optional[str] = None, 
                     is_json: bool = True):
        """Save output to file or print to stdout"""
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                if is_json:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    f.write(str(data))
            print(f"✅ Output saved to: {output_path}")
        else:
            if is_json:
                print(json.dumps(data, indent=2, ensure_ascii=False))
            else:
                print(data)
    
    def run(self, args: Optional[List[str]] = None):
        """Run CLI with arguments"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        try:
            if parsed_args.command == 'validate':
                self._cmd_validate(parsed_args)
            elif parsed_args.command == 'stats':
                self._cmd_stats(parsed_args)
            elif parsed_args.command == 'format':
                self._cmd_format(parsed_args)
            elif parsed_args.command == 'query':
                self._cmd_query(parsed_args)
            elif parsed_args.command == 'flatten':
                self._cmd_flatten(parsed_args)
            elif parsed_args.command == 'tree':
                self._cmd_tree(parsed_args)
            elif parsed_args.command == 'csv':
                self._cmd_csv(parsed_args)
            elif parsed_args.command == 'xml':
                self._cmd_xml(parsed_args)
            elif parsed_args.command == 'html':
                self._cmd_html(parsed_args)
            elif parsed_args.command == 'diff':
                self._cmd_diff(parsed_args)
                
        except JSONMindError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _cmd_validate(self, args):
        """Handle validate command"""
        data = self._load_json(args.file)
        is_valid, errors = JSONValidator.validate(data)
        
        if is_valid:
            print("✅ JSON is valid!")
            if args.verbose:
                stats = JSONValidator.get_stats(data)
                print(f"\n📊 Statistics:")
                print(f"   • Total keys: {stats['total_keys']}")
                print(f"   • Objects: {stats['total_objects']}")
                print(f"   • Arrays: {stats['total_arrays']}")
                print(f"   • Max depth: {stats['max_depth']}")
        else:
            print("❌ JSON validation failed!")
            for error in errors:
                print(f"   {error}")
    
    def _cmd_stats(self, args):
        """Handle stats command"""
        data = self._load_json(args.file)
        stats = JSONValidator.get_stats(data)
        
        if args.format == 'json':
            self._save_output(stats)
        else:
            print("📊 JSON Statistics")
            print("=" * 50)
            print(f"📦 Total Size: {stats['total_size_bytes']:,} bytes")
            print(f"🔑 Total Keys: {stats['total_keys']}")
            print(f"📁 Objects: {stats['total_objects']}")
            print(f"📋 Arrays: {stats['total_arrays']}")
            print(f"📝 Strings: {stats['total_strings']}")
            print(f"🔢 Numbers: {stats['total_numbers']}")
            print(f"✅ Booleans: {stats['total_booleans']}")
            print(f"⚪ Nulls: {stats['total_nulls']}")
            print(f"📏 Max Depth: {stats['max_depth']}")
            print("\n📈 Key Types Distribution:")
            for type_name, count in stats['key_types'].most_common():
                print(f"   • {type_name}: {count}")
    
    def _cmd_format(self, args):
        """Handle format command"""
        data = self._load_json(args.file)
        formatted = JSONVisualizer.format_json(data, args.indent, args.sort_keys)
        self._save_output(formatted, args.output, is_json=False)
    
    def _cmd_query(self, args):
        """Handle query command"""
        data = self._load_json(args.file)
        results = JSONQuery.query(data, args.query)
        self._save_output(results, args.output)
    
    def _cmd_flatten(self, args):
        """Handle flatten command"""
        data = self._load_json(args.file)
        flattened = JSONTransformer.flatten(data, args.separator)
        self._save_output(flattened, args.output)
    
    def _cmd_tree(self, args):
        """Handle tree command"""
        data = self._load_json(args.file)
        tree_view = JSONVisualizer.to_tree_view(data, args.max_depth)
        print(tree_view)
    
    def _cmd_csv(self, args):
        """Handle csv command"""
        data = self._load_json(args.file)
        JSONTransformer.to_csv(data, args.output)
        print(f"✅ CSV saved to: {args.output}")
    
    def _cmd_xml(self, args):
        """Handle xml command"""
        data = self._load_json(args.file)
        xml_output = JSONTransformer.to_xml(data, args.root)
        self._save_output(xml_output, args.output, is_json=False)
    
    def _cmd_html(self, args):
        """Handle html command"""
        data = self._load_json(args.file)
        html_output = JSONVisualizer.to_html_table(data, args.title)
        self._save_output(html_output, args.output, is_json=False)
    
    def _cmd_diff(self, args):
        """Handle diff command"""
        data1 = self._load_json(args.file1)
        data2 = self._load_json(args.file2)
        diffs = JSONVisualizer.generate_diff(data1, data2)
        
        if args.format == 'json':
            self._save_output(diffs, args.output)
        else:
            if not diffs:
                print("✅ No differences found!")
            else:
                print(f"🔍 Found {len(diffs)} difference(s):\n")
                for diff in diffs:
                    print(f"📍 Path: {diff['path']}")
                    print(f"   Type: {diff['type']}")
                    if 'old' in diff and 'new' in diff:
                        print(f"   - {diff['old']}")
                        print(f"   + {diff['new']}")
                    elif 'value' in diff:
                        print(f"   Value: {diff['value']}")
                    print()


def main():
    """Main entry point"""
    cli = JSONMindCLI()
    cli.run()


if __name__ == '__main__':
    main()
