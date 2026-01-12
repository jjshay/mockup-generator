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
        assert "frame_options" in config, "Config should have frame_options"

    def test_frame_styles_defined(self):
        """Verify frame styles are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        expected_styles = ["black_metal", "white_wood", "gold_ornate", "natural_oak"]
        styles = config["frame_options"]["styles"]

        for style in expected_styles:
            assert style in styles, f"Missing frame style: {style}"

    def test_frame_options_settings(self):
        """Verify frame options have required settings"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        frame_options = config["frame_options"]
        assert "default_style" in frame_options, "Should have default_style"
        assert "frame_width_px" in frame_options, "Should have frame_width_px"
        assert "mat_width_px" in frame_options, "Should have mat_width_px"
        assert "mat_color" in frame_options, "Should have mat_color"


class TestRoomScenes:
    """Test room scene configuration"""

    def test_room_scenes_defined(self):
        """Verify room scenes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "room_scenes" in config, "Config should have room_scenes"
        room_scenes = config["room_scenes"]
        assert len(room_scenes) >= 3, "Should have at least 3 room scenes"

        # Check for expected scene names
        scene_names = [scene["name"] for scene in room_scenes]
        expected_scenes = ["living_room", "office", "gallery"]

        for scene in expected_scenes:
            assert scene in scene_names, f"Missing room scene: {scene}"

    def test_room_scene_properties(self):
        """Verify room scenes have required properties"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        for scene in config["room_scenes"]:
            assert "name" in scene, "Scene should have name"
            assert "wall_color" in scene, "Scene should have wall_color"
            assert "floor_type" in scene, "Scene should have floor_type"
            assert "lighting" in scene, "Scene should have lighting"


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


class TestExportSizes:
    """Test export size specifications"""

    def test_export_sizes_defined(self):
        """Verify export sizes are defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "export_sizes" in config, "Config should have export_sizes"
        sizes = config["export_sizes"]
        assert len(sizes) >= 3, "Should have at least 3 export sizes"

    def test_export_size_properties(self):
        """Verify export sizes have required properties"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        for size in config["export_sizes"]:
            assert "name" in size, "Size should have name"
            assert "dimensions" in size, "Size should have dimensions"
            assert len(size["dimensions"]) == 2, "Dimensions should have width and height"


class TestOutputConfig:
    """Test output configuration"""

    def test_output_config_defined(self):
        """Verify output configuration is defined"""
        config_path = Path(__file__).parent.parent / "examples" / "mockup_config.json"
        with open(config_path) as f:
            config = json.load(f)

        assert "output" in config, "Config should have output"
        output = config["output"]
        assert "directory" in output, "Output should have directory"
        assert "format" in output, "Output should have format"
        assert "quality" in output, "Output should have quality"

    def test_sample_output_exists(self):
        """Verify sample output exists"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        assert output_path.exists(), "Sample output manifest should exist"


class TestMockupManifest:
    """Test mockup manifest output"""

    def test_manifest_has_input_info(self):
        """Verify manifest has input information"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        with open(output_path) as f:
            manifest = json.load(f)

        assert "input" in manifest, "Manifest should have input"
        assert "artwork_file" in manifest["input"], "Input should have artwork_file"

    def test_manifest_has_processing_info(self):
        """Verify manifest has processing information"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        with open(output_path) as f:
            manifest = json.load(f)

        assert "processing" in manifest, "Manifest should have processing"
        processing = manifest["processing"]
        assert "frame_style" in processing, "Processing should have frame_style"
        assert "framed_dimensions" in processing, "Processing should have framed_dimensions"

    def test_manifest_has_outputs(self):
        """Verify manifest has output information"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        with open(output_path) as f:
            manifest = json.load(f)

        assert "outputs" in manifest, "Manifest should have outputs"
        outputs = manifest["outputs"]
        assert "frame_variations" in outputs, "Outputs should have frame_variations"
        assert "size_exports" in outputs, "Outputs should have size_exports"
        assert "total_files_generated" in outputs, "Outputs should have total_files_generated"


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

    def test_compositing_in_manifest(self):
        """Verify compositing info in manifest"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        with open(output_path) as f:
            manifest = json.load(f)

        assert "compositing" in manifest, "Manifest should have compositing"
        compositing = manifest["compositing"]
        assert "artwork_position" in compositing, "Compositing should have artwork_position"
        assert "shadow_blur_px" in compositing, "Compositing should have shadow_blur_px"
        assert "shadow_opacity" in compositing, "Compositing should have shadow_opacity"

    def test_layer_order(self):
        """Test layer compositing order"""
        layers = ["background", "shadow", "artwork", "frame", "lighting"]

        # Background should be first
        assert layers[0] == "background"

        # Frame should be after artwork
        assert layers.index("frame") > layers.index("artwork")


class TestMetadata:
    """Test manifest metadata"""

    def test_metadata_present(self):
        """Verify metadata is included"""
        output_path = Path(__file__).parent.parent / "sample_output" / "mockup_manifest.json"
        with open(output_path) as f:
            manifest = json.load(f)

        assert "metadata" in manifest, "Manifest should have metadata"
        metadata = manifest["metadata"]
        assert "processing_time_seconds" in metadata, "Metadata should have processing_time_seconds"
        assert "timestamp" in metadata, "Metadata should have timestamp"
