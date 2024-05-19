import os

import matplotlib
import matplotlib.pyplot as plt

ALL_COLOURS = ["yellow", "green", "orange", "blue", "red"]
ANSWER_COLOURS = ["yellow", "green", "orange", "blue"]

# Runtime Configuration Parameters
matplotlib.rcParams["mathtext.fontset"] = "cm"  # Font changed to Computer Modern


def latex2image(
    latex_expression, image_name, image_size_in=(3, 0.5), fontsize=16, dpi=200
):
    """
    A simple function to generate an image from a LaTeX language string.

    Parameters
    ----------
    latex_expression : str
        Equation in LaTeX markup language.
    image_name : str or path-like
        Full path or filename including filetype.
        Accepeted filetypes include: png, pdf, ps, eps and svg.
    image_size_in : tuple of float, optional
        Image size. Tuple which elements, in inches, are: (width_in, vertical_in).
    fontsize : float or str, optional
        Font size, that can be expressed as float or
        {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}.

    Returns
    -------
    # fig : object
    #     Matplotlib figure object from the class: matplotlib.figure.Figure.

    """

    fig = plt.figure(figsize=image_size_in, dpi=dpi)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=latex_expression,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=fontsize,
    )
    file_path = os.path.join(os.getcwd(), "Questions", "Images", f"{image_name}.png")
    plt.savefig(file_path)

    return 
    # return fig


if __name__ == "__main__":
    latex_expression = r"""$\vec{\nabla}\times\vec{H}=\vec{J}+\dfrac{\partial\vec{D}}{\partial t},$"""
    image_name = "ampere_maxwell_law@2x"
    fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.5))
    
    latex_expression = r"$e^{i\pi}+1=0$"
    image_name = "euler_identity@2x"
    fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.5))
    
    latex_expression = r"""$\underset{S}{\int\int}\ \vec{\nabla}\times\vec{B}\cdot d\vec{S}=\underset{C}{\oint}\ \vec{B}\cdot d\vec{l},$"""
    image_name = "stokes_theorem@2x.png"
    fig = latex2image(latex_expression, image_name, image_size_in=(3, 0.75))
