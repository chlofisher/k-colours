import imageio.v3 as iio
from scipy.cluster.vq import kmeans
import numpy as np
from rich.console import Console
import click


def main():
    colour_palette()


@click.command()
@click.option('--k', type=int, default=6, help='Number of clusters.')
@click.argument('path')
def colour_palette(path, k):
    im = iio.imread(path)

    flattened = im.reshape(-1, 3)
    data = flattened.astype(np.float32)
    data /= 256

    centroids, distortion = kmeans(data, k)

    colours = np.rint(centroids * 255).astype(int)
    colours = [tuple(col) for col in colours]

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

    console.print(f"[bold {text_colour} on {hex}]  {label}  [/]", justify="left")


def is_light_colour(rgb: tuple[int, int, int]):
    r, g, b = rgb
    THRESHOLD = 186

    # Perceived brightness formula (ITU-R BT.601)
    brightness = (0.299 * r + 0.587 * g + 0.114 * b)

    return brightness > THRESHOLD


if __name__ == "__main__":
    main()
