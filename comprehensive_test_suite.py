#!/usr/bin/env python3
"""
Comprehensive Test Suite for Data Visualization Repository
Tests all Python files for syntax, imports, and execution
"""

import os
import sys
import ast
import importlib.util
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
import json

class ComprehensiveTestSuite:
    def __init__(self, directory="."):
        self.directory = Path(directory)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "syntax_errors": [],
            "import_errors": [],
            "execution_results": [],
            "dependency_check": {},
            "summary": {}
        }

    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80 + "\n")

    def print_section(self, text):
        """Print formatted section"""
        print("\n" + "-" * 80)
        print(f"  {text}")
        print("-" * 80 + "\n")

    def find_all_python_files(self):
        """Find all Python files in the directory"""
        python_files = sorted(self.directory.glob("*.py"))
        # Exclude this test file itself
        python_files = [f for f in python_files if f.name != "comprehensive_test_suite.py"]
        return python_files

    def check_syntax(self, file_path):
        """Check Python syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return True, None
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error reading file: {str(e)}"

    def check_imports(self, file_path):
        """Check if file imports can be resolved"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source)
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])

            return True, imports, None
        except Exception as e:
            return False, [], str(e)

    def check_dependencies(self, all_imports):
        """Check which dependencies are available"""
        unique_imports = set(all_imports)
        available = {}

        for module in sorted(unique_imports):
            try:
                __import__(module)
                available[module] = "✓ Available"
            except ImportError:
                available[module] = "✗ Missing"
            except Exception as e:
                available[module] = f"✗ Error: {str(e)}"

        return available

    def run_test_files(self):
        """Run specific test files"""
        test_files = [
            "testing_magnetic_force.py",
            "3D_testing_magnetic_force_visualization.py"
        ]

        results = []
        for test_file in test_files:
            file_path = self.directory / test_file
            if not file_path.exists():
                results.append({
                    "file": test_file,
                    "status": "not_found",
                    "output": "File does not exist"
                })
                continue

            try:
                # Run in non-interactive mode to avoid display issues
                result = subprocess.run(
                    [sys.executable, str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    env={**os.environ, "MPLBACKEND": "Agg"}
                )

                results.append({
                    "file": test_file,
                    "status": "completed" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                })
            except subprocess.TimeoutExpired:
                results.append({
                    "file": test_file,
                    "status": "timeout",
                    "output": "Execution exceeded 30 seconds"
                })
            except Exception as e:
                results.append({
                    "file": test_file,
                    "status": "error",
                    "output": str(e)
                })

        return results

    def run_sample_files(self, sample_size=5):
        """Run a sample of visualization files"""
        all_files = self.find_all_python_files()
        # Exclude test files
        viz_files = [f for f in all_files if "test" not in f.name.lower()]

        # Select sample files
        import random
        random.seed(42)  # For reproducibility
        sample_files = random.sample(viz_files, min(sample_size, len(viz_files)))

        results = []
        for file_path in sample_files:
            try:
                result = subprocess.run(
                    [sys.executable, str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env={**os.environ, "MPLBACKEND": "Agg"}
                )

                results.append({
                    "file": file_path.name,
                    "status": "completed" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout_length": len(result.stdout),
                    "stderr_length": len(result.stderr),
                    "has_errors": bool(result.stderr and "Error" in result.stderr)
                })
            except subprocess.TimeoutExpired:
                results.append({
                    "file": file_path.name,
                    "status": "timeout",
                })
            except Exception as e:
                results.append({
                    "file": file_path.name,
                    "status": "error",
                    "error": str(e)
                })

        return results

    def run_comprehensive_test(self):
        """Run all tests"""
        self.print_header("COMPREHENSIVE TEST SUITE - Data Visualization Repository")
        print(f"Test started at: {self.results['timestamp']}")
        print(f"Test directory: {self.directory.absolute()}")

        # Find all Python files
        self.print_section("1. DISCOVERING PYTHON FILES")
        python_files = self.find_all_python_files()
        self.results['total_files'] = len(python_files)
        print(f"Found {len(python_files)} Python files")

        # Check syntax
        self.print_section("2. SYNTAX VALIDATION")
        all_imports = []
        syntax_pass = 0
        syntax_fail = 0

        for file_path in python_files:
            is_valid, error = self.check_syntax(file_path)
            if is_valid:
                syntax_pass += 1
                print(f"✓ {file_path.name}")

                # Also collect imports
                _, imports, _ = self.check_imports(file_path)
                all_imports.extend(imports)
            else:
                syntax_fail += 1
                print(f"✗ {file_path.name}")
                print(f"  Error: {error}")
                self.results['syntax_errors'].append({
                    "file": str(file_path),
                    "error": error
                })

        print(f"\nSyntax Check Summary: {syntax_pass} passed, {syntax_fail} failed")

        # Check dependencies
        self.print_section("3. DEPENDENCY CHECK")
        dependency_status = self.check_dependencies(all_imports)
        self.results['dependency_check'] = dependency_status

        print("Required Dependencies:")
        for module, status in dependency_status.items():
            print(f"  {status:15} {module}")

        # Count missing dependencies
        missing = sum(1 for v in dependency_status.values() if "✗" in v)
        available = len(dependency_status) - missing
        print(f"\nDependency Summary: {available} available, {missing} missing")

        # Run test files
        self.print_section("4. EXECUTING TEST FILES")
        test_results = self.run_test_files()
        self.results['execution_results'] = test_results

        for result in test_results:
            print(f"\nTest File: {result['file']}")
            print(f"Status: {result['status'].upper()}")
            if 'return_code' in result:
                print(f"Return Code: {result['return_code']}")
            if 'stdout' in result and result['stdout']:
                print(f"Output:\n{result['stdout'][:500]}")
            if 'stderr' in result and result['stderr']:
                print(f"Errors:\n{result['stderr'][:500]}")
            if 'output' in result:
                print(f"Info: {result['output']}")

        # Run sample files
        self.print_section("5. SAMPLE EXECUTION TEST (Random 5 Files)")
        sample_results = self.run_sample_files(5)

        for result in sample_results:
            status_symbol = "✓" if result['status'] == "completed" else "✗"
            print(f"{status_symbol} {result['file']:60} - {result['status']}")
            if 'has_errors' in result and result['has_errors']:
                print(f"  Warning: Contains error messages in output")

        # Generate summary
        self.print_section("6. TEST SUMMARY")

        summary = {
            "total_files": len(python_files),
            "syntax_valid": syntax_pass,
            "syntax_errors": syntax_fail,
            "dependencies_available": available,
            "dependencies_missing": missing,
            "test_files_passed": sum(1 for r in test_results if r['status'] == 'completed'),
            "test_files_failed": sum(1 for r in test_results if r['status'] in ['failed', 'error', 'timeout']),
            "sample_files_passed": sum(1 for r in sample_results if r['status'] == 'completed'),
            "sample_files_failed": sum(1 for r in sample_results if r['status'] != 'completed')
        }

        self.results['summary'] = summary

        print(f"Total Python Files: {summary['total_files']}")
        print(f"Syntax Validation: {summary['syntax_valid']} passed, {summary['syntax_errors']} failed")
        print(f"Dependencies: {summary['dependencies_available']} available, {summary['dependencies_missing']} missing")
        print(f"Test Files: {summary['test_files_passed']} passed, {summary['test_files_failed']} failed")
        print(f"Sample Files: {summary['sample_files_passed']} passed, {summary['sample_files_failed']} failed")

        # Calculate overall score
        if summary['total_files'] > 0:
            syntax_score = (summary['syntax_valid'] / summary['total_files']) * 100
            print(f"\nOverall Syntax Health: {syntax_score:.1f}%")

        # Save detailed results
        self.print_section("7. SAVING DETAILED RESULTS")
        results_file = self.directory / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Detailed results saved to: {results_file}")

        self.print_header("TEST SUITE COMPLETED")

        return self.results

if __name__ == "__main__":
    suite = ComprehensiveTestSuite()
    results = suite.run_comprehensive_test()

    # Exit with appropriate code
    if results['summary']['syntax_errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
