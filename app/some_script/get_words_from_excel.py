import openpyxl
from collections import defaultdict


# Función para leer el Excel y procesar las palabras
def procesar_excel(file_path):
    # Cargar el archivo de Excel
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    # Diccionario para contar las palabras
    word_count = defaultdict(int)
    
    # Leer la primera columna
    for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
        # Obtener la celda (en este caso de la primera columna)
        text = row[0]
        
        # Realizar el split por espacio y contar las palabras
        if text:
            words = text.split(" ")
            for word in words:
                word_count[word.lower()] += 1  # Contar palabra en minúsculas
    
    # Ordenar las palabras alfabéticamente
    sorted_words = sorted(word_count.items())
    
    # Guardar los resultados en un archivo de texto
    with open("resultado.txt", "w", encoding="utf-8") as f:
        for word, count in sorted_words:
            f.write(f"\"{word}\",\n")
    
    print("El procesamiento ha finalizado. El archivo 'resultado.txt' ha sido generado.")

# Llamada a la función con el archivo Excel
archivo_excel = 'C:\\Users\\ManuelMartinez\\Desktop\\universidad\\dnend\\archivos\\2025-2\\libro.xlsx'
print(archivo_excel)
procesar_excel(archivo_excel)