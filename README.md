# Jak zacząć

Wystarczy że skopiujesz `template.py`, nadasz swojemu skryptowi unikalną nazwę i możesz kodzić.
Najlepiej żeby Twój skrypt był w głównym katalogu projektu (obok template.py), dzięki czemu ściezki będą takie same jak na raspberry.
Stworzone API zakłada użycie biblioteki numpy, a kolory powinny być w zakresie [0, 1]

# Struktura projektu

 - raw.txt - plik z pozycjami światełek
 - template.py - przykładowa animacja

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
    - renderer.py - bazowy interfejs, przyjmuje tablicę punktów i odpowiadającym im kolorom w przestrzeni RGB, w skali [0, 1] lub [0, 255]
    - neoPixelRenderer.py - implementacja renderera dla choinki. Metoda `render` i `render256` uwzględnia tylko tablicę kolorów, która musi być posortowana i odpowiadać kolejnym lampkom
    - o3dRenderer.py - implementacja renderera dla open3d. Renderer do symulacji
    - visualizer.py - dodatkowa abstrakcja dla open3d

      Skróty klawiszowe w oknie symulatora:
       - Q - wyjście
       - B - ustaw czarne tło
       - W - ustaw białe tło

    - rendererFactory.py - konfiguracja renderera, aby skrypty z animacjami były przenaszalne 1 do 1 z symulatora do raspberry

      Metoda `createRenderer()` przyjmuje słownik z parametrami do konfiguracji.
      Dostepone parametry:
        - windowsName - nazwa okna, domyślnie "Test"
        - axis - `True/False` - pokazywanie osi x-y-z
        - axisScale - skala strzałek osi, domyślnie 1/100
        - axisLabelEnable - czy podpisy osi włączone, domyślnie True
        - axisFontLocation - lokalizacja pliku z czcionką do wyświetlenia podpisu, domyślnie /usr/share/fonts/truetype/freefont/FreeMono.ttf
        - axisFontSize - rozmiar podpisu, domyślnie 12
        - pointSize - wielkość wyswietlanych punktów, domyślnie 8.0

