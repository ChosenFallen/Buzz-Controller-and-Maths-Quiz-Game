from os import getcwd
from os.path import join

import matplotlib
import matplotlib.pyplot as plt
import pygame


def import_image(*path, alpha=True, format="png"):
    full_path = f"{join(*path)}.{format}"
    return (
        pygame.image.load(full_path).convert_alpha()
        if alpha
        else pygame.image.load(full_path).convert()
    )


def import_svg(*path, size: list[float]):
    full_path = f"{join(*path)}.svg"
    return pygame.image.load_sized_svg(full_path, size)


def latex2image(
    latex_expression, image_name, image_size_in=(3, 0.5), fontsize=16, dpi=200
):

    # Runtime Configuration Parameters
    matplotlib.rcParams["mathtext.fontset"] = "cm"  # Font changed to Computer Modern

    fig = plt.figure(figsize=image_size_in, dpi=dpi)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=latex_expression,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=fontsize,
    )
    file_path = join(getcwd(), "questions", "images", f"{image_name}.png")
    plt.savefig(file_path, transparent=True)

    return
    # return fig


if __name__ == "__main__":
    latex_expression = r"""$\vec{\nabla}\times\vec{H}=\vec{J}+\dfrac{\partial\vec{D}}{\partial t},$"""
    image_name = "ampere_maxwell_law@2x"
    fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.5))

#     latex_expression = r"$e^{i\pi}+1=0$"
#     image_name = "euler_identity@2x"
#     fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.5))

#     latex_expression = r"""$\underset{S}{\int\int}\ \vec{\nabla}\times\vec{B}\cdot d\vec{S}=\underset{C}{\oint}\ \vec{B}\cdot d\vec{l},$"""
#     image_name = "stokes_theorem@2x.png"
#     fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.75))
