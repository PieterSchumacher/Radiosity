import numpy as np


def convert_power_to_color(power_red, power_green, power_blue, nb_triangles):

    """
    Zet de ontvangen vermogens (in Watt) om in RGB-kleuren.
    """
    max_reflected_radiosity_red = max(power_red)
    max_reflected_radiosity_green = max(power_green)
    max_reflected_radiosity_blue = max(power_blue)
    # max(lijst met alle uiteindelijk berekende radiositeiten)
    for i in range(len(power_red)):
        power_red[i] *= (254.0/(255.0*max_reflected_radiosity_red))
        power_green[i] *= (254.0/(255.0*max_reflected_radiosity_green))
        power_blue[i] *= (254.0/(255.0*max_reflected_radiosity_blue))
    # gamma correction
    rgb_red, rgb_green, rgb_blue = np.zeros(nb_triangles), np.zeros(nb_triangles), np.zeros(nb_triangles)
    for i in range(len(power_red)):
        rgb_red[i] = 255.0*gamma_correction(power_red[i])
        rgb_green[i] = 255.0*gamma_correction(power_green[i])
        rgb_blue[i] = 255.0*gamma_correction(power_blue[i])
    return rgb_red, rgb_green, rgb_blue


def gamma_correction(x):

    """
    Past de gammacorrectie toe op een bepaalde kleur.
    Gamma bedraagt 2.4 in dit algoritme.
    """

    if x <= 0.0031308:
        return 12.92*x
    else:
        return 1.055*(x**(1/2.4))-0.055
