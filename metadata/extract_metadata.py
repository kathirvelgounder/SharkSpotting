#we are going to be provided a .srt file, as well an interval 
#range that sharks are found in the video. Extract the other
#pertinent information that is present at that time

class DroneInfo():
    """
    Stores information logged into a given entry of the 
    SRT file created in the drones flight. Contains useful
    information such as drone altitude, drone GPS location, etc.
    """

    def __init__(self, gps_loc: tuple, barometer: float=None):
        self.gps_loc = gps_loc
        self.barometer = barometer

    def __repr__(self):
        return 'DroneInfo(%s, %s)' % (self.gps_loc, self.barometer)

def get_metadata_from_srt(file: str, interval: tuple) -> dict:
    metadata: dict = {}
    start = interval[0]
    end = interval[1]
    cnt = 0
    with open(file) as fp:
        line = fp.readline()
        while line:
            line = line.strip()
            if (line.isdigit()):
                cnt += 1
                if cnt > end:
                    break
                if cnt >= start:
                    drone_info = get_single_entry(fp)
                    metadata[cnt] = drone_info
            line = fp.readline()
    return metadata

def get_single_entry(fp) -> DroneInfo:
    cnt = 0
    gps_loc: tuple = None
    barometer: float = None
    while cnt < 4:
        line = fp.readline()
        if cnt == 0:
            pass
        elif cnt == 1:
            pass
        elif cnt == 2:
            readings = line.split()
            gps_loc = get_gps_from_entry(readings[0])
            barometer = get_floats_from_str(readings[1])[0]
        elif cnt == 3:
            pass
        cnt += 1
    drone_info = DroneInfo(gps_loc, barometer)
    return drone_info

# extract a tuple of gps coordinates from a string gps 
# entry of the form GPS(-117.6868,33.4609,18)
def get_gps_from_entry(gps_entry: str) -> tuple:
    nums = get_floats_from_str(gps_entry)
    coords = (nums[0], nums[1])
    return coords

# filters out all non numeric symbols, and returns
# list of floats
def get_floats_from_str(s: str):
    num_strs = list()
    nums = list()
    i = 0
    temp = ''
    while i < len(s):
        if s[i].isnumeric() or s[i] == '-' or s[i] == '.':
            temp += s[i]
            if (i == len(s) - 1):
                nums.append(temp)
        elif len(temp) > 0:
            nums.append(temp)
            temp = ''
        i += 1
    for num in num_strs:
        nums.append(float(num))
    return nums


if __name__ == '__main__':
    interval = (22, 23)
    metadata = get_metadata_from_srt("example_data/DJI_0001.SRT", interval)
    for m in metadata:
        print(metadata[m])


