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

![25673514_1817237721634501_1889371567_o](https://user-images.githubusercontent.com/32960213/42384357-083837ec-813a-11e8-9b96-9650c9b72fa2.png)


![25637183_1817239868300953_1482502332_o](https://user-images.githubusercontent.com/32960213/42384288-e41ffaca-8139-11e8-8db6-ab2f6b26cfe9.png)


Highlight of the purple light as a result of the blue light colliding with a red wall.
![25625401_1817239321634341_355038500_o](https://user-images.githubusercontent.com/32960213/42384452-4cb65cc8-813a-11e8-8669-898c8223638c.png)

For more information on radiosity, visit the wikipedia page (https://en.wikipedia.org/wiki/Radiosity).
