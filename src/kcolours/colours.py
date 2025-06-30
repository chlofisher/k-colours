import imageio.v3 as iio
from scipy.cluster.vq import kmeans
import numpy as np


def colour_palette(path, k, samples) -> list[tuple[int, int, int]]:
    im = iio.imread(path).astype(np.float32)
    im /= 255

    flat_image = im.reshape(-1, 3)

    compression = flat_image.shape[0] // samples

    data = flat_image[::compression].astype(np.float32)

    centroids, distortion = kmeans(data, k)

    colours = np.rint(centroids * 255).astype(int)

    return [tuple(col) for col in colours]


def brightness(rgb: tuple[int, int, int]):
    r, g, b = rgb

    # Perceived brightness formula (ITU-R BT.601)
    return 0.299 * r + 0.587 * g + 0.114 * b
