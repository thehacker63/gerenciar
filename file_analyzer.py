class FileAnalyzer:
    def __init__(self):
        self.malware_signatures = self.load_malware_signatures()

    def load_malware_signatures(self):
        try:
            with open('malware_signatures.txt', 'r') as file:
                signatures = file.read().splitlines()
            return signatures
        except FileNotFoundError:
            return []

    def analyze_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()

            for signature in self.malware_signatures:
                if signature.encode() in file_content:
                    return "Malware detectado!"
            return "Malware não detectado."
        except Exception as e:
            return f"Erro na analise do arquivo: {str(e)}"
