
from ableton.v2.control_surface.elements.color import Color
from .debug import initialize_debug

debug = initialize_debug()


class MonoColor(Color):


	def draw(self, interface):
		try:
			# interface.set_darkened_value(0)
			super(MonoColor, self).draw(interface)
		except:
			super(MonoColor, self).draw(interface)



class BiColor(MonoColor):


	def __init__(self, darkened_value = 0, *a, **k):
		super(BiColor, self).__init__(*a, **k)
		self._darkened_value = darkened_value


	def draw(self, interface):
		try:
			interface.set_darkened_value(self._darkened_value)
			interface.send_value(self.midi_value)
		except:
			debug(interface, 'is not MonoButtonElement, cannot use BiColor')
			super(BiColor, self).draw(interface)




class LividRGB:

	OFF = MonoColor(0)
	WHITE = MonoColor(1)
	YELLOW = MonoColor(2)
	CYAN = MonoColor(3)
	MAGENTA = MonoColor(4)
	RED = MonoColor(5)
	GREEN = MonoColor(6)
	BLUE = MonoColor(7)

	class BlinkFast:
		WHITE = MonoColor(8)
		YELLOW = MonoColor(9)
		CYAN = MonoColor(10)
		MAGENTA = MonoColor(11)
		RED = MonoColor(12)
		GREEN = MonoColor(13)
		BLUE = MonoColor(14)


	class BlinkMedium:
		WHITE = MonoColor(15)
		YELLOW = MonoColor(16)
		CYAN = MonoColor(17)
		MAGENTA = MonoColor(18)
		RED = MonoColor(19)
		GREEN = MonoColor(20)
		BLUE = MonoColor(21)


	class BlinkSlow:
		WHITE = MonoColor(22)
		YELLOW = MonoColor(23)
		CYAN = MonoColor(24)
		MAGENTA = MonoColor(25)
		RED = MonoColor(26)
		GREEN = MonoColor(27)
		BLUE = MonoColor(28)


	class BiColor:
		class WHITE:
			YELLOW = BiColor(1, 16)
			CYAN = BiColor(1, 17)
			MAGENTA = BiColor(1, 18)
			RED = BiColor(1, 19)
			GREEN = BiColor(1, 20)
			BLUE = BiColor(1, 21)


		class YELLOW:
			WHITE = BiColor(2, 15)
			CYAN = BiColor(2, 17)
			MAGENTA = BiColor(2, 18)
			RED = BiColor(2, 19)
			GREEN = BiColor(2, 20)
			BLUE = BiColor(2, 21)


		class CYAN:
			WHITE = BiColor(3, 15)
			YELLOW = BiColor(3, 16)
			MAGENTA = BiColor(3, 18)
			RED = BiColor(3, 19)
			GREEN = BiColor(3, 20)
			BLUE = BiColor(3, 21)

		class MAGENTA:
			WHITE = BiColor(4, 15)
			YELLOW = BiColor(4, 16)
			CYAN = BiColor(4, 17)
			RED = BiColor(4, 19)
			GREEN = BiColor(4, 20)
			BLUE = BiColor(4, 21)

		class RED:
			WHITE = BiColor(5, 15)
			YELLOW = BiColor(5, 16)
			CYAN = BiColor(5, 17)
			MAGENTA = BiColor(5, 18)
			GREEN = BiColor(5, 20)
			BLUE = BiColor(5, 21)

		class GREEN:
			WHITE = BiColor(6, 15)
			YELLOW = BiColor(6, 16)
			CYAN = BiColor(6, 17)
			MAGENTA = BiColor(6, 18)
			RED = BiColor(6, 19)
			BLUE = BiColor(6, 21)

		class BLUE:
			WHITE = BiColor(7, 15)
			YELLOW = BiColor(7, 16)
			CYAN = BiColor(7, 17)
			MAGENTA = BiColor(7, 18)
			RED = BiColor(7, 19)
			GREEN = BiColor(7, 20)


LIVE_COLORS_TO_MIDI_VALUES = {10927616:28, 
16149507:10, 
4047616:37, 
6441901:86, 
14402304:19, 
8754719:31, 
16725558:4, 
3947580:2, 
10056267:5, 
8237133:38, 
12026454:8, 
12565097:14, 
13381230:118, 
12243060:32, 
16249980:23, 
13013643:3, 
10208397:33, 
695438:55, 
13821080:27, 
3101346:79, 
16749734:3, 
8962746:33, 
5538020:80, 
13684944:15, 
15064289:127, 
14183652:104, 
11442405:102, 
13408551:13, 
1090798:87, 
11096369:7, 
16753961:16, 
1769263:46, 
5480241:37, 
1698303:69, 
16773172:23, 
7491393:2,
8940772:92, 
14837594:5, 
8912743:38, 
10060650:8, 
13872497:14, 
16753524:11, 
8092539:8, 
2319236:76, 
1716118:82, 
12349846:119, 
11481907:4, 
15029152:119, 
2490280:42, 
11119017:3, 
10701741:95, 
15597486:24, 
49071:48, 
10851765:102, 
12558270:123, 
32192:76, 
8758722:99, 
10204100:99, 
11958214:98, 
8623052:99, 
16726484:110, 
12581632:28, 
13958625:127, 
12173795:102, 
13482980:105, 
16777215:127, 
6094824:65, 
13496824:127, 
9611263:99, 
9160191:99}


RGB_COLOR_TABLE = ((0, 0), (1, 15862796), (2, 15882328), (3, 15902117), (4, 15870988), (5, 15887960), 
		   (6, 15904933), (7, 15879436), (8, 15893592), (9, 15907749), (10, 15887884), (11, 15899224), 
		   (12, 15910565), (13, 15896332), (14, 15904856), (15, 15913381), (16, 15904780), (17, 15910488), 
		   (18, 15916197), (19, 15913228), (20, 15916120), (21, 15919013), (22, 15921676), (23, 15921752), 
		   (24, 15921829), (25, 13758988), (26, 14479960), (27, 13759141), (28, 11596300), (29, 13038168), 
		   (30, 11596453), (31, 9433612), (32, 11596376), (33, 9433765), (34, 7270924), (35, 10154584), 
		   (36, 7271077), (37, 5108236), (38, 8712792), (39, 5108389), (40, 2945548), (41, 7271000), 
		   (42, 2945701), (43, 848396), (44, 5829208), (45, 848549), (46, 848428), (47, 5829230), 
		   (48, 848560), (49, 848461), (50, 5829252), (51, 848571), (52, 848494), (53, 5829274), 
		   (54, 848582), (55, 848527), (56, 5829296), (57, 848593), (58, 848560), (59, 5829318), 
		   (60, 848604), (61, 848593), (62, 5829340), (63, 848615), (64, 848626), (65, 5829362), 
		   (66, 848626), (67, 840178), (68, 5823730), (69, 845810), (70, 831730), (71, 5818098), 
		   (72, 842994), (73, 823282), (74, 5812466), (75, 840178), (76, 814834), (77, 5806834), 
		   (78, 837362), (79, 806386), (80, 5801202), (81, 834546), (82, 797938), (83, 5795570), 
		   (84, 831730), (85, 789746), (86, 5789938), (87, 828914), (88, 2886898), (89, 7231730), 
		   (90, 2926066), (91, 5049586), (92, 8673522), (93, 5088754), (94, 7212274), (95, 10115314), 
		   (96, 7251442), (97, 9374962), (98, 11557106), (99, 9414130), (100, 11537650), (101, 12998898), 
		   (102, 11576818), (103, 13700338), (104, 14440690), (105, 13739506), (106, 15863026), 
		   (107, 15882482), (108, 15902194), (109, 15862993), (110, 15882460), (111, 15902183), 
		   (112, 15862960), (113, 15882438), (114, 15902172), (115, 15862927), (116, 15882416), 
		   (117, 15902161), (118, 15862894), (119, 15882394), (120, 15902150), (121, 15862861), 
		   (122, 15882372), (123, 15902139), (124, 15862828), (125, 15882350), (126, 15902128), (127, 15790320))