# Informe de actualización del curso — septiembre de 2026

**Repo:** `llm_engineering`
**Rama:** `actualizacion-transformers-2026-09-13` (local, sin push y sin PR; `main` intacto)
**Entorno de verificación:** macOS (Apple Silicon, 24 GB, sin GPU CUDA — solo MPS), Python 3.12, venv `.venv_qa`

---

## 1. Resumen

El curso se grabó con las librerías de finales de 2024 y `requirements.txt` no fijaba **ni una sola versión**. Eso es lo que ha causado el desfase: cada alumno nuevo instalaba lo último que hubiera ese día, y varias APIs del ecosistema han cambiado de forma incompatible desde entonces.

Se han corregido **11 commits** de arreglos sobre los 3 que ya existían. El cambio de fondo, además de los arreglos concretos, es que ahora las versiones están fijadas: el curso deja de moverse solo.

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

**Nota sobre las Semanas 3 y 7:** sus `dayN.ipynb` eran punteros a Colab de una sola celda Markdown. Ahora contienen el notebook real, integrado desde `_colabs_originales/`, con los arreglos aplicados.

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
| transformers | 4.4x | **5.17.0** |
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
| 10 | **`pipeline("text-to-speech")` está roto en transformers 5.17.0** — `text_to_audio.py` llama a `.to(dtype=...)` sobre un `BatchEncoding`, que solo acepta `device`. Es un bug **de la librería**, no del curso; se ha esquivado usando SpeechT5 directamente. Si lo arreglan río arriba, se podría volver al pipeline de una línea. | Esquivado, revisar en el futuro |

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
- **`week6/day2` con las 8 categorías** — son **24 GB** de descargas y quedan 37 GB de disco, más un procesado largo con 8 procesos en paralelo. Se decidió no ejecutarlo: es el **mismo código** que ya se ha probado con datos reales en `day1` (cifras idénticas al original) y en `lite` (0 errores), solo que con más datos. Como consecuencia, `week6/train.pkl` y `test.pkl` siguen vacíos (5 bytes, los dejó así la auditoría anterior) y por eso `week6/day3` y `week8/day2.x` siguen dando errores en cascada. **No es un fallo de código: se resuelve ejecutando `week6/day2.ipynb` una vez.**
- **`week6/day5`** — el `openai.fine_tuning.jobs.create(...)` se deja sin ejecutar a propósito, como paso manual documentado.
- **Semanas 2, 4 y 5 completas** — bloqueadas por el saldo de OpenAI.
- **`push_to_hub`** — no se ha ejecutado en ningún notebook, para no escribir en la cuenta de HuggingFace del usuario.

---

## 7. Lo siguiente

1. **Recargar saldo en OpenAI** y volver a lanzar las Semanas 1, 2, 4, 5 y `week6/day4-day5` para cerrar la verificación.
2. **Terminar de subir `joanby/pricer-data`**; con eso se desbloquea la Semana 7 entera y se puede validar la migración de `trl` con datos de verdad.
3. **Ejecutar `week6/day2.ipynb` una vez** para regenerar `train.pkl`/`test.pkl` y desbloquear `week6/day3` y toda la Semana 8.
4. Aceptar los gates de FLUX.1-schnell y Llama-2-7b-chat-hf si se quieren esas dos celdas vivas.
5. Decidir sobre la regrabación de la parte de memoria/cadenas de LangChain (punto 8 de la sección 5).

> La rama está **solo en local**: sin push y sin PR, como se pidió. `main` no se ha tocado.
> Los directorios `.venv_qa/`, `_colabs_originales/` y `_qa_run_outputs/` están sin trackear a propósito (son material de trabajo de la auditoría). Conviene decidir si se añaden a `.gitignore` o se borran antes de hacer push.
