
def createRenderer():
    return __createO3dRenderer() # używać do symulacji
    # return __createO3dRendererNoAxis()  # używać do symulacji
    # return __createNepPixelRenderer() # używać na raspberry


def __createO3dRenderer():
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    v = visualizerOf([], axis=True)
    return O3dRenderer(v)


def __createO3dRendererNoAxis():
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    v = visualizerOf([], axis=False)
    return O3dRenderer(v)


def __createNepPixelRenderer():
    from renderer.neoPixelRenderer import NeoPixelRenderer

    return NeoPixelRenderer()
