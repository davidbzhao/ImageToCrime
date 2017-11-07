from GoogleMapImageLib import download_map_image, get_second_point, get_pic_width_meters, is_within_city
row_counter = 0
key = ""
image_coord_file = open("image_coords.txt", "w")
image_coord_file.close()


def get_top_left_corner(center_lat, center_long, half_pic_width):
    center_left_side = get_second_point(center_lat, center_long, half_pic_width, 4)
    top_left_corner = get_second_point(center_left_side[0], center_left_side[1], half_pic_width, 1)
    return top_left_corner


def get_bot_right_corner(center_lat, center_long, half_pic_width):
    center_right_side = get_second_point(center_lat, center_long, half_pic_width, 2)
    bot_right_corner = get_second_point(center_right_side[0], center_right_side[1], half_pic_width, 3)
    return bot_right_corner


def download_right(lat, long, bound, width_pic, key):
    half_pic_width = width_pic / 2
    col_counter = 0

    while long < bound:
        if is_within_city(lat, long, "Chicago", key): # within the city ranges

            filename = str(row_counter) + "_" + str(col_counter)
            download_map_image(lat, long, key, filename+".png")

            TL_corner = get_top_left_corner(lat, long, half_pic_width)
            BR_corner = get_bot_right_corner(lat, long, half_pic_width)

            image_coord_file = open("image_coords.txt", "a")
            image_coord_file.write(filename + ",%s,%s,%s,%s\n" % (TL_corner[0], TL_corner[1], BR_corner[0], BR_corner[1]))
            image_coord_file.close()
        lat,long = get_second_point(lat, long, half_pic_width, 2) # move east by half of the pic's width
        col_counter += 1


def download_entire_lat(lat, long, right_bound, pic_width, key):
    # download_left(lat, long, left_bound, key)
    download_right(lat, long, right_bound, pic_width, key)
    return


# general setup
upper_left_boundary_lat, upper_left_boundary_long = 42.023827, -87.932487 # 42.017191, -87.819896 = dont include airport
intmd_left_bound = 41.946839, -87.867751
lower_right_boundary_lat = 41.643764
lower_right_boundary_long = -87.522456

# picture width in meters changes everytime the latitude changes
pic_width = get_pic_width_meters(upper_left_boundary_lat, 640, 17)
starting_point = get_second_point(upper_left_boundary_lat, upper_left_boundary_long, pic_width / 2, 2)
starting_point = get_second_point(starting_point[0], starting_point[1], pic_width/2, 3)
print(starting_point)

print(get_top_left_corner(starting_point[0], starting_point[1], get_pic_width_meters(starting_point[0], 640, 17)/2))

test_point = (upper_left_boundary_lat, upper_left_boundary_long)
pic_width = get_pic_width_meters(starting_point[0], 640, 17)
while(test_point[1] < intmd_left_bound[1]):
    test_point = get_second_point(test_point[0], test_point[1], pic_width/2, 2)
# print(test_point)
intmd_starting_long = test_point[1]

while(starting_point[0] >= lower_right_boundary_lat):
    # width changes everytime the latitude changes
    pic_width = get_pic_width_meters(starting_point[0], 640, 17)
    # download images for the current row
    download_entire_lat(starting_point[0], starting_point[1], lower_right_boundary_long, pic_width, key)

    # move down ; starting point will be the center of the leftmost square in the row below the current row
    starting_point = get_second_point(starting_point[0], starting_point[1], pic_width/2, 3)
    row_counter += 1

    #
    if starting_point[0] <= intmd_left_bound[0]:
        starting_point[1] = get_second_point(starting_point[0], intmd_starting_long, pic_width/2, 2)

