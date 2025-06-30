import click
from .colours import colour_palette, brightness
from rich.console import Console


@click.command()
@click.option('--k', type=int, default=6, help='Number of clusters.')
@click.option('--samples', type=int, default=1000, help='Number of samples to take from the image.')
@click.argument('path')
def run(path: str, k: int, samples: int):
    colours: list[tuple[int, int, int]] = colour_palette(path, k, samples)

    output_colours(colours)


def output_colours(colours: list[tuple[int, int, int]]):
    console = Console()

    for col in colours:
        print_colour(col, console)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def print_colour(rgb: tuple[int, int, int], console: Console,
                 label: str | None = None):
    hex: str = rgb_to_hex(rgb)
    label: str = label or hex

    if is_light_colour(rgb):
        text_colour = 'black'
    else:
        text_colour = 'bright_white'

    console.print(f"[bold {text_colour} on {hex}]  {
                  label}  [/]", justify="left")


def is_light_colour(rgb: tuple[int, int, int]):
    THRESHOLD = 186

    return brightness(rgb) > THRESHOLD
