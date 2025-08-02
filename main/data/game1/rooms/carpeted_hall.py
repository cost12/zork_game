from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    east_path = SingleEndPath(
        name="Carpeted Hall East Exit",
        description="A wooden door awaits you in the east.",
        end=StandIn[Location]("Carpeted Hall", "location")
    )

    west_path = SingleEndPath(
        name="Carpeted Hall West Exit",
        description=Description[PlainTextContext](PlainTextContext("In the west, a wooden door stands stoically."), PlainTextDescription()),
        end=StandIn[Location]("Theatre Stage", "location")
    )

    location = Location(
        name="Carpeted Hall",
        description=Description[PlainTextContext](PlainTextContext("You stand in a long torch-lit hallway adorned with an ornate, illustrative carpet stretching as far as you can see to the East."), PlainTextDescription()),
        paths={
            name_space.get_from_id('east', 'direction') : east_path,
            name_space.get_from_id('west', 'direction') : west_path
        }
    )
    name_space.add_many([east_path, west_path, location])
