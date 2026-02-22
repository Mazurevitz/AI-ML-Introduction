#!/usr/bin/env python3
"""IT Helpdesk MCP Server — zbudowany na szkoleniu AI/ML."""

from fastmcp import FastMCP

mcp = FastMCP("IT Helpdesk")


# === Baza wiedzy ===

KB_ARTICLES = {
    "drukarka": "Drukarki sieciowe: sprawdz ping do IP. Brak odpowiedzi = siec. Odpowiada ale nie drukuje = sprzet.",
    "vpn": "VPN: sprawdz certyfikat, firewall, split tunneling. Rozlaczanie = idle timeout.",
    "haslo": "Reset hasla: AD > ADUC > Reset Password. Sync z Azure AD do 30 min.",
    "outlook": "Outlook: sprawdz profil (Mail), wyczysc .ost, sprawdz autodiscover.",
    "teams": "Teams: kamera w Settings > Privacy. Cache: %appdata%/Microsoft/Teams.",
}


@mcp.tool
def search_knowledge_base(query: str) -> str:
    """Przeszukaj baze wiedzy IT (runbooki, procedury) po slowach kluczowych."""
    results = [a for k, a in KB_ARTICLES.items() if k in query.lower()]
    if results:
        return " | ".join(results)
    return "Brak artykulow dla: '{}'. Dostepne tematy: {}".format(
        query, ", ".join(KB_ARTICLES.keys())
    )


# === Zgloszenia ===

TICKETS = {
    "T-001": {"text": "Laptop nie wlacza sie", "category": "Sprzet", "status": "Otwarty", "priority": "P1"},
    "T-002": {"text": "VPN rozlacza sie co 10 min", "category": "Siec", "status": "W trakcie", "priority": "P1"},
    "T-003": {"text": "Outlook nie synchronizuje", "category": "Oprogramowanie", "status": "Otwarty", "priority": "P2"},
    "T-004": {"text": "Konto zablokowane po 3 probach", "category": "Konto", "status": "Zamkniety", "priority": "P2"},
    "T-005": {"text": "Drukarka sieciowa nie odpowiada", "category": "Siec", "status": "Otwarty", "priority": "P2"},
}

_next_id = len(TICKETS) + 1


@mcp.tool
def get_ticket(ticket_id: str) -> str:
    """Sprawdz status zgloszenia IT po jego ID (np. T-001, T-002)."""
    ticket = TICKETS.get(ticket_id.upper())
    if not ticket:
        return "Zgloszenie {} nie znalezione. Dostepne: {}".format(
            ticket_id, ", ".join(TICKETS.keys())
        )
    return "[{}] {} | {} | {} | {}".format(
        ticket_id, ticket["text"], ticket["category"], ticket["status"], ticket["priority"]
    )


@mcp.tool
def create_ticket(summary: str, category: str, priority: str) -> str:
    """Utworz nowe zgloszenie IT. Kategorie: Sprzet, Siec, Oprogramowanie, Konto. Priorytety: P1-P4."""
    global _next_id
    tid = "T-{:03d}".format(_next_id)
    TICKETS[tid] = {
        "text": summary,
        "category": category,
        "status": "Otwarty",
        "priority": priority,
    }
    _next_id += 1
    return "Utworzono {}: {} [{}, {}]".format(tid, summary, category, priority)


# === Status systemow ===

SYSTEMS = {
    "Active Directory": {"status": "Online", "uptime": "99.9%"},
    "Exchange Online": {"status": "Online", "uptime": "99.7%"},
    "VPN Gateway": {"status": "Degraded", "uptime": "98.2%"},
    "Jira": {"status": "Online", "uptime": "99.5%"},
    "Drukarki sieciowe": {"status": "Offline", "uptime": "95.1%"},
}


@mcp.tool
def check_system_status(system_name: str) -> str:
    """Sprawdz status systemu IT. Dostepne: Active Directory, Exchange Online, VPN Gateway, Jira, Drukarki sieciowe."""
    system = SYSTEMS.get(system_name)
    if not system:
        return "System '{}' nieznany. Dostepne: {}".format(
            system_name, ", ".join(SYSTEMS.keys())
        )
    return "{}: {} | Uptime: {}".format(system_name, system["status"], system["uptime"])


if __name__ == "__main__":
    mcp.run()
