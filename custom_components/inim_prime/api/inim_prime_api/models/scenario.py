from dataclasses import dataclass

from .panel_item import PanelItemStatus


@dataclass(frozen = True)
class ScenarioStatus(PanelItemStatus):
    state: bool  # "st" - scenario state

    def __str__(self) -> str:
        return (
            f"Scenario {self.id}: {self.name}\n"
            f"  State: {'Active' if self.state else 'Inactive'}"
        )


@dataclass(frozen = True)
class ActivateScenarioRequest:
    scenario_id: int
