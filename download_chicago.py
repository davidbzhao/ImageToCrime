from GoogleMapImageLib import download_map_image, get_second_point, get_pic_width_meters, is_within_city
row_counter = 0
upper_left_boundary_lat, upper_left_boundary_long = 42.023827, -87.932487 # 42.017191, -87.819896 = dont include airport
intmd_left_bound = 41.946839, -87.867751
lower_right_boundary_lat = 41.643764
lower_right_boundary_long = -87.522456

key = ""
key = input("API Key: ")
starting_row = int(input("row to start from? "))
image_coord_file = open("image_coords.txt", "a")
image_coord_file.close()


def get_top_left_corner(center_lat, center_long, half_pic_width):
    center_left_side = get_second_point(center_lat, center_long, half_pic_width, 4)
    top_left_corner = get_second_point(center_left_side[0], center_left_side[1], half_pic_width, 1)
    return top_left_corner


def get_bot_right_corner(center_lat, center_long, half_pic_width):
    center_right_side = get_second_point(center_lat, center_long, half_pic_width, 2)
    bot_right_corner = get_second_point(center_right_side[0], center_right_side[1], half_pic_width, 3)
    return bot_right_corner


def init_bounds(key, width_pic, lat, lng):
    half_pic_width = width_pic / 2

    col = 0
    while True:
        if is_within_city(lat, lng, "Chicago", key):
            left_long, left_col = lng, 0
            right_long, right_col = left_long, left_col
            break
        _, lng = get_second_point(lat, lng, half_pic_width, 2)
        col += 1
    while True:
        _, lng = get_second_point(lat, lng, half_pic_width, 2)
        col += 1
        if is_within_city(lat, lng, "Chicago", key):
            right_long, right_col = lng, col
        else:
            break

    return left_long, right_long, left_col, right_col


def find_bounds(key, width_pic, lat, left_long, right_long, left_col, right_col):
    half_pic_width = width_pic / 2

    if is_within_city(lat, left_long, "Chicago", key):
        while True:
            _, lng = get_second_point(lat, left_long, half_pic_width, 4)
            if not is_within_city(lat, lng, "Chicago", key):
                break
            left_long = lng
            left_col -= 1
    else:
        while left_col < right_col - 1:
            _, lng = get_second_point(lat, left_long, half_pic_width, 2)
            left_long = lng
            left_col += 1
            if is_within_city(lat, lng, "Chicago", key):
                break

    if is_within_city(lat, right_long, "Chicago", key):
        while True:
            _, lng = get_second_point(lat, right_long, half_pic_width, 2)
            if not is_within_city(lat, lng, "Chicago", key):
                break
            right_long = lng
            right_col += 1
    else:
        while right_col > left_col + 1:
            _, lng = get_second_point(lat, right_long, half_pic_width, 4)
            right_long = lng
            right_col -= 1
            if is_within_city(lat, lng, "Chicago", key):
                break

    return left_long, right_long, left_col, right_col

def download_right(lat, lng, left_col, right_col, width_pic, key):
    half_pic_width = width_pic / 2

    for col in range(left_col, right_col + 1):
        filename = str(row_counter) + "_" + str(col) + ".png"
        download_map_image(lat, lng, key, filename)

        TL_corner = get_top_left_corner(lat, lng, half_pic_width)
        BR_corner = get_bot_right_corner(lat, lng, half_pic_width)

        image_coord_file = open("image_coords.txt", "a")
        image_coord_file.write(filename + ",%s,%s,%s,%s\n" % (TL_corner[0], TL_corner[1], BR_corner[0], BR_corner[1]))
        image_coord_file.close()

        lat, lng = get_second_point(lat, lng, half_pic_width, 2) # move east by half of the pic's width


def download_entire_lat(lat, lng, left_col, right_col, pic_width, key):
    # download_left(lat, lng, left_bound, key)
    download_right(lat, lng, left_col, right_col, pic_width, key)
    return


def get_starting_point(row_num):
    global row_counter
    pic_width = get_pic_width_meters(upper_left_boundary_lat, 640, 17)
    starting_point = get_second_point(upper_left_boundary_lat, upper_left_boundary_long, pic_width / 2, 2)
    starting_point = get_second_point(starting_point[0], starting_point[1], pic_width / 2, 3)
    for i in range(row_num):
        pic_width = get_pic_width_meters(starting_point[0], 640, 17)
        starting_point = get_second_point(starting_point[0], starting_point[1], pic_width / 2, 3)
        row_counter += 1
    return starting_point


# picture width in meters changes everytime the latitude changes
starting_point = get_starting_point(starting_row)
print(starting_point)

# test_point = (upper_left_boundary_lat, upper_left_boundary_long)
# pic_width = get_pic_width_meters(starting_point[0], 640, 17)
#
#
# while(test_point[1] < intmd_left_bound[1]):
#     test_point = get_second_point(test_point[0], test_point[1], pic_width/2, 2)
# # print(test_point)
# intmd_starting_long = test_point[1]

left_long, right_long, left_col, right_col = init_bounds(key, get_pic_width_meters(starting_point[0], 640, 17), starting_point[0], starting_point[1])
while(starting_point[0] >= lower_right_boundary_lat):
    # width changes everytime the latitude changes
    pic_width = get_pic_width_meters(starting_point[0], 640, 17)
    # download images for the current row

    left_long, right_long, left_col, right_col = find_bounds(key, pic_width, starting_point[0], left_long, right_long, left_col, right_col)
    col_start = download_entire_lat(starting_point[0], starting_point[1], left_col, right_col, pic_width, key)

    # move down ; starting point will be the center of the leftmost square in the row below the current row
    starting_point = get_second_point(starting_point[0], starting_point[1], pic_width/2, 3)
    row_counter += 1

    #
    # if starting_point[0] <= intmd_left_bound[0]:
    #     starting_point[1] = get_second_point(starting_point[0], intmd_starting_long, pic_width/2, 2)

