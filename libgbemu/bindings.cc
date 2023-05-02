#include "gbemu/src/gameboy_prelude.h"
#include <memory>
#include <cstring>

struct File
{
    unsigned char *contents;
    unsigned long length;
};

static std::unique_ptr<Gameboy> gbemu;
static uint32_t framebuffer[GAMEBOY_HEIGHT * GAMEBOY_WIDTH];
static std::vector<unsigned char> rom_data;
static std::vector<unsigned char> state_data;
static Options opts {};

static unsigned char get_real_color(Color color) {
    switch (color) 
    {
        case Color::White: return 255;
        case Color::LightGray: return 170;
        case Color::DarkGray: return 85;
        case Color::Black: return 0;
    }

    return 0;
}

static void vblank_cb(const FrameBuffer &buffer)
{
    for (int y = 0; y < GAMEBOY_HEIGHT; ++y)
    {
        for (int x = 0; x < GAMEBOY_WIDTH; ++x)
        {
            uint8_t pixel_value = get_real_color(buffer.get_pixel(x, y));
            uint32_t index = GAMEBOY_WIDTH * y + x;
            memset(&framebuffer[index], pixel_value, sizeof(unsigned char) * 4);
        }
    }
}

static void copy_contents(std::vector<unsigned char> &buffer, File &rom)
{
    if (!rom.contents || rom.length == 0)
        return;

    buffer.resize(rom.length);
    memcpy(buffer.data(), rom.contents, rom.length);
}

extern "C" void load_rom(File rom, File state)
{
    copy_contents(rom_data, rom);
    copy_contents(state_data, state);

    gbemu.reset();
    gbemu = std::make_unique<Gameboy>(rom_data, opts, state_data);
    gbemu->register_vblank_callback(vblank_cb);
}

extern "C" void loop()
{
    while (1)
    {
        if (gbemu) gbemu->tick();
    }
}

extern "C" void set_button(unsigned char key, int state)
{
    if (state)
        gbemu->button_pressed(static_cast<GbButton>(key));
    else
        gbemu->button_released(static_cast<GbButton>(key));
}

extern "C" uint8_t *get_frame()
{
    return reinterpret_cast<uint8_t *>(framebuffer);
}
