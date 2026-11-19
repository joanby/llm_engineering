# Informe de actualización del curso — septiembre de 2026

**Repo:** `llm_engineering`
**Rama:** `actualizacion-transformers-2026-09-13` (local, sin push y sin PR; `main` intacto)
**Entorno de verificación:** macOS (Apple Silicon, 24 GB, sin GPU CUDA — solo MPS), Python 3.12, venv `.venv_qa`

---

## 1. Resumen

El curso se grabó con las librerías de finales de 2024 y `requirements.txt` no fijaba **ni una sola versión**. Eso es lo que ha causado el desfase: cada alumno nuevo instalaba lo último que hubiera ese día, y varias APIs del ecosistema han cambiado de forma incompatible desde entonces.

Se han corregido **11 commits** de arreglos sobre los 3 que ya existían, más **5** de la revisión final previa a publicar (sección 7). El cambio de fondo, además de los arreglos concretos, es que ahora las versiones están fijadas: el curso deja de moverse solo.

Hay tres categorías de problema, y conviene no mezclarlas:

1. **Desfase real de librerías** (lo que se arregla en esta rama): tareas de `pipeline()` eliminadas, `langchain` partido en varios paquetes, `datasets` que ya no ejecuta scripts de carga, `trl` que ha reescrito su API de fine-tuning, Modal que ha renombrado métodos, modelos retirados de las APIs de pago.
2. **Bugs propios del repo, sin relación con las versiones** (2 encontrados de paso, también arreglados): una `x` suelta que rompía `week6/lite.ipynb`, y unos imports que faltaban en `week3/day5`.
3. **Cosas que NO se arreglan tocando código** (sección 5): un dataset vacío en HuggingFace, gates de licencia no aceptados, infraestructura de pago del alumno, y la cuenta de OpenAI sin saldo.

---

## 2. Los commits

| Commit | Qué cubre |
|---|---|
| `5e27f55` | **Semana 2** — modelos retirados de Claude/Gemini/DALL·E, `temperature`, `workspace_id`, Gradio |
| `80cb64e` | **Semana 4** — modelo de Claude retirado y `workspace_id` opcional |
| `ce288e7` | **Semana 5** — migrar los imports de `langchain` a los paquetes actuales |
| `2d37001` | **Semana 3 Día 2** — integrar el notebook real y arreglar los pipelines retirados |
| `3e93219` | **Semana 3 Día 1** — integrar el notebook real y arreglar la celda de audio |
| `d87be55` | **Semana 3 Día 3** — integrar el notebook real (sin cambios de código) |
| `23598bf` | **Semana 3 Días 4 y 5** — `apply_chat_template` + `generate()` |
| `5697492` | **Semana 6** — cargar Amazon-Reviews-2023 sin script de carga |
| `0718b07` | **Semana 6 Día 4** — modelo de Claude retirado y `workspace_id` |
| `5d640ab` | **Semana 8** — API actual de Modal y dependencias que faltaban |
| `c8ed40f` | **Semana 7** — integrar los notebooks reales y los dos auxiliares |
| `bf4c3d8` | **Semana 7 Días 3-4** — migrar el fine-tuning a la API actual de `trl` |
| `b7d703a` | **Semana 6** — `lite.ipynb` no cargaba ningún dataset (una `x` suelta) |
| `f321cd4` | **Dependencias** — fijar versiones reales y añadir los paquetes que faltaban |

**Nota sobre las Semanas 3 y 7:** sus `dayN.ipynb` eran punteros a Colab de dos celdas (un Markdown de presentación y una celda de código vacía). Ahora contienen el notebook real, integrado desde `_colabs_originales/`, con los arreglos aplicados.

A esos 14 se suman los 5 de la **revisión final antes de publicar** (sección 7), que es una pasada distinta: no busca desfase de librerías, busca lo que se nos haya escapado al arreglarlo.

| Commit | Qué cubre |
|---|---|
| `fe269e1` | **Semana 8** — el comentario del `.from_name()` rompía la asignación en `day1` (`SyntaxError`) |
| `e6fb19e` | **Semanas 4 y 6** — limpiar dos salidas guardadas que contradicen el código actual |
| `ec4e68e` | **README y comentarios** — nombres de modelo viejos supervivientes, incluido uno que se ejecutaría |
| `eb55ca5` | **Semana 7** — quitar el estado de widgets huérfano que impide renderizar en GitHub |
| `0386f18` | **Semanas 3 y 7** — los notebooks integrados no pasaban `nbformat.validate()` |

---

## 3. Qué fallaba, lección por lección

### Semana 1 — sin cambios
Sigue funcionando tal cual. La descarga de `llama3.2` por Ollama, que en la auditoría falló por red, **funciona ahora**: se descargó correctamente y `week1/day2 EXERCISE.ipynb` ejecuta con 0 errores.

### Semana 2 (`5e27f55`)
| Qué rompía | Arreglo |
|---|---|
| `claude-3-5-sonnet-20240620` y `claude-3-haiku-20240307` → 404, retirados | `claude-sonnet-5` y `claude-haiku-4-5` |
| `messages.create/stream(temperature=...)` → `TypeError` | Se elimina el parámetro (los modelos actuales lo rechazan) |
| `message.content[0].text` → `AttributeError: 'ThinkingBlock'` | `content[-1].text` |
| `gemini-1.5-flash` → 404 | `gemini-3.6-flash` |
| `gr.ChatInterface/Chatbot(type="messages")` → `TypeError` | Se elimina el parámetro (Gradio 6) |
| `dall-e-3` + `response_format` → no existen | `gpt-image-1`, que ya devuelve `b64_json` |

### Semana 3
| Día | Qué rompía | Arreglo | Commit |
|---|---|---|---|
| 1 | `datasets` no carga `cmu-arctic-xvectors` (script de carga) | `revision="refs/convert/parquet"` | `3e93219` |
| 1 y 2 | `pipeline("text-to-speech")` → `TypeError: BatchEncoding.to() got an unexpected keyword argument 'dtype'` | SpeechT5 directo (procesador → modelo → vocoder) | `3e93219`, `2d37001` |
| 2 | `pipeline("ner", grouped_entities=True)` → `TypeError` | `aggregation_strategy="simple"` | `2d37001` |
| 2 | `question-answering`, `summarization`, `translation_en_to_fr` → tareas **eliminadas** del registro | Un modelo de chat (`Qwen3-4B-Instruct`) compartido por las tres celdas | `2d37001` |
| 2 | `text-generation` sin modelo: el default cambió de GPT-2 a SmolLM3-3B y la salida pasa a ser buena, cargándose el punto pedagógico | Se fija `model="gpt2"` | `2d37001` |
| 2 | `stabilityai/stable-diffusion-2` → 404, retirado del Hub | `stable-diffusion-xl-base-1.0` | `2d37001` |
| 3 | *nada* | — | `d87be55` |
| 4 y 5 | `apply_chat_template(return_tensors="pt")` ya no da un tensor plano → `generate()` peta con un `AttributeError` **vacío** | `return_dict=True` + `generate(**inputs, ...)` | `23598bf` |
| 5 | `AutoModelForSpeechSeq2Seq`, `AutoProcessor` y `pipeline` usados sin importar (**bug previo, no de versiones**) | Se añaden al import | `23598bf` |

**Sobre el cambio a un modelo de chat (Semana 3 Día 2):** es el cambio más visible de toda la actualización y conviene que quede explicado en la clase de actualizaciones. Las tres tareas (`question-answering`, `summarization`, `translation_en_to_XX`) no se han renombrado: se han **eliminado de raíz** del registro `SUPPORTED_TASKS` de transformers, y no queda ningún pipeline de una línea equivalente. La vía que recomienda hoy HuggingFace es pedírselo a un modelo de chat, que es lo que se ha hecho. El modelo se carga **una sola vez** en la celda de question-answering y se reutiliza en las otras dos, para no tener tres modelos en memoria. *Alternativa descartada:* fijar `transformers<5` para conservar las tareas — se descarta porque arrastraría al alumno a una versión antigua en todo el curso y esas tareas no van a volver. Para el alumno cambia la forma de leer el resultado (`result[0]["generated_text"][-1]["content"]`), no el fondo de la lección.

### Semana 4 (`80cb64e`)
Mismo problema de Claude que la Semana 2. El endpoint de inferencia de pago (`CODE_QWEN_URL`) sigue pausado: es del mantenedor del curso original, ajeno al repo.

### Semana 5 (`ce288e7`)
`langchain` se ha partido en 1.x. Un solo fallo raíz (`ModuleNotFoundError: No module named 'langchain.document_loaders'`) bloqueaba la semana entera desde la primera celda. Migrados `document_loaders`, `text_splitter`, `schema`, `vectorstores`, `memory` y `chains` a `langchain_community`, `langchain_text_splitters`, `langchain_core` y `langchain_classic`.

### Semana 6
| Qué rompía | Arreglo | Commit |
|---|---|---|
| `load_dataset("McAuley-Lab/Amazon-Reviews-2023")` → `RuntimeError: Dataset scripts are no longer supported`; bloqueaba la semana entera y, en cascada, la Semana 8 | `load_amazon_meta()` en `loaders.py`: descarga el `.jsonl` del Hub y reconstruye el Dataset reproduciendo línea a línea lo que hacía el script original | `5697492` |
| `claude-3-5-sonnet-20240620` en day4 | `claude-sonnet-5` + `workspace_id` + `content[-1]` | `0718b07` |
| `lite.ipynb`: una `x` suelta dejaba `dataset_names = [x]` → `NameError`, y todas las categorías comentadas (**bug previo**) | Se quita la `x` y se activa `Musical_Instruments` | `b7d703a` |

### Semana 7
Los Días 1, 2 y 5 se integran **sin cambios de código**. Todo el desfase está en el notebook de entrenamiento (`day3 and 4.ipynb`), y conviene subrayar algo: la celda de instalación de ese notebook, a diferencia de la de los otros días, **no fija** `trl` ni `transformers`, así que estos errores le pasan de verdad a cualquier alumno que lo ejecute hoy.

| Qué rompía | Arreglo |
|---|---|
| `from trl import DataCollatorForCompletionOnlyLM` → `ImportError`, la clase ya no existe | Dataset en formato prompt/completion (partido por `"Price is $"`) + `completion_only_loss=True` |
| `SFTConfig(warmup_ratio=...)` → `TypeError` | `warmup_steps`, calculado para conservar el mismo 3% |
| `SFTConfig(group_by_length=True)` → `TypeError` | Se elimina (solo era una optimización de batching) |
| `SFTConfig(max_seq_length=...)` → `TypeError` | `max_length` |
| `report_to=None` → `ValueError` | `report_to="none"` |
| `SFTTrainer(tokenizer=...)` | `processing_class=` |

**`group_by_length`, `max_seq_length` y `report_to` no estaban en el inventario de la auditoría:** aquel análisis paró en el primer `TypeError` y no llegó a ver los siguientes, que solo aparecen al ir arreglándolos uno a uno.

### Semana 8 (`5d640ab`)
| Qué rompía | Arreglo |
|---|---|
| `modal.Function.lookup()` / `modal.Cls.lookup()` → `AttributeError` | `.from_name()`, mismos argumentos |
| `app.run(show_progress=False)` → `TypeError` | Se elimina el parámetro |
| `feedparser` y `twilio` sin declarar en `requirements.txt` | Añadidos |

Matiz que conviene no perder: `environment.yml` **sí** tenía `feedparser` y `twilio`. El agujero era solo de la vía pip.
No se toca el `show_progress` de `agents/deals.py` ni el de `day3.ipynb`: ese es un parámetro de la propia función `ScrapedDeal.fetch()` del curso, solo coincide el nombre con el de Modal.

---

## 4. Versiones, antes y después

**Antes:** `requirements.txt` no fijaba nada. Las únicas versiones fijadas en todo el repo estaban dentro de los notebooks de la Semana 7 (`transformers==4.43.1`, `datasets==2.21.0`), y solo en los Días 1, 2 y 5.

**Después** (`f321cd4`) — 47 dependencias fijadas a las versiones exactas del entorno en el que se verificó el curso; comprobado por script que los 47 pines coinciden uno a uno con el `pip freeze` real:

| Paquete | Grabación (2024) | Ahora |
|---|---|---|
| transformers | 4.4x | **5.17.0** → **5.18.0** en noviembre (sección 9) |
| datasets | 2.21.0 | **5.0.1** |
| langchain | 0.2.x | **1.4.0** |
| trl | 0.9-0.11 | **1.13.0** |
| peft | 0.11-0.12 | **0.20.0** |
| gradio | 4.x | **6.27.0** |
| openai | 1.x | **3.13.0** |
| anthropic | 0.3x | **1.5.0** |
| modal | 0.6x | **1.5.5** |
| torch | 2.4 | **2.14.0** |
| diffusers | 0.30 | **0.40.0** |

Correcciones de contenido, no solo pines:
- Fuera `langchain[docarray]` (ese extra ya no existe); en su lugar, los paquetes reales que el código importa.
- Añadidos paquetes que el curso usa pero nunca estuvieron declarados: `peft`, `trl`, `wandb`, `diffusers`, `soundfile`, `huggingface_hub`, `sentence-transformers`, `langchain-core`, `langchain-classic`, `langchain-community`.
- `google.generativeai` → `google-generativeai` (con punto no instala).
- Quitados los duplicados (`matplotlib`, `scikit-learn`, `sentencepiece` estaban dos veces).

---

## 5. Lo que NO se arregla con código

| # | Qué | Estado |
|---|---|---|
| 1 | **`joanby/pricer-data` sigue vacío.** El repo existe y ya tiene `data/train-*.parquet` y `data/test-*.parquet`, pero pesan **805 bytes** cada uno y `load_dataset()` sigue fallando con `ValueError: Instruction "train" corresponds to no data!`. Bloquea los Días 2, 3 y 5 de la Semana 7. | **Pendiente de confirmación del usuario**, que lo está resolviendo por su cuenta |
| 2 | **La cuenta de OpenAI se ha quedado sin saldo.** `RateLimitError 429: You have no credits remaining`. Esto ha impedido la re-ejecución final de las Semanas 1, 2, 4, 5 y de `week6/day4-day5`. **No es un fallo del curso**, pero hay que recargar para poder cerrar la verificación. | **Acción del usuario** |
| 3 | **Gate de `black-forest-labs/FLUX.1-schnell`** (Semana 3 Día 1): `GatedRepoError 403`. Hay que aceptar la licencia en huggingface.co con la cuenta del token. Se ha añadido un comentario en la celda avisando. | Acción del usuario, no es desfase |
| 4 | **Gate de `meta-llama/Llama-2-7b-chat-hf`** (`Notebook 1 Antes del Fine-tuning`): mismo caso. | Acción del usuario, no es desfase |
| 5 | **Endpoint de inferencia de pago pausado** (Semana 4 Día 4, `CODE_QWEN_URL`): "The endpoint is paused, ask a maintainer to restart it". Es infraestructura del mantenedor del curso original. | Ajeno al repo |
| 6 | **Modal sin credenciales** (Semana 8): tras arreglar la API, `keep_warm.py` llega ya hasta `AuthError: Token missing`, que es justo lo que se buscaba. Requiere `modal token new`. | Acción del usuario |
| 7 | **Cuantización de `bitsandbytes` en este Mac** (Semana 7 Día 1): 8-bit y 4-bit fallan con "Some modules are dispatched on the CPU or the disk". Es una limitación de no tener GPU CUDA; en Colab con T4 no ocurre. | Limitación del entorno de verificación |
| 8 | **Deprecaciones de LangChain que siguen funcionando pero avisan**: `ConversationBufferMemory` y `ConversationalRetrievalChain` avisan de `will be removed in 2.0.0`. LangChain recomienda `langchain.agents.create_agent` con checkpointing. Cambiar a ese enfoque sería otra lección distinta. | **Candidato a regrabación**, no urgente |
| 9 | **`environment.yml` declara `python=3.11`** y la verificación se hizo con 3.12. No se ha tocado porque cambiar la versión de Python del entorno de conda es una decisión de más calado que un pin. | A decidir |
| 10 | **`pipeline("text-to-speech")` está roto en transformers 5.17.0** — `text_to_audio.py` llama a `.to(dtype=...)` sobre un `BatchEncoding`, que solo acepta `device`. Es un bug **de la librería**, no del curso; se ha esquivado usando SpeechT5 directamente. Se arregló río arriba en **transformers 5.18.0** (30-sep-2026), y desde noviembre la rama fija esa versión (sección 9): la línea del vídeo vuelve a funcionar. Los cuadernos siguen con SpeechT5 directo, que funciona con las dos. | **Arreglado río arriba; pin subido a 5.18.0** |

---

## 6. Qué se ha verificado de verdad, y qué no

Toda la verificación se hizo **secuencialmente, nunca en paralelo**, y comprobando que no quedaran procesos huérfanos después de cada notebook. (La sesión anterior de esta fase tuvo que interrumpirse porque `week3/day2` carga Qwen3-4B + SDXL + SpeechT5 en el mismo kernel, unos 16 GB en una máquina de 24 GB, y agotó la memoria.)

**Ejecutado de principio a fin, 0 errores:**
- `week1/day1` *(salvo las celdas de OpenAI, ver punto 2 de la sección 5)*, `week1/day2 EXERCISE` (Ollama + llama3.2), `week1/day5` *(idem)*
- `week3/day2` — verificado celda a celda en procesos aislados (sentiment, NER, las tres celdas del modelo de chat, zero-shot, gpt2, SDXL y audio), más una ejecución con nbconvert de la primera mitad completa
- `week3/day3` — notebook entero
- `week6/day1` — notebook entero, y con la mejor prueba posible: devuelve **exactamente las mismas cifras que los outputs grabados del original** (94.327 electrodomésticos, 46.726 con precio = 49,5%, 29.191 items)
- `week6/lite` — notebook entero, genera 25.000 + 2.000 items reales

**Verificado en aislado (el arreglo, no el notebook entero):**
- `apply_chat_template` + `generate(**inputs)` con `gemma-2-2b-it`, confirmando además que el patrón antiguo **sí** lanza el `AttributeError` vacío
- La migración de `trl`: `SFTConfig` y `SFTTrainer` se construyen, y al inspeccionar el primer batch la pérdida queda enmascarada sobre 29 de 33 tokens, puntuando **solo el precio** — es decir, se conserva el comportamiento del `DataCollatorForCompletionOnlyLM` original
- La llamada a Claude de `week6/day4` contra la API real
- Los imports de la Semana 8 y que `modal.Cls.from_name` existe

**NO verificado, y por qué:**
- **Semana 7 completa** — bloqueada por el dataset vacío (punto 1 de la sección 5). El `SFTTrainer(...).train()` real tampoco se ha lanzado: son horas de GPU y un push de modelo al Hub.
- **`week6/day2` con las 8 categorías** — esta vez sí se intentó ejecutar (con `push_to_hub` desactivado en una copia de prueba, para no escribir en `joanby/pricer-data`), y se reprodujo un fallo real, dos veces, con diagnóstico de causa:
  - Con `ItemLoader(...).load()` en su valor por defecto (`workers=8`) sobre `Automotive` (la primera categoría del bucle, 2.003.129 filas / 5,35 GB en jsonl), la máquina pasó de tener margen de sobra a **144 MB libres** en menos de 20 segundos, con los 8 procesos `spawn` ya en ~5,3 GB de RSS cada uno y subiendo. Se mató el proceso a mano de inmediato, como exige la auditoría, sin llegar a agotar la memoria del sistema.
  - Para aislar si era un problema de paralelismo, se probó `ItemLoader("Automotive").load(workers=2)` y `load(workers=1)` en un script suelto (sin notebook), con vigilancia de memoria cada pocos segundos. **Ambas veces**, antes de que el `ProcessPoolExecutor` llegara a procesar un solo chunk, el propio proceso principal —todavía en `Dataset.from_generator(...)` construyendo la caché Arrow de las 2 millones de filas— ya pesaba **~5 GB de RSS él solo**, y el sistema operativo mató un proceso del pool por presión de memoria (`BrokenProcessPool: A process in the process pool was terminated abruptly`). Es decir: **no es un problema de cuántos workers usa `ItemLoader`** (falla igual con 1 que con 8): es `load_amazon_meta`/`Dataset.from_generator` construyendo la caché de una categoría de 2 millones de filas, en una máquina cuyas otras aplicaciones (Chrome, Slack, Dropbox, el propio Claude Code) ya tenían consumidos unos 20 de los 24 GB de RAM antes de empezar.
  - Tras el segundo fallo se paró la ejecución (tal y como exigen las reglas de seguridad de esta pieza: no insistir sin ajustar el paralelismo, y no forzarlo si el ajuste no basta) y se revirtió `week6/day2.ipynb` a su estado del commit anterior — no se ha dejado ningún cambio a medio verificar en el notebook. Se comprobó que no quedó ningún proceso huérfano y que el disco y la memoria volvieron a sus valores normales.
  - `week6/train.pkl` y `test.pkl` **siguen vacíos** (5 bytes). `week6/day3` y `week8/day2.x` **no se han podido ejecutar** en esta sesión: seguirían fallando en cascada exactamente igual que antes, porque la causa (pickles vacíos) no ha cambiado.
  - **`Appliances` y `Musical_Instruments`** (las dos categorías más pequeñas de las ya descargadas, 94.327 y 213.593 filas) no mostraron este problema — `Appliances` ya se había verificado entera en `day1` y en el `ItemLoader` aislado (28.625 items, ver commit `5697492`). El problema es específico de categorías grandes (`Automotive` con 2 millones de filas es, con diferencia, la mayor de las 8) combinado con la carga de fondo ya existente en esta máquina.
- **`week6/day5`** — el `openai.fine_tuning.jobs.create(...)` se deja sin ejecutar a propósito, como paso manual documentado.
- **Semanas 2, 4 y 5 completas** — bloqueadas por el saldo de OpenAI.
- **`push_to_hub`** — no se ha ejecutado en ningún notebook, para no escribir en la cuenta de HuggingFace del usuario.

**Salidas que se han limpiado en vez de refrescarse** (ver sección 7):
- **`week6/day4.ipynb`, celda `Tester.test(claude_sonnet, test)`** — se deja con la salida vacía. Refrescarla son 250 llamadas reales a Claude sobre los 250 items del test, que no es una comprobación puntual barata. Lo que sí está verificado contra la API real es la llamada corregida (commit `0718b07`). El alumno verá esa celda sin ejecutar, que es honesto; la referencia de resultados sigue estando en `day4-results.ipynb`.
- **`week6/day4-results.ipynb`** — este SÍ conserva su salida, a propósito: su razón de existir es enseñar los resultados sin que el alumno pague por ellos. Pero conviene saberlo: esas 250 predicciones y ese gráfico se generaron con `claude-3-5-sonnet-20240620`, el modelo de antes. Con `claude-sonnet-5` los números **serán distintos** (probablemente mejores). No hay nada engañoso a la vista —no aparece ningún nombre viejo en la salida— pero si se quiere una referencia fiel al código de hoy, hay que regenerarla pagando esas 250 llamadas.
- **`week4/day3.ipynb`, celda del `gr.Blocks(...)`** — se deja con la salida vacía. Lanzar esa celda abre un servidor Gradio interactivo; no tiene sentido guardarle una salida.

**Comprobado y correcto, pero merece constar porque es el tipo de cosa que falla en silencio:** el índice literal `embeddings_dataset[7306]["xvector"]` (Semana 3, Días 1 y 2) se escribió contra la carga antigua del dataset, y el arreglo la cambió a `revision="refs/convert/parquet"`. Si esa conversión hubiera reordenado las filas, la celda seguiría funcionando pero el alumno oiría **otra voz** que la del vídeo, sin ningún error de por medio. Comprobado contra la API de HuggingFace: el split `validation` tiene las mismas 7.931 filas y la 7306 sigue siendo `cmu_us_slt_arctic-wav-arctic_a0508`. Es la misma voz. No hay que tocar nada.

---

## 7. Revisión final antes de publicar

Pasada específica de control de calidad sobre la rama ya montada, con la checklist del método de actualización de cursos. Lo que buscaba y lo que encontró:

| Commit | Qué encontró |
|---|---|
| `fe269e1` | **Dos celdas de `week8/day1.ipynb` con `SyntaxError`.** El comentario del `.from_name()` se había colado **detrás** del `=` (`pricer = # comentario` y luego la llamada en la línea siguiente). Ninguna de las dos celdas podía ejecutarse. Lo tapaba su propia salida guardada (`133.0`), de la ejecución original del autor, que hacía parecer que la celda estaba bien. Lo delató comparar con los ficheros hermanos: el mismo arreglo en `agents/specialist_agent.py` y en `keep_warm.py` estaba bien hecho |
| `e6fb19e` | **Dos salidas guardadas que contradecían el código.** En `week6/day4.ipynb`, un `InternalServerError: 500` cuyo traceback mostraba literalmente `claude_3_point_5_sonnet` y `model="claude-3-5-sonnet-20240620"`, es decir, el código que `0718b07` ya había cambiado. En `week4/day3.ipynb`, un `NameError: name 'gr' is not defined` con `execution_count: 1`, de una ejecución suelta de esa celda sin pasar por los imports |
| `ec4e68e` | **Cuatro nombres de modelo viejos supervivientes en comentarios y prosa.** El peor, en `README.md`: la guía de costes del curso seguía diciendo "utilice siempre `claude-3-haiku-20240307`", que devuelve 404 |
| `eb55ca5` | **620 KB de estado de widgets huérfano** en los cuatro notebooks grandes de la Semana 7. Mal formado tal y como lo exporta Colab (sin la clave `state`), que es justo lo que hace que **GitHub se niegue a renderizar el notebook**. La Semana 3 ya lo tenía quitado; la 7 no |
| `0386f18` | **Los nueve notebooks integrados de las Semanas 3 y 7 no pasaban `nbformat.validate()`**: conservaban el `id` de celda del stub 4.5 al que sustituyeron dentro de un fichero que declara 4.0. Se ve en que el mismo `id` estaba repetido en cuatro ficheros distintos. Jupyter lo avisa al alumno con "Notebook JSON is invalid" |

**Lo que se buscó y resultó estar limpio**, que también conviene saberlo:

- **Salidas contaminadas por las ejecuciones de diagnóstico de la auditoría.** Era la sospecha principal: durante la Fase 2 se ejecutaron muchos notebooks con `nbconvert --execute --allow-errors` y claves reales, antes de arreglar el código. Comprobado celda a celda en los 29 notebooks tocados, comparando cada `outputs` contra el de `d298c9a`: **no ha cambiado ni una sola línea dentro de ningún bloque `outputs`**. Los 14 commits de arreglo son cambios de código puros. Las dos salidas del commit `e6fb19e` ya venían commiteadas desde antes del fork.
- **Sintaxis de todas las celdas.** Los 51 notebooks (fuera de `community-contributions/`) y los 24 `.py` del árbol, parseados con `ast`. Tras `fe269e1`, cero errores.
- **Tamaño real del repo.** Medido con `git ls-tree` y no con `find`, porque ejecutar notebooks puede dejar basura en el working tree: 41,84 MiB en `d298c9a` → 41,99 MiB ahora. Nada se ha colado; los `.pkl`, los vectorstores y los `__pycache__` están todos ignorados.
- **Las celdas `!pip install` de los notebooks integrados** siguen ahí, palabra por palabra como en los Colabs originales. No se borró ninguna al integrarlos.
- **Consistencia del patrón `workspace_id`.** Las seis implementaciones (Semanas 2, 4 y 6) son idénticas línea a línea.
- **Efectos de segundo orden de fijar `model="gpt2"`** en `week3/day2`: esa variable (`generator`) no se reutiliza en ninguna celda posterior. El `chat_model` que sí se comparte entre tres celdas está documentado en la propia celda.
- **Los notebooks de la Semana 7 contra sus Colabs originales**: los Días 1, 2 y 5 y los dos auxiliares son idénticos en código, celda por celda. Solo cambió `day3 and 4.ipynb`, como dice la sección 3. Lo mismo en la Semana 3: el Día 3 tiene cero cambios de código.

---

## 8. Lo siguiente

1. **Recargar saldo en OpenAI** y volver a lanzar las Semanas 1, 2, 4, 5 y `week6/day4-day5` para cerrar la verificación.
2. **Terminar de subir `joanby/pricer-data`**; con eso se desbloquea la Semana 7 entera y se puede validar la migración de `trl` con datos de verdad.
3. **Ejecutar `week6/day2.ipynb` para regenerar `train.pkl`/`test.pkl` y desbloquear `week6/day3` y toda la Semana 8.** Ya se intentó y se diagnosticó por qué falla en esta máquina (ver sección 6): `Dataset.from_generator` necesita ~5 GB de RSS solo para construir la caché de `Automotive` (2 millones de filas), y esta máquina ya tiene ~20 de sus 24 GB de RAM ocupados por otras aplicaciones antes de empezar. No es un problema de `workers` de `ItemLoader` (falla igual con 1 que con 8). Para la próxima vez: cerrar el resto de aplicaciones antes de lanzarlo (liberar RAM real, no solo no competir por CPU) y volver a intentarlo con vigilancia de memoria; si sigue sin caber, la alternativa sin tocar el resultado sería procesar `Automotive` en lotes más pequeños dentro de `load_amazon_meta` (p. ej. `writer_batch_size` más bajo en `Dataset.from_generator`) en vez de construir la caché de las 2 millones de filas de una vez.
4. Aceptar los gates de FLUX.1-schnell y Llama-2-7b-chat-hf si se quieren esas dos celdas vivas.
5. Decidir sobre la regrabación de la parte de memoria/cadenas de LangChain (punto 8 de la sección 5).

> La rama está **solo en local**: sin push y sin PR, como se pidió. `main` no se ha tocado.
> Los directorios `.venv_qa/`, `_colabs_originales/` y `_qa_run_outputs/` son material de trabajo de la auditoría y **ya están en `.gitignore`** desde el commit `992b3e3`, así que no se subirán. Queda decidir si se borran del disco o se guardan aparte: `_colabs_originales/` contiene los Colabs reales recuperados de Drive, que conviene no perder.

---

## 9. Correcciones (noviembre de 2026)

Segunda pasada, hecha al preparar la mejora del curso en Thinkific: el análisis lección a lección encontró cuatro defectos de código que la verificación de septiembre no vio: un fichero que nadie había importado, un error que solo salta al pulsar un botón de la interfaz, un ejemplo de JSON mal escrito que no da error y una tarea que venía resuelta. Mismo método: cambio mínimo, reproducir antes, verificar después. Ninguno cambia lo que se teclea en el vídeo salvo lo indicado.

| Commit | Qué fallaba | Arreglo | Verificación |
|---|---|---|---|
| `410fa03` | **`week8/pricer_service2.py`** usaba `@modal.build()`, que no existe en Modal 1.x. Con el pin `modal==1.5.5`, importarlo o hacer `modal deploy pricer_service2` (lo que manda `week8/day1`) da `AttributeError: module 'modal' has no attribute 'build'`, y con él cae el agente especialista y el proyecto de la Semana 8. La pasada de septiembre comprobó `Cls.from_name`, no este fichero | `@modal.build()` → `@modal.enter()` en `download_model_to_folder`. Modal ejecuta los `@enter` en el orden en que se definen, así que la descarga sigue yendo antes que `setup()` | Con modal 1.5.5: antes, `AttributeError`; después, el import funciona, los `@enter` quedan en orden `[download_model_to_folder, setup]` y `modal deploy` llega hasta `Token missing` (sin credenciales a propósito). El resto de ficheros de Modal de la semana (`hello.py`, `llama.py`, `pricer_ephemeral.py`, `pricer_service.py`) también importan |
| `665552e` | **`week4/day3` y `day4`, `execute_python`**: `exec(code)` dentro de una función deja las funciones del código ejecutado (`lcg` en `python_hard`) en el `locals` de `exec`, y quien las llama las busca en `globals`: `NameError: name 'lcg' is not defined` al pulsar «Run Python». En el Día 3 funcionaba por casualidad si antes se había ejecutado la celda `exec(python_hard)` | `exec(code, {"__name__": "__main__"})` | Con el `python_hard` y el `pi` reales de los dos cuadernos: antes, `NameError`; después, ejecutan y dan lo mismo que con el `exec` global |
| `9d41e76` | **`week1/day5`, `link_system_prompt`**: el ejemplo de JSON que se le da al modelo era inválido (`{"type": "Pagina de Cursos": "url": …}`). Viene de la traducción (noviembre de 2024), no de las versiones | Coma en vez de dos puntos, en la celda y en su salida guardada | El ejemplo extraído del prompt construido pasa `json.loads` (antes: `Expecting ',' delimiter`) |
| `ac23464` | **`week1/week1 EXERCISE.ipynb`** venía resuelto: el 14-ene-2025 un contribuidor commiteó su solución encima del enunciado (`d262119`) | Su solución se mueve tal cual a `week1/community-contributions/week1 Ferransson EXERCISE.ipynb` (misma convención que `day2 Sebastian Tobon EXERCISE.ipynb`) y el enunciado vuelve byte a byte a su versión de `e71a7e7`, la de la grabación. La solución oficial sigue en `week1/solutions/week1 SOLUTION.ipynb`, la que cita el vídeo | Los dos notebooks pasan `nbformat.validate()`; el enunciado es idéntico al de `e71a7e7` |

**Lo que puede verse distinto al vídeo:** solo `pricer_service2.py`. Antes los pesos (Llama 3.1 8B base + el adaptador) se descargaban una vez y quedaban horneados en la imagen; ahora se descargan en cada arranque en frío del contenedor, así que el primer `price.remote()` tras un rato parado tarda más (`keep_warm.py` lo evita). La guía de migración de Modal 1.0 recomienda guardar los pesos en un `modal.Volume`; no se ha hecho para no alejar el fichero del vídeo. Si el arranque en frío molesta, es el siguiente paso.

**Lo que no se ha ejecutado:** el despliegue real en Modal con GPU (requiere cuenta, token y el gate de Llama 3.1) y la interfaz de Gradio de la Semana 4 (se probó la función `execute_python`, no el botón).

### Notas que corrigen o completan este informe

- **Llama 3.1 también tiene gate.** `meta-llama/Meta-Llama-3.1-8B` (hoy redirige a `meta-llama/Llama-3.1-8B`) es de acceso restringido con aprobación manual (`"gated": "manual"` en la API del Hub, comprobado el 19-nov-2026). Hasta que se acepta la licencia en huggingface.co con la cuenta del token, la descarga da 403 (401 sin token). Lo usan la Semana 7 y `week8/pricer_service*.py`. El punto 4 de la sección 5 solo avisaba de Llama-2-7b-chat-hf y FLUX. El adaptador `ed-donner/pricer-2024-09-13_13.04.39` es público.
- **La Semana 8 no necesita regenerar la Semana 6.** El punto 3 de la sección 8 lo daba por necesario, pero `week8/day2.0.ipynb` ya enlaza una carpeta pública de Google Drive con `train.pkl`, `test.pkl`, `random_forest_model.pkl` y `ensemble_model.pkl`. La carpeta respondía y listaba esos cuatro ficheros el 19-nov-2026 (no se han descargado ni abierto). Regenerar `week6/day2` sigue siendo necesario solo para quien quiera rehacer la curación de datos.
- **Pushover ya no es «totalmente gratis».** Hoy son 30 días de prueba y después un pago único de 4,99 USD por plataforma; enviar es gratis hasta 10.000 mensajes al mes (pushover.net/pricing, 19-nov-2026). No toca el código.
- **El Open LLM Leaderboard está archivado.** El Space `open-llm-leaderboard/open_llm_leaderboard` lo cerró Hugging Face el 13-mar-2025 (commit «Hasta la vista, leaderboard»; la etiqueta «Archived» de la cabecera se retocó el 25-mar-2025). Sigue en línea como consulta histórica, pero ya no evalúa modelos nuevos.
- **Semana 5: este informe y `PENDIENTE.md` no dicen lo mismo.** La sección 6 la pone entre las no verificadas («Semanas 2, 4 y 5 completas — bloqueadas por el saldo de OpenAI») y `PENDIENTE.md` la da por «ejecutada de principio a fin». Lo que hay: el mensaje del commit `ce288e7` dice que day1–day5 y day4.5 se ejecutaron enteros con claves reales y 0 errores; ese commit es anterior a `f321cd4`, el que fijó las versiones, y el punto 2 de la sección 5 dice que lo que impidió el saldo fue la **re-ejecución final**. La lectura coherente es que la Semana 5 se ejecutó entera tras su arreglo, pero no se volvió a ejecutar con el entorno ya fijado. No se ha podido comprobar (necesita OpenAI). Sí se ha comprobado que `chromadb==1.5.9` con `langchain-chroma==1.1.0` crea, persiste, consulta y borra la base vectorial siguiendo el patrón de `week5/day3` (con embeddings falsos, sin API).

### Week 7: la celda de instalación contradecía la propia migración

- **`week7/day3 and 4.ipynb` en Colab no instalaba el `trl` para el que se migró.** Su celda `!pip install` fijaba `datasets==2.21.0` y dejaba `trl` libre. `trl` 1.13 exige `datasets>=4.7.0`, así que pip retrocedía hasta `trl==0.15.2` (comprobado con `pip install --dry-run`: `datasets 2.21.0`, `trl 0.15.2`, `transformers 5.23.0`). En esa versión `SFTConfig` no tiene `completion_only_loss` ni `max_length`, que es justo lo que usa la migración de `bf4c3d8`: la celda de `SFTConfig` habría fallado con `TypeError`. La migración se había verificado con el `trl` de `requirements.txt`, no con la celda del notebook, que es la que ejecuta el alumno. **Arreglo:** en esa celda, `datasets==2.21.0` → `datasets==5.0.1` y `trl` → `trl==1.13.0`, los dos pines de `requirements.txt`; el resto de la línea no cambia. **Verificado:** el `pip install --dry-run` de la celda nueva resuelve `datasets 5.0.1` y `trl 1.13.0`, y `SFTConfig(...)` se construye con los argumentos exactos de la celda (sin GPU) con `trl` 1.13.0 y `transformers` 5.17.0 y 5.23.0 (el que instala hoy Colab, porque `transformers` sigue sin fijar en la celda). El `.train()` real sigue sin lanzarse (GPU y `joanby/pricer-data` vacío).
- **Los Días 1, 2 y 5 no se tocan**: fijan `transformers==4.43.1` y `datasets==2.21.0` sin fijar `peft`, `trl`, `accelerate` ni `bitsandbytes`, y no usan `SFTConfig`. No se han ejecutado en una T4.

### Semana 2

Comprobado contra la documentación oficial y los SDK fijados, **sin claves**: ninguna llamada a OpenAI ni a Google se ha ejecutado; las celdas se han probado contra servidores simulados.

| Commit | Qué fallaba | Arreglo | Verificación |
|---|---|---|---|
| `9861a9b` | **`week2/day5`, `artist()`**: el sustituto de `dall-e-3` que puso esta rama, `gpt-image-1`, «was shut down on October 23, 2026» ([referencia de la API](https://developers.openai.com/api/reference/resources/images/methods/generate)). Corrige la fila de la sección 3 que decía «`gpt-image-1`, que ya devuelve `b64_json`» | `model="gpt-image-2.5-flare"`, uno de los dos sustitutos que da la [tabla de deprecaciones](https://developers.openai.com/api/docs/deprecations) («Fast, high-quality everyday image generation»; está en el literal `ImageModel` de `openai==3.13.0`). `size="1024x1024"`, `n=1` y `data[0].b64_json` siguen siendo válidos | `artist()` contra un transporte HTTP simulado envía `{model: gpt-image-2.5-flare, n: 1, size: 1024x1024}` y decodifica la imagen. **No ejecutado contra OpenAI** (sin saldo) |
| `f2ee239` | **Gemini en `week2/day1` y `day2`**: `google-generativeai` está sin soporte («All support for this repository ended permanently on November 30, 2025», PyPI). Corrige el punto de la sección 4 que lo daba por bueno | Migración a `google-genai==2.34.0` según la [guía oficial](https://aistudio.google.com/docs/migrate): `Client()` en vez de `configure()`, `client.models.generate_content(model=…, contents=…)` y `system_instruction` dentro de `GenerateContentConfig`. Mismo modelo, `gemini-3.6-flash` (GA, sin fecha de cierre). Cambian también `requirements.txt` y `environment.yml` | Las tres celdas contra un servidor Gemini falso local mandan el texto y el `systemInstruction` esperados y leen `response.text`; `requirements.txt` resuelve entero. **No ejecutado contra Google** |
| `36a9c91` | **`week2/day2`**: `gr.Interface(..., js=force_dark_mode)` avisa en Gradio 6 de que `js` se ha movido a `launch()` | `.launch(js=force_dark_mode)` | Con `gradio==6.27.0`, antes 1 aviso y después 0; el js llega al `/config` servido en los dos casos, así que en 6.27 **era un aviso, no una rotura**. Los `gr.Blocks(css=css)` de la Semana 4 dan el mismo aviso y siguen funcionando: no se tocan |
| `31d86c0` | **`week2/day3`, chat del «cinturon»**: el mensaje del usuario se enviaba dos veces en cada turno (en la lista inicial y en un `append` final), resto del refactor de upstream `86763f2` (octubre de 2024) | Se comenta el `append` sobrante (la línea se ve en el vídeo) | Con un transporte simulado: antes, el mensaje viajaba 2 veces; después, 1 |

**Lo que puede verse distinto al vídeo:** las celdas de Gemini (otra forma de llamar al SDK, mismo resultado) y el nombre del modelo de imagen.

### `transformers` 5.17.0 → 5.18.0

- **`pipeline("text-to-speech", "microsoft/speecht5_tts")` fallaba con el pin 5.17.0** (`TypeError: BatchEncoding.to() got an unexpected keyword argument 'dtype'`, punto 10 de la sección 5) y funciona desde 5.18.0 (PyPI, 30-sep-2026). Reproducido en CPU con la voz 7306 real: con 5.17.0, `TypeError`; con 5.18.0, el pipeline devuelve audio a 16 kHz. La vía directa de SpeechT5 que usan `week3/day1` y `day2` funciona con las dos. **Arreglo:** `transformers==5.18.0` en `requirements.txt` y `environment.yml` (la versión mínima que funciona), y el comentario de esas dos celdas ya no dice que el pipeline esté «roto en la versión actual».
- **No rompe el resto:** `uv pip compile` de `requirements.txt` con 5.18.0 resuelve el mismo entorno salvo `transformers` (ningún otro paquete cambia de versión). Comprobado en CPU con 5.17.0 y 5.18.0, con resultados idénticos: tokenizadores y plantillas de chat de `Phi-3-mini-4k-instruct`, `Qwen2-7B-Instruct` y `starcoder2-3b` (Semana 3 Día 3), el patrón `apply_chat_template(..., return_dict=True)` + `generate(**inputs)` de los Días 4 y 5 (con un modelo pequeño sin gate, en greedy), el pipeline de sentimiento y `gpt2` de `week3/day2`, los embeddings de `all-MiniLM-L6-v2` (`sentence-transformers` 6.0.1) y el `SFTConfig` de `week7/day3 and 4`. No se han probado en este cambio los modelos con gate (Llama, Gemma), NER ni zero-shot (modelos de más de 1 GB), ni nada en GPU.
- Con esto, `requirements.txt` ya no es exactamente el `pip freeze` de septiembre que describe la sección 4: difieren `transformers` (5.18.0) y `google-genai` (sustituye a `google-generativeai`).

### Semanas 6 y 7 (tercera tanda)

| Commit | Qué fallaba | Arreglo | Verificación |
|---|---|---|---|
| `a1bcb5b` | **`week6/lite.ipynb` cargaba `Musical_Instruments`**. El vídeo (60652765) deja activos solo los electrodomésticos, y la salida guardada dice «Completado Appliances con 28,625 datapoints». En upstream la línea activa era `"Appliances"`: en la traducción se perdió y quedó la `x` suelta, y `b7d703a` la arregló activando la categoría equivocada. Además, subía siempre a `joanby/lite-data`, una cuenta en la que el alumno no puede escribir | Se restaura `"Appliances"` (y `Musical_Instruments` vuelve a estar comentada). Para el destino se usa el patrón de `day2` y de la Semana 7: `HF_USER = "joanby" # tu nombre de HF va aquí!` y `DATASET_NAME = f"{HF_USER}/lite-data"` | La celda da `['Appliances']`, y la de subida construye el nombre a partir de `HF_USER` (`push_to_hub` simulado). `Appliances` con el `ItemLoader` de la rama ya se verificó en septiembre (28.625 items, `5697492`) |
| `3ade7df` | **`week7/day5`, `improved_model_predict`**: si ninguno de los tres tokens es un precio, devuelve la tupla `(0.0, 0.0)` y el `Tester` falla con `TypeError: unsupported operand type(s) for -: 'tuple' and 'float'`. Viene del Colab original | `return 0.0` | Con un modelo y un tokenizador falsos: antes, `TypeError` en `Tester.run_datapoint`; después, predicción 0,0 y el punto se registra |

**`hub_strategy="every_save"` no se cambia.** En el vídeo el `"every_save"` sirve para tener una revisión del modelo en el Hub cada 5.000 pasos y elegir la mejor después (60652774, 60652787, 60652847). Eso es justo lo que hace, y lo que usa el Día 5 con `REVISION`. Ninguna lección reanuda un entrenamiento cortado, y el notebook no llama a `resume_from_checkpoint`. `"checkpoint"` («Like `"every_save"` plus push latest checkpoint to `"last-checkpoint"` subfolder for easy resuming», docstring de transformers 5.18.0) es útil para quien quiera reanudar tras un corte de Colab: haría falta además `trainer.train(resume_from_checkpoint=...)`. Va como consejo en una clase, no como arreglo del código.

### Restos (cuarta tanda)

- **`week2/day1`, `call_claude`** (la conversación adversarial) seguía leyendo `message.content[0].text`. Con los modelos de Claude de hoy el primer bloque puede ser de razonamiento: `AttributeError: 'ThinkingBlock' object has no attribute 'text'`, el mismo fallo que ya se arregló en la celda 13. Pasa a `content[-1].text`. Comprobado con una respuesta simulada de la API (bloque `thinking` y después `text`): antes, `AttributeError`; después, devuelve el texto. La llamada no pasa `temperature` (ninguna llamada a Claude de la Semana 2 lo hace ya; los `temperature=` que quedan son de OpenAI, que sí lo admite). Se mantiene `**claude_extra`, el `workspace_id` opcional de la sección 7: es un diccionario vacío salvo que el alumno defina `ANTHROPIC_WORKSPACE_ID`. `day2` no tiene ningún `content[0]` (Claude va en streaming).
- **`week3/day2`**: el comentario de los imports todavía decía que el pipeline `text-to-speech` «está roto en esta versión». Ahora dice que fallaba en 5.17.0 y se arregló en 5.18.0.
