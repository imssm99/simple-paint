import numpy as np
import cv2 as cv
import math

def mouse_event_handler(event, x, y, flags, param):
    # Change 'mouse_state' (given as 'param') according to the mouse 'event'
    if event == cv.EVENT_LBUTTONDOWN:
        param[0] = True
        param[1] = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        param[0] = False
    elif event == cv.EVENT_MOUSEMOVE:
        param[1] = (x, y)

def simple_paint(canvas_width=640, canvas_height=480, init_brush_radius=3):
    # Prepare a canvas and palette
    canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
    palette = [(0, 0, 0), (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    # Initialize drawing states
    mouse_state = [False, (-1, -1)] # Note) [mouse_left_button_click, mouse_xy]
    brush_color = 0
    brush_radius = init_brush_radius

    # Instantiate a window and register the mouse callback function
    cv.namedWindow('Simple Paint')
    cv.setMouseCallback('Simple Paint', mouse_event_handler, mouse_state)

    prev_xy = (0, 0)
    mode = None
    shape_xy = (0, 0)
    euclid_dist = lambda t1, t2: math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2)

    while True:
        # Draw a point if necessary
        mouse_left_button_click, mouse_xy = mouse_state
        if mouse_left_button_click:
            if mode == "rect":
                cv.rectangle(canvas, shape_xy, mouse_xy, palette[brush_color], brush_radius)
                mode = None
            elif mode == "circle":
                cv.circle(canvas, shape_xy, int(round(euclid_dist(shape_xy, mouse_xy))), palette[brush_color], brush_radius)
                mode = None
            else:
                cv.line(canvas, prev_xy, mouse_xy, palette[brush_color], max(brush_radius, 1))
        prev_xy = mouse_xy

        # Show the canvas
        canvas_copy = canvas.copy()
        info = f'Brush Radius: {brush_radius}'
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (127, 127, 127), thickness=2)
        cv.putText(canvas_copy, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, palette[brush_color])
        
        # Show cursor
        if mode == "rect":
            cv.rectangle(canvas_copy, shape_xy, mouse_xy, palette[brush_color], brush_radius)
        elif mode == "circle":
            cv.circle(canvas_copy, shape_xy, int(round(euclid_dist(shape_xy, mouse_xy))), palette[brush_color], brush_radius)
        else:
            cv.circle(canvas_copy, mouse_xy, int(round(brush_radius/2)), palette[brush_color], 1)
        cv.imshow('Simple Paint', canvas_copy)

        # Process the key event
        key = cv.waitKey(1)
        if key == 27: # ESC
            break
        elif key == ord('x'):
            canvas = np.full((canvas_height, canvas_width, 3), 255, dtype=np.uint8)
        elif key == ord('\t'):
            brush_color = (brush_color + 1) % len(palette)
        elif key == ord('+') or key == ord('='):
            brush_radius += 1
        elif key == ord('-') or key == ord('_'):
            brush_radius = max(brush_radius - 1, -1)
        elif key == ord('r'):
            mode = "rect"
            shape_xy = mouse_xy
        elif key == ord('c'):
            mode = "circle"
            shape_xy = mouse_xy


    cv.destroyAllWindows()

if __name__ == '__main__':
    simple_paint()
