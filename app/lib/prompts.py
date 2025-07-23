
def sector_validation_prompt(sector: str) -> str:
    return (
        f'You are a business analyst. Is "{sector}" a valid business or industrial sector in India or in the world?\n'
        f'Reply strictly with "valid" or "invalid".'
    )
