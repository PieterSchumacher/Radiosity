# Radiosity

This program works in three steps:

- Model a 3D scene in Blender. The scene is exported as a .obj file (vertices) and .mtl (material information).
- Process the scene to simulate diffuse lighting.
  - Read the .obj and .mtl and build a kd-tree (import_file_mp.py).
  - Calculate the formfactor for each combination of triangles in the scene  (Main_multiprocessing_2.py).
  - Calculate the emission of red, green and blue light for each triangle by approximating the solution of the set of linear equations
    using the Gauss-Seidel method (Main_multiprocessing_2.py).
- Visualise the scene using the VTK library (visualise_calculated_scene.py).

Result:  

For more information on radiosity, visit the wikipedia page (https://en.wikipedia.org/wiki/Radiosity).

Upper view.

![25673514_1817237721634501_1889371567_o](https://user-images.githubusercontent.com/32960213/42385624-92760f1c-813d-11e8-8f13-eb15489563e6.png)

Sideways.

![25637183_1817239868300953_1482502332_o](https://user-images.githubusercontent.com/32960213/42385623-92548d92-813d-11e8-89c4-7e21f26604a3.png)

Highlight of the purple light as a result of the blue light colliding with a red wall.
![25625401_1817239321634341_355038500_o](https://user-images.githubusercontent.com/32960213/42385625-929602ea-813d-11e8-9cbb-786d8a69a98f.png)
