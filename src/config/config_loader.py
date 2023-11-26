import yaml

def load_config(config_file_path="config.yml"):
    with open(config_file_path, "r") as config_file:
        config_data = yaml.safe_load(config_file)

    language = config_data.get("language", "default_value")
    max_ngram_size = config_data.get("max_ngram_size", "default_value")
    deduplication_threshold = config_data.get("deduplication_threshold", "default_value")
    deduplication_algo = config_data.get("deduplication_algo", "default_value")
    window_size = config_data.get("window_size", "default_value")
    num_of_keywords = config_data.get("num_of_keywords", "default_value")

    # Convertir a tipos específicos según sea necesario
    max_ngram_size = int(max_ngram_size)
    deduplication_threshold = float(deduplication_threshold)
    window_size = int(window_size)
    num_of_keywords = int(num_of_keywords)

    return {
        "language": language,
        "max_ngram_size": max_ngram_size,
        "deduplication_threshold": deduplication_threshold,
        "deduplication_algo": deduplication_algo,
        "window_size": window_size,
        "num_of_keywords": num_of_keywords,
    }
