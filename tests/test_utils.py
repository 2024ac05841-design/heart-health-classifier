"""
Unit tests for utility functions"""

import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path
import joblib
from src.utils import (
    ensure_dir,
    save_json,
    load_json,
    save_model_artifacts,
    load_model_artifacts,
)


class TestDirectoryOperations:
    """Test suite for directory utility functions"""

    def test_ensure_dir_creates_new_directory(self):
        """Test creating a new directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "test_dir")
            ensure_dir(test_dir)

            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)

    def test_ensure_dir_creates_nested_directories(self):
        """Test creating nested directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "level1", "level2", "level3")
            ensure_dir(test_dir)

            assert os.path.exists(test_dir)
            assert os.path.isdir(test_dir)

    def test_ensure_dir_existing_directory(self):
        """Test that ensure_dir works with existing directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Directory already exists
            ensure_dir(tmpdir)

            # Should not raise any errors
            assert os.path.exists(tmpdir)


class TestJSONOperations:
    """Test suite for JSON utility functions"""

    def test_save_json(self):
        """Test saving dictionary to JSON file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            test_data = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}

            save_json(test_data, filepath)

            assert os.path.exists(filepath)

            # Verify content
            with open(filepath, "r") as f:
                loaded_data = json.load(f)
            assert loaded_data == test_data

    def test_load_json(self):
        """Test loading JSON file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            test_data = {"name": "test", "value": 123}

            # Create test file
            with open(filepath, "w") as f:
                json.dump(test_data, f)

            loaded_data = load_json(filepath)

            assert loaded_data == test_data

    def test_save_and_load_json_roundtrip(self):
        """Test saving and loading JSON maintains data integrity"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "roundtrip.json")
            original_data = {
                "string": "hello",
                "integer": 42,
                "float": 3.14,
                "list": [1, 2, 3],
                "nested": {"a": 1, "b": 2},
            }

            save_json(original_data, filepath)
            loaded_data = load_json(filepath)

            assert loaded_data == original_data


class TestModelArtifacts:
    """Test suite for model artifact functions"""

    @pytest.fixture
    def simple_model(self):
        """Create a simple pickleable model"""
        from sklearn.linear_model import LogisticRegression

        model = LogisticRegression()
        return model

    @pytest.fixture
    def simple_scaler(self):
        """Create a simple pickleable scaler"""
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        return scaler

    @pytest.fixture
    def feature_names(self):
        """Create sample feature names"""
        return ["age", "chol", "trestbps", "thalach"]

    def test_save_model_artifacts(self, simple_model, simple_scaler, feature_names):
        """Test saving model artifacts"""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_model_artifacts(simple_model, simple_scaler, feature_names, tmpdir)

            # Check that all files were created
            assert os.path.exists(os.path.join(tmpdir, "model.pkl"))
            assert os.path.exists(os.path.join(tmpdir, "scaler.pkl"))
            assert os.path.exists(os.path.join(tmpdir, "feature_names.json"))

    def test_save_model_artifacts_creates_directory(
        self, simple_model, simple_scaler, feature_names
    ):
        """Test that save_model_artifacts creates output directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "new_dir")
            save_model_artifacts(simple_model, simple_scaler, feature_names, output_dir)

            assert os.path.exists(output_dir)
            assert os.path.isdir(output_dir)

    def test_load_model_artifacts(self, simple_model, simple_scaler, feature_names):
        """Test loading model artifacts"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save artifacts first
            save_model_artifacts(simple_model, simple_scaler, feature_names, tmpdir)

            # Load artifacts
            artifacts = load_model_artifacts(tmpdir)

            assert "model" in artifacts
            assert "scaler" in artifacts
            assert "feature_names" in artifacts
            assert artifacts["feature_names"] == feature_names

    def test_save_and_load_roundtrip(self, simple_model, simple_scaler, feature_names):
        """Test complete save and load cycle"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Save
            save_model_artifacts(simple_model, simple_scaler, feature_names, tmpdir)

            # Load
            artifacts = load_model_artifacts(tmpdir)

            # Verify all components are present
            assert artifacts["model"] is not None
            assert artifacts["scaler"] is not None
            assert artifacts["feature_names"] == feature_names

    def test_load_model_artifacts_missing_file(self):
        """Test loading artifacts when files are missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                load_model_artifacts(tmpdir)


class TestPathOperations:
    """Test suite for path-related utilities"""

    def test_ensure_dir_with_pathlib(self):
        """Test ensure_dir works with Path objects"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "subdir" / "nested"
            ensure_dir(str(test_path))

            assert test_path.exists()
            assert test_path.is_dir()
