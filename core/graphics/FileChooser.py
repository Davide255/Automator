import os, string
from ctypes import windll
from kivy.uix.scrollview import ScrollView
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivymd.uix.dialog import MDDialog


class DialogDirectoryWidget(MDDialog):
    
    def __init__(self, **kwargs):
        if kwargs.get('start_directory') != None:
            start_dir = kwargs.pop('start_directory')
        super().__init__(**kwargs)
        self.content_cls = DirectoryWidget(start_dir)


class DirectoryWidget(ScrollView):

    def __init__(self, **kwargs):
        if kwargs.get('start_directory') != None:
            start_dir = kwargs.pop('start_directory')
        super().__init__(**kwargs)

        tv = TreeDirectoryWidget(start_dir, root_options=dict(text=os.getcwd() if not start_dir else start_dir), hide_root=False, indent_level=4)
        with tv.canvas.before:
            Color(0, 0, 0, 1)
            self.background_rect = Rectangle()
        tv.bind(pos=self.adjust_rect_pos)
        tv.bind(size=self.adjust_rect_size)

        tv.size_hint = 1, None
        tv.bind(minimum_height = tv.setter('height'))
        self.add_widget(tv)


class TreeDirectoryWidget(TreeView):


    class Directory(ButtonBehavior, TreeViewLabel):

        def __init__(self, _dir, **kwargs):
            self.dir = os.path.realpath(_dir) if os.path.isdir(os.path.realpath(_dir)) else None
            super().__init__(**kwargs)
            self.text = os.path.basename(self.dir)

        def __repr__(self) -> str:
            return '<Directory: ' + str(self.dir) + '>'


    class File(ButtonBehavior, TreeViewLabel):
        def __init__(self, file, **kwargs):
            super().__init__(**kwargs)
            self.text = os.path.basename(file)
        
        def __repr__(self) -> str:
            return '<Directory: ' + str(self.text) + '>'


    def __init__(self, _dir, **kwargs):
        super().__init__(**kwargs)
        self.dir_tree = dict()

        if _dir in ('computer', 'Computer', 'Machine', 'machine'):
            drives = self.get_drives()
            for d in drives:
                _drive_node = self.add_node(TreeViewLabel(text=d+':'))
                self._populate_node(_drive_node, d+':\\', True)
        else:
            from System import Environment

            # Special folders are ['music', 'video', 'user', 'appdata']
            if _dir in ('user', 'User', 'userprofile', 'UserProfile'):
                self._root_dir = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            elif _dir in ('music', 'Music', 'musicfolder', 'MusicFolder'):
                self._root_dir = Environment.GetFolderPath(Environment.SpecialFolder.MyMusic)
            elif _dir in ('video', 'Video', 'videofolder', 'VideoFolder'):
                self._root_dir = Environment.GetFolderPath(Environment.SpecialFolder.MyVideos)
            elif _dir in ('appdata', 'AppData', 'applicationdata', 'ApplicationData'):
                self._root_dir = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData)
            else:
                self._root_dir = _dir if os.path.isdir(_dir) else os.getcwd()
            dirs, files = self.get_file_and_dirs(self._root_dir)

            for d in dirs:
                d = os.path.join(self._root_dir, d)
                _node = self.add_node(self.Directory(d))
                if not self.get_file_and_dirs(d) == ([], []):
                    _node.bind(on_release=lambda *args: self._populate_node(args[0], args[0].dir))
                self.dir_tree[d] = _node

            for f in files:
                f = os.path.join(self._root_dir, f)
                self.add_node(self.File(f))

    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1

        return drives

    def get_file_and_dirs(self, dir=os.getcwd()):
        onlyfiles = list()
        try:
            for f in os.scandir(dir):
                try:
                    if os.path.isfile(os.path.join(dir, f)):
                        onlyfiles.append(f)
                except (OSError, PermissionError):
                    pass
            
            onlydir = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]
            return onlydir, onlyfiles
        except (OSError, PermissionError):
            return ([], [])

    def _populate_subnode(self, node, subdir):
        pass

    def _populate_node(self, node, dir, create_mode=False):

        if hasattr(self.dir_tree.get(dir), 'nodes') and self.dir_tree.get(dir).nodes == []:
            dirs, files = self.get_file_and_dirs(dir)

            for d in dirs:
                d = os.path.join(dir, d)
                _node = self.add_node(self.Directory(d), node)
                if not self.get_file_and_dirs(d) == ([], []):
                    _node.bind(on_release=lambda *args: self._populate_node(args[0], args[0].dir))
                self.dir_tree[d] = _node
                del d

            for f in files:
                f = os.path.join(dir, f)
                self.add_node(self.File(f), node)
                del f
        elif not hasattr(self.dir_tree.get(dir), 'nodes'):
            dirs, files = self.get_file_and_dirs(dir)
            for d in dirs:
                d = os.path.join(dir, d)
                _node = self.add_node(self.Directory(d), node)
                if not self.get_file_and_dirs(d) == ([], []):
                    _node.bind(on_release=lambda *args: self._populate_node(args[0], args[0].dir))
                self.dir_tree[d] = _node
                del d

            for f in files:
                f = os.path.join(dir, f)
                self.add_node(self.File(f), node)
                del f

        if not create_mode:
            self.toggle_node(node)
