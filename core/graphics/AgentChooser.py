from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    DictProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.datatables import TableData

from kivy.clock import Clock
from kivy.lang import Builder

from typing import Union
from kivy.uix.widget import Widget

Builder.load_string(
"""
#:import DEVICE_TYPE kivymd.material_resources.DEVICE_TYPE
#:import StiffScrollEffect kivymd.effects.stiffscroll.StiffScrollEffect


<AgentCellRow>
    orientation: "vertical"

    canvas.before:
        Color:
            rgba:
                (\
                root.theme_cls.bg_darkest \
                if root.theme_cls.theme_style == "Light" else \
                root.theme_cls.bg_light \
                ) \
                if self.selected else root.theme_cls.bg_normal
        Rectangle:
            pos: self.pos
            size: self.size

    on_press: if DEVICE_TYPE != "desktop": root.table.on_mouse_select(self)
    on_enter: if DEVICE_TYPE == "desktop": root.table.on_mouse_select(self)

    MDBoxLayout:
        id: box
        padding: "8dp", "8dp", 0, "8dp"
        spacing: "16dp"

        MDIcon:
            id: state_icon
            icon: "menu-right"

        MDBoxLayout:
            id: inner_box

            MDIcon:
                id: icon
                size_hint: None, None
                pos_hint: {"center_y": 0.5}
                size: ("24dp", "24dp") if root.icon else (0, 0)
                icon: root.icon if root.icon else ""
                theme_text_color: "Custom"
                text_color:
                    root.icon_color if root.icon_color else \
                    root.theme_cls.primary_color

            MDLabel:
                id: label
                text: " " + root.text
                markup: True
                color:
                    (1, 1, 1, 1) \
                    if root.theme_cls.theme_style == "Dark" else \
                    (0, 0, 0, 1)

    MDSeparator:

<ActionsTable>

    MDCard:
        id: container
        orientation: "vertical"
        elevation: root.elevation
        padding: "24dp", "24dp", "8dp", "8dp"

""")

default = {
            "Network":{
                "connect":"connect to a spcified SSID", 
                "disconnect":"disconnect the machine from network"
                },
            "Bluetooth":{
                "switch_on":"Turn on bluetooth sensor",
                "switch_off":"Turn off bluetooth sensor"
                },
            "Process":{
                "start":"Starts a new process",
                "kill":"Kill a process by his name"
                },
            "Audio":{
                "set_master_volume":"Set the master volume of the system to a specified percentage",
                "mute_process":"Mute a specific process",
                "unmute_process":"Unmute a specific process muted by \"mute_process\"",
                "stop/play_audio":"Virtual press the stop media button (0xB3)",
                "play_audio":"Play an mp3 file from specific path"
                },
            "System":{
                "shotdown":"Stotdown the system",
                "reboot":"Reboot the system",
                "suspend":"Suspend the system",
                "look":"Look the machine",
                "logoff":"Logout the current user",
                "set_brightness":"Fade the Screen 0 brightness to a new value",
                "take_screenshot":"Take one screenshot and save it",
                "send_notification":"Send a local push notification"
                },
            }

from core.graphics.Selector import TableHeader, TablePagination, TableData

class AgentCellRow(    
    ThemableBehavior,
    RecycleDataViewBehavior,
    HoverBehavior,
    ButtonBehavior,
    BoxLayout,
):
    text = StringProperty()  # row text
    table = ObjectProperty()  # <TableData object>
    index = None
    icon = StringProperty()
    icon_copy = icon
    icon_color = ColorProperty(None)
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(AgentCellRow, self).__init__(**kwargs)

    def notify_checkbox_click(self, instance, active):
        self.table.get_select_row(self.index)

    def on_icon(self, instance, value):
        self.icon_copy = value

    def on_table(self, instance, table):
        """Sets padding/spacing to zero if no checkboxes are used for rows."""

        if not table.check:
            self.ids.box.padding = 0
            self.ids.box.spacing = 0

    def refresh_view_attrs(self, table_data, index, data):
        
        self.index = index
        return super().refresh_view_attrs(table_data, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            if self.table._parent:
                self.table._parent.dispatch("on_row_press", self)
            return True

    def apply_selection(self, table_data, index, is_selected):
        """Called when list items of table appear on the screen."""

        self.selected = is_selected

        # Fixes cloning of icons.
        ic = table_data.recycle_data[index].get("icon", None)
        cell_row_obj = table_data.view_adapter.get_visible_view(index)

        if not ic:
            cell_row_obj.icon = ""
        else:
            cell_row_obj.icon = cell_row_obj.icon_copy

        # Set checkboxes.
        if table_data.check:
            if self.index in table_data.data_first_cells:
                self.ids.check.size = (dp(32), dp(32))
                self.ids.check.opacity = 1
                self.ids.box.spacing = dp(16)
                self.ids.box.padding[0] = dp(8)
            else:
                self.ids.check.size = (0, 0)
                self.ids.check.opacity = 0
                self.ids.box.spacing = 0
                self.ids.box.padding[0] = 0

        # Set checkboxes state.
        if table_data._rows_number in table_data.current_selection_check:
            for index in table_data.current_selection_check[
                table_data._rows_number
            ]:
                if (
                    self.index
                    in table_data.current_selection_check[
                        table_data._rows_number
                    ]
                ):
                    self.change_check_state_no_notif("down")
                else:
                    self.change_check_state_no_notif("normal")
        else:
            self.change_check_state_no_notif("normal")

    def change_check_state_no_notif(self, new_state):
        checkbox = self.ids.check
        checkbox.unbind(active=self.notify_checkbox_click)
        checkbox.state = new_state
        checkbox.bind(active=self.notify_checkbox_click)

    def _check_all(self, state):
        """Checks if all checkboxes are in same state"""

        if state == "down" and self.table.check_all(state):
            self.table.table_header.ids.check.state = "down"
        else:
            self.table.table_header.ids.check.state = "normal"

    def select_check(self, instance, active):
        """Called upon activation/deactivation of the checkbox."""

        if active:
            if (
                self.table._rows_number
                not in self.table.current_selection_check
            ):
                self.table.current_selection_check[self.table._rows_number] = []
            if (
                self.index
                not in self.table.current_selection_check[
                    self.table._rows_number
                ]
            ):
                self.table.current_selection_check[
                    self.table._rows_number
                ].append(self.index)
        else:
            if self.table._rows_number in self.table.current_selection_check:
                if (
                    self.index
                    in self.table.current_selection_check[
                        self.table._rows_number
                    ]
                    and not active
                ):
                    self.table.current_selection_check[
                        self.table._rows_number
                    ].remove(self.index)

class SortButton(MDIconButton):
    pass

class AgentsTableData(RecycleView): # use this instead of core.graphics.Selector.TableData

    recycle_data = ListProperty()  # kivy.uix.recycleview.RecycleView.data
    data_first_cells = ListProperty()  # list of first row cells
    row_data = ListProperty()  # MDDataTable.row_data
    total_col_headings = NumericProperty(0)  # TableHeader.col_headings
    cols_minimum = DictProperty()  # TableHeader.cols_minimum
    table_header = ObjectProperty()  # <TableHeader object>
    pagination_menu = ObjectProperty()  # <MDDropdownMenu object>
    pagination = ObjectProperty()  # <TablePagination object>
    check = ObjectProperty()  # MDDataTable.check
    rows_num = NumericProperty()  # number of rows displayed on the table page
    # Open or close the menu for selecting the number of rows displayed
    # on the table page.
    pagination_menu_open = BooleanProperty(True)
    # List of indexes of marked checkboxes.
    current_selection_check = DictProperty()
    cell_row_obj_dict = {}
    static = BooleanProperty(False)
    use_default = BooleanProperty(False)
    default = DictProperty(default)

    _parent = ObjectProperty()
    _rows_number = NumericProperty(0)
    _rows_num = NumericProperty()
    _current_value = NumericProperty(1)
    _to_value = NumericProperty()
    _row_data_parts = ListProperty()

    def __init__(self, table_header, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_y = False
        if self.static:
            self.do_scroll_x = False
        self.table_header = table_header
        self.total_col_headings = len(table_header.col_headings)
        self.cols_minimum = table_header.cols_minimum
        self.set_row_data()
        #Clock.schedule_once(lambda *args: self._get_all_checkboxes(), 0)
        #Clock.schedule_once(self.set_default_first_row, 0)

    def get_select_row(self, index):
        """Returns the current row with all elements."""

        row = []
        for data in self.recycle_data:
            if index in data["range"]:
                row.append(data["text"])
        self._parent.dispatch("on_check_press", row)
        self._get_row_checks()  # update the dict

    def set_default_first_row(self, dt):
        """Set default first row as selected."""

        self.ids.row_controller.select_next(self)

    def set_row_data(self):
        data = []
        low = 0
        high = self.total_col_headings - 1
        self.recycle_data = []
        self.data_first_cells = []

        if self._row_data_parts:
            # for row in self.row_data:
            for row in self._row_data_parts[self._rows_number]:
                for i in range(len(row)):
                    data.append([row[i], row[0], [low, high]])
                low += self.total_col_headings
                high += self.total_col_headings

            for j, x in enumerate(data):
                if x[0] == x[1]:
                    self.data_first_cells.append(x[2][0])
                    self.recycle_data.append(
                        {
                            "text": str(x[0]),
                            "Index": str(j),
                            "range": x[2],
                            "selectable": True,
                            "viewclass": "CellRow",
                            "table": self,
                        }
                    )
                else:
                    r_data = {
                        "Index": str(j),
                        "range": x[2],
                        "selectable": True,
                        "viewclass": "CellRow",
                        "table": self,
                    }

                    if (
                        isinstance(x[0], tuple) or isinstance(x[0], list)
                    ) and len(x[0]) == 3:
                        r_data["icon"] = x[0][0]
                        r_data["icon_color"] = x[0][1]
                        r_data["text"] = str(x[0][2])

                        self.recycle_data.append(r_data)

                    elif (
                        isinstance(x[0], tuple) or isinstance(x[0], list)
                    ) and len(x[0]) == 2:
                        r_data["icon"] = x[0][0]
                        r_data["text"] = str(x[0][1])

                        self.recycle_data.append(r_data)

                    else:
                        r_data["text"] = str(x[0])
                        self.recycle_data.append(r_data)

            if not self.table_header.column_data:
                raise ValueError("Set value for column_data in class TableData")
            self.data_first_cells.append(self.table_header.column_data[0][0])

    def _get_all_checkboxes(self):
        for i in range(0, len(self.recycle_data), self.total_col_headings):
            cell_row_obj = cell_row_obj = self.view_adapter.get_visible_view(i)
            self.cell_row_obj_dict[i] = cell_row_obj
            print(cell_row_obj)

    def set_text_from_of(self, direction):
        """Sets the text of the numbers of displayed pages in table."""

        if self.pagination:
            if direction == "reset":
                self._current_value = 1
                self._to_value = len(self._row_data_parts[self._rows_number])
            elif direction == "forward":
                if (
                    len(self._row_data_parts[self._rows_number])
                    < self._to_value
                ):
                    self._current_value = self._current_value + self.rows_num
                else:
                    self._current_value = self._current_value + len(
                        self._row_data_parts[self._rows_number]
                    )
                self._to_value = self._to_value + len(
                    self._row_data_parts[self._rows_number]
                )
            if direction == "back":
                self._current_value = self._current_value - len(
                    self._row_data_parts[self._rows_number]
                )
                self._to_value = self._to_value - len(
                    self._row_data_parts[self._rows_number + 1]
                )
            if direction == "increment":
                self._current_value = 1
                self._to_value = self.rows_num + self._current_value - 1

            self.pagination.ids.label_rows_per_page.text = (
                f"{self._current_value}-{self._to_value} "
                f"of {len(self.row_data)}")

    def select_all(self, state):
        """Sets the checkboxes of all rows to the active/inactive position."""

        for i in range(0, len(self.recycle_data), self.total_col_headings):
            cell_row_obj = cell_row_obj = self.view_adapter.get_visible_view(i)
            self.cell_row_obj_dict[i] = cell_row_obj
            self.on_mouse_select(cell_row_obj)
            cell_row_obj.ids.check.state = state

        if state == "down":
            # select all checks on all pages
            rows_num = self.rows_num
            columns = self.total_col_headings
            full_pages = len(self.row_data) // self.rows_num
            left_over_rows = len(self.row_data) % self.rows_num

            new_checks = {}
            for page in range(full_pages):
                new_checks[page] = list(range(0, rows_num * columns, columns))

            if left_over_rows:
                new_checks[full_pages] = list(
                    range(0, left_over_rows * columns, columns)
                )

            self.current_selection_check = new_checks
            return

        # resets all checks on all pages
        self.current_selection_check = {}

    def check_all(self, state):
        """Checks if checkboxes of all rows are in the same state"""

        tmp = []
        for i in range(0, len(self.recycle_data), self.total_col_headings):
            if self.cell_row_obj_dict.get(i, None):
                cell_row_obj = self.cell_row_obj_dict[i]
            else:
                cell_row_obj = self.view_adapter.get_visible_view(i)
                if cell_row_obj:
                    self.cell_row_obj_dict[i] = cell_row_obj
            if cell_row_obj:
                tmp.append(cell_row_obj.ids.check.state == state)
        return all(tmp)

    def _get_row_checks(self):
        """
        Returns all rows that are checked
        """

        tmp = []
        for i in range(0, len(self.recycle_data), self.total_col_headings):
            if self.cell_row_obj_dict.get(i, None):
                cell_row_obj = self.cell_row_obj_dict[i]
            else:
                cell_row_obj = self.view_adapter.get_visible_view(i)
                if cell_row_obj:
                    self.cell_row_obj_dict[i] = cell_row_obj

            if cell_row_obj and cell_row_obj.ids.check.state == "down":
                idx = cell_row_obj.index
                row = []
                for data in self.recycle_data:
                    if idx in data["range"]:
                        row.append(data["text"])

                tmp.append(row)
        return tmp

    def close_pagination_menu(self, *args):
        """Called when the pagination menu window is closed."""

        self.pagination_menu_open = False

    def open_pagination_menu(self):
        """Open pagination menu window."""

        if self.pagination_menu.items:
            self.pagination_menu_open = True
            self.pagination_menu.open()

    def set_number_displayed_lines(self, text_item):
        """
        Called when the user sets the number of pages displayed
        in the table.
        """

        self.rows_num = int(text_item)
        self.set_next_row_data_parts("reset")
        self.set_text_from_of("reset")

    def set_next_row_data_parts(self, direction):
        """Called when switching the pages of the table."""

        if direction == "reset":
            self._rows_number = 0
            self.pagination.ids.button_back.disabled = True
            self.pagination.ids.button_forward.disabled = False
        elif direction == "forward":
            self._rows_number += 1
            self.pagination.ids.button_back.disabled = False
        elif direction == "back":
            self._rows_number -= 1
            self.pagination.ids.button_forward.disabled = False

        self.set_row_data()
        self.set_text_from_of(direction)

        if self._to_value == len(self.row_data):
            self.pagination.ids.button_forward.disabled = True
        if self._current_value == 1:
            self.pagination.ids.button_back.disabled = True

    def on_mouse_select(self, instance):
        """Called on the ``on_enter`` event of the :class:`~CellRow` class."""

        if not self.pagination_menu_open:
            if self.ids.row_controller.selected_row != instance.index:
                self.ids.row_controller.selected_row = instance.index
                self.ids.row_controller.select_current(self)

    def on_rows_num(self, instance, value):
        if not self._to_value:
            self._to_value = value

        self._rows_number = 0
        self._row_data_parts = list(
            self._split_list_into_equal_parts(self.row_data, value)
        )

    def on_pagination(self, instance, value):
        if self._to_value < len(self.row_data):
            self.pagination.ids.button_forward.disabled = False

    def _split_list_into_equal_parts(self, lst, parts):
        for i in range(0, len(lst), parts):
            yield lst[i : i + parts]


class ActionsTable(ThemableBehavior, AnchorLayout):
    
    default = DictProperty(default)
    column_data = ListProperty(
        [("Type", dp(30)),
        ("Description", dp(121)),]
    )
    row_data = ListProperty()
    sorted_on = StringProperty()
    sorted_order = OptionProperty("ASC", options=["ASC", "DSC"])
    check = BooleanProperty(False)
    use_pagination = BooleanProperty(False)
    elevation = NumericProperty(8)
    rows_num = NumericProperty(5)
    pagination_menu_pos = OptionProperty("center", options=["center", "auto"])
    pagination_menu_height = NumericProperty("140dp")
    background_color = ColorProperty([0, 0, 0, 0])
    static = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header = TableHeader(
            column_data=self.column_data,
            sorted_on=self.sorted_on,
            sorted_order=self.sorted_order,
        )
        if True: #not self.row_data and not self.column_data:

            self.header.ids.check.disabled = True, # deactivating the select all checkbox
            self.header.ids.check.opacity = 0

            self.header.ids.check.parent.remove_widget(self.header.ids.check) # remove the select all checkbox
            self.table_data = self._process_default_data()
            self.register_event_type("on_row_press")
            self.register_event_type("on_check_press")
            self.pagination = TablePagination(table_data=self.table_data)
            self.table_data.pagination = self.pagination
            self.header.table_data = self.table_data
            self.table_data.fbind("scroll_x", self._scroll_with_header)
            self.ids.container.add_widget(self.header)
            self.ids.container.add_widget(self.table_data)
            if self.use_pagination:
                self.ids.container.add_widget(self.pagination)
            Clock.schedule_once(self.create_pagination_menu, 0.5)
            self.bind(row_data=self.update_row_data)
        else:
            self.table_data = TableData(
                self.header,
                row_data=self.row_data,
                check=self.check,
                rows_num=self.rows_num,
                _parent=self,
            )
            self.register_event_type("on_row_press")
            self.register_event_type("on_check_press")
            self.pagination = TablePagination(table_data=self.table_data)
            self.table_data.pagination = self.pagination
            self.header.table_data = self.table_data
            self.table_data.fbind("scroll_x", self._scroll_with_header)
            self.ids.container.add_widget(self.header)
            self.ids.container.add_widget(self.table_data)
            if self.use_pagination:
                self.ids.container.add_widget(self.pagination)
            Clock.schedule_once(self.create_pagination_menu, 0.5)
            self.bind(row_data=self.update_row_data)

    def _process_default_data(self):
        self.row_num = 0
        for i in self.default:
            self.row_num += len(self.default[i])
        print(self.row_num)
        
        cats = list()
        for i in self.default:
            cats.append((i, i))
        
        print(cats)
        
        '''return AgentsTableData(
            self.header,
            row_data=cats,
            rows_num=self.row_num,
            _parent=self
        )'''

    def add_row(self, data: Union[list, tuple], next_to: Union[Widget, str] = 'last') -> None:

        if next_to == 'last':
            self.row_data.append(data)
        elif isinstance(next_to, Widget):
            self.row_data.insert(self.row_data.index(next_to), data)

    def remove_row(self, data: Union[list, tuple]) -> None:
        self.row_data.remove(data)

    def update_row(
        self, old_data: Union[list, tuple], new_data: Union[list, tuple]
    ) -> None:

        for data in self.row_data:
            if data == old_data:
                index_data = self.row_data.index(data)
                self.row_data[index_data] = new_data
                break

    def update_row_data(self, instance, value):
        """
        Called when a the widget data must be updated.

        Remember that this is a heavy function. since the whole data set must
        be updated. you can get better results calling this metod with in a
        coroutine.
        """

        self.table_data.row_data = value
        self.table_data.on_rows_num(self, self.table_data.rows_num)
        # Set cursors to 0
        self.table_data._rows_number = 0
        self.table_data._current_value = 1

        if len(value) < self.table_data.rows_num:
            self.table_data._to_value = len(value)
            self.table_data.pagination.ids.button_forward.disabled = True
        else:
            self.table_data._to_value = self.table_data.rows_num
            self.table_data.pagination.ids.button_forward.disabled = False

        self.table_data.set_next_row_data_parts("")
        self.pagination.ids.button_back.disabled = True
        Clock.schedule_once(self.create_pagination_menu, 0.5)

    def on_row_press(self, *args):
        """Called when a table row is clicked."""

    def on_check_press(self, *args):
        """Called when the check box in the table row is checked."""

    def get_row_checks(self):
        """Returns all rows that are checked."""

        return self.table_data._get_row_checks()

    def create_pagination_menu(self, interval):
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.table_data.set_number_displayed_lines(
                    x
                ),
            }
            for i in range(
                self.rows_num, len(self.row_data) // 2, self.rows_num
            )
        ]
        pagination_menu = MDDropdownMenu(
            caller=self.pagination.ids.drop_item,
            items=menu_items,
            position=self.pagination_menu_pos,
            max_height=self.pagination_menu_height,
            width_mult=2,
        )
        pagination_menu.bind(
            on_dismiss=self.table_data.close_pagination_menu,
        )
        self.table_data.pagination_menu = pagination_menu

    def _scroll_with_header(self, instance, value):
        self.header.scroll_x = value

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return 'ActionsTable'
