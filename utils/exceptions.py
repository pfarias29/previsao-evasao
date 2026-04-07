class InvalidModelException(Exception):
    """Erro quando o tipo de modelo não é selecionado"""
    pass

class EmtpyDocumentException(Exception):
    """Erro quando o documento enviado não é um histórico ou não foram encontradas matérias"""
    pass