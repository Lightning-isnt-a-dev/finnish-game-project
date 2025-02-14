import os, pygame, sys, time, random, pickle


# clear console
def cls():
  input("\nPaina enter jatkaaksesi.")
  os.system('cls' if os.name == 'nt' else 'clear')
  return

def cls_inst():
  os.system('cls' if os.name == 'nt' else 'clear')
  return




def matopeli():
  cls_inst()
  #jos on tallennetut scoret file
  if os.path.exists("matopeli"):
    with open("matopeli", "rb") as scoresfile:
      scores = pickle.load(scoresfile)
  else:
    scores = {}

  #kysytään nimi
  while True:
    name = str(input("Kerro nimesi (paras pisteet tallentuu): "))


    #ei saa olla nimetön
    if name == "":
      print("\nAnna nimesi.")
      cls()
      continue

    #nimi ainakin 3 kirjainta
    if len(name.strip()) <= 2:
      print("\nNimesi tulee olla vähintään 3 kirjainta.")
      cls()
      continue

    #varmistetaan että ei ole väliä lopussa eikä alussa
    if name[0] == " " or name[-1] == " ":
      print("Nimessä ei saa olla väliä alussa eikä lopussa.\n")

      if name.strip() != "":
        inp = input(f"\nSopiiko, että nimesi on {name.strip()}? (y/n)\n\n:").lower()
        if inp == "y":
          name = name.strip()
          break

      cls()
      continue
    break

  cls_inst()

  #jos nimi on tallennettu
  if name in scores:
    print(f"Moi {name}! Sinun tallennettu pisteet: {scores[name]}")
  else:
     print(f"Moi {name}! Tervetuloa matopeliin!")

  cls()
  difficulty = None

  while type(difficulty) != int:
    try:
      #Vaikeus (kuinka nopea mato on)
      difficulty = int(input("Valitse vaikeus (anna joku numero, isompi on vaikeampi eli nopeampi)\n\n:"))
    except ValueError:
      print("Anna numero.")
      cls()

  cls_inst()

  print("Vaihda output-sivuun pelataaksesi matopeliä.")
  time.sleep(3)

  # ikkunan suuruus
  frame_size_x = 640
  frame_size_y = 480

  # aloita peli
  pygame.init()


  # avataaan pelin ikkuna
  pygame.display.set_caption('Matopeli')
  game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


  # värit (R, G, B)
  black = pygame.Color(0, 0, 0)
  white = pygame.Color(255, 255, 255)
  red = pygame.Color(255, 0, 0)
  green = pygame.Color(0, 255, 0)
  blue = pygame.Color(0, 0, 255)


  # FPS
  fps_controller = pygame.time.Clock()


  # aloitus muuttujat
  snake_pos = [100, 50]
  snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

  food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
  food_spawn = True

  direction = 'RIGHT'
  change_to = direction

  score = 0


  # kuoleminen
  def game_over(points, name, scores):
      my_font = pygame.font.SysFont('times new roman', 50)
      game_over_surface = my_font.render('YOU DIED', True, red)
      game_over_rect = game_over_surface.get_rect()
      game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
      game_window.fill(white)
      game_window.blit(game_over_surface, game_over_rect)
      show_score(0, red, 'times', 20)
      pygame.display.flip()
      time.sleep(3)
      pygame.quit()

      if name not in list(scores.keys()):
        scores[name] = points
        print(f"Pisteesi ({points}) ovat tallennettu nimellä {name}!")

      elif scores[name] < points:
        scores[name] = points
        print(f"Pisteesi ({points}) ovat tallennettu nimellä {name}!")

      else:
        print("Sait vähemmän pisteet kuin ennen, mitään ei vaihdu.")


      with open("matopeli", "wb") as points:
        pickle.dump(scores, points)


      again = input("\nHaluatko pelata uudestaan? (y/n)\n\n:").lower()
      cls_inst()

      if again == "y":
        matopeli()
      else:
        main()


  # pisteet
  def show_score(choice, color, font, size):
      score_font = pygame.font.SysFont(font, size)
      score_surface = score_font.render('Pisteet : ' + str(score), True, color)
      score_rect = score_surface.get_rect()
      if choice == 1:
          score_rect.midtop = (frame_size_x/10, 15)
      else:
          score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
      game_window.blit(score_surface, score_rect)


  # pelin koodi
  while True:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          # kun painat näppäin
          elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_UP or event.key == ord('w'):
                  change_to = 'UP'
              if event.key == pygame.K_DOWN or event.key == ord('s'):
                  change_to = 'DOWN'
              if event.key == pygame.K_LEFT or event.key == ord('a'):
                  change_to = 'LEFT'
              if event.key == pygame.K_RIGHT or event.key == ord('d'):
                  change_to = 'RIGHT'
              # voit painaa esc et meet pois pelistä
              if event.key == pygame.K_ESCAPE:
                  pygame.event.post(pygame.event.Event(pygame.QUIT))

      # varmistetaan että mato ei voi vaihtaa suuntana vastaiseksi heti
      if change_to == 'UP' and direction != 'DOWN':
          direction = 'UP'
      if change_to == 'DOWN' and direction != 'UP':
          direction = 'DOWN'
      if change_to == 'LEFT' and direction != 'RIGHT':
          direction = 'LEFT'
      if change_to == 'RIGHT' and direction != 'LEFT':
          direction = 'RIGHT'

      # liikkuminen
      if direction == 'UP':
          snake_pos[1] -= 10
      if direction == 'DOWN':
          snake_pos[1] += 10
      if direction == 'LEFT':
          snake_pos[0] -= 10
      if direction == 'RIGHT':
          snake_pos[0] += 10

      # madon kasvaminen
      snake_body.insert(0, list(snake_pos))
      if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
          score += 1
          food_spawn = False
      else:
          snake_body.pop()

      # ruoan spawnamnien
      if not food_spawn:
          food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
      food_spawn = True

      # piirtäminen
      game_window.fill(white)
      for pos in snake_body:
          # mato
          pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

      # ruoka
      pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

      # pelin loppumisen varmistaminen
      # tarkistetaan että mato ei ole pelin rajojen ulkopuolella
      if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over(score, name, scores)
      if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over(score, name, scores)
      # jos mato osuu itseensä peli loppuu
      for block in snake_body[1:]:
          if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
              game_over(score, name, scores)

      show_score(1, white, 'consolas', 20)
      # päivitetään ikkuna
      pygame.display.update()
      # kuinka nopeasti päivitetään
      fps_controller.tick(difficulty)








def jarjestyspeli():
  pelimuodot = {
    "Nettovarallisuus": 0,
    "Ikä": 1,
    "Spotify Kuunteljiat": 2
  }
  #valitetaan pelimuoto
  muoto = pelimuodot[random.choice(list(pelimuodot.keys()))]

  print(f"Tervetuloa järjestyspeliin! Pelimuoto on valittu. Muoto on {list(pelimuodot.keys())[muoto]}!")
  cls()

  #jos on tallennettu ihmisiä
  if os.path.exists("ihmiset"):
    with open("ihmiset", "rb") as f:
      ihmiset = pickle.load(f)


  else:
    ihmiset = {
      #muoto = nimi: (ikä, raha, kuullut),

      "Kanye West": (46, 400000000, 78500000),
      "Travis Scott": (32, 80000000, 66000000),
      "The Notorious B.I.G": (24, 10000000, 21000000),
      "Kendrick Lamar": (36, 85000000, 53000000),
      "Eminem": (51, 250000000, 69000000),
      "Katy Perry": (39, 34000000, 58000000),
      "Jay-Z": (54, 2500000000, 8400000),
      "Ice Spice": (24, 8000000, 23700000),
      "Beyonce": (42, 800000000, 73000000),
      "21 Savage": (31, 12000000, 63000000),
      "Drake": (37, 250000000, 84000000),
      "Snoop Dogg": (52, 160000000, 28000000),
      "Tupac": (25, 28000000, 23000000),
      "Ariana Grande": (30, 240000000, 84300000),
      "Playboi Carti": (27, 10000000, 54000000),
    }

  elämät = 7

  #5 random ihmistä valitaan peliin
  valittu = list(ihmiset.keys())
  random.shuffle(valittu)
  valittu = valittu[:5]

  oikein = []
  #yksi väärin lista, yksi oikein
  for ihminen in valittu:
    oikein.append((ihmiset[ihminen][muoto], ihminen))
  jarjesta = [x[1] for x in oikein]
  oikein.sort(key=lambda x: x[0], reverse=True)
  oikein = [x[1] for x in oikein]

  print(f"Peli alkaa! Sinulla on {elämät} elämää. Ihmiset pitää järjestää isommasta pienempään.")
  cls()
  print(f"Valitse ihmisen numero, joka haluat vaihtaa, sitten kirjoita mihiin haluat sijoittaa sitä.")
  cls()

  naytaOikein = False
  Laske = False
  Voitti = False

  while True:
    cls_inst()

    #katotaan jos on järjestelty oikein
    if Laske:
      if oikein == jarjesta:
        Voitti = True
        break

      oikeinm = 0
      for right, test in zip(oikein, jarjesta):
        if right == test:
          oikeinm+=1

      print("Et saanu oikein.")
      print(f"Sinulla on {oikeinm} oikeissa paikoissa.\n")

      naytaOikein = True
      Laske = False
      elämät -= 1

      if elämät == 0:
        break


    elif naytaOikein:
      print(f"Sinulla oli {oikeinm} oikeissa paikoissa.\n")
    print(f"Sinulla on {elämät} elämää jäljellä ja muoto on {list(pelimuodot.keys())[muoto]}.\n\n")

    #näytetään ihmistä
    for index, ihminen in enumerate(jarjesta):
      print(f"{index}: {ihminen}")

    print(f"\n\n{len(oikein)}: Laske oikein (-1 elämä jos on väärin)")

    #mistä vaihdetaan
    try:
      kuka = int(input("\nMikä numero haluat vahitaa?\n:"))
    except ValueError:
      print("Anna numero.")
      cls()
      continue

    #jos käyttäjä haluaa tarkistaa
    if kuka == len(oikein):
      Laske = True
      continue

    #jos numero on liian iso tai pieni
    if kuka < 0 or kuka > len(valittu):
      print(f"Valitse numero 0-{len(valittu)}")
      cls()
      continue

    #mihin
    try:
      mihin = int(input("\n\nMihin numero haluat sijoittaa?\n:"))
    except ValueError:
      print("\nAnna numero.")
      cls()
      continue

    #jos numeroa on sama
    if mihin == kuka:
      print(f"Numero ei saa olla sama.")
      cls()
      continue

    #ihmisten tarkistaminen
    if kuka == len(oikein):
      Laske = True
      continue

    #jos numero on liian iso tai pieni
    if mihin < 0 or mihin > len(valittu):
      print(f"Valitse numero 0-{len(valittu)}")
      cls()
      continue

    #vaihtaminen
    jarjesta[kuka], jarjesta[mihin] = jarjesta[mihin], jarjesta[kuka]

  cls_inst()

  if Voitti:
    print("Voitit! Nämä oli oikean järjestysksen arvot:\n")

    #näytetään arvot
    for index, ihminen in enumerate(jarjesta):
      print(f"{index}: {ihminen}, {list(pelimuodot.keys())[muoto+1]} = {ihmiset[ihminen][muoto+1]}")

  else:
    print(f"Hävisit... Tämä oli oikea järjestys verrattuna sinun järjestykseen muodolla {list(pelimuodot.keys())[muoto]}:\n")
    #näytetään oikea jäjrestys
    for index, ihminen in enumerate(jarjesta):
      print(f"{index}: {ihminen}, oikea: {oikein[index]}")

    cls()
    vastaus = input(f"Haluatko jatkaa saman pelin? (y/n)\n").lower()
    cls_inst()


    inp = input("Haluatka laittaa uuden ihmisen valikoimaan? (y/n)\n")

    if inp == "y":
      cls_inst()

      while True:
        ihminen = input("Anna uusi ihminen\n:")

        #varmistetaan että ihminen ei ole jo olemassa
        if ihminen not in ihmiset:
          cls_inst()
          print("Anna nämät arvot:\n")

          while True:
            cls_inst()
            #kysytään arvoja
            try:
              age = int(input("Ikä: "))
              money = int(input("Raha: "))
              listeners = int(input("Spotify Kuunteljiat: "))
              break

            except Exception as error:
              print(f"\nTeit jotain väärin. Yritä uudelleen. (Virhe oli: {error})")
              cls()
              continue
          #laitetaan uusi ihminen dictionariin
          ihmiset[ihminen] = (age, money, listeners)
          break

        else:
          print("Ihminen on jo listassa.")
          cls()
          continue

      #tallennetaan ihmisten "ihmiset" tiedostoon
      with open("ihmiset", "wb") as words:
        pickle.dump(ihmiset, words)


    cls_inst()

    if vastaus == "y":
      jarjestyspeli()
    else:
      main()








def hirsipuu():
  print("Tervetuloa pelaamaan hirsipuuta!")
  cls()

  #jos on tallennettu tiedosto
  if os.path.exists("hirsipuu"):
    with open("hirsipuu", "rb") as words:
      sanat = list(pickle.load(words))

  else:
    sanat = ["tietotekniikka", "python", "reppu", "replit", "pöytä", "haastava sana", "tietokone", "kamera", "kirjasto", "puhelin", "youtube", "koulu", "wordle", "koulu ei ole hauska"]

  elämät = 6

  #valitaan sana
  ValittuSana = random.choice(sanat)
  Sana = []

  #jos on enemmän kuin 1 sana niin saat enemmän elämää
  if " " in ValittuSana:
    elämät = 9
  
  #kertoo monta kirjaimia on sanassa
  for _ in range(0, len(ValittuSana)):
    Sana.append("_")

  #jos on välit niin laitetaan ne sanaan
  JosVälit = [index for index, item in enumerate(ValittuSana) if item == " "]
  for VäliIndex in JosVälit:
    Sana[VäliIndex] = " "

  ValittuKirjaimet = []


  while elämät > 0 and "".join(Sana) != ValittuSana:
    print(f"Sinulla on {elämät} elämää.\n\n")

    #näytetään kirjaimet jotka ovat valittu
    if len(ValittuKirjaimet) > 0:
      print(f"Kirjaimet jotka olet valinnut: {''.join(ValittuKirjaimet)}")

    print("".join(Sana))

    kirjain = input("Anna kirjain: \n").lower()

    #ei voi olla numero
    try:
      int(kirjain)
      print("Et voi laittaa numeroa.")
      cls()
      continue

    except:
      pass

    #jos kirjain on liian pitkä tai ei mitään kirjoiteta
    if len(kirjain) != 1:
      if len(kirjain) < 1:
        print("Anna yksi kirjain.")
      else:
        print("Kirjoittamasi kirjain on liian pitkä.")
      cls()
      continue

    #varmistetaan että ei annettu erikoismerkit
    if not kirjain.isalnum():
      print(f"Et voi kirjoittaa erikoismerkkejä ({kirjain}).")
      cls()
      continue

    #jos kirjain on jo valittu
    if kirjain + ", " in ValittuKirjaimet:
      print("Olet jo arvannut tämän kirjaimen.")
      cls()
      continue

    #katotaan jos kirjain on sanassa
    sanassa = [index for index, item in enumerate(ValittuSana) if item == kirjain]

    #jos on, laitetaan näytetään sitä
    if len(sanassa) != 0:
      print(f"\nKirjain {kirjain} on sanassa.")
      for index in sanassa:
        Sana[index] = kirjain

    else:
      elämät -= 1
      print(f"Kirjainta {kirjain} ei löydy sanassa")

    #lisätään kirjain valittui listaan
    ValittuKirjaimet.append(kirjain + ", ")

    cls()


  voitti = "Voitit!"
  if elämät == 0:
    voitti = "Hävisit.."


  #näytetäämn sana
  vastaus = input(f"{voitti} Sana oli: {ValittuSana}, haluatko jatkaa saman pelin? (y/n)\n").lower()

  cls_inst()


  inp = input("Haluatka laittaa uuden sanan valikoimaan? (y/n)\n")

  if inp == "y":
    cls_inst()

    #varmistetaan että ei ole numero
    while True:
      try:
        sana = input("Anna uusi sana\n:")
        int(sana)
        print("Et voi laittaa numeroa.")
        cls()
        continue

      except:
        pass

      #varmistetaan että ei ole erikoismerkkeja
      if any(not c.isalnum() for c in sana):
        print(f"Et voi kirjoittaa erikoismerkkejä. ({sana})")
        cls()
        continue

      #varmistetaan että sana on ainakin 2 kirjainta ja että on jotain
      if sana == "" or len(sana) == 1:
        print("Anna sana.")
        cls()
        continue

      #sanan alussa ja lopussa ei voi olla väliä
      if sana[0] == " " or sana[-1] == " ":
        print("Sanassa ei saa olla väliä alussa eikä lopussa.\n")

        if sana.strip() != "":
          inp = input(f"\nSopiiko, että sana on {sana.strip()}? (y/n)\n\n:").lower()

          if inp == "y":
            sana = sana.strip()
          else:
            continue


      #varmistetaan että sana ei ole jo listassa
      if sana not in sanat:
        sanat.append(sana)
        break

      else:
        print("Sana on jo listassa.")
        cls()
        continue

    #tallenetaan sanat tiedostoon "hirsipuu"
    with open("hirsipuu", "wb") as words:
      pickle.dump(sanat, words)


  cls_inst()

  if vastaus == "y":
    hirsipuu()
  else:
    main()





def main():
  inp = None
  cls_inst()
  pelit = {
    "hirsipuu": hirsipuu,
    "järjestyspeli": jarjestyspeli,
    "matopeli": matopeli
  }

  while True:
    print("Valitse peli. (e jos haluat pois, r jos haluat random pelin)\n")

    #näytetään pelit
    for nimi in pelit:
      print(nimi)

    inp = input("\n:")

    #jos haluaa pois
    if inp == "e":
      cls_inst()
      exit("Heippa!")

    #valitaan joku random peli
    if inp == "r":
      cls_inst()
      pelit[random.choice(list(pelit))]()

    #jos peli ei ole olemassa
    if inp not in pelit:
      cls_inst()
      print(f"Peli {inp} ei ole olemassa.")
      cls()
      continue

    cls_inst()
    pelit[inp]()


if __name__ == "__main__":
  main()
