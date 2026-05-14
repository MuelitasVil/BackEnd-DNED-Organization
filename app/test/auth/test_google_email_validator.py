import pytest

from app.utils.google_email_validator import GoogleEmailValidator


def test_validate_unal_email_format_valid():
    assert GoogleEmailValidator.validate_unal_email_format(
        "student@unal.edu.co"
    ) is True
    assert GoogleEmailValidator.validate_unal_email_format(
        "professor.name@unal.edu.co"
    ) is True
    assert GoogleEmailValidator.validate_unal_email_format(
        "user123@unal.edu.co"
    ) is True


def test_validate_unal_email_format_invalid_domain():
    assert GoogleEmailValidator.validate_unal_email_format(
        "user@gmail.com"
    ) is False
    assert GoogleEmailValidator.validate_unal_email_format(
        "user@hotmail.com"
    ) is False
    assert GoogleEmailValidator.validate_unal_email_format(
        "user@example.com"
    ) is False


def test_validate_unal_email_format_invalid_format():
    assert GoogleEmailValidator.validate_unal_email_format(
        "invalid-email@unal.edu.co."
    ) is False
    assert GoogleEmailValidator.validate_unal_email_format(
        "@unal.edu.co"
    ) is False
    assert GoogleEmailValidator.validate_unal_email_format(
        "user@unal.edu.co.extra"
    ) is False


def test_validate_and_raise_with_invalid_domain():
    with pytest.raises(ValueError, match="must be from @unal.edu.co"):
        GoogleEmailValidator.validate_and_raise("user@gmail.com")


def test_validate_and_raise_with_valid_email():
    GoogleEmailValidator.validate_and_raise("student@unal.edu.co")
