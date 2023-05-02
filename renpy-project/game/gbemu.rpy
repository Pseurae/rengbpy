init python in gbemu:
    import ctypes, os, threading

    GAMEBOY_WIDTH = 160
    GAMEBOY_HEIGHT = 144
    SCREEN_SCALE = 3

    class File(ctypes.Structure):
        _fields_ = [
            ("contents", ctypes.c_char_p), 
            ("length", ctypes.c_ulong)
        ]

    def load_gbemu():
        gbemu = None

        for suf in [ "windows-x86_64.dll", "linux-x86_64.so", "mac-x86_64.dylib" ]:
            try:
                gbemu = ctypes.cdll[os.path.join(renpy.config.gamedir, "libgbemu", f"libgbemu-{suf}")]
                break
            except Exception as e:
                pass

        if gbemu is None:
            raise Exception("Could not load libgbemu.")

        gbemu.load_rom.argtypes = [ File, File ]
        gbemu.load_rom.restype = None

        gbemu.loop.argtypes = [ ]
        gbemu.loop.restype = None

        gbemu.set_button.argtypes = [ ctypes.c_ubyte, ctypes.c_int ]
        gbemu.set_button.restype = None

        gbemu.get_frame.argtypes = [ ]
        gbemu.get_frame.restype = ctypes.POINTER(ctypes.c_ubyte)

        return gbemu

    libgbemu = load_gbemu()

    main_thread = threading.Thread(target=libgbemu.loop)
    main_thread.daemon = True
    main_thread.start()

    class GBEmu(renpy.Displayable):
        _event_map = { }
        _loaded = False

        def __init__(self, rom, **properties):
            super(renpy.Displayable, self).__init__(**properties)
            self.rom = rom
            self._create_event_map()

        def _create_event_map(self):
            Up     = 0
            Down   = 1
            Left   = 2
            Right  = 3
            A      = 4
            B      = 5
            Select = 6
            Start  = 7

            def key(key, button):
                self._event_map["keydown_" + key] = [ (button, True) ]
                self._event_map["keyup_" + key] = [ (button, False) ]

            key("K_UP", Up)
            key("K_DOWN", Down)
            key("K_LEFT", Left)
            key("K_RIGHT", Right)
            key("K_z", A)
            key("K_x", B)
            key("K_RETURN", Start)
            key("K_BACKSPACE", Select)

        def _load_rom(self):
            if self._loaded:
                return

            with renpy.open_file(self.rom) as f:
                rom = f.read()
                libgbemu.load_rom(File(rom, len(rom)), File(0, 0))

            self._loaded = True

        def render(self, width, height, st, at):
            self._load_rom()

            rgba = ctypes.string_at(libgbemu.get_frame(), GAMEBOY_WIDTH * GAMEBOY_HEIGHT * 4)
            tex = renpy.load_rgba(rgba, (GAMEBOY_WIDTH, GAMEBOY_HEIGHT))

            rv = renpy.display.render.Render(GAMEBOY_WIDTH, GAMEBOY_HEIGHT)

            rv.blit(tex, (0, 0))

            renpy.redraw(self, 1.0 / 30.0)
            return rv

        def event(self, ev, x, y, st):
            matched = False

            for k, v in self._event_map.items():
                if renpy.map_event(ev, k):

                    for button, state in v:
                        libgbemu.set_button(button, state)

                    matched = True

            if matched:
                raise renpy.IgnoreEvent()
