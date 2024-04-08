import pygame 
from functools import lru_cache

class LampDisplay:
    BACKGROUND = (76, 45, 28)
    LAMP_ON = (242, 201, 159)
    LAMP_OFF = (173, 101, 62)
    BORDER_RATIO = 0.15

    def __init__(self, size: tuple[int, int], pixels_per_lamp: int) -> None:
        self.size = size
        pixels_per_lamp = pixels_per_lamp
        border = pixels_per_lamp * 0.5 * LampDisplay.BORDER_RATIO
        self.a = pixels_per_lamp + border
        self.b = pixels_per_lamp - 2 * border
        

        pygame.display.set_caption("Lamp Display")

        self.screen = pygame.display.set_mode(
            (
                size[0] * pixels_per_lamp,
                size[1] * pixels_per_lamp,
            )
        )

        self.clear()

    def clear(self) -> None:
        self.screen.fill(LampDisplay.BACKGROUND)

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.set_pixel((x, y), False)

    def set_pixel(self, pixel: tuple[int, int], on: bool) -> None:
        
        pygame.draw.rect(
            self.screen,
            LampDisplay.LAMP_ON if on else LampDisplay.LAMP_OFF,
            pygame.Rect(
                round(pixel[0]) * self.a,
                round(pixel[1]) * self.a,
                self.b,
                self.b,
            )
        )

    def update(self) -> bool:
        pygame.display.update()



w = 50
h = 50
inv = []


#display.set_pixel((50,50), True)
glider =((0,0,1),
		 (1,0,1),
		 (0,1,1))

glider = [(y,x) for y,_ in enumerate(glider) for x,a in enumerate(glider[y]) if bool(a)]
print(glider)



#speed on hz
speed = 9999999999999

#"returns list version of iterables else return original obj"

deep_copy = lambda data: [deep_copy(data[i]) for i in range(len(data))] if isinstance(data, (list,tuple)) else data

from time import time,sleep
from threading import Thread
display = LampDisplay((w,h),13)
def rusn():
	global inv
	inv = [[(1 if (y,x) in glider else 0) for x in range(w) ] for y in range(h)]
	
	cinv = deep_copy(inv)
	
	def process():
		for y in range(h):
			for x in range(w):
				s = sum((inv[(y + i) % h][(x + j) % w] for i in range(-1, 2) for j in range(-1, 2))) - inv[y][x]
				if s == 3:
					cinv[y][x] = 1
				if s > 3 or s < 2:
					cinv[y][x] = 0
		return

	while True:
		n1 = time()
		#print("\x1b[;H\x1b[J"+("\n".join(map(lambda x: str(x),inv))))
		#inv = deepcopy(cinv)
		
		a = Thread(target=process)
		a.start()
		
		for y in range(h):
			for x in range(w):
				display.set_pixel((x,y),bool(inv[y][x]))
		display.update()
		
		inv = [[cinv[y][x] for x in range(w)] for y in range(h)]
		
		
		a.join()
		
		#raise Exception("stoped")
		sleep(max((1/speed-(time()-n1),0)))



rusn()