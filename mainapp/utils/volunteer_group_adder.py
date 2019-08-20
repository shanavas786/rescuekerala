

def async_volunteer_group_adder(volunteer_group,volunteers):
    for volunteer in volunteers:
        volunteer.groups.add(volunteer_group)
    print("Completed Added group {}".format(volunteer_group))