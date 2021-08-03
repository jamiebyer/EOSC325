# EOSC 325 Demos

Creating a demos for EOSC325 using Python Dash. 

## Unconfined Flow with Recharge
This demo is based on the supplemental file for the book "Hydrogeological Properties of Earth Materials and Principles of Groundwater Flow", by the Groundwater Project.

The dash has 5 parameters:
- $h_1$, hydraulic head at $x=0$
- $h_2$, hydraulic head at $x=L$
- $W$, recharge
- $K$, hydraulic conductivity
- $L$, max $x$

The first plot plots $h(x)$. It shows the location of $d$, the groundwater divide. The plot has qualitative arrows indicating the direction and magnitude of flow.

The second plot plots $q^{\prime}_x(x)$ and $y=0$. $q^{\prime}_x$ is the flow per unit width, and the groundwater divide occurs where $q^{\prime}_x=0$.

## Storativity
This demo is based on the video [here](https://www.youtube.com/watch?v=SPunca56Vds&list=PLp1lK6n-xb5O8RnVhcfYvqy1kzU_5IfDF&index=7) and its [associated spreadsheet](https://drive.google.com/file/d/1WIMPJ2ZS_rEd54-sw0cIqxvwyjLahRv0/view).

The demo is a bar graph comparing the storativity for 5 different materials, with customizable water density, porosity, alpha values (aquifer compressibility), and aquifer thickness.