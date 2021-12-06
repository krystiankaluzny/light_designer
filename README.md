# Struktura projektu

 - **data** - katalog z różnymi danymi wejściowymi; csv, ply, jpg
    - **cone_test** - pliki csv z wgenerowanymi punktami do symulacji światełek choinkowych
    - **images** - obrazki
    - **lights** - wyniki przetwarzania chmur ply
    - **point_clouds** - pliki z chmurami punktów z VisualSFM, ewetualnie dodatkowo obrobione np. w MeshLab

 - **tools** - rózne pomocnicze skrypty
    - fileLighThreshold.py - progowanie obrazków w katalogu względem jasności piksela
    - spiralConeGenerator.py - generator 500 punktów na spirali
    - pointCloud.py - analizator chmury punktów z Visual SFM, po ewentualnej obróbce szumów w MeshLab

 - **renderer** - abstrakcja do wyświetlenia punktów i ich kolorów
    - renderer.py - bazowy interfejs, przyjmuje tablicę punktów i odpowiadającym im kolorom w przestrzeni RGB, w skali [0, 1]
    - neoPixelRenderer.py - implementacja renderera dla choinki. Metoda `render` uwzględnia tylko tablicę kolorów, która musi być posortowana i odpowiadać kolejnym lampkom
    - o3dRenderer.py - implementacja renderera dla open3d. Renderer do symulacji
    - visualizer.py - dodatkowa abstrakcja dla open3d

 - rendererFactory.py - konfiguracja renderera, aby skrypty z animacjami były przenaszalne 1 do 1 z symulatora do raspberry