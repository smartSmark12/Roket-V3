from game.scripts.event_related.action_event import ActionEvent
from game.scripts.helper import Helper

from game.scripts.event_related.action_event_type import ActionEventType
from game.scripts.event_related.action_event_target import ActionEventTarget

class EventExecutor:
    def __init__(self, appInstance, actionList:list[ActionEvent]):
        self.app = appInstance
        self.actionlist = actionList

        """ self.probability_actionlist """
        """ self.actionevent_actionlist """

        self.action_type = ActionEventType
        self.action_target = ActionEventTarget

        self.current_event_index = 0

    def _next(self):
        return int(Helper.clamp(self.current_event_index + 1, 0, len(self.actionlist) - 1))

    def _next_event(self):
        return self.actionlist[self._next()]

    def _validate_condition(self, event:ActionEvent): # will be different for every executor type
        return event.get_condition() < self.app.get_gamestate().get_game_time()

    def update(self):
        while self._validate_condition(self._next_event()): # should stay same for every executor type
            self._execute_at_index()

            self.current_event_index += 1

    def _execute_event(self, event:ActionEvent):
        match event.atype:
            case self.action_type.ACTION_SPAWN:
                pass

            case self.action_type.ACTION_EXPLODE:
                pass

            case self.action_type.ACTION_HEAL:
                pass

            case self.action_type.ACTION_DAMAGE:
                pass

    def _execute_at_index(self, index:int):
        self._execute_event(self.actionlist[index])