from typing import Literal


type YesNoType = Literal['Ano',  'Ne', 'Není k dispozici']
type Gender = Literal["Muž", "Žena", "Jiné"] # Undifferentiated = Jiné

type Smoker = Literal[
    "Aktivní kuřák", "Bývalý kuřák", "Pasivní kuřák", "Nekuřák", "Údaj není k dispozici"
]
type Alcohol = Literal[
    "Abstinent", "Příležitostní konzumace", "Denní konzumace", "Údaj není k dispozici"
]
type DrugAddiction = Literal[
    "Aktuálně drogově závislý(á)", "Nikdy drogově závislý(á)", "Drogově závislý(á) v minulosti", "Údaj není k dispozici"
]