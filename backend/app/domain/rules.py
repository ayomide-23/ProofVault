from .entities import Agreement

def is_fully_signed(agreement: Agreement) -> bool: #rules to check if an agreement is fully signed by both parties
    return agreement.creator_signed and agreement.counterparty_signed

def can_sign(signer_id: str, agreement:Agreement) -> bool: #rules to check if a user can sign an agreement
    if agreement.counterparty_signed:
        return False
    return signer_id == agreement.counterparty_id