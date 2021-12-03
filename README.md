# Struktura projektu

 - **data** - katalog z różnymi danymi wejściowymi; csv, ply, jpg
    - **cone_test** - pliki csv z wgenerowanymi punktami do symulacji światełek choinkowych
    - **point_clouds** - pliki z chmurami punktów z VisualSFM, ewetualnie dodatkowo obrobione np. w MeshLab
 - **tools** - rózne pomocnicze skrypty
    - **fileLighThreshold** - progowanie obrazków w katalogu względem jasności piksela
    - **spiralConeGenerator** - generator 500 punktów na spirali
    - **pointCloud** - analizator chmury punktów z Visual SFM, po ewentualnej obróbce szumów w MeshLab