# Mockup Generator - Presentation Guide

## Elevator Pitch (30 seconds)

> "Mockup Generator automatically creates professional product mockups from artwork images. It takes a plain photo of art and places it into realistic room scenes with proper perspective, shadows, and framing. What a graphic designer does in 30 minutes, this system does in seconds—and outputs multiple sizes for eBay, Instagram, and web."

---

## Key Talking Points

### 1. The Problem It Solves

- **Mockups Sell Products**: Buyers want to see art "in a room"
- **Designer Bottleneck**: Each mockup takes 15-30 minutes manually
- **Consistency**: Manual mockups vary in quality
- **Multi-Platform Needs**: Different sizes for eBay, Etsy, Instagram, web

### 2. The Solution

- **Perspective Transformation**: Mathematically correct placement
- **Multiple Frame Styles**: Black metal, white wood, gold ornate, etc.
- **Room Scene Library**: Living room, office, gallery settings
- **Multi-Size Export**: Square, 4:3, 16:9 in one pass

### 3. Technical Architecture

```
Artwork → Perspective Transform → Shadow Layer → Frame Composite → Room Scene → Export
```

---

## Demo Script

### What to Show

1. **Run the Demo** (`python demo.py`)
   - Show artwork image being processed
   - Walk through frame style selection
   - Display room scene compositing

2. **Key Moments to Pause**
   - Perspective transformation (how the math works)
   - Shadow generation (adds realism)
   - Final composite in multiple room scenes

3. **Sample Output Discussion**
   - Show `sample_output/mockup_manifest.json`
   - Display the different size exports
   - Explain the compositing layers

---

## Technical Highlights to Mention

### Perspective Mathematics
- "Proper 3D perspective transformation using matrix math"
- "Artwork correctly 'sits' in the scene, not floating"
- "Adjustable viewing angles for different room templates"

### Layer Compositing
- "5-layer system: background, shadow, artwork, frame, lighting"
- "Proper alpha blending for realistic shadows"
- "Color matching to room scene palette"

### Batch Processing
- "Process entire inventory folders automatically"
- "Generate all frame/room combinations in one pass"
- "Consistent naming conventions for e-commerce"

---

## Anticipated Questions & Answers

**Q: How realistic are these mockups?**
> "Very realistic. We use proper perspective transformation, soft shadows, and lighting adjustments. They're indistinguishable from professionally designed mockups for product listing purposes."

**Q: Can you add custom room scenes?**
> "Yes, the template system is extensible. Adding a new room requires defining the artwork placement coordinates and lighting parameters. Takes about 30 minutes to calibrate a new scene."

**Q: What about different artwork sizes?**
> "The system automatically scales artwork to fit the room template proportionally. Very large or small pieces are flagged for manual review if they'd look unrealistic."

**Q: How does frame selection work?**
> "You can specify a frame style or let the system suggest one based on artwork colors and style. The matching algorithm considers color contrast and aesthetic compatibility."

---

## Key Metrics to Share

| Metric | Value |
|--------|-------|
| Processing Time | ~2 seconds per mockup |
| Frame Styles | 6 (black, white, gold, oak, floating, none) |
| Room Scenes | 5 (living room, office, gallery, bedroom, minimal) |
| Export Sizes | 4 (1200x1200, 1600x1200, 1920x1080, 800x800) |
| Layer System | 5 layers (background, shadow, art, frame, lighting) |

---

## Output Example

```
output/
├── artwork_black_frame_living_room_1200x1200.jpg   # Instagram
├── artwork_black_frame_living_room_1600x1200.jpg   # eBay main
├── artwork_black_frame_living_room_1920x1080.jpg   # Hero image
├── artwork_gold_frame_gallery_1200x1200.jpg        # Variation
└── ...
```

---

## Why This Project Matters

1. **Image Processing Expertise**: Perspective transforms, compositing
2. **Template System Design**: Extensible architecture
3. **Business Value**: Dramatically speeds up listing creation
4. **Quality Consistency**: Every mockup meets same standard
5. **Production-Ready**: Batch processing, error handling

---

## Closing Statement

> "This project showcases my image processing skills and understanding of e-commerce needs. The combination of mathematical rigor in perspective transformation with practical batch processing creates real business value."
