import io
import os

def createRenderer(config={}):
    if __isRaspberrypi():
        return __createNepPixelRenderer(config)  # używać na raspberry  
    else:
        return __createO3dRenderer(config)  # używać do symulacji
    # return __createO3dRendererNoAxis(config)  # używać do symulacji


def __createO3dRenderer(config):
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    config['axis'] = True
    v = visualizerOf([], config)
    return O3dRenderer(config, v)


def __createO3dRendererNoAxis(config):
    from renderer.o3dRenderer import O3dRenderer
    from renderer.visualizer import visualizerOf

    config['axis'] = False
    v = visualizerOf([], config)
    return O3dRenderer(config, v)


def __createNepPixelRenderer(config):
    from renderer.neoPixelRenderer import NeoPixelRenderer

    return NeoPixelRenderer(config)

def __isRaspberrypi():
    if os.name != 'posix':
        return False
    chips = ('BCM2708','BCM2709','BCM2711','BCM2835','BCM2836')
    try:
        with io.open('/proc/cpuinfo', 'r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    _, value = line.strip().split(':', 1)
                    value = value.strip()
                    if value in chips:
                        return True
    except Exception:
        pass
    return False