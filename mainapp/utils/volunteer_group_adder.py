

def async_volunteer_group_adder(volunteer_group,volunteers):
    through_model = volunteers[0].groups.through  # gives you access to auto-created through model
    # print through_model
    #print(through_model.objects.all()[0].__dict__ )
    # <class 'app_label.models.Photo_which_stream'>  # or sth. similar
    dups = through_model.objects.all().filter(volunteergroup_id=volunteer_group.pk).values_list('volunteer_id', flat=True)
    data = []
    for pk in volunteers.values_list('pk', flat=True):
        if pk not in dups:
            data.append(through_model(volunteer_id=pk, volunteergroup_id=volunteer_group.pk) )
    through_model.objects.bulk_create(data)
    #for volunteer in volunteers:
    #    volunteer.groups.add(volunteer_group)
    print("Completed Added group {}".format(volunteer_group))