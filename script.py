import mdl
from display import *
from matrix import *
from draw import *


#setting defaults

num_frames = 1
basename = "default"
knobs = []
animate = 0


"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """
def first_pass( commands ):
    #keeping track of available commands
    contains = []
    global num_frames
    global basename
    global animate
    for command in commands:
        cmd = command['op']
        args = command['args']
        print cmd
        print args
        if cmd == "basename":
            animate = 1
            basename = args[0]
            contains.append("b")
        elif cmd == "frames":
            animate = 1
            if "b" not in contains:
                print "no basename provided so it will be default"
            print "NUM FRAMES:"
            print num_frames
            num_frames = args[0]
            contains.append("f")
        elif cmd == "vary":
            animate = 1
            if "b" not in contains:
                print "frames must preceed vary"
                return
        # catching bound errors for start_frame end_frame start_val end_val
            start = args[0]
            end = args[1]
            if start > num_frames-1 or start < 0 or end > num_frames-1 or end < 0: 
                print "bounds!"
                return
        
"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands):
    global num_frames
    global knobs
    for i in range(int(num_frames)):
        knobs.append({})
 #   print knobs
    for command in commands:
        cmd = command['op']
        args = command['args']
    
        if cmd == "vary":
            k = command['knob']
            start_f = args[0]
            end_f = args[1]
            start_v = args[2]
            end_v = args[3]
            k_val = start_v
            incr = (end_v - start_v) / (end_f - start_f)

            for i in range(int(start_f), int(end_f +1)):
            
                knobs[i][k] = start_v + incr * (i- start_v)
        

def run(filename):
    global num_frames
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    consts = ''
    coords = []
    coords1 = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
    
    first_pass(commands)
    second_pass(commands)
    

    for f in range(int(num_frames)):
#        print "BOOP"
#        print "FRAME # +"
#        print f
        for k in knobs[f]:
            symbols[k][1] = knobs[f][k] 

        for command in commands:
#            print command
            c = command['op']
            args = command['args']

            #preventing:
            #KeyError: 'knob'
            #KeyError: None

            if (not args == None):
                args = command['args'][:]
            
            if (not args ==  None) and 'knob' in command and (not command['knob'] == None) and (c == "move" or c == "scale" or c == "rotate"):
                k = command['knob']
                for i in range(len(args)):
                    if not isinstance(args[i], basestring):
                        args[i] = args[i] * symbols[k][1]


            if c == 'box':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[-1], str):
                    coords = args[-1]
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'sphere':
                add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'torus':
                add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'square_pyramid':
                add_square_pyramid(tmp, args[0], args[1], args[2], args[3], args[4])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'crystal':
                add_crystal(tmp, args[0], args[1], args[2], args[3], args[4])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'cylinder':
                add_cylinder(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'cone':
                add_cone(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif c == 'line':
                if isinstance(args[0], str):
                    consts = args[0]
                    args = args[1:]
                if isinstance(args[3], str):
                    coords = args[3]
                    args = args[:3] + args[4:]
                if isinstance(args[-1], str):
                    coords1 = args[-1]
                add_edge(tmp,
                     args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                tmp = make_translate(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                tmp = make_scale(args[0], args[1], args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])

        if animate == 1:
            save_extension(screen, ("./anim/" + basename + ('%03d.png' %int(f))))

        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
        zbuffer = new_zbuffer()
        tmp = []
        step_3d = 20

    if animate == 1:
        make_animation(basename)
