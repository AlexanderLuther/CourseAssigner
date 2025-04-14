# Sistema: Generador de Horarios 
---

##  1. Introducción

**Generador de Horarios** es una aplicación de escritorio construida con Python y Tkinter. Automatiza la asignación de horarios académicos utilizando un algoritmo genético configurable por el usuario. Está orientada a coordinadores de carrera y personal administrativo.

---

##  2. Requisitos del Sistema

**Sistema Operativo Compatible:**
- Windows 10/11
- Linux (Ubuntu/Debian recomendado)

**Python:**
- Versión 3.10 o superior

**Librerías necesarias:**
- `sqlalchemy`
- `pymysql`
- `reportlab`
- `matplotlib`
- `pandas`

### Instalación rápida de dependencias
```bash
pip install sqlalchemy pandas pymysql reportlab matplotlib
```

---

##  3. Estructura del Proyecto

```
GeneradorDeHorarios/
├── backend/
│   ├── controller/
│   ├── db/
│   │   ├── model/
│   │   ├── query/
│   │   └── connection/
├── frontend/
│   ├── course/
│   ├── teacher/
│   ├── classroom/
│   ├── assignment/
│   ├── genetic_algorithm/
├── main.py
```

---

##  4. Modelo de Datos

###  Entidades

| Modelo        | Atributos |
|---------------|-----------|
| Career        | id, description |
| Classroom     | id, description |
| Course        | code, name, id_career, id_semester, id_section, id_course_type |
| CourseType    | id, description |
| Period        | id, start_time, end_time, description |
| Section       | id, description |
| Semester      | id, description |
| Teacher       | id, name, entry_time, departure_time |
| Time          | id, time |

###  Query Layer
Cada entidad tiene su clase en `db.query`, con métodos como:
- `find_all_*`
- `find_by_id`, `delete_by_id`, `update`, `save`

---

##  5. Interfaz Gráfica (Frontend)

###  Pantalla Principal – `CourseAssigner`
Menú de navegación con:
- Archivo
- Cursos
- Docentes
- Salones
- Docente-Curso
- Generar

###  Gestión de Cursos
- `AddCourseForm`: Formulario para registrar cursos.
- `CourseViewer`: Tabla para ver, editar y eliminar.

Campos:
- Nombre
- Código
- Carrera
- Semestre
- Sección
- Tipo

###  Gestión de Docentes
- `AddTeacherForm`: Formulario con nombre, ID y horario.
- `TeacherViewer`: Tabla editable de docentes.

Validaciones:
- Horarios válidos (entrada < salida)
- ID numérico

###  Gestión de Salones
- `AddClassroomForm`: Formulario para nuevo salón.
- `ClassroomViewer`: Tabla editable de salones.

### Relación Docente-Curso
- `AssignmentViewer`: Vista jerárquica por docente
  - Cada docente con cursos asignados debajo

###  Configuración del Algoritmo Genético
- `GeneticAlgorithmSetup`: ventana de configuración y ejecución.

Componentes:
- Tabla de cursos (`CourseTableFrame`)
- Tabla de docentes (`TeacherTableFrame`)
- Campo de población inicial
- Criterios de parada:
  - Número de generaciones
  - Porcentaje de aptitud óptima (1-100)

Salida:
- PDF de horario
- PDF resumen de ejecución
- Gráfico de evolución del del valor de aptitud

###  Visualización de errores
- `LogViewer`: muestra archivos como:
  - `importacion_docentes.txt`
  - `importacion_cursos.txt`
  - `importacion_docente_curso.txt`

---

## 6. Ejecución del Sistema

### 📄 Archivo: `main.py`

```python
DatabaseSession.initialize(
    user='root',
    password='*****.',
    host='localhost',
    db_name='COURSE_ASSIGNER'
)

root = tk.Tk()
app = CourseAssigner(root)
```

###  Cómo ejecutar
Desde la raíz del proyecto:

```bash
python main.py
```

---

## 7. Formato de Archivos CSV para Importación

### 1. `docentes.csv`

```
Juan Pérez,123456,13:00,18:00
```

Sin encabezado. Columnas:
- Nombre
- Numero de registro  (`Longitud maxima 10`)
- Hora de entrada (`HH:MM`)
- Hora de salida (`HH:MM`)

### 2. `cursos.csv`

```
Programación I,2025000000,sistemas,1,A,Obligatorio
```

Sin encabezado. Columnas:
- Nombre
- Código (`Longitud maxima 10`)
- Carrera (`mecanica, industrial, civil, sistemas, mecanica indsutrial`)
- Semestre  (`1, 2, 3, 4, 5, 6, 7, 8, 9, 10`)
- Sección (`A, B, C, D, E, F, G, H, I, J, K, L`)
- Tipo de curso (`Obligatorio, Opcional`)

### 3. `docente_curso.csv`

```
123456,2025000000
```

Sin encabezado. Columnas:
- Numero de registro del docente
- Código del curso

### Validaciones y errores
- Se generan logs de error automáticamente
- Se muestran con `LogViewer` si hay problemas

---

## 8. Flujo Recomendado de Uso

1. Cargar cursos y docentes (manualmente o vía CSV)
2. Crear salones.
2. Importar relación docente-curso
3. Verificar asignaciones visualmente
4. Acceder a `Generar > Nuevo Horario`
5. Seleccionar docentes, cursos y configurar parámetros
6. Ejecutar y analizar:
   - PDF de horario
   - Gráfico de evolución
   - PDF resumen de ejecución

