import re

from pydantic import BaseModel

class FormatRegex:
    """
    Regexes to check data validity in various communication types.
    """
    USERNAME_REGEX: re.Pattern = re.compile(r'^[a-zA-Z0-9]{8, 17}')

    # 'john.doe@email.com'
    EMAIL_REGEX: re.Pattern = re.compile(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    # EMAIL_REGEX: str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    PHONE_REGEX_IN: re.Pattern = re.compile(r'^[6-9]{1}[0-9]{9}$')  # 9864049831

    # prithoo: I don't know what the format is; I just copied this from the internet.
    PHONE_REGEX_US: re.Pattern = re.compile(r'^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$')

    # 1 UC char, 1 LC char, 1 NUM char, 1 SPC char; between 8 to 64 chars
    PASSWORD_REGEX: re.Pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\-\_])[A-Za-z\d@$!%*?&\-\_]{8,65}$')