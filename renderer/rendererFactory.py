def createRenderer(config={}):
    return __createO3dRenderer(config)  # używać do symulacji
    # return __createO3dRendererNoAxis(config)  # używać do symulacji
    # return __createNepPixelRenderer()  # używać na raspberry


def __createO3dRenderer(config):
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    config['axis'] = True
    v = visualizerOf([], config)
    return O3dRenderer(v)


def __createO3dRendererNoAxis(config):
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    config['axis'] = False
    v = visualizerOf([], config)
    return O3dRenderer(v)


def __createNepPixelRenderer():
    from renderer.neoPixelRenderer import NeoPixelRenderer

    return NeoPixelRenderer()
