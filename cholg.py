#todo:
#przeciwnicy sie respoą na sobie nw czemu (chyba naprawilem)
#pathfinding i tury przeciwnikow

import math
import random
import pyray as pr #pyray to jakas inna biblioteka ale chodzi o "raylib", niewiem czemu w pythonie nazywa sie pyray zamiast raylib
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pr.init_window(1024,960,"cholg")
pr.set_target_fps(60) 

Plansza =[[0 for x in range(15)] for y in range(15)] #plansza 15x15 glownie uzywania do trawy
menu_eq = False #zmienna ktora pokazuje ze jest sie w menu
PlayerTurn=True #zmienna ktora pokazuje ze jest tura gracza
start_menu = True #zmienna ktora pozazuje czy gracz jest w menu startowym gdzie jest przycisk start czy cos?
poziom = 0 #poziom na jakim aktualnie jest gracz
level_shift_animation = 0 #0 - brak animacii 90 - poczatek animacii (1.5 sek powinna trwac animacja)
koszty_strzalu = {"railgun_barrel":3,"normal_barrel":3,"prisma_barrel":4,"bubble_barrel":2,"cow_barrel":3,"shotgun_barrel":6,"chain_barrel":1,"sword_barrel":5,"lego_barrel":3,"golden_barrel":6}
pr.init_audio_device()
class gracz:
    def __init__(self,posx,posy):
        self.x = posx #aktualna w poziomie pozycja na planszy 15x15
        self.y = posy #aktualna w pionie pozycja na planszy 15x15
        self.maxenergii = 8 #maxymalna energia jaka gracz moze posiadac
        self.aktualnaenergia = 8 #aktualna energia potrzebna do wykonywania czynnosci takich jak poruszanie sie, strzelanie czy zmienianie broni
        self.obrot = 0 #obrot gracza od 0 do 3 
        self.hp = 25
        self.maxhp = 25
        self.posiadane_bronie = ["railgun_barrel","normal_barrel"] #lista posiadanych barreli przez gracza
        self.aktualna_bron = "railgun_barrel" #jaka jest aktualna bron zalozona przez gracza
        self.animacja = 0 #0 to koniec/brak animacji 16 to poczatek
        self.money = 50 #pieniądze używane do kupowania w sklepie
    def narysuj(self):
        if(self.animacja !=0):
            match self.obrot:
                case 0:
                    pr.draw_texture_tiled(czolg,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32 ,self.y*64+32+(self.animacja*4),64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
                    Rysowanie_Broni(self.aktualna_bron,self.x,self.y+(self.animacja/16),self.obrot)
                case 1:
                    pr.draw_texture_tiled(czolg,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32-(self.animacja*4) ,self.y*64+32,64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
                    Rysowanie_Broni(self.aktualna_bron,self.x-(self.animacja/16),self.y,self.obrot)
                case 2:
                    pr.draw_texture_tiled(czolg,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32 ,self.y*64+32-(self.animacja*4),64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
                    Rysowanie_Broni(self.aktualna_bron,self.x,self.y-(self.animacja/16),self.obrot)
                case 3:
                    pr.draw_texture_tiled(czolg,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32+(self.animacja*4) ,self.y*64+32,64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
                    Rysowanie_Broni(self.aktualna_bron,self.x+(self.animacja/16),self.y,self.obrot)
            if (self.animacja >0):
                self.animacja -=1
            if(self.animacja <0):
                self.animacja +=1
        else:
            pr.draw_texture_tiled(czolg,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32,self.y*64+32,64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
            Rysowanie_Broni(self.aktualna_bron,self.x,self.y,self.obrot)
        if (pr.get_mouse_x() > self.x*64 and pr.get_mouse_x() < (self.x+1)*64 and pr.get_mouse_y() > self.y*64 and pr.get_mouse_y() < (self.y+1)*64 and menu_eq == False):
                pr.draw_text(str(self.hp),self.x*64,self.y*64,64,pr.YELLOW)
    def strzel(self):
        if self.aktualnaenergia >= koszty_strzalu[self.aktualna_bron]:
            self.aktualnaenergia -=koszty_strzalu[self.aktualna_bron]
            strzal(obiekt_gracz.x,obiekt_gracz.y,obiekt_gracz.obrot,obiekt_gracz.aktualna_bron)
    def zadaj_obrazenia(self,obrazenia):
        self.hp -= obrazenia
        if (self.hp <=0):
            temp = Explosion(self.x,self.y)
            print("koniec gry")
        else:
            temp = Damage(self.x,self.y)
    


class przeszkody:
    def __init__(self,posx,posy):
        self.x=posx
        self.y=posy
        self.hp = 10
        temp = random.randint(0,2)
        match temp:
            case 0:
                self.sprite = budynek_tile1
            case 1:
                self.sprite = budynek_tile2
            case 2:
                self.sprite = budynek_tile3
    def narysuj(self):
        pr.draw_texture(self.sprite,self.x*64,self.y*64,pr.WHITE)
        if (pr.get_mouse_x() > self.x*64 and pr.get_mouse_x() < (self.x+1)*64 and pr.get_mouse_y() > self.y*64 and pr.get_mouse_y() < (self.y+1)*64 and menu_eq == False):
            pr.draw_text(str(self.hp),self.x*64,self.y*64,64,pr.YELLOW)
    def zadaj_obrazenia(self,obrazenia):
        self.hp -= obrazenia
        if (self.hp <=0):
            temp = Explosion(self.x,self.y)
            przeszkody_arr.remove(self)
        else:
            temp = Damage(self.x,self.y)

class trawa:
    def __init__(self,posx,posy):
        self.x=posx
        self.y=posy
        temp = random.randint(0,2)
        match temp:
            case 0:
                self.sprite = trawa_tile1
            case 1:
                self.sprite = trawa_tile2
            case 2:
                self.sprite = trawa_tile3
    def narysuj(self):
        pr.draw_texture(self.sprite,self.x*64,self.y*64,pr.WHITE)

class przeciwnik:
    def __init__(self,posx,posy):
        self.x = posx
        self.y = posy
        self.obrot = 0
        self.hp = 10
        self.aktualna_bron = "normal_barrel"
        
    def narysuj(self):
        pr.draw_texture_tiled(przeciwnik_textue,pr.Rectangle(0,0,64,64),pr.Rectangle(self.x*64+32,self.y*64+32,64,64),pr.Vector2(32,32),90*self.obrot,1,pr.WHITE)
        Rysowanie_Broni(self.aktualna_bron,self.x,self.y,self.obrot)
        if (pr.get_mouse_x() > self.x*64 and pr.get_mouse_x() < (self.x+1)*64 and pr.get_mouse_y() > self.y*64 and pr.get_mouse_y() < (self.y+1)*64 and menu_eq == False):
            pr.draw_text(str(self.hp),self.x*64,self.y*64,64,pr.YELLOW)
    def zadaj_obrazenia(self,obrazenia):
        self.hp -= obrazenia
        if (self.hp <=0): #jezeli hp jest mniejsze rowne 0
            temp = Explosion(self.x,self.y) #twozy nowy obiekt "temp" klasy Explosion w miejscu czolgu
            global obiekt_gracz #tylko po to by dodac pieniadze linijke nizej
            obiekt_gracz.money += random.randint(10,30) #jak przeciwnik zostaje zniszczony do pieniędzy gracza zostaje dodane od 10 do 30 pieniędzy włącznie
            przeciwnicy_arr.remove(self) #usuwa sie z listy
        else:
            temp = Damage(self.x,self.y)
    def tura_przeciwnika(self): #https://www.youtube.com/watch?v=8SigT_jhz4I - tutorial z jakiego kozystalem do pathfindingu 
        czy_strzelono = False #czolg nie poruszy sie w tej tuze gdy strzeli, nie wazne czy to 1 czy 2 czy 3 ruch
        for i in range(3):
            matrix =[[1 for x in range(15)] for y in range(15)]
            for obj in przeciwnicy_arr:
                
                matrix[obj.y][obj.x] = 0
            for obj in przeszkody_arr:
                matrix[obj.y][obj.x] = 0
            grid = Grid(matrix = matrix)
            start = grid.node(self.x,self.y)
            end = grid.node(obiekt_gracz.x,obiekt_gracz.y)
            finder = AStarFinder()
            path,runs = finder.find_path(start,end,grid)
            if len(path)>1 and czy_strzelono == False:
                next_x = path[1][0]
                next_y = path[1][1]
                kierunek = ''
                if(self.x == next_x+1 and self.y == next_y):
                    kierunek = "lewo"
                elif(self.x == next_x-1 and self.y == next_y):
                    kierunek = "prawo"
                elif(self.x == next_x and self.y == next_y+1):
                    kierunek = "gora"
                elif(self.x == next_x and self.y == next_y-1):
                    kierunek = "dol"
                
                match self.obrot:
                    case 0:
                        if kierunek == "gora":
                            if [obiekt_gracz.x,obiekt_gracz.y]in[[self.x,self.y-1],[self.x,self.y-2],[self.x,self.y-3]]:
                                czy_strzelono = True
                                strzal(self.x,self.y,self.obrot,self.aktualna_bron)
                            elif obiekt_gracz.y != self.y-1 or obiekt_gracz.x !=self.x:
                                if CzyJestobiekt(next_x,next_y) == False:
                                    self.y -= 1
                        elif kierunek == "prawo" or kierunek == "dol":
                            self.obrot+=1
                            if(self.obrot>=4):
                                self.obrot=0
                        elif kierunek == "lewo":
                            self.obrot-=1
                            if(self.obrot<0):
                                self.obrot=3
                    case 1:
                        if kierunek == "prawo":
                            if [obiekt_gracz.x,obiekt_gracz.y]in[[self.x+1,self.y],[self.x+2,self.y],[self.x+3,self.y]]:
                                czy_strzelono = True
                                strzal(self.x,self.y,self.obrot,self.aktualna_bron)
                            elif obiekt_gracz.x != self.x+1 or obiekt_gracz.y != self.y:
                                if CzyJestobiekt(next_x,next_y) == False:
                                    self.x +=1
                        elif kierunek == "dol" or kierunek == "lewo":
                            self.obrot+=1
                            if(self.obrot>=4):
                                self.obrot=0
                        elif kierunek == "gora":
                            self.obrot-=1
                            if(self.obrot<0):
                                self.obrot=3
                    case 2:
                        if kierunek == "dol" :
                            if [obiekt_gracz.x,obiekt_gracz.y]in[[self.x,self.y+1],[self.x,self.y+2],[self.x,self.y+3]]:
                                czy_strzelono = True
                                strzal(self.x,self.y,self.obrot,self.aktualna_bron)
                            elif obiekt_gracz.y != self.y+1 or obiekt_gracz.x !=self.x:
                                if CzyJestobiekt(next_x,next_y) == False:
                                    self.y +=1
                        elif kierunek == "lewo" or kierunek == "gora":
                            self.obrot+=1
                            if(self.obrot>=4):
                                self.obrot=0
                        elif kierunek == "prawo":
                            self.obrot-=1
                            if(self.obrot<0):
                                self.obrot=3
                    case 3: 
                        if kierunek == "lewo":
                            if [obiekt_gracz.x,obiekt_gracz.y]in[[self.x-1,self.y],[self.x-2,self.y],[self.x-3,self.y]]:
                                czy_strzelono = True
                                strzal(self.x,self.y,self.obrot,self.aktualna_bron)
                            elif obiekt_gracz.x != self.x-1 or obiekt_gracz.y != self.y:
                                if CzyJestobiekt(next_x,next_y) == False:
                                    self.x -=1
                        elif kierunek == "gora" or kierunek =="prawo":
                            self.obrot+=1
                            if(self.obrot>=4):
                                self.obrot=0
                        elif kierunek == "dol":
                            self.obrot-=1
                            if(self.obrot<0):
                                self.obrot=3
                pr.begin_drawing()
                pr.clear_background(pr.WHITE)
                
                RysowaniePlanszy()
                RysowanieUi()
                pr.end_drawing()
        
            
        

class dash_smoke:
    def __init__(self,posx,posy,obrotval):
        self.x = posx
        self.y=posy
        self.obrot = obrotval
        self.lifetime = 11
        smoke_arr.append(self)
    def narysuj(self):
        pr.draw_texture_tiled(steam_dash_sheet,pr.Rectangle(0 + (11-self.lifetime)*64,0,64,64),pr.Rectangle(self.x*64+32,self.y*64+32,64,64),pr.Vector2(32,32),90*(self.obrot-1),1,pr.WHITE)
        self.lifetime -=1
        if self.lifetime<=0:
            smoke_arr.remove(self)

class Explosion:
    def __init__(self,posx,posy):
        self.x = posx
        self.y=posy
        self.lifetime = 7
        particles_arr.append(self)
    def narysuj(self):
        pr.draw_texture_tiled(explosion_sheet,pr.Rectangle(0 + (7-self.lifetime)*64,0,64,64),pr.Rectangle(self.x*64+32,self.y*64+32,64,64),pr.Vector2(32,32),0,1,pr.WHITE)
        self.lifetime -=1
        if self.lifetime<=0:
            particles_arr.remove(self)

class Damage:
    def __init__(self,posx,posy):
        self.x = posx
        self.y=posy
        self.lifetime = 6
        particles_arr.append(self)
    def narysuj(self):
        pr.draw_texture_tiled(damage_sheet,pr.Rectangle(0 + (6-self.lifetime)*64,0,64,64),pr.Rectangle(self.x*64+32,self.y*64+32,64,64),pr.Vector2(32,32),0,1,pr.WHITE)
        self.lifetime -=1
        if self.lifetime<=0:
            particles_arr.remove(self)


temp = pr.load_image("sprite/czolg-gracz.png")
pr.image_resize(temp,64,64)
czolg = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/explosion.png")
pr.image_resize(temp,448,64)
explosion_sheet = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/steam_dash.png")
pr.image_resize(temp,704,64)
steam_dash_sheet = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/damage.png")
pr.image_resize(temp,384,64)
damage_sheet = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/railgun.png")
pr.image_resize(temp,64,64)
railgun_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/normal_barrel.png")
pr.image_resize(temp,64,64)
normal_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/prisma_barrel.png")
pr.image_resize(temp,64,64)
prisma_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/bubble_barrel.png")
pr.image_resize(temp,64,64)
bubble_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/cow_barrel.png")
pr.image_resize(temp,64,64)
cow_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/shotgun_barrel.png")
pr.image_resize(temp,64,64)
shotgun_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/chain_barrel.png")
pr.image_resize(temp,64,64)
chain_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/sword_barrel.png")
pr.image_resize(temp,64,64)
sword_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/lego_barrel.png")
pr.image_resize(temp,64,64)
lego_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/golden_barrel.png")
pr.image_resize(temp,64,64)
golden_barrel_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)


temp = pr.load_image("sprite/enemy.png")
pr.image_resize(temp,64,64)
przeciwnik_textue = pr.load_texture_from_image(temp)
pr.unload_image(temp)


temp = pr.load_image("sprite/trawa1.png")
pr.image_resize(temp,64,64)
trawa_tile1 = pr.load_texture_from_image(temp)
pr.unload_image(temp)
temp = pr.load_image("sprite/trawa2.png")
pr.image_resize(temp,64,64)
trawa_tile2 = pr.load_texture_from_image(temp)
pr.unload_image(temp)
temp = pr.load_image("sprite/trawa3.png")
pr.image_resize(temp,64,64)
trawa_tile3 = pr.load_texture_from_image(temp)
pr.unload_image(temp)


temp = pr.load_image("sprite/budynek1.png")
pr.image_resize(temp,64,64)
budynek_tile1 = pr.load_texture_from_image(temp)
pr.unload_image(temp)
temp = pr.load_image("sprite/budynek2.png")
pr.image_resize(temp,64,64)
budynek_tile2 = pr.load_texture_from_image(temp)
pr.unload_image(temp)
temp = pr.load_image("sprite/budynek3.png")
pr.image_resize(temp,64,64)
budynek_tile3 = pr.load_texture_from_image(temp)
pr.unload_image(temp)


temp = pr.load_image("sprite/energy_full.png")
pr.image_resize(temp,32,32)
energy_full_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/energy_empty.png")
pr.image_resize(temp,32,32)
energy_empty_texture = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/menu_pixelart.png")
pr.image_resize(temp,512,128)
menu_sprite = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/start_button_sprite.png")
pr.image_resize(temp,128,64)
start_button_sprite = pr.load_texture_from_image(temp)
pr.unload_image(temp)

temp = pr.load_image("sprite/shift_animation_sprite.png")
pr.image_resize(temp,1536,960)
shift_animation_sprite = pr.load_texture_from_image(temp)
pr.unload_image(temp)


ui_cancel_audio = pr.load_sound("sounds/ui_cancel.wav")


obiekt_gracz = gracz(-1,-1)
przeszkody_arr = [przeszkody(-1,-1) for i in range(10)]
przeciwnicy_arr = [przeciwnik(-1,-1) for i in range(1)]
trawy_arr =[trawa(x,y) for x in range(15) for y in range(15)]
smoke_arr = []
particles_arr = [] #eksplozje itp

def RysowaniePlanszy():
    for obj in trawy_arr:
        obj.narysuj()
    obiekt_gracz.narysuj()
    for obj in przeszkody_arr:
        obj.narysuj()
    for obj in przeciwnicy_arr:
        obj.narysuj()
    for obj in smoke_arr:
        obj.narysuj()
    for obj in particles_arr:
        obj.narysuj()


def RysowanieUi():
    
    global obiekt_gracz
    for i in range(obiekt_gracz.maxenergii):
        if(i<obiekt_gracz.aktualnaenergia):
            pr.draw_texture(energy_full_texture,976,16+i*48,pr.WHITE)
        else:
            pr.draw_texture(energy_empty_texture,976,16+i*48,pr.WHITE)
    
    pr.draw_text(str(obiekt_gracz.maxhp),976,930,32,pr.RED)
    pr.draw_rectangle(970,928,40,3,pr.RED)
    pr.draw_text(str(obiekt_gracz.hp),976,900,32,pr.RED)
    pr.draw_text(str(poziom),976,870,32,pr.BLUE)
    if menu_eq == True:
        
        pr.draw_rectangle(0,0,1024,960,pr.Color(0,0,0,100))
        pr.draw_text("Available Wepons",208,0,64,pr.WHITE) #na oko jest po środku ;)
        if "railgun_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(0,96,64,64,pr.WHITE)
            pr.draw_texture_ex(railgun_texture,pr.Vector2(0,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(0,96,64,64,pr.RED)
            pr.draw_texture_ex(railgun_texture,pr.Vector2(0,96),0,1,pr.RED)

        if pr.get_mouse_x() > 0 and pr.get_mouse_x()<64 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "railgun_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "railgun_barrel"
            else:
                pr.play_sound(ui_cancel_audio)


        if "normal_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(96,96,64,64,pr.WHITE)
            pr.draw_texture_ex(normal_barrel_texture,pr.Vector2(96,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(96,96,64,64,pr.RED)
            pr.draw_texture_ex(normal_barrel_texture,pr.Vector2(96,96),0,1,pr.RED)

        if pr.get_mouse_x() > 96 and pr.get_mouse_x()<160 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "normal_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "normal_barrel"
            else:
                pr.play_sound(ui_cancel_audio)
        

        if "prisma_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(192,96,64,64,pr.WHITE)
            pr.draw_texture_ex(prisma_barrel_texture,pr.Vector2(192,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(192,96,64,64,pr.RED)
            pr.draw_texture_ex(prisma_barrel_texture,pr.Vector2(192,96),0,1,pr.RED)

        if pr.get_mouse_x() > 192 and pr.get_mouse_x()<256 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "prisma_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "prisma_barrel"
            else:
                pr.play_sound(ui_cancel_audio)
        
        if "bubble_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(288,96,64,64,pr.WHITE)
            pr.draw_texture_ex(bubble_barrel_texture,pr.Vector2(288,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(288,96,64,64,pr.RED)
            pr.draw_texture_ex(bubble_barrel_texture,pr.Vector2(288,96),0,1,pr.RED)

        if pr.get_mouse_x() > 288 and pr.get_mouse_x()<352 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "bubble_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "bubble_barrel"
            else:
                pr.play_sound(ui_cancel_audio)
        
        if "cow_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(384,96,64,64,pr.WHITE)
            pr.draw_texture_ex(cow_barrel_texture,pr.Vector2(384,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(384,96,64,64,pr.RED)
            pr.draw_texture_ex(cow_barrel_texture,pr.Vector2(384,96),0,1,pr.RED)
        
        if pr.get_mouse_x() > 384 and pr.get_mouse_x()<448 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "cow_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "cow_barrel"
            else:
                pr.play_sound(ui_cancel_audio)

        if "shotgun_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(480,96,64,64,pr.WHITE)
            pr.draw_texture_ex(shotgun_barrel_texture,pr.Vector2(480,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(480,96,64,64,pr.RED)
            pr.draw_texture_ex(shotgun_barrel_texture,pr.Vector2(480,96),0,1,pr.RED)
        if pr.get_mouse_x() > 480 and pr.get_mouse_x()<544 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "shotgun_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "shotgun_barrel"
            else:
                pr.play_sound(ui_cancel_audio)
        
        if "chain_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(576,96,64,64,pr.WHITE)
            pr.draw_texture_ex(chain_barrel_texture,pr.Vector2(576,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(576,96,64,64,pr.RED)
            pr.draw_texture_ex(chain_barrel_texture,pr.Vector2(576,96),0,1,pr.RED)
        if pr.get_mouse_x() > 576 and pr.get_mouse_x()<640 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "chain_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "chain_barrel"
            else:
                pr.play_sound(ui_cancel_audio)

        if "sword_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(672,96,64,64,pr.WHITE)
            pr.draw_texture_ex(sword_barrel_texture,pr.Vector2(672,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(672,96,64,64,pr.RED)
            pr.draw_texture_ex(sword_barrel_texture,pr.Vector2(672,96),0,1,pr.RED)
        if pr.get_mouse_x() > 672 and pr.get_mouse_x()<736 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "sword_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "sword_barrel"
            else:
                pr.play_sound(ui_cancel_audio)

        if "lego_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(768,96,64,64,pr.WHITE)
            pr.draw_texture_ex(lego_barrel_texture,pr.Vector2(768,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(768,96,64,64,pr.RED)
            pr.draw_texture_ex(lego_barrel_texture,pr.Vector2(768,96),0,1,pr.RED)
        if pr.get_mouse_x() > 768 and pr.get_mouse_x()<832 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "lego_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "lego_barrel"
            else:
                pr.play_sound(ui_cancel_audio)
        if "golden_barrel" in obiekt_gracz.posiadane_bronie:
            pr.draw_rectangle(864,96,64,64,pr.WHITE)
            pr.draw_texture_ex(golden_barrel_texture,pr.Vector2(864,96),0,1,pr.WHITE)
        else:
            pr.draw_rectangle(864,96,64,64,pr.RED)
            pr.draw_texture_ex(golden_barrel_texture,pr.Vector2(864,96),0,1,pr.RED)
        if pr.get_mouse_x() > 864 and pr.get_mouse_x()<928 and pr.get_mouse_y() > 96 and pr.get_mouse_y() < 160 and pr.is_mouse_button_pressed(0):
            if "golden_barrel" in obiekt_gracz.posiadane_bronie:
                obiekt_gracz.aktualna_bron = "golden_barrel"
            else:
                pr.play_sound(ui_cancel_audio)

    global level_shift_animation
    if(level_shift_animation >0):
        if (level_shift_animation>30):
            pr.draw_texture(shift_animation_sprite,0,0,pr.WHITE)
            pr.draw_text("poziom: "+str(poziom),450,500,32,pr.WHITE)
        else:
            pr.draw_texture(shift_animation_sprite,0+math.floor(level_shift_animation*100 - 3000),0,pr.WHITE)
            pr.draw_text("poziom: "+str(poziom),450+math.floor(level_shift_animation*100 - 3000),500,32,pr.WHITE)
        level_shift_animation -=1
        
def Rysowanie_Menu_Glownego():
    global start_menu
    pr.clear_background(pr.WHITE)
    pr.draw_texture(menu_sprite,256,200,pr.WHITE)
    pr.draw_texture(start_button_sprite,448,500,pr.WHITE)
    if (pr.get_mouse_x()>448 and pr.get_mouse_x()<576 and pr.get_mouse_y() >500 and pr.get_mouse_y() < 564 and pr.is_mouse_button_pressed(0)):
        start_menu = False
            
            
            
def CzyJestobiekt(xpos,ypos):
    for obj in przeszkody_arr:
        if(xpos==obj.x and ypos==obj.y):
            return True
    for obj in przeciwnicy_arr:
        if(xpos==obj.x and ypos==obj.y):
            return True
    if(obiekt_gracz.x==xpos and obiekt_gracz.y==ypos):
        return True
    else:
        return False
    

def Poruszanie_gracza(tryb):
    if(obiekt_gracz.aktualnaenergia>0):
        match tryb:
            case 0:#jazda na wprost
                match obiekt_gracz.obrot:
                    case 0: 
                        if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y-1)==False and obiekt_gracz.y>0 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.y-=1
                            obiekt_gracz.animacja = 16
                    case 1:  
                        if(CzyJestobiekt(obiekt_gracz.x+1,obiekt_gracz.y)==False and obiekt_gracz.x<14 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.x+=1
                            obiekt_gracz.animacja = 16
                    case 2: 
                        if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y+1)==False and obiekt_gracz.y<14 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.y+=1
                            obiekt_gracz.animacja = 16
                    case 3:
                        if(CzyJestobiekt(obiekt_gracz.x-1,obiekt_gracz.y)==False and obiekt_gracz.x>0 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.x-=1
                            obiekt_gracz.animacja = 16
            case 1:#dash w prawo
                if(obiekt_gracz.aktualnaenergia>1):
                    match obiekt_gracz.obrot:
                        case 0:
                            if(CzyJestobiekt(obiekt_gracz.x+1,obiekt_gracz.y)==False and obiekt_gracz.x<14):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.x+=1
                                temp = dash_smoke(obiekt_gracz.x -1,obiekt_gracz.y,obiekt_gracz.obrot)
                        case 1:
                            if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y+1)==False and obiekt_gracz.y<14):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.y+=1
                                temp = dash_smoke(obiekt_gracz.x ,obiekt_gracz.y -1,obiekt_gracz.obrot)
                        case 2:
                            if(CzyJestobiekt(obiekt_gracz.x-1,obiekt_gracz.y)==False and obiekt_gracz.x>0):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.x-=1
                                temp = dash_smoke(obiekt_gracz.x+1,obiekt_gracz.y,obiekt_gracz.obrot)
                        case 3:
                            if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y-1)==False and obiekt_gracz.y>0):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.y-=1
                                temp = dash_smoke(obiekt_gracz.x ,obiekt_gracz.y+1,obiekt_gracz.obrot)
            case 2:#dash w lewo
                if(obiekt_gracz.aktualnaenergia>1):
                    match obiekt_gracz.obrot:
                        case 0:
                            if(CzyJestobiekt(obiekt_gracz.x-1,obiekt_gracz.y)==False and obiekt_gracz.x>0):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.x-=1
                                temp = dash_smoke(obiekt_gracz.x +1,obiekt_gracz.y,obiekt_gracz.obrot-2)
                        case 1:
                            if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y-1)==False and obiekt_gracz.y>0):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.y-=1
                                temp = dash_smoke(obiekt_gracz.x ,obiekt_gracz.y+1,obiekt_gracz.obrot-2)
                        case 2:
                            if(CzyJestobiekt(obiekt_gracz.x+1,obiekt_gracz.y)==False and obiekt_gracz.x<14):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.x+=1
                                temp = dash_smoke(obiekt_gracz.x -1,obiekt_gracz.y,obiekt_gracz.obrot-2)
                        case 3:
                            if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y+1)==False and obiekt_gracz.y<14):
                                obiekt_gracz.aktualnaenergia-=2
                                obiekt_gracz.y+=1
                                temp = dash_smoke(obiekt_gracz.x ,obiekt_gracz.y-1,obiekt_gracz.obrot-2)
            case 3: #obrot w prawo
                obiekt_gracz.aktualnaenergia-=1
                obiekt_gracz.obrot+=1
                if(obiekt_gracz.obrot>=4):
                    obiekt_gracz.obrot=0
            case 4: #obrot w lewo
                obiekt_gracz.aktualnaenergia-=1
                obiekt_gracz.obrot-=1
                if(obiekt_gracz.obrot<=-1):
                    obiekt_gracz.obrot=3
            case 5: #jazda w tył
                match obiekt_gracz.obrot:
                    case 0:
                        if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y+1)==False and obiekt_gracz.y<14 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.y+=1
                            obiekt_gracz.animacja = -16
                    case 1: 
                        if(CzyJestobiekt(obiekt_gracz.x-1,obiekt_gracz.y)==False and obiekt_gracz.x>0 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.x-=1
                            obiekt_gracz.animacja = -16
                    case 2:
                        if(CzyJestobiekt(obiekt_gracz.x,obiekt_gracz.y-1)==False and obiekt_gracz.y>0 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.y-=1
                            obiekt_gracz.animacja = -16
                    case 3:
                        if(CzyJestobiekt(obiekt_gracz.x+1,obiekt_gracz.y)==False and obiekt_gracz.x<14 and obiekt_gracz.animacja==0):
                            obiekt_gracz.aktualnaenergia-=1
                            obiekt_gracz.x+=1
                            obiekt_gracz.animacja = -16

def Kolejna_Tura():
    obiekt_gracz.aktualnaenergia = obiekt_gracz.maxenergii
    for obj in przeciwnicy_arr:
        obj.tura_przeciwnika()

def Rysowanie_Broni(nazwa,x,y,obrot):
    match nazwa:
            case "railgun_barrel":
                pr.draw_texture_tiled(railgun_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "normal_barrel":
                pr.draw_texture_tiled(normal_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "prisma_barrel":
                pr.draw_texture_tiled(prisma_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "bubble_barrel":
                pr.draw_texture_tiled(bubble_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "cow_barrel":
                pr.draw_texture_tiled(cow_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "shotgun_barrel":
                pr.draw_texture_tiled(shotgun_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "chain_barrel":
                pr.draw_texture_tiled(chain_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "sword_barrel":
                pr.draw_texture_tiled(sword_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "lego_barrel":
                pr.draw_texture_tiled(lego_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)
            case "golden_barrel":
                pr.draw_texture_tiled(golden_barrel_texture,pr.Rectangle(0,0,64,64),pr.Rectangle(x*64+32,y*64+32,64,64),pr.Vector2(32,32),90*obrot,1,pr.WHITE)

def strzal(poczatekx,poczateky,kierunek,nazwa):
    targets = []
    match nazwa: 
        case "railgun_barrel": #zasieg 3 na wprzod , 3 obr , wszystkie cele
            for i in range(3):
                match kierunek:
                    case 0:
                        targets.append([poczatekx,poczateky-i-1])
                    case 1:
                        targets.append([poczatekx+i+1,poczateky])
                    case 2:
                        targets.append([poczatekx,poczateky+i+1])
                    case 3:
                        targets.append([poczatekx-i-1,poczateky])
    
            for i in targets:
                if obiekt_gracz.x == i[0] and obiekt_gracz.y == i[1]:
                    obiekt_gracz.zadaj_obrazenia(3)
                for obj in przeciwnicy_arr:
                    if obj.x == i[0] and obj.y ==i[1]:
                        obj.zadaj_obrazenia(3)
                for obj in przeszkody_arr:
                    if obj.x == i[0] and obj.y == i[1]:
                        obj.zadaj_obrazenia(3)
        case "normal_barrel": #zasieg 3 w przod , 5 obr, pierwszy cel
            temp = True #zmienna sie zmienia na False jak trafi cel
            for i in range(3):
                match kierunek:
                    case 0:
                        targets.append([poczatekx,poczateky-i-1])
                    case 1:
                        targets.append([poczatekx+i+1,poczateky])
                    case 2:
                        targets.append([poczatekx,poczateky+i+1])
                    case 3:
                        targets.append([poczatekx-i-1,poczateky])
            for i in targets:
                if temp == True:
                    if obiekt_gracz.x == i[0] and obiekt_gracz.y == i[1]:
                        obiekt_gracz.zadaj_obrazenia(5)
                        temp = False
                    for obj in przeciwnicy_arr:
                        if obj.x == i[0] and obj.y ==i[1]:
                            obj.zadaj_obrazenia(5)
                            temp = False
                    for obj in przeszkody_arr:
                        if obj.x == i[0] and obj.y == i[1]:
                            obj.zadaj_obrazenia(5)
                            temp = False
        case "prisma_barrel": #zasieg 5 na wprzod , 2 obr , wszystkie cele
            for i in range(5):
                match kierunek:
                    case 0:
                        targets.append([poczatekx,poczateky-i-1])
                    case 1:
                        targets.append([poczatekx+i+1,poczateky])
                    case 2:
                        targets.append([poczatekx,poczateky+i+1])
                    case 3:
                        targets.append([poczatekx-i-1,poczateky])
    
            for i in targets:
                if obiekt_gracz.x == i[0] and obiekt_gracz.y == i[1]:
                    obiekt_gracz.zadaj_obrazenia(2)
                for obj in przeciwnicy_arr:
                    if obj.x == i[0] and obj.y ==i[1]:
                        obj.zadaj_obrazenia(2)
                for obj in przeszkody_arr:
                    if obj.x == i[0] and obj.y == i[1]:
                        obj.zadaj_obrazenia(2)

def nowy_poziom():
    global poziom,obiekt_gracz,przeciwnicy_arr,przeciwnicy_arr,przeszkody_arr,level_shift_animation
    level_shift_animation = 90
    poziom +=1
    obiekt_gracz.x = -1 #zmienia lokacje gracza na taka poza plansza zeby nie przeszkadzal w rozmieszczaniu przeszkod i przeciwnikow
    obiekt_gracz.y = -1
    obiekt_gracz.aktualnaenergia = obiekt_gracz.maxenergii #odnawia energie na poczatku nowego poziomu
    temp = math.floor(obiekt_gracz.maxhp/10) #10% max hp gracza
    obiekt_gracz.hp += temp #odnawia hp gracza o te 10% maxhp co wyrzej bylo policzone
    if (obiekt_gracz.hp > obiekt_gracz.maxhp): #jezeli gracz ma wiecej hp niz maxhp
        obiekt_gracz.hp = obiekt_gracz.maxhp #ustawia hp na max hp
    if poziom < 10:
        przeszkody_arr = [przeszkody(-1,-1) for i in range(10 + poziom *2)]
        przeciwnicy_arr = [przeciwnik(-1,-1) for i in range(5 + math.floor(poziom/2))]
    else:
        przeszkody_arr = [przeszkody(-1,-1) for i in range(30)]
        przeciwnicy_arr = [przeciwnik(-1,-1) for i in range(10)]
    for obj in przeszkody_arr:
        temp = True
        while(temp):
            licznik = 0
            temp = False 
            obj.x = random.randint(0,14)
            obj.y = random.randint(0,14)
            for obiekttemp in przeszkody_arr:
                if(obiekttemp.x == obj.x and obiekttemp.y == obj.y):
                    licznik+=1
                    if (licznik ==2):
                        temp = True
        
    
    temp = True
    while(temp):
        temp = False
        obiekt_gracz.x = random.randint(0,14)
        obiekt_gracz.y = random.randint(0,14)
        for obiekttemp in przeszkody_arr:
                if(obiekttemp.x == obiekt_gracz.x and obiekttemp.y == obiekt_gracz.y):
                    temp=True

    for obj in przeciwnicy_arr:
        temp = True
        while(temp):
            licznik = 0
            temp = False 
            obj.x = random.randint(0,14)
            obj.y = random.randint(0,14)
            for obiekttemp in przeszkody_arr:
                if(obiekttemp.x == obj.x and obiekttemp.y == obj.y):
                    licznik+=1
                if(obiekt_gracz.x == obj.x and obiekt_gracz.y == obj.y):
                    licznik +=1
                if (licznik ==1):
                    temp = True
                else:
                    temp = False

nowy_poziom()
while not pr.window_should_close():
    if(start_menu == True):
        Rysowanie_Menu_Glownego()
    else:
        if(pr.is_key_pressed(pr.KEY_W) and menu_eq==False): #jazda na wprost
            Poruszanie_gracza(0)
        if(pr.is_key_pressed(pr.KEY_E) and menu_eq==False): #dash w prawo
            Poruszanie_gracza(1)
        if(pr.is_key_pressed(pr.KEY_Q) and menu_eq==False): #dash w lewo
            Poruszanie_gracza(2)
        if(pr.is_key_pressed(pr.KEY_D) and menu_eq==False): #obrot w prawo
            Poruszanie_gracza(3)
        if(pr.is_key_pressed(pr.KEY_A) and menu_eq==False): #obrot w lewo
            Poruszanie_gracza(4)
        if(pr.is_key_pressed(pr.KEY_S) and menu_eq==False): #jazda w tył
            Poruszanie_gracza(5)
        if(pr.is_key_pressed(pr.KEY_P) and menu_eq==False): #kolejna tura
            Kolejna_Tura()
        if(pr.is_key_pressed(pr.KEY_SPACE) and menu_eq==False): #strzal
            obiekt_gracz.strzel()
        if(pr.is_key_pressed(pr.KEY_M) ): #odpala menu eq
            if menu_eq== False:
                menu_eq = True
            else:
                menu_eq = False
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        
        RysowaniePlanszy()
        RysowanieUi()
        if(przeciwnicy_arr ==[]): #jezeli wszyscy przeciwnicy zostali pokonani
            nowy_poziom()
    
    pr.end_drawing()

    

pr.close_window()