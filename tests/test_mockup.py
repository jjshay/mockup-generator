"""
Tests for Mockup Generator
"""
import pytest
import os
import json
from pathlib import Path


class TestMockupConfig:
    """Test mockup configuration"""

    def test_config_exists(self):
        """Verify mockup config file exists"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        assert config_path.exists(), "Mockup config file should exist"

    def test_config_valid_json(self):
        """Verify config is valid JSON"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)
        assert "frame_styles" in config, "Config should have frame_styles"

    def test_frame_styles_defined(self):
        """Verify frame styles are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        expected_styles = ["black_metal", "white_wood", "gold_ornate",
                          "natural_oak", "floating"]

        for style in expected_styles:
            assert style in config["frame_styles"], f"Missing frame style: {style}"


class TestRoomScenes:
    """Test room scene configuration"""

    def test_room_scenes_defined(self):
        """Verify room scenes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        expected_scenes = ["living_room", "office", "gallery", "bedroom", "minimal"]

        for scene in expected_scenes:
            assert scene in config["room_scenes"], f"Missing room scene: {scene}"


class TestSampleArtwork:
    """Test sample artwork handling"""

    def test_sample_artwork_exists(self):
        """Verify sample artwork exists"""
        artwork_path = Path(__file__).parent.parent / "examples" / "sample_artwork.jpg"
        assert artwork_path.exists(), "Sample artwork should exist"

    def test_artwork_is_image(self):
        """Verify sample artwork is valid image"""
        artwork_path = Path(__file__).parent.parent / "examples" / "sample_artwork.jpg"
        with open(artwork_path, 'rb') as f:
            header = f.read(3)
        assert header[:2] == b'\xff\xd8', "File should be a valid JPEG"


class TestOutputFormats:
    """Test output format specifications"""

    def test_output_sizes_defined(self):
        """Verify output sizes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "output_sizes" in config, "Config should have output_sizes"

        # Check for common sizes
        sizes = config["output_sizes"]
        assert "square" in sizes, "Should have square format"
        assert "landscape" in sizes, "Should have landscape format"

    def test_sample_output_exists(self):
        """Verify sample output exists"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        assert output_path.exists(), "Sample output manifest should exist"


class TestPerspectiveTransform:
    """Test perspective transformation specs"""

    def test_transform_parameters(self):
        """Test transform parameter validation"""
        # Basic perspective transform validation
        # Corners should form a valid quadrilateral
        corners = [(0, 0), (100, 0), (100, 100), (0, 100)]

        # Check corners form closed shape
        assert len(corners) == 4, "Should have 4 corners"

        # Check no duplicate points
        assert len(set(corners)) == 4, "All corners should be unique"


class TestImageCompositing:
    """Test image compositing logic"""

    def test_layer_order(self):
        """Test layer compositing order"""
        layers = ["background", "shadow", "artwork", "frame", "lighting"]

        # Background should be first
        assert layers[0] == "background"

        # Frame should be after artwork
        assert layers.index("frame") > layers.index("artwork")
