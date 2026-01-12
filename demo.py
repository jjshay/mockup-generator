#!/usr/bin/env python3
"""
Mockup Generator Demo
Creates sample mockups with rich visual output.

Run: python demo.py
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    print("Installing Pillow...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFilter

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_header(text: str) -> None:
    if RICH_AVAILABLE:
        console.print()
        console.rule(f"[bold magenta]{text}[/bold magenta]", style="magenta")
        console.print()
    else:
        print(f"\n{'='*60}\n {text}\n{'='*60}\n")


def show_banner() -> None:
    if RICH_AVAILABLE:
        banner = """
[bold cyan]╔═══════════════════════════════════════════════════════════════════╗
║[/bold cyan] [bold gold1]  __  __            _                 ____                        [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1] |  \/  | ___   ___| | ___   _ _ __  / ___| ___ _ __               [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1] | |\/| |/ _ \ / __| |/ / | | | '_ \| |  _ / _ \ '_ \              [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1] | |  | | (_) | (__|   <| |_| | |_) | |_| |  __/ | | |             [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1] |_|  |_|\___/ \___|_|\_\\__,_| .__/ \____|\___|_| |_|             [/bold gold1][bold cyan]║
║[/bold cyan] [bold gold1]                              |_|                                  [/bold gold1][bold cyan]║
║[/bold cyan]                                                                       [bold cyan]║
║[/bold cyan]            [bold white]Professional Product Mockups from Any Artwork[/bold white]           [bold cyan]║
╚═══════════════════════════════════════════════════════════════════╝[/bold cyan]
"""
        console.print(banner)
    else:
        print("\n" + "="*60 + "\n  MOCKUP GENERATOR\n" + "="*60)


def create_artwork() -> Image.Image:
    img = Image.new('RGB', (800, 1000), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    draw.ellipse([100, 150, 400, 450], fill='#E74C3C')
    draw.rectangle([350, 400, 700, 800], fill='#3498DB')
    draw.polygon([(400, 100), (650, 350), (200, 400)], fill='#F1C40F')
    draw.text((650, 950), "Artist", fill='#2C3E50')
    return img


def create_frame(artwork: Image.Image, style: str = 'black_metal', width: int = 40) -> Image.Image:
    colors = {
        'black_metal': ('#1a1a1a', '#333333'),
        'white_wood': ('#F5F5F5', '#E0E0E0'),
        'gold_ornate': ('#D4AF37', '#B8860B'),
        'natural_oak': ('#DEB887', '#D2691E'),
    }
    outer, inner = colors.get(style, colors['black_metal'])

    aw, ah = artwork.size
    framed = Image.new('RGB', (aw + width*2, ah + width*2), outer)
    draw = ImageDraw.Draw(framed)
    draw.rectangle([width//4, width//4, aw + width*2 - width//4, ah + width*2 - width//4], fill=inner)
    draw.rectangle([width - 10, width - 10, width + aw + 10, width + ah + 10], fill='#FAFAFA')
    framed.paste(artwork, (width, width))
    return framed


def create_room() -> Image.Image:
    room = Image.new('RGB', (1600, 1200), '#F5F2EF')
    draw = ImageDraw.Draw(room)
    draw.rectangle([0, 800, 1600, 1200], fill='#D4C4B5')
    draw.rectangle([0, 780, 1600, 800], fill='#FFFFFF')
    return room


def create_mockup(framed: Image.Image, room: Image.Image) -> Image.Image:
    result = room.copy()
    x = (room.size[0] - framed.size[0]) // 2
    y = (room.size[1] * 2 // 3 - framed.size[1]) // 2 - 50
    result.paste(framed, (x, y))
    return result


def demo_mockups() -> Path:
    print_header("GENERATING MOCKUPS")

    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    if RICH_AVAILABLE:
        console.print("[dim]Creating artwork and mockups...[/dim]\n")

    artwork = create_artwork()
    room = create_room()

    frame_styles = ['black_metal', 'white_wood', 'gold_ornate', 'natural_oak']
    files = []

    if RICH_AVAILABLE:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                      BarColumn(), console=console) as progress:
            task = progress.add_task("[magenta]Creating mockups...", total=len(frame_styles))

            for style in frame_styles:
                framed = create_frame(artwork, style)
                mockup = create_mockup(framed, room)
                filename = f"mockup_{style}.jpg"
                mockup.save(output_dir / filename, quality=95)
                files.append((filename, style, mockup.size))
                progress.update(task, advance=1, description=f"[magenta]{style}")
                time.sleep(0.2)

        table = Table(title="🖼️ Generated Mockups", box=box.ROUNDED)
        table.add_column("File", style="cyan")
        table.add_column("Frame Style", style="magenta")
        table.add_column("Size", style="gold1")

        for filename, style, size in files:
            table.add_row(filename, style, f"{size[0]}x{size[1]}")
        console.print(table)
    else:
        for style in frame_styles:
            framed = create_frame(artwork, style)
            mockup = create_mockup(framed, room)
            mockup.save(output_dir / f"mockup_{style}.jpg", quality=95)
            print(f"  Created: mockup_{style}.jpg")

    return output_dir


def demo_sizes() -> None:
    print_header("EXPORT SIZES")

    sizes = [
        ("Square (Instagram)", "1200x1200"),
        ("Landscape (eBay)", "1600x1200"),
        ("Hero (Website)", "1920x1080"),
        ("Thumbnail", "800x800"),
    ]

    if RICH_AVAILABLE:
        table = Table(title="📐 Export Formats", box=box.ROUNDED)
        table.add_column("Format", style="cyan")
        table.add_column("Dimensions", style="gold1")
        table.add_column("Use Case", style="dim")

        uses = ["Social media", "Marketplace", "Hero images", "Previews"]
        for (name, dims), use in zip(sizes, uses):
            table.add_row(name, dims, use)
        console.print(table)
    else:
        for name, dims in sizes:
            print(f"  {name}: {dims}")


def main() -> None:
    show_banner()

    if RICH_AVAILABLE:
        console.print("[dim]Create professional product mockups from artwork images.[/dim]\n")

    output_dir = demo_mockups()
    demo_sizes()

    print_header("SUMMARY")
    if RICH_AVAILABLE:
        console.print(Panel(f"""
[cyan]Created:[/cyan] 4 mockups with different frame styles
[cyan]Location:[/cyan] {output_dir}/

[bold]Frame Styles:[/bold]
  • Black Metal - Modern, minimal
  • White Wood - Light, airy
  • Gold Ornate - Classical
  • Natural Oak - Rustic

[bold magenta]Next Steps:[/bold magenta]
  1. Use your own artwork images
  2. Add PhotoRoom API for background removal
  3. Run: [cyan]python mockup_generator.py[/cyan]
""", title="📊 Results", border_style="cyan", box=box.ROUNDED))

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
