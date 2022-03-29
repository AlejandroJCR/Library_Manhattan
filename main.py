import json
import os
import re

# Lee y obtiene la info de los archivos JSON
def start():
    if os.stat('arr.json').st_size == 0:
        arr = [[] for i in range(2)]
        overflow_0 = [[] for i in range(6)]
        overflow_1 = [[] for i in range(6)]
        index_title = []
        index_serial = []
    else:
        with open('arr.json', 'r') as fp:
            arr = json.load(fp)
        
        with open('of0.json', 'r') as fp:
            overflow_0 = json.load(fp)
        
        with open('of1.json', 'r') as fp:
            overflow_1 = json.load(fp)
        
        with open('indserial.json', 'r') as fp:
            index_serial = json.load(fp)
        
        with open('indtitle.json', 'r') as fp:
            index_title = json.load(fp)

    return arr, overflow_0, overflow_1, index_serial, index_title

     # Busca el grupo al que va a permanecer el libro basado en el serial
def get_hash(key):
    num = 0
    for character in key:
      characterNum = ord(character)
      num += characterNum
    hash = num % 2
    return hash
    
def binarySearch(key, index_title, index_serial):
  lo = 0
  if key.istitle():
      hi = len(index_title) - 1
      while lo <= hi:
        mid = (hi + lo) // 2
        if index_title[mid][0] < key:
            lo = mid + 1
        elif index_title[mid][0] > key:
            hi = mid - 1
        else:
            return index_title[mid][1]
          
      return -1
  else:
      hi = len(index_serial) - 1
      while lo <= hi:
        mid = (hi + lo) // 2
        if index_serial[mid][0] < key:
            lo = mid + 1
        elif index_serial[mid][0] > key:
            hi = mid - 1
        else:
            return index_serial[mid][1]
      return -1

# Agregar libros
def add_book(arr, overflow_0, overflow_1, index_serial, index_title):
    try:
             # Inputs para agrear el libro
        serial = input("\nIngrese serial (12 numeros): ")
        if len(serial) != 12 or not serial.isnumeric():
            raise Exception
        found = found_search(serial, index_title, index_serial, arr, overflow_0, overflow_1)
        if found:
            print(f"El serial: {serial} se encuentra registrado.")
            return
        cota = input("Ingrese cota (6 letras y 2 numeros): ")
        if len(cota) == 8 and cota.isalnum():
            for letter in range(6):
                if not cota[letter].isalpha():
                    raise Exception
                else:
                    continue
            for number in range(6,8):
                if not cota[number].isnumeric():
                    raise Exception
                else:
                    continue
        found = found_search(cota, index_title, index_serial, arr, overflow_0, overflow_1)
        if found:
            print(f"La cota: {cota} se encuentra registrada.")
            return
        title =  input("Ingrese title (max. 30 caracteres): ").title()
        if len(title) > 30 or len(title) == 0:
            raise Exception
        found = found_search(title, index_title, index_serial, arr, overflow_0, overflow_1)
        if found:
            print(f"El title: {title} se encuentra registrado.")
            return

        copies = input("Ingrese la cantidad de ejemplares que hay (min. 1 ejemplar): ")
        copies = int(copies)
        if copies <= 0:
            raise Exception
        
        borrowed_copies = 0

        def orderIndex(elem):
            return elem[0]
      
             # Añade al indice
        index_title.append([title, cota])
        index_serial.append([serial, cota])

        index_title.sort(key=orderIndex)
        index_serial.sort(key=orderIndex)
      
             # Añade al Hash
        h = get_hash(cota)
        added = False
      
        if len(arr[h]) < 3:
            arr[h].append({'serial':serial, 'cota':cota,'title':title, 'copies':copies, 'borrowed_copies':borrowed_copies})
            added = True
        else:
            if h == 0:
                for item in overflow_0:
                    if len(item) < 3:
                        item.append({'serial':serial, 'cota':cota,'title':title, 'copies':copies, 'borrowed_copies':borrowed_copies})
                        added = True
                        break
            elif h == 1:
                for item in overflow_1:
                    if len(item) < 3:
                        item.append({'serial':serial, 'cota':cota,'title':title, 'copies':copies, 'borrowed_copies':borrowed_copies})
                        added = True
                        break
            
        if not added:
            print('Error! -Maxima Capacidad- ')
            
    except:
        print('Error! -Ingrese Los Datos De Manera Correcta- ')

  
     # Chequea si el titulo, cota o serial y aestan registrados
def found_search(search_key, index_title, index_serial, arr, overflow_0, overflow_1):
    if index_title == []:
        return False
           
    if len(search_key) == 12 and search_key.isnumeric():
        serial = search_key
        cota = binarySearch(serial, index_title, index_serial)
        if cota != -1:
          return True
        else:
          return False
                
    elif len(search_key) == 8 and search_key.isalnum() :
        cota = search_key

        hashNum = get_hash(search_key)
        for item in arr[hashNum]:
          if cota == item["cota"]:
            return True
          else:
            continue
        if hashNum == 0:
          for lista in overflow_0:
            for item in lista:
              if cota == item["cota"]:
                return True
              else:
                continue
        elif hashNum == 1:
          for lista in overflow_1:
            for item in lista:
              if cota == item["cota"]:
                return True
              else:
                continue
        else:
          return False
        
    elif search_key.istitle():
        title = search_key
        cota = binarySearch(title, index_title, index_serial)
        if cota != -1:
          return True
        else:
          return False
    else:
      return False

         # Buscar un libro
def search_book(arr, overflow_0, overflow_1, index_serial, index_title):
    search_type = input('''\n 
    ~~~~~~~ Tipos de Búsqueda ~~~~~~~
    Seleccione la opción a utilizar:
    1. Búsqueda por Serial.
    2. Búsqueda por Cota.
    3. Búsqueda por Título.
    -> ''')
    if search_type == '1':
      serial_search = input('Ingrese el serial del libro que desea buscar: ')
      cota = binarySearch(serial_search, index_title, index_serial)
      if cota != -1:
        ha = get_hash(cota)
      else:
        print(f"El serial: {serial_search} no se encuentra registrado")
        return

    elif search_type == '2':
        cota = input('Ingrese el cota del libro que desea buscar: ')
        found = found_search(cota, index_title, index_serial, arr, overflow_0, overflow_1)
        if not found:
            print('La cota: '+ cota + ' no se encuentra registrada.')
            return
        else:
          ha = get_hash(cota)

    elif search_type == '3':
        title_search = input('Ingrese el titulo del libro que desea buscar: ').title()
        cota = binarySearch(title_search, index_title, index_serial)
        if cota != -1:
          ha = get_hash(cota)
        else:
          print(f"El título: {title_search} no se encuentra registrado")
          return
    else:
        print('Su entrada es incorrecta.')
        return

    found = False
    for idx in arr[ha]:
 
        if idx['cota'] == cota :

            s = idx['serial']
            ct = idx['cota']
            t = idx['title']
            cp = idx['copies']
            b_cp = idx['borrowed_copies']
            found = True

            print(f'''
            Serial: {s}
            Cota: {ct}
            Titulo: {t}
            Ejemplares Disponibles: {cp}
            Ejemplares Prestados: {b_cp}
            ''' )
                
    if not found:
        if ha == 0:
            for lista in overflow_0:
                for item in lista:
                    if item['cota'] == cota:
                        s = item['serial']
                        ct = item['cota']
                        t = item['title']
                        cp =  item['copies']
                        b_cp = item['borrowed_copies']
                        
                        found = True

                        print(f'''
                        Serial: {s}
                        Cota: {ct}
                        Titulo: {t}
                        Ejemplares Disponibles: {cp}
                        Ejemplares Prestados: {b_cp}
                        ''' )

        if ha == 1:
            for lista in overflow_1:
                for item in lista:
                    if item['cota'] == cota:
                        s = item['serial']
                        ct = item['cota']
                        t = item['title']
                        cp = item['copies']
                        b_cp = item['borrowed_copies']
                        
                        found = True

                        print(f'''
                        Serial: {s}
                        Cota: {ct}
                        Titulo: {t}
                        Ejemplares Disponibles: {cp}
                        Ejemplares Prestados: {b_cp}
                        ''' )



     # Prestar un libro por serial              
def borrow_book(arr, overflow_0, overflow_1, index_serial, index_title):
  nombre = input("Ingrese el nombre del libro que desea tomar prestado: ").title()
  cota = binarySearch(nombre, index_title, index_serial)
  if cota != -1:
    hashNum = get_hash(cota)
    for item in arr[hashNum]:
        if cota == item["cota"]:
          if item["copies"] != 0:
            item["copies"] -= 1
            item["borrowed_copies"] += 1
            print("Libro prestado exitosamente!")
            return
          else:
            print(f"{nombre} no se encuentra disponible en estos momentos.")
            return
        else:
          continue

    if hashNum == 0:
        for lista in overflow_0:
          for item in lista:
            if cota == item["cota"]:
              if item["copies"] != 0:
                item["copies"] -= 1
                item["borrowed_copies"] += 1
                print("Libro prestado exitosamente!")
                return
              else:
                print(f"{nombre} no se encuentra disponible en estos momentos.")
                return
            else:
              continue
              
    elif hashNum == 1:
        for lista in overflow_1:
          for item in lista:
            if cota == item["cota"]:
              if item["copies"] != 0:
                item["copies"] -= 1
                item["borrowed_copies"] += 1
                print("Libro prestado exitosamente!")
                return
              else:
                print(f"{nombre} no se encuentra disponible en estos momentos.")
                return
            else:
              continue
    else:
        return False
  else:
    print(f"{nombre} no se encuentra registrado.")
    

     # Devolver un libro por serial
def return_book(arr, overflow_0, overflow_1, index_serial, index_title):
  nombre = input("Ingrese el nombre del libro que desea regresar: ").title()
  cota = binarySearch(nombre, index_title, index_serial)
  if cota != -1:
    hashNum = get_hash(cota)
    for item in arr[hashNum]:
        if cota == item["cota"]:
          if item["borrowed_copies"] != 0:
            item["borrowed_copies"] -= 1
            item["copies"] += 1
            print("Libro devuelto exitosamente!")
            return
          else:
            print(f"No hay ejemplares prestados de {nombre}")
            return
        else:
          continue

    if hashNum == 0:
        for lista in overflow_0:
          for item in lista:
            if cota == item["cota"]:
              if item["borrowed_copies"] != 0:
                item["borrowed_copies"] -= 1
                item["copies"] += 1
                print("Libro devuelto exitosamente!")
                return
              else:
                print(f"No hay ejemplares prestados de {nombre}")
                return
            else:
              continue
              
    elif hashNum == 1:
        for lista in overflow_1:
          for item in lista:
            if cota == item["cota"]:
              if item["borrowed_copies"] != 0:
                item["borrowed_copies"] -= 1
                item["copies"] += 1
                print("Libro devuelto exitosamente!")
                return
              else:
                print(f"No hay ejemplares prestados de {nombre}")
                return
            else:
              continue
    else:
        return False
  else:
    print(f"{nombre} no se encuentra registrado.")

     # Eliminar un libro por serial
def delete_book(arr, overflow_0, overflow_1, index_serial, index_title):
  cota_search = input('\nIngrese la cota del libro que desea eliminar: ')
  ha = get_hash(cota_search)
  found = False
  for idx in arr[ha]:
    if idx['cota'] == cota_search:
      titulo = idx['title']
      serial = idx['serial']
      arr[ha].remove(idx)
      found = True
      print('Eliminación Exitosa del arr.json')
  
  if not found:
    if ha == 0: 
      for item in overflow_0:
        for i in item:
          if i['cota'] == cota_search:
            titulo = i['title']
            serial = i['serial']
            item.remove(i)
            found = True
            print('Eliminación Exitosa del of0.json')
              
    else:
      for item in overflow_1:
        for i in item:
          if i['cota'] == cota_search:
            titulo = i['title']
            serial = i['serial']
            item.remove(i)
            found = True
            print('Eliminación Exitosa del of1.json')
    
    
  if found:
    #lo eliminamos de indices por titulo
    lo = 0
    hi = len(index_title) - 1
    while lo <= hi:
      mid = (hi + lo) // 2
      if index_title[mid][0] < titulo:
        lo = mid + 1
      elif index_title[mid][0] > titulo:
        hi = mid - 1
      else:
        index_title.remove(index_title[mid]) 
        hi = -1
        print('Eliminación Exitosa del indtilte.json')

    lo = 0
    hi = len(index_serial) - 1
    while lo <= hi:
      mid = (hi + lo) // 2
      if index_serial[mid][0] < serial:
        lo = mid + 1
      elif index_serial[mid][0] > serial:
        hi = mid - 1
      else:
        index_serial.remove(index_serial[mid]) 
        hi = -1
        print('Eliminación Exitosa del indserial.json')
  else:
    print('El libro no se encuentra registrado.')

  pack(ha, arr, overflow_0, overflow_1)

def pack(hash, arr, overflow_0, overflow_1):
  if hash == 0:
    if len(arr[hash]) < 3:
      if len(overflow_0[0]) != 0:
        arr[hash].append(overflow_0[0][0])
        overflow_0[0].remove(overflow_0[0][0])
    
    for indice in range(len(overflow_0)):
      if (len(overflow_0[indice]) < 3) and (indice != len(overflow_0) - 1):
        if len(overflow_0[indice + 1]) != 0:
          overflow_0[indice].append(overflow_0[indice + 1][0])
          overflow_0[indice + 1].remove(overflow_0[indice + 1][0])
                
  else:
    if len(arr[hash]) < 3:
      if len(overflow_1[0]) != 0:
        arr[hash].append(overflow_1[0][0])
        overflow_1[0].remove(overflow_1[0][0])
      
    
    for indice in range(len(overflow_1)):
      if (len(overflow_1[indice]) < 3) and (indice != len(overflow_1) - 1):
        if len(overflow_1[indice + 1]) != 0:
          overflow_1[indice].append(overflow_1[indice + 1][0])
          overflow_1[indice + 1].remove(overflow_1[indice + 1][0])
              

     # Agrega los registros realizados a los archivos JSON
def load(arr, overflow_0, overflow_1, index_serial, index_title):
    
    with open('arr.json', 'w') as fp:
        json.dump(arr, fp)
        
    with open('of0.json', 'w') as fp:
        json.dump(overflow_0, fp)
    
    with open('of1.json', 'w') as fp:
        json.dump(overflow_1, fp)

    with open('indserial.json', 'w') as fp:
        json.dump(index_serial, fp)
    
    with open('indtitle.json', 'w') as fp:
        json.dump(index_title, fp)


def main():

    arr, overflow_0, overflow_1, index_serial, index_title = start()

    while True:
        action = input('''\n
        ~~~~~~~ Librería Pública de Manhattan ~~~~~~~
        Bienvenido a utilizar el sistema de gestión de la librería. Seleccione la acción a realizar:
        1. Agregar un nuevo libro.
        2. Buscar un libro.
        3. Prestar un libro.
        4. Devolver un libro.
        5. Eliminar un libro.
        0. Salir.
        -> ''')
        if action == '1':
            add_book(arr, overflow_0, overflow_1, index_serial, index_title)
            load(arr, overflow_0, overflow_1, index_serial, index_title)
        elif action == '2':
            search_book(arr, overflow_0, overflow_1, index_serial, index_title)
        elif action == '3':
            borrow_book(arr, overflow_0, overflow_1, index_serial, index_title)
        elif action == '4':
            return_book(arr, overflow_0, overflow_1, index_serial, index_title)
        elif action == '5':
            delete_book(arr, overflow_0, overflow_1, index_serial, index_title)
            load(arr, overflow_0, overflow_1, index_serial, index_title)
        elif action == '0':
            load(arr, overflow_0, overflow_1, index_serial, index_title)
            print('Gracias por usar el sistema de Librería Pública de Manhattan. Hasta la Proxima!\n')
            break
        else:
            print('Su entrada es incorrecta, por favor seleccione de nuevo.')

if __name__ == "__main__":
    main()