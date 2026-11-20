from auth.validators import password_valida, have_all_data, confirm_password, email_valido, username_valido

def test_password_boa_e_aceite():
    assert password_valida("Sup3rSegura")[0]

def test_password_so_com_simbolos_e_aceite():
    assert password_valida(":-Al.@%Sup/")[0]

def test_password_sem_numero_nem_simbolo_e_rejeitada():
    assert not password_valida("SoLetrasAqui")[0]

def test_password_curta_e_rejeitada():
    assert not password_valida("curta1!")[0]

def test_password_sem_vazada_e_rejeitada():
    assert not password_valida("password")[0]