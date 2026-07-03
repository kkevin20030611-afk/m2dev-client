import ui
import net
import localeInfo
import chat
import wndMgr
import app

DUNGEON_DATA = [
	{
		"id": 1,
		"name": "Démon Torony",
		"min_level": 40,
		"ticket": "Nincs",
		"boss": "Kaszás",
	},
	{
		"id": 2,
		"name": "Ördög Katakomba",
		"min_level": 75,
		"ticket": "Zsugorított fej",
		"boss": "Azrael",
	},
	{
		"id": 3,
		"name": "Kék Sárkány Terme",
		"min_level": 75,
		"ticket": "Csavart kulcs",
		"boss": "Beran-Setaou",
	},
	{
		"id": 4,
		"name": "Vörös Sárkány Erőd",
		"min_level": 100,
		"ticket": "Átjáró jegy",
		"boss": "Razador",
	},
	{
		"id": 5,
		"name": "Nemere Őrtornya",
		"min_level": 100,
		"ticket": "Átjáró jegy",
		"boss": "Nemere",
	},
	{
		"id": 6,
		"name": "Pókkirálynő Barlangja",
		"min_level": 50,
		"ticket": "Arachnida Kulcs",
		"boss": "Pókkirálynő",
	}
]

class DungeonInfoWindow(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.BuildWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def BuildWindow(self):
		self.SetSize(450, 350)
		self.SetPosition((wndMgr.GetScreenWidth() - 450) / 2, (wndMgr.GetScreenHeight() - 350) / 2)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("Kazamata Információ (F6)")
		self.SetCloseEvent(self.Close)
		
		self.dungeonButtons = []
		self.selectedDungeon = 0
		
		# Left side: List of dungeons
		self.bgLeft = ui.Bar()
		self.bgLeft.SetParent(self)
		self.bgLeft.SetPosition(10, 35)
		self.bgLeft.SetSize(180, 300)
		self.bgLeft.SetColor(0x77000000)
		self.bgLeft.Show()
		
		yPos = 0
		for i, data in enumerate(DUNGEON_DATA):
			btn = ui.Button()
			btn.SetParent(self.bgLeft)
			btn.SetPosition(5, 5 + yPos)
			btn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			btn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			btn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			btn.SetText(data["name"])
			btn.SetEvent(lambda arg=i: self.SelectDungeon(arg))
			btn.Show()
			self.dungeonButtons.append(btn)
			yPos += 25
			
		# Right side: Info and actions
		self.bgRight = ui.Bar()
		self.bgRight.SetParent(self)
		self.bgRight.SetPosition(200, 35)
		self.bgRight.SetSize(240, 300)
		self.bgRight.SetColor(0x77000000)
		self.bgRight.Show()
		
		self.infoTextBoss = ui.TextLine()
		self.infoTextBoss.SetParent(self.bgRight)
		self.infoTextBoss.SetPosition(10, 10)
		self.infoTextBoss.SetText("Boss: -")
		self.infoTextBoss.Show()
		
		self.infoTextLevel = ui.TextLine()
		self.infoTextLevel.SetParent(self.bgRight)
		self.infoTextLevel.SetPosition(10, 30)
		self.infoTextLevel.SetText("Szükséges szint: -")
		self.infoTextLevel.Show()
		
		self.infoTextTicket = ui.TextLine()
		self.infoTextTicket.SetParent(self.bgRight)
		self.infoTextTicket.SetPosition(10, 50)
		self.infoTextTicket.SetText("Belépő tárgy: -")
		self.infoTextTicket.Show()
		
		self.btnShop = ui.Button()
		self.btnShop.SetParent(self.bgRight)
		self.btnShop.SetPosition(20, 220)
		self.btnShop.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.btnShop.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.btnShop.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.btnShop.SetText("Bolt megnyitása")
		self.btnShop.SetEvent(self.ClickShop)
		self.btnShop.Show()
		
		self.btnTeleport = ui.Button()
		self.btnTeleport.SetParent(self.bgRight)
		self.btnTeleport.SetPosition(20, 250)
		self.btnTeleport.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.btnTeleport.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.btnTeleport.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.btnTeleport.SetText("Teleportálás")
		self.btnTeleport.SetEvent(self.ClickTeleport)
		self.btnTeleport.Show()
		
		if len(DUNGEON_DATA) > 0:
			self.SelectDungeon(0)

	def SelectDungeon(self, index):
		self.selectedDungeon = index
		data = DUNGEON_DATA[index]
		self.infoTextBoss.SetText("Főellenség: " + data["boss"])
		self.infoTextLevel.SetText("Szükséges szint: " + str(data["min_level"]))
		self.infoTextTicket.SetText("Belépő tárgy: " + data["ticket"])

	def ClickShop(self):
		net.SendChatPacket("/dungeon_cmd shop " + str(DUNGEON_DATA[self.selectedDungeon]["id"]))
		
	def ClickTeleport(self):
		net.SendChatPacket("/dungeon_cmd teleport " + str(DUNGEON_DATA[self.selectedDungeon]["id"]))

	def Open(self):
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
