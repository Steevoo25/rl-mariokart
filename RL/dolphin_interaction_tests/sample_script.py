from dolphin import event, gui

red = 0xffff0000
frame_counter = 0

# Call this function on frame advance (updates every frame)
@event.on_frameadvance()
def update():
    frame_counter += 1
    # Draw on screen
    gui.draw_text((10, 10), red, f"Frame: {frame_counter}")
    # Print to console
    if frame_counter % 60 == 0:
        print(f"The frame count has reached {frame_counter}")