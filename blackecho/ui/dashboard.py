from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DashboardCard:
    title: str
    icon: str
    animation: str = "fadeIn"


@dataclass
class DashboardLayout:
    theme: str = "glassmorphic"
    cards: list[DashboardCard] = field(default_factory=list)

    def add_card(self, title: str, icon: str, animation: str = "fadeIn") -> None:
        self.cards.append(DashboardCard(title=title, icon=icon, animation=animation))
