"""Testes básicos do phd-progress-tracker."""


def test_import_principal():
    """Verifica que o pacote importa sem erros."""
    import phd_progress_tracker
    assert phd_progress_tracker is not None


def test_versao_existe():
    """Verifica que a versão está definida."""
    from phd_progress_tracker import __version__
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_placeholder():
    """Teste placeholder — substitua por testes reais."""
    assert 1 + 1 == 2
