import json
from datetime import datetime
from tqdm import tqdm
from datasets import Dataset, Features, Value, List
from huggingface_hub import hf_hub_download
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from items import Item

CHUNK_SIZE = 1000
MIN_PRICE = 0.5
MAX_PRICE = 999.49

# La librería `datasets` ya no ejecuta los scripts de carga de los datasets (se eliminaron por seguridad),
# y McAuley-Lab/Amazon-Reviews-2023 sigue publicándose con uno. Descargamos el mismo fichero .jsonl del
# Hub y reproducimos aquí, línea a línea, exactamente lo que hacía aquel script: `details` y `author` se
# serializan a texto con json.dumps, `price` se pasa por str() (así los precios ausentes llegan como el
# texto "None" y `float(price)` sigue lanzando ValueError), y se rellenan las claves opcionales.
AMAZON_META_FEATURES = Features({
    'main_category': Value('string'),
    'title': Value('string'),
    'average_rating': Value('float64'),
    'rating_number': Value('int64'),
    'features': List(Value('string')),
    'description': List(Value('string')),
    'price': Value('string'),
    'images': List({'hi_res': Value('string'), 'large': Value('string'),
                    'thumb': Value('string'), 'variant': Value('string')}),
    'videos': List({'title': Value('string'), 'url': Value('string'), 'user_id': Value('string')}),
    'store': Value('string'),
    'categories': List(Value('string')),
    'details': Value('string'),
    'parent_asin': Value('string'),
    'bought_together': Value('string'),
    'subtitle': Value('string'),
    'author': Value('string'),
})


def _amazon_meta_generator(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                dp = json.loads(line)
                if 'details' in dp:
                    dp['details'] = json.dumps(dp['details'])
                if 'price' in dp:
                    dp['price'] = str(dp['price'])
                for optional_key in ['subtitle', 'author']:
                    if optional_key not in dp:
                        dp[optional_key] = None
                    elif not isinstance(dp[optional_key], (str, type(None))):
                        dp[optional_key] = json.dumps(dp[optional_key])
                for i in range(len(dp['images'])):
                    for k in ['hi_res', 'large', 'thumb', 'variant']:
                        if k not in dp['images'][i]:
                            dp['images'][i][k] = None
                for i in range(len(dp['videos'])):
                    for k in ['title', 'url', 'user_id']:
                        if k not in dp['videos'][i]:
                            dp['videos'][i][k] = None
            except Exception:
                continue
            yield dp


def load_amazon_meta(category):
    """Carga los metadatos de productos de una categoría de Amazon Reviews 2023."""
    filepath = hf_hub_download(
        "McAuley-Lab/Amazon-Reviews-2023",
        f"raw/meta_categories/meta_{category}.jsonl",
        repo_type="dataset",
    )
    return Dataset.from_generator(
        _amazon_meta_generator,
        gen_kwargs={"filepath": filepath},
        features=AMAZON_META_FEATURES,
    )

class ItemLoader:


    def __init__(self, name):
        self.name = name
        self.dataset = None

    def from_datapoint(self, datapoint):
        """
        Intenta crear un elemento a partir de este punto de datos
        Devuelve el elemento si se realiza correctamente o Ninguno si no se debe incluir
        """
        try:
            price_str = datapoint['price']
            if price_str:
                price = float(price_str)
                if MIN_PRICE <= price <= MAX_PRICE:
                    item = Item(datapoint, price)
                    return item if item.include else None
        except ValueError:
            return None

    def from_chunk(self, chunk):
        """
        Crea una lista de elementos a partir de este fragmento de elementos del conjunto de datos
        """
        batch = []
        for datapoint in chunk:
            result = self.from_datapoint(datapoint)
            if result:
                batch.append(result)
        return batch

    def chunk_generator(self):
        """
        Iterar sobre el conjunto de datos, generando fragmentos de puntos de datos a la vez
        """
        size = len(self.dataset)
        for i in range(0, size, CHUNK_SIZE):
            yield self.dataset.select(range(i, min(i + CHUNK_SIZE, size)))

    def load_in_parallel(self, workers):
        """
        Utiliza concurrent.futures para subcontratar el trabajo de procesamiento de fragmentos de puntos de datos. 
        Esto acelera significativamente el procesamiento, pero ocupará espacio en su computadora mientras lo hace.
        """
        results = []
        chunk_count = (len(self.dataset) // CHUNK_SIZE) + 1
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for batch in tqdm(pool.map(self.from_chunk, self.chunk_generator()), total=chunk_count):
                results.extend(batch)
        for result in results:
            result.category = self.name
        return results
            
    def load(self, workers=8):
        """
        Cargar en este conjunto de datos; el parámetro de trabajadores especifica cuántos procesos
        deben trabajar en la carga y limpieza de los datos
        """
        start = datetime.now()
        print(f"Cargando dataset {self.name}", flush=True)
        self.dataset = load_amazon_meta(self.name)
        results = self.load_in_parallel(workers)
        finish = datetime.now()
        print(f"Completado {self.name} con {len(results):,} datapoints en {(finish-start).total_seconds()/60:.1f} mins", flush=True)
        return results
        

    
    