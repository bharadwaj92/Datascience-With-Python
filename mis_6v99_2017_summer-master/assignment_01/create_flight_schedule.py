from collections import OrderedDict
import operator
class Flight_schedule():
    def __init__(self) :
        self.startpoint = None
        self.endpoint = None
        self.tail_no = None
        self.starttime = None
        self.arrivaltime = None

final_schedule = []
departure_start = 360
arrival_end = 1320
tails = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
locations = ['AUS', 'DAL', 'HOU']
flight_travel = {'AUS': {'DAL': 50, 'HOU': 45}, 'DAL': {'HOU' :65, 'AUS':50},'HOU':{'AUS':45 ,'DAL':65}}
gates = {'AUS': 1, 'DAL': 2, 'HOU': 3}
groundtime = {'AUS' : 25 , 'DAL' : 30 , 'HOU' : 35}
austin_latest = []
dallas_latest = []
houston_latest = []
tails_used = []
current_flights = {'AUS': 0, 'DAL': 0, 'HOU': 0}
tails_loc = {}
dept_tails = {}
gates_aus = {'1': []}
gates_dal = {'1': [], '2': []}
gates_hou = {'1': [], '2': [], '3': []}

## method to continue the schedule once the intital schedule has been given.
def continue_schedule():
    gates_free = gates.copy()
    local_gates = gates.copy()
    gates_filled = {'AUS': 0, 'DAL': 0, 'HOU': 0}
    local_gates = OrderedDict(sorted(local_gates.items()))
    global tails_loc
    global dept_tails
    tails_loc = OrderedDict(sorted(tails_loc.items()))
    for tail, loc in tails_loc.items(): ## logic for iterating over each tail after intital schedule
        avail_locations = [x for x in locations if x != loc]
        inner_flag = False
        for avail_loc in avail_locations:
            if (avail_loc == 'DAL' and inner_flag == False):
                if (gates_filled[avail_loc] < local_gates[avail_loc]):
                    for gate, interval in gates_dal.items():
                        if (dept_tails[tail] > interval[1]):## Check before scheduling the flight for arrival time at end point
                            f = Flight_schedule()
                            f.tail_no = tail
                            f.startpoint = loc
                            f.endpoint = avail_loc
                            f.starttime = dept_tails[tail]
                            f.arrivaltime = f.starttime + flight_travel[f.startpoint][f.endpoint]
                            if (f.arrivaltime <= 1320):## append it arrival time is less than constraint else loop through other end point
                                final_schedule.append(f)
                                dept_tails[f.tail_no] = f.arrivaltime + groundtime['DAL']
                                gates_dal[gate] = [f.arrivaltime, f.arrivaltime + groundtime['DAL']]
                                gates_filled[f.endpoint] += 1
                                gates_free[f.startpoint] -= 1
                                tails_loc[tail] = f.endpoint
                                inner_flag = True
                                break

            elif (avail_loc == 'HOU' and inner_flag == False):
                if (gates_filled[avail_loc] < local_gates[avail_loc]):
                    for gate, interval in gates_hou.items():
                        if (dept_tails[tail] > interval[1]):
                            f = Flight_schedule()
                            f.tail_no = tail
                            f.startpoint = loc
                            f.endpoint = avail_loc
                            f.starttime = dept_tails[tail]
                            f.arrivaltime = f.starttime + flight_travel[f.startpoint][f.endpoint]
                            if (f.arrivaltime <= 1320):
                                final_schedule.append(f)
                                dept_tails[f.tail_no] = f.arrivaltime + groundtime['HOU']
                                gates_hou[gate] = [f.arrivaltime, f.arrivaltime + groundtime['HOU']]
                                gates_filled[f.endpoint] += 1
                                gates_free[f.startpoint] -= 1
                                tails_loc[tail] = f.endpoint
                                inner_flag = True
                                break
            elif (avail_loc == 'AUS' and inner_flag == False):
                if (gates_filled[avail_loc] < local_gates[avail_loc]):
                    for gate, interval in gates_aus.items():
                        if (dept_tails[tail] > interval[1]):
                            f = Flight_schedule()
                            f.tail_no = tail
                            f.startpoint = loc
                            f.endpoint = avail_loc
                            f.starttime = dept_tails[tail]
                            f.arrivaltime = f.starttime + flight_travel[f.startpoint][f.endpoint]
                            if (f.arrivaltime <= 1320):
                                dept_tails[f.tail_no] = f.arrivaltime + groundtime['AUS']
                                gates_aus['1'] = [f.arrivaltime, f.arrivaltime + groundtime['AUS']]
                                final_schedule.append(f)
                                gates_filled[f.endpoint] += 1
                                gates_free[f.startpoint] -= 1
                                tails_loc[tail] = f.endpoint
                                inner_flag = True
                                break
        if (inner_flag == False): ## If none of the above logics worked, then find the gate with min dept time and use that.
            loc_tails_temp = [k for k, v in tails_loc.items() if v in avail_locations]
            dept_tails_temp = dict([(k, v) for k, v in dept_tails.items() if k in loc_tails_temp])
            dept_tails_temp = OrderedDict(sorted(dept_tails_temp.items()))
            try:## Exceptional handling if there are no locations available.
                min_key = min(dept_tails_temp, key=dept_tails_temp.get)
            except ValueError:
                print(dept_tails_temp, loc_tails_temp, tails_loc, dept_tails, avail_locations)
                break
            nearest_location = tails_loc[min_key]
            f = Flight_schedule()
            f.tail_no = tail
            f.startpoint = loc
            f.endpoint = nearest_location
            f.starttime = dept_tails_temp[min_key]
            f.arrivaltime = f.starttime + flight_travel[f.startpoint][f.endpoint]
            if (f.arrivaltime <= 1320 and nearest_location == 'AUS'and gates_filled[f.endpoint] < local_gates[f.endpoint]):
                dept_tails[f.tail_no] = f.arrivaltime + groundtime['AUS']
                gates_aus['1'] = [f.arrivaltime, f.arrivaltime + groundtime['AUS']]
                final_schedule.append(f)
                gates_filled[f.endpoint] += 1
                gates_free[f.startpoint] -= 1
                tails_loc[tail] = f.endpoint
                inner_flag = True
            elif (f.arrivaltime <= 1320 and nearest_location == 'DAL' and gates_filled[f.endpoint] < local_gates[f.endpoint] ):
                try:
                    gate = [k for k, v in gates_dal.items() if v[1] == dict(dept_tails_temp)[min_key]][0]
                except IndexError:
                    break
                final_schedule.append(f)
                dept_tails[f.tail_no] = f.arrivaltime + groundtime['DAL']
                gates_dal[gate] = [f.arrivaltime, f.arrivaltime + groundtime['DAL']]
                gates_filled[f.endpoint] += 1
                gates_free[f.startpoint] -= 1
                tails_loc[tail] = f.endpoint
                inner_flag = True ## break the loop
            elif(f.arrivaltime <= 1320 and nearest_location == 'HOU' and gates_filled[f.endpoint] < local_gates[f.endpoint]):
                print(gates_filled, local_gates, min_key)
                gate = [k for k, v in gates_hou.items() if v[1] == dict(dept_tails_temp)[min_key]]
                final_schedule.append(f)
                dept_tails[f.tail_no] = f.arrivaltime + groundtime['HOU']
                try:
                    gates_dal[gate] = [f.arrivaltime, f.arrivaltime + groundtime['HOU']]
                except TypeError:
                    continue
                gates_filled[f.endpoint] += 1
                gates_free[f.startpoint] -= 1
                tails_loc[tail] = f.endpoint
                inner_flag = True
        if inner_flag == False:
            break
    return

## Method that generates initial schedule
def initial_schedule():
    global tails_used
    local_gates = gates.copy()
    local_gates = OrderedDict(sorted(local_gates.items(), reverse=True))
    for loc in local_gates.keys():
        num_iterations = gates[loc]  ## tracks the number of gates to schedule
        while (num_iterations > 0):
            avail_locations = [x for x in locations if x != loc]
            for item in avail_locations:  # for each item loops and checks if there are any gates available for endpoint
                if (local_gates[item] > 0):
                    f = Flight_schedule()
                    f.tail_no = [x for x in tails if x not in tails_used][0]
                    f.startpoint = loc
                    f.endpoint = item
                    f.starttime = departure_start
                    f.arrivaltime = f.starttime + flight_travel[f.startpoint][f.endpoint]
                    if (f.endpoint == 'AUS'):
                        tails_loc[f.tail_no] = 'AUS'
                        gates_aus['1'] = [f.arrivaltime, f.arrivaltime + groundtime['AUS']]
                        dept_tails[f.tail_no] = f.arrivaltime + groundtime['AUS']
                    elif (f.endpoint == 'DAL'):
                        tails_loc[f.tail_no] = 'DAL'
                        gates_dal[[k for (k, v) in gates_dal.items() if len(v) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + groundtime[
                                                                                                'DAL']]
                        dept_tails[f.tail_no] = f.arrivaltime + groundtime['DAL']
                    else:
                        tails_loc[f.tail_no] = 'HOU'
                        gates_hou[[k for (k, v) in gates_hou.items() if len(v) == 0][0]] = [f.arrivaltime,
                                                                                            f.arrivaltime + groundtime[
                                                                                                'HOU']]
                        dept_tails[f.tail_no] = f.arrivaltime + groundtime['HOU']
                    current_flights[f.endpoint] += 1
                    local_gates[f.endpoint] -= 1
                    tails_used.append(f.tail_no)
                    final_schedule.append(f)
                    break
            num_iterations -= 1

## Method to convert time to necessary format
def convert_time(value):
    hours = str(int(value/60))
    minutes = str(int(value)%60)
    return hours.zfill(2)+minutes.zfill(2)

## Driver method that calls the functions and prepares csv file
if __name__ == "__main__":
    initial_schedule()
    while (True):
        inital_len = len(final_schedule) ## checks if there is any change in the schedule, if not breaks the while loop
        continue_schedule()
        if( inital_len == len(final_schedule)):
            break
    final_schedule.sort(key=operator.attrgetter("tail_no", "starttime"), reverse=False)## sort the final schedule in necessary order
    with open("flight_schedule.csv", 'wt') as f:
        csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
        print(csv_header,file= f)
        for item in final_schedule:
            temp = item.tail_no + ',' + item.startpoint + ',' + item.endpoint + ',' + convert_time(item.starttime) + ',' + convert_time(
                item.arrivaltime)
            print(temp,file =f)
