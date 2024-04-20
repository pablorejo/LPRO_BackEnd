from shapely.geometry import Point, Polygon
import gmplot
import matplotlib.pyplot as plt

# Coordenadas del área original
coords_original = [(42.22259255448751, -7.7482447028160095),
                   (42.222553573687755, -7.7482423558831215),
                   (42.22215234316532, -7.7485715970396996),
                   (42.221494627468, -7.748884409666061),
                   (42.22124211645043, -7.74941984564066),
                   (42.22116738094084, -7.749530151486396),
                   (42.221308410001186, -7.749596200883389),
                   (42.22169027936151, -7.74977456778288),
                   (42.221911504312814, -7.749478183686733),
                   (42.222280707415514, -7.7498047426342955),
                   (42.22191771151127, -7.750540003180505),
                   (42.22198524579101, -7.750600352883338),
                   (42.222033413578735, -7.750500775873661),
                   (42.22217245440937, -7.750652991235255),
                   (42.22223427782323, -7.750729098916055),
                   (42.222440852003956, -7.750732451677322),
                   (42.22248926772979, -7.750282175838947),
                   (42.2226518946397, -7.7499985322356215),
                   (42.222719179849356, -7.74979367852211),
                   (42.22287882675738, -7.749067470431329),
                   (42.22298161631033, -7.748790867626667),
                   (42.22292103504818, -7.7486688271164885),
                   (42.22286889539073, -7.7485595270991325),
                   (42.222786464987315, -7.748439833521842),
                   (42.22270055848854, -7.748388200998306),
                   (42.222660088045444, -7.748359031975268),
                   (42.22266828145012, -7.748302705585957)]

# Crear un polígono que represente el área original
area_original = Polygon(coords_original)

# Área deseada en metros cuadrados
metros_cuadrados_deseados = 649

# Calcular el ancho y alto del área deseada (suponiendo que sea cuadrada)
lado = (metros_cuadrados_deseados)**0.5


# Crear un punto dentro del área original
punto = Point(42.222760, -7.749561)

# Crear un polígono alrededor del punto que represente el área deseada
trozo_area = punto.buffer(lado/2)

# Intersección entre el área original y el trozo de área deseada
area_final = area_original.intersection(trozo_area)
print(area_final)

# Coordenadas del polígono final
x_final, y_final = area_final.exterior.xy

# Crear una lista para almacenar las coordenadas del polígono final
coordenadasSector = []

# Guardar las coordenadas del polígono final en la lista
for i in range(len(x_final)):
    coordenadasSector.append((x_final[i], y_final[i]))


# Extraer latitudes y longitudes
lats, lons = zip(*coordenadasSector)

# Inicializar el objeto gmplot
gmap = gmplot.GoogleMapPlotter(lats[0], lons[0], 18)

# Dibujar el polígono
gmap.plot(lats, lons, 'cornflowerblue', edge_width=5)

# Guardar el mapa como HTML
gmap.draw("mapa.html")

print("Mapa generado. Abre el archivo 'mapa.html' en tu navegador web para ver el mapa.")
