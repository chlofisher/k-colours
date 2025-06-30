import click
from .colours import brightness, colour_palette
from rich.console import Console


@click.command()
@click.option('--k', type=int, default=6, help='Number of clusters.')
@click.option('--samples', type=int, default=1000, help='Number of samples to take from the image. Higher numbers result in more accurate clustering, at the cost of performance.')
@click.argument('path')
def run(path, k, samples):
    colours = colour_palette(path, k, samples)

    console = Console()
    for col in colours:
        print_colour(col, console)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def print_colour(rgb: tuple[int, int, int], console: Console, label=None):
    hex = rgb_to_hex(rgb)
    label = label or hex

    if is_light_colour(rgb):
        text_colour = 'black'
    else:
        text_colour = 'bright_white'

    console.print(f"[bold {text_colour} on {hex}]  {
                  label}  [/]", justify="left")


def is_light_colour(rgb: tuple[int, int, int]):
    THRESHOLD = 186

    return brightness(rgb) > THRESHOLD
