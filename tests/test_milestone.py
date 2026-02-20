from datetime import date, timedelta
import pytest
from phd_progress_tracker.models.milestone import Milestone


@pytest.fixture
def milestone_data():
    """Dados básicos para criar um Milestone."""
    return {
        "id": "milestone-1",
        "title": "Qualificação",
        "description": "Qualificação do doutorado",
        "target_date": date.today() + timedelta(days=60),
    }


@pytest.fixture
def sample_milestone(milestone_data):
    """Uma instância de Milestone com dados padrão."""
    return Milestone(**milestone_data)


@pytest.fixture
def achieved_milestone(milestone_data):
    """Uma instância de Milestone já alcançada."""
    achieved_data = milestone_data.copy()
    achieved_data["is_achieved"] = True
    return Milestone(**achieved_data)


@pytest.fixture
def future_milestone(milestone_data):
    """Uma instância de Milestone com data futura."""
    future_data = milestone_data.copy()
    future_data["target_date"] = date.today() + timedelta(days=30)
    return Milestone(**future_data)


@pytest.fixture
def past_milestone(milestone_data):
    """Uma instância de Milestone com data passada."""
    past_data = milestone_data.copy()
    past_data["target_date"] = date.today() - timedelta(days=30)
    return Milestone(**past_data)


def test_milestone_creation(milestone_data):
    """Verifica a criação de um Milestone com todos os campos."""
    milestone = Milestone(**milestone_data)
    assert milestone.id == milestone_data["id"]
    assert milestone.title == milestone_data["title"]
    assert milestone.description == milestone_data["description"]
    assert milestone.target_date == milestone_data["target_date"]
    assert milestone.is_achieved is False


def test_milestone_creation_achieved(milestone_data):
    """Verifica a criação de um Milestone já alcançado."""
    milestone = Milestone(**milestone_data, is_achieved=True)
    assert milestone.is_achieved is True


def test_milestone_days_until_future(future_milestone):
    """Verifica days_until() com data futura."""
    expected_days = (future_milestone.target_date - date.today()).days
    assert future_milestone.days_until() == expected_days


def test_milestone_days_until_past(past_milestone):
    """Verifica days_until() com data passada."""
    expected_days = (past_milestone.target_date - date.today()).days
    assert past_milestone.days_until() == expected_days


def test_milestone_days_until_today(milestone_data):
    """Verifica days_until() com data de hoje."""
    milestone_today = Milestone(
        id=milestone_data["id"],
        title=milestone_data["title"],
        description=milestone_data["description"],
        target_date=date.today(),
    )
    assert milestone_today.days_until() == 0


def test_milestone_is_achieved_true(achieved_milestone):
    """Verifica is_achieved retorna True quando o milestone está alcançado."""
    assert achieved_milestone.is_achieved is True


def test_milestone_is_achieved_false(sample_milestone):
    """Verifica is_achieved retorna False quando o milestone não está alcançado."""
    assert sample_milestone.is_achieved is False


def test_milestone_to_dict(sample_milestone):
    """Verifica a conversão de Milestone para dicionário."""
    milestone_dict = sample_milestone.to_dict()
    assert isinstance(milestone_dict, dict)
    assert milestone_dict["id"] == sample_milestone.id
    assert milestone_dict["title"] == sample_milestone.title
    assert milestone_dict["description"] == sample_milestone.description
    assert milestone_dict["target_date"] == sample_milestone.target_date.isoformat()
    assert milestone_dict["is_achieved"] == sample_milestone.is_achieved


def test_milestone_from_dict(sample_milestone):
    """Verifica a criação de Milestone a partir de dicionário."""
    milestone_dict = sample_milestone.to_dict()
    new_milestone = Milestone.from_dict(milestone_dict)
    assert new_milestone.id == sample_milestone.id
    assert new_milestone.title == sample_milestone.title
    assert new_milestone.description == sample_milestone.description
    assert new_milestone.target_date == sample_milestone.target_date
    assert new_milestone.is_achieved == sample_milestone.is_achieved
