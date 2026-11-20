import pytest
from auth.validators import password_valida, have_all_data, confirm_password, email_valido, username_valido


def test_password_valida():
    ok, messagem = password_valida(":-Al.@%Sup/19")
    assert ok == True