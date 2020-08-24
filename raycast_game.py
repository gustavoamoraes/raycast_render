from background import * 
import concurrent.futures
import copy
import sys
import os
from multiprocessing import Pool

screen_size = (1920,1080)
game = Instance("Raycast",screen_size,(180, 225, 255),True)
block_colors = [(25,25,25),(135,0,0),(0,135,0),(0,0,135),(25,56,135),(66,135,55),(46,0,135),(0,66,135),(135,0,0)]

textures = ["images/brick.jpg","images/wood.jpg","images/img.jpg","images/img1.png","images/img2.jpg","images/mario1.jpg"]
(frames_path, _, anim_frames) = next(os.walk("images/anim"))
frame_index = 0

for n in range(len(textures)):
    img = pygame.image.load(os.path.abspath(textures[n]))
    textures[n] = (img.convert(),img.get_rect().size)

for n in range(len(anim_frames)):
    img = pygame.image.load(os.path.abspath(frames_path+'/'+anim_frames[n]))
    anim_frames[n] = (img.convert(),img.get_rect().size)

map_colors = [(25,25,25),(135,0,0),(0,135,0),(0,0,135),(25,56,135),(66,135,55),(46,0,135),(0,66,135),(135,0,0)]

cell_grid =[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,2,2,2,2,2,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],]
'''
cell_grid =[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
      
'''
largest_row_is = 0
for row in cell_grid:
    if len(row) > largest_row_is:
        largest_row_is = len(row)
        
#How big does the cube have to be in each axis to fit on the screen?
max_sizes = ((screen_size[0]/3)//largest_row_is,(screen_size[1]/3)//len(cell_grid))
#Making the smallest axis cube size the size of the other axis so the draw fits the entire screen
cell_size = min(max_sizes)
#Vector containing the cube size
cell_size_vec = Vector2(cell_size,cell_size)

fov = 60
resolution = 3
number_of_rays = math.ceil(screen_size[0]/resolution)
wall_height = 125

cores = 1
angle_step = fov/number_of_rays
screen_part = screen_size[0]/cores

#Creating floor
floor_color = (100,100,100)
floor = GameObject([Surface(floor_color,Vector2(screen_size[0],screen_size[1]/2),Vector2(screen_size[0]/2,screen_size[1]/2+screen_size[1]/4))],game)

#texture collums
render_lines = GameObject([Image(None,None) for _ in range(number_of_rays)],game)

#region inputs
player_angle = 0
player = GameObject([],game)
player.position = Vector2(3,3)
mouse_speed = 1
player_speed = 2
mouse_pos = Vector2(0,0)
pygame.mouse.set_visible(False) 
pygame.event.set_grab(True)
#endregion

#region Creating map
cubes = []
current_cube_pos = cell_size_vec/2 
for row in cell_grid:
    for block in row:
        cube = cubes.append(Surface(map_colors[block],cell_size_vec,current_cube_pos))
        current_cube_pos += Vector2(cell_size_vec.x,0)
    current_cube_pos = Vector2(cell_size_vec.x/2,current_cube_pos.y+cell_size_vec.y)

cubes_father = GameObject(cubes,game)
map_player = GameObject([Circle(int(cell_size//4),(255,255,255),Vector2(0,0))],game)
#endregion

def Raycast(ray_angle,cell_pos,origin):

    if ray_angle == 0:
        ray_angle = 0.01

    quadrant = math.ceil(ray_angle/90)
    ray_tan = abs(math.tan(math.radians(ray_angle)))

    #Copying vector so the func dont write to same place in memory
    copy_cell_pos = Vector2(cell_pos.x,cell_pos.y)

    tile_stepX,tile_stepY = -1,-1
    if quadrant > 2:
        copy_cell_pos.y = 1-copy_cell_pos.y
        tile_stepY = 1
    if quadrant == 1 or quadrant == 4:
        copy_cell_pos.x = 1-copy_cell_pos.x
        tile_stepX = 1
    
    #small number just for the points to be inside
    small_number = 0.001
    vert_intercept = Vector2((copy_cell_pos.x+small_number)*tile_stepX,tile_stepY*copy_cell_pos.x*ray_tan)
    hor_intercept =  Vector2((copy_cell_pos.y/ray_tan)*tile_stepX,(copy_cell_pos.y+small_number)*tile_stepY)
    StepX,StepY = 1/ray_tan,ray_tan

    def grid_index (vec):
        grid_index = Vector2(int(vec.x),int(vec.y))
        if grid_index.y >= 0 and grid_index.y < len(cell_grid) and grid_index.x >= 0 and grid_index.x < len(cell_grid[grid_index.y]):
            return grid_index 
        else:
            return -1

    clossest_point_dist = 999
    cell_type = None
    point_cell_pos = None

    while(1):

        world_pos = origin+hor_intercept
        grid_pos = grid_index(world_pos)
        
        if grid_pos != -1:
            grid_index_x = cell_grid[grid_pos.y][grid_pos.x]
            if grid_index_x > 0:
                dist = hor_intercept.magnitude()
                if dist < clossest_point_dist:
                    point_cell_pos = ((world_pos.x-grid_pos.x)+1)%1
                    cell_type = grid_index_x
                    clossest_point_dist = dist
                break
            else:
                hor_intercept += Vector2(StepX*tile_stepX,tile_stepY)
        else:
            break
            
    while(1):

        world_pos = origin+vert_intercept
        grid_pos = grid_index(world_pos)

        if grid_pos != -1:
            grid_index_y = cell_grid[grid_pos.y][grid_pos.x]
            if grid_index_y > 0:
                dist = vert_intercept.magnitude()
                if dist < clossest_point_dist:
                    point_cell_pos = ((world_pos.y-grid_pos.y)+1)%1
                    cell_type = grid_index_y
                    clossest_point_dist = dist
                break
            else:
                vert_intercept += Vector2(tile_stepX,StepY*tile_stepY)
        else:
            break

    return (cell_type,clossest_point_dist,point_cell_pos)

def FixAngle(angle):
    if angle > 360:
        angle -= 360
    elif angle < 0:
        angle = 360+angle
    return angle

def MaxValue(value,min,max):
    if value > max:
        value = max
    if value < min:
        value = min
    return value

def RaycastManager (current_angle,player_angle,index,player_cell_pos):

    for n in range(round(index*screen_part),round((index+1)*screen_part),resolution):

        ray_angle = FixAngle(player_angle-current_angle)
        ray = Raycast(ray_angle,player_cell_pos,player.position)
        fixed_dist = math.cos(math.radians(FixAngle(ray_angle-player_angle)))*ray[1]
        #fixed_dist = ray[1]
        ray_index = n//resolution
        if type(ray[0]) != type(None):

            #test_circles.draw_functions[n].local_position = test.position+(ray[0]*cell_size)
            number = 15
            const = abs(number/fixed_dist)
            line_height = int(const*wall_height)
            position = (n,(screen_size[1]/2)-line_height/2)

            #textures
            img_size = textures[ray[0]-1][1]
            pixel_cord = (ray[2]*img_size[0]- resolution/2)
            if pixel_cord < 0:
                pixel_cord = 0

            column = textures[ray[0]-1][0].subsurface(pixel_cord,0,1,img_size[1])

            if line_height < 60000:
                scaled_img = pygame.transform.scale(column,(resolution,line_height))
                render_lines.draw_functions[ray_index].image_surface = scaled_img
                render_lines.draw_functions[ray_index].position = position

            #region color walls
            '''
            #line = render_lines.draw_functions[n//resolution]
            block_color = block_colors[ray[0]]
            color_const = fixed_dist/2
            line.color = (MaxValue(block_color[0]/color_const,0,block_color[0]),MaxValue(block_color[1]/color_const,0,block_color[1]),MaxValue(block_color[2]/color_const,0,block_color[2]))
            line.start = Vector2(n,(screen_size[1]/2)+line_height/2)
            line.end = Vector2(n,(screen_size[1]/2)-line_height/2)
            line.thickness = resolution
            '''
            #endregion

        current_angle+=angle_step

def Update (self):
    global player_angle
    global frame_index

    player_angle -= pygame.mouse.get_rel()[0]*mouse_speed*self.delta_time
    player_angle = FixAngle(player_angle)
    
    textures[5] = anim_frames[int(frame_index)]
    frame_index+=1
    frame_index = frame_index%(len(anim_frames))
    
    #up is negative
    player_forward = Vector2(math.cos(math.radians(player_angle)),-math.sin(math.radians(player_angle)))
    player_right = player_forward.perpendicular()
    player.position += player_forward*player_speed*(self.keys[K_w]-self.keys[K_s])*self.delta_time
    player.position += player_right*player_speed*(self.keys[K_d]-self.keys[K_a])*self.delta_time

    map_player.position = player.position*cell_size
    player_cell_pos = player.position-Vector2(int(player.position.x),int(player.position.y))

    current_angle = -fov/2
    fov_parts = fov/cores

    for i in range(cores):

        RaycastManager(current_angle,player_angle,i,player_cell_pos)
        current_angle += fov_parts

if __name__ == "__main__":
    game.Start(Update)