from webstore.task3.user_events import find_and_replace

def test_positive_basic_replacement():
    """
    Tests basic replacement functionality for one instance of phone, email, and token.
    """
    line = "phone=+7-999-111-22-33 email=test@mail.com token=bearer_eyJhbGciOiJIUzI1NiJ9.xyz.123"
    result = find_and_replace(line)
    expected_line = "<PHONE> <EMAIL> <TOKEN>"
    assert result.get("line") == expected_line
    assert result.get("phone_count") == 1
    assert result.get("email_count") == 1
    assert result.get("token_count") == 1

def test_positive_mixed_phone_formats():
    """
    Ensures the pattern correctly captures multiple phone numbers in various supported formats.
    """
    line = "phone=+7 999 555 44 33 phone=8(900)123-45-67 phone=79998887766"
    result = find_and_replace(line)
    expected_line = "<PHONE> <PHONE> <PHONE>"
    assert result["line"] == expected_line
    assert result["phone_count"] == 3

def test_positive_complex_emails():
    """
    Verifies that complex email addresses (with dots, dashes, subdomains) are masked.
    """
    line = "email=long.user-name@sub.domain.co.uk email=test123@site.ru"
    result = find_and_replace(line)
    expected_line = "<EMAIL> <EMAIL>"
    assert result["line"] == expected_line
    assert result["email_count"] == 2

def test_positive_mixed_token_formats():
    """
    Checks if tokens with and without the 'bearer_' prefix are masked correctly.
    """
    line = "token=bearer_eyJhbGciOiJIUzI1NifhdkibfdJ9.IUzI1N action token=eyJhbGciOiJIUzI1Ni34tfgbtyhJ9.abc"
    result = find_and_replace(line)
    expected_line = "<TOKEN> action <TOKEN>"
    assert result["line"] == expected_line
    assert result["token_count"] == 2

def test_negative_no_matches_found():
    """
    Tests a safe string that should result in zero replacements.
    """
    line = "login_attempt click path=/profile safe_line"
    result = find_and_replace(line)
    assert result["line"] == line
    assert result.get("phone_count") + result.get("email_count") + result.get("token_count") == 0

def test_edge_empty_string():
    """
    Tests handling of an empty input string.
    """
    line = ""
    result = find_and_replace(line)
    assert result.get("line") == ""
    assert result.get("phone_count") + result.get("email_count") + result.get("token_count") == 0

def test_edge_very_long_string():
    """
    Tests processing of a very long string with many PII instances.
    """
    long_data = "token=bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTk5fQ.signature phone=+7 999 555 44 33 phone=7999-888-77-66 phone=+7 999 555 44 33 email=katya-95@inbox.ru phone=8(900)123-45-67 email=ivan@example.com phone=+7-999-111-22-33 token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123 email=support@shop.ru email=petr@mail.ru phone=+7(926)777-88-99 phone=+7 999 555 44 33 login_attempt click path=/profile phone=8-999-123-45-67 email=support@shop.ru phone=7999-888-77-66 email=katya-95@inbox.ru token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abc123 token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxx phone=+7-495-123-45-67 token=bearer_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.longstring email=anna@gmail.com token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.aaaaabbbbbcccccdddddeeeeefffff action login_attempt phone=+79991234567 email=quick@fastmail.fm phone=+79991234567 token=eyJhbGciOiJIUzI1NiJ9.signature12345 view path=/profile phone=+7(926)777-88-99 email=anna@gmail.com token=eyJhbGciOiJIUzI1NiJ9.test123 phone=7999-888-77-66 login_attempt email=support@shop.ru token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.aaaaabbbbbcccccdddddeeeeefffff email=petr@mail.ru token=eyJhbGciOiJIUzI1NiJ9.xyz789 token=eyJhbGciOiJIUzI1NiJ9.signature12345 phone=+7-999-111-22-33 email=long.email.with+dots@sub.domain.co.uk login_attempt path=/profile token=eyJhbGciOiJIUzI1NiJ9.xyz789 token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.aaaaabbbbbcccccdddddeeeeefffff email=anna@gmail.com token=bearer_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.longstring token=bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTk5fQ.signature safe_line safe_line action phone=8(900)123-45-67 token=bearer_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.longstring phone=7999-888-77-66 email=petr@mail.ru path=/profile view email=hidden@secret.com email=petr@mail.ru phone=+7(926)777-88-99 phone=+79991234567 token=eyJhbGciOiJIUzI1NiJ9.signature12345 path=/profile token=bearer_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.longstring login_attempt action phone=+79991234567"
    result = find_and_replace(long_data)
    assert result.get("phone_count") + result.get("email_count") + result.get("token_count") > 10
    assert result["line"] != long_data

def test_negative_invalid_short_phone():
    """
    Ensures that phone numbers shorter than the expected minimum are not masked.
    """
    line = "phone=123-45"
    result = find_and_replace(line)
    assert result["line"] == line
    assert result["phone_count"] == 0

def test_negative_email_no_domain():
    """
    Checks that an email address without a valid top-level domain is not masked.
    """
    line = "email=user@.com"
    result = find_and_replace(line)
    assert result["line"] == line
    assert result["email_count"] == 0

def test_negative_false_token_positive():
    """
    Tests that the token pattern requires the 'eyJhbGciOiJIUzI1Ni...J9' prefix to prevent false positives.
    """
    line = "safe_action.user_id.123.log token=eyJ.aGci.IUzI1N another_action."
    result = find_and_replace(line)
    expected_line = "safe_action.user_id.123.log token=eyJ.aGci.IUzI1N another_action."
    assert result["line"] == expected_line
    assert result["token_count"] == 0
    assert result["email_count"] == 0
    assert result["phone_count"] == 0
